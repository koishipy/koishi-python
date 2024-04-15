from typing import TypedDict, overload, Protocol, Optional, Union, TypeVar, Callable, Any, Literal
from typing_extensions import TypeAlias

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


Disposable: TypeAlias = Callable[..., None]


class HasDisposable(Protocol):
    def dispose(self) -> None: ...


DisposableLike: TypeAlias = Union[Disposable, HasDisposable]


TDisp = TypeVar("TDisp", bound=DisposableLike)
R = TypeVar("R")
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
    root: "Context"
    config: Any

    def inject(self, deps: Union[list[str], Inject], callback: PluginFunction["Context", None]): ...

    def plugin(self, plugin: PluginType, *args): ...

    @overload
    def effect(self, callback: Callable[["Context"], TDisp]) -> TDisp: ...
    @overload
    def effect(self, callback: Callable[["Context", R], TDisp], config: R) -> TDisp: ...
    def effect(self, callback, config: Optional[Any] = None) -> Any: ...

    def on(self, name: str, listener: Callable[..., Any], prepend: Optional[bool] = None) -> Callable[..., bool]: ...

    def start(self): ...
    def stop(self): ...


class TKoishi(TypedDict):
    Context: type[Context]
