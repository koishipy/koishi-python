from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Iterable, List, Literal, Optional, TypedDict, TypeVar, Union
from typing_extensions import overload

from .element import Fragment
from .models import Channel, Event, Guild, Member, User

if TYPE_CHECKING:
    from .context import Context

T = TypeVar("T")


class Stripped(TypedDict):
    content: str
    prefix: str
    appel: bool
    hasAt: bool
    atSelf: bool


class SendOptions(TypedDict, total=False):
    session: "Session"
    linkPreview: bool


class PromptOptions(TypedDict, total=False):
    timeout: float


class SuggestOptions(TypedDict, total=False):
    actual: bool
    expect: list[str]
    filter: Callable[[str], bool]
    prefix: str
    suffix: str
    timeout: float


class Session:
    id: int
    app: "Context"
    event: Event
    locales: List[str] = []

    user: Optional[User] = None
    channel: Optional[Channel] = None
    guild: Optional[Guild] = None
    permissions: List[str] = []
    scope: Optional[str] = None
    response: Optional[Any] = None

    _stripped: Stripped

    @property
    def isDirect(self) -> bool:
        return self.channel and self.channel.type == "private"  # type: ignore

    @property
    def author(self) -> Union[User, Member]:
        return self.user if self.isDirect else self.event.author  # type: ignore

    @property
    def uid(self) -> str:
        return self.user.id  # type: ignore

    @property
    def gid(self) -> str:
        return self.guild.id  # type: ignore

    @property
    def cid(self) -> str:
        return self.channel.id  # type: ignore

    @property
    def fid(self) -> str:
        return self.event.message.id  # type: ignore

    @property
    def sid(self) -> str:
        return self.event.self_id  # type: ignore

    @property
    def elements(self) -> List[Fragment]:
        return self.event.message.elements  # type: ignore

    @property
    def content(self) -> str:
        return self.event.message.content  # type: ignore

    @property
    def username(self) -> str:
        return self.user.name  # type: ignore

    @property
    def stripped(self) -> Stripped:
        return self._stripped

    def send(self, fragment: Fragment, options: Optional[SendOptions] = None, /): ...

    def cancelQueued(self, delay: float = 1, /): ...

    def sendQueued(self, fragment: Fragment, delay: Optional[float] = None, /): ...

    def getChannel(self, id: Optional[str] = None, fields: Optional[list[str]] = None, /) -> Channel: ...

    def observeChannel(self, fields: Iterable[str], /) -> Channel: ...

    def getUser(self, id: Optional[str] = None, fields: Optional[list[str]] = None, /) -> User: ...

    def observeUser(self, fields: Iterable[str], /) -> User: ...

    def withScope(self, scope: str, callback: Callable[..., str]) -> str: ...

    def resolveScope(self, scope: str, /) -> str: ...

    def text(self, path: Union[str, list[str]], params: Optional[dict[str, Any]] = None, /) -> str: ...

    def i18n(
        self, path: Union[str, list[str]], params: Optional[dict[str, Any]] = None, /
    ) -> list[Fragment]: ...

    def execute(self, content: str, next: Union[Literal[True], Callable[..., Any]], /): ...

    def middleware(self, middleware: Callable[["Session", Callable[..., Any]], Any], /): ...

    @overload
    def prompt(self, timeout: Optional[float] = None, /) -> str: ...
    @overload
    def prompt(self, callback: Callable[["Session"], T], options: Optional[PromptOptions] = None, /) -> T: ...
    def prompt(self, *args) -> Any: ...

    def suggest(self, options: SuggestOptions): ...
