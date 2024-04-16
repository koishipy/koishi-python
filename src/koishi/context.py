import asyncio
from typing import TypedDict, overload, Protocol, Optional, Union, TypeVar, Callable, Any, Literal
from typing_extensions import TypeAlias
from .command import Command, CommandConfig

import javascript

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
    PluginDictObject
]


class Context:
    def __init__(self, ctx_obj: javascript.proxy.Proxy):
        self._obj = ctx_obj()

    @property
    def root(self):
        if self._obj.root == self._obj:
            return self
        return Context(self._obj.root)

    @property
    def config(self):
        return self._obj.config

    def inject(self, deps: Union[list[str], Inject], callback: PluginFunction["Context", None]):
        self._obj.inject(deps, callback)

    def require(self, name: str, config: Optional[dict[str, Any]] = None, version: Optional[str] = None):
        plugin = javascript.require(name, version)
        if not plugin.apply:
            self._obj.plugin(plugin["default"], config)
        else:
            self._obj.plugin(plugin, config)

    def plugin(self, plugin: PluginType, config: Optional[T] = None):
        if isinstance(plugin, dict):
            self._obj.plugin(plugin)
        else:
            self._obj.plugin(plugin, config)

    @overload
    def on(self, name: str, callback: Callable[..., Any], prepend: bool = False) -> Callable[..., bool]:
        ...

    @overload
    def on(self, name: str, *, prepend: bool = False) -> Callable[[Callable[..., Any]], Callable[..., bool]]:
        ...

    def on(self, name: str, callback: Optional[Callable[..., Any]] = None, prepend: Optional[bool] = None):
        if callback:
            return self._obj.on(name, callback, prepend)

        def wrapper(fn: Callable[..., Any]):
            return self._obj.on(name, fn, prepend)

        return wrapper

    def emit(self, name: str, *args: Any):
        return self._obj.emit(name, *args)

    def command(self, cmd: str, config: Optional[CommandConfig] = None, /) -> Command:
        return self._obj.command(cmd, config)

    def start(self):
        loop = asyncio.get_running_loop()

        async def _task():
            self._obj.start()
            while True:
                await asyncio.sleep(0.01)

        return loop.create_task(_task(), name="Koishi-Daemon")

    def stop(self):
        self._obj.stop()
