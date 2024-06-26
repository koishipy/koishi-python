import asyncio
from typing import Any, Callable, ClassVar, Literal, Optional, Protocol, TypedDict, TypeVar, Union, overload
from typing_extensions import TypeAlias

import javascript
from loguru import logger

from .bot import Bot
from .command import Command, CommandConfig

T = TypeVar("T")
S = TypeVar("S")


class Inject(Protocol):
    required: Optional[list[str]]
    optional: Optional[list[str]]


class PluginBase(Protocol[T]):
    name: Optional[str]
    reactive: Optional[str]
    reusable: Optional[str]
    Config: Optional[Callable[[Any], T]]
    inject: Optional[Union[list[str], Inject]]


class PluginTransform(Protocol[S, T]):
    schema: Literal[True]
    Config: Callable[[S], T]


C = TypeVar("C", bound="Context", contravariant=True)


class PluginFunction(PluginBase[T], Protocol[C, T]):
    def __call__(self, ctx: C, config: T) -> None: ...


C1 = TypeVar("C1", bound="Context", covariant=True)


class PluginInit(PluginBase[T], Protocol[C1, T]):
    def __init__(self, ctx: C1, config: T) -> None: ...


class PluginObject(PluginBase[T], Protocol[C, T]):
    def apply(self, ctx: C, config: T) -> None: ...


class PluginTransformFunction(PluginFunction[C, T], PluginTransform[S, T], Protocol[C, S, T]):
    pass


class PluginTransformInit(PluginInit[C1, T], PluginTransform[S, T], Protocol[C1, S, T]):
    pass


class PluginTransformObject(PluginObject[C, T], PluginTransform[S, T], Protocol[C, S, T]):
    pass


class PluginDictObject(TypedDict):
    apply: Callable[["Context", Any], None]


PluginType: TypeAlias = Union[
    PluginTransformFunction["Context", None, None],
    PluginTransformInit["Context", None, None],
    PluginTransformObject["Context", None, None],
    PluginFunction["Context", None],
    PluginInit["Context", None],
    PluginObject["Context", None],
    PluginDictObject,
]


class Context:
    __context_type__: ClassVar[javascript.proxy.Proxy]

    def __init__(self, config: Any):
        self._obj = self.__class__.__context_type__(config)

    @property
    def root(self):
        if self._obj.root == self._obj:
            return self
        return Context(self._obj.root)

    @property
    def config(self):
        return self._obj.config

    @property
    def bots(self) -> dict[Union[int, str], Bot[Any]]:
        return self._obj.bots

    def inject(self, deps: Union[list[str], Inject], callback: PluginFunction["Context", None]):
        self._obj.inject(deps, callback)

    def require(self, name: str, config: Optional[dict[str, Any]] = None, version: Optional[str] = None):
        plugin = javascript.require(name, version)
        if not plugin.apply:
            self._obj.plugin(plugin["default"], config)
        else:
            self._obj.plugin(plugin, config)

    def requires(self, *names: str, config: Optional[dict[str, dict[str, Any]]] = None):
        for name in names:
            self.require(name, config.get(name) if config else None)

    def plugin(self, plugin: PluginType, config: Optional[T] = None):
        if isinstance(plugin, dict):
            self._obj.plugin(plugin)
        else:
            self._obj.plugin(plugin, config)

    @overload
    def on(self, name: str, callback: Callable[..., Any], prepend: bool = False) -> Callable[..., bool]: ...

    @overload
    def on(
        self, name: str, *, prepend: bool = False
    ) -> Callable[[Callable[..., Any]], Callable[..., bool]]: ...

    def on(self, name: str, callback: Optional[Callable[..., Any]] = None, prepend: Optional[bool] = None):
        if callback:
            return self._obj.on(name, callback, prepend)

        def wrapper(fn: Callable[..., Any]):
            return self._obj.on(name, fn, prepend)

        return wrapper

    def emit(self, name: str, *args: Any):
        return self._obj.emit(name, *args)

    @overload
    def command(self, cmd: str, config: Optional[CommandConfig] = None, /) -> Command: ...
    @overload
    def command(self, cmd: str, desc: str, config: Optional[CommandConfig] = None, /) -> Command: ...

    def command(self, cmd: str, *args):
        return self._obj.command(cmd, *args)

    def start(self):
        self._obj.start()

    def stop(self):
        self._obj.stop()

    async def daemon(self):
        self.start()
        while True:
            await asyncio.sleep(0.1)

    async def quit(self):
        self.stop()

    async def _main(self):
        await self.daemon()
        await self.quit()

    def run(self):
        loop = asyncio.events.new_event_loop()
        try:
            asyncio.events.set_event_loop(loop)
            return loop.run_until_complete(self._main())
        except KeyboardInterrupt:
            logger.warning("Interrupt detected, stopping ...")
        finally:
            try:
                to_cancel = asyncio.tasks.all_tasks(loop)
                if not to_cancel:
                    return

                for task in to_cancel:
                    task.cancel()

                loop.run_until_complete(asyncio.gather(*to_cancel, loop=loop, return_exceptions=True))

                for task in to_cancel:
                    if task.cancelled():
                        continue
                    if task.exception() is not None:
                        loop.call_exception_handler(
                            {
                                "message": "unhandled exception during asyncio.run() shutdown",
                                "exception": task.exception(),
                                "task": task,
                            }
                        )
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.run_until_complete(loop.shutdown_default_executor())
            finally:
                asyncio.events.set_event_loop(None)
                loop.close()
