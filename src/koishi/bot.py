from typing import TYPE_CHECKING, Any, Generic, Iterable, Optional, TypeVar, Union
from typing_extensions import Self

from .element import Fragment
from .models import Channel, Guild, Login, LoginStatus, Member, MessageObject, PageResult, Role, User

if TYPE_CHECKING:
    from .adapter import Adapter
    from .context import Context
    from .session import SendOptions, Session

T = TypeVar("T")


class Bot(Generic[T]):
    user: User
    isBot: bool = True
    hidden: bool = False
    platform: str
    selfId: str
    adapter: "Adapter[Self]"
    error: Optional[Exception] = None
    callbacks: dict[str, Any]
    config: T

    _status: LoginStatus

    def __init__(self, ctx: "Context", config: T, platform: Optional[str] = None):
        self.internal = None
        self.context = ctx
        self.config = config
        if platform:
            self.platform = platform
        raise NotImplementedError("Bot is an abstract class")

    def update(self, login: Login): ...

    def dispose(self): ...

    @property
    def status(self) -> LoginStatus:
        return self._status

    @status.setter
    def status(self, value: LoginStatus):
        self._status = value

    @property
    def isActive(self) -> bool:
        return self.status != LoginStatus.OFFLINE and self.status != LoginStatus.DISCONNECT

    def online(self): ...

    def offline(self): ...

    def start(self): ...

    def stop(self): ...

    @property
    def sid(self) -> str:
        return f"{self.platform}:{self.selfId}"

    def session(self, event: dict) -> "Session": ...

    def dispatch(self, session: "Session"): ...

    def createMessage(
        self,
        channelId: str,
        content: Fragment,
        guildId: Optional[str] = None,
        options: Optional["SendOptions"] = None,
        /,
    ) -> list[MessageObject]: ...

    def sendMessages(
        self,
        channelId: str,
        content: Fragment,
        guildId: Optional[str] = None,
        options: Optional["SendOptions"] = None,
        /,
    ) -> list[str]: ...

    def sendPrivateMessage(
        self,
        userId: str,
        content: Fragment,
        guildId: Optional[str] = None,
        options: Optional["SendOptions"] = None,
        /,
    ) -> list[str]: ...

    def checkPermission(self, name: str, session: "Session") -> bool: ...

    def getMessage(self, channelId: str, messageId: str, /) -> MessageObject: ...

    def getMessageList(self, channelId: str, next: Optional[str] = None, /) -> PageResult[MessageObject]: ...

    def getMessageIter(self, channelId: str, /) -> Iterable[MessageObject]: ...

    def editMessage(self, channelId: str, messageId: str, content: Fragment, /) -> None: ...

    def deleteMessage(self, channelId: str, messageId: str, /) -> None: ...

    def createReaction(self, channelId: str, messageId: str, emoji: str, /) -> None: ...

    def deleteReaction(
        self, channelId: str, messageId: str, emoji: str, userId: Optional[str] = None, /
    ) -> None: ...

    def clearReactions(self, channelId: str, messageId: str, emoji: Optional[str] = None, /) -> None: ...

    def getReactionList(
        self, channelId: str, messageId: str, emoji: str, next: Optional[str] = None, /
    ) -> PageResult[User]: ...

    def getReactionIter(self, channelId: str, messageId: str, emoji: str, /) -> Iterable[User]: ...

    def getLogin(self) -> Login: ...

    def getUser(self, userId: str, guildId: Optional[str] = None, /) -> User: ...

    def getFriendList(self, next: Optional[str] = None, /) -> PageResult[User]: ...

    def getFriendIter(self, /) -> Iterable[User]: ...

    def deleteFriend(self, userId: str, /) -> None: ...

    def getGuild(self, guildId: str, /) -> Guild: ...

    def getGuildList(self, next: Optional[str] = None, /) -> PageResult[Guild]: ...

    def getGuildIter(self, /) -> Iterable[Guild]: ...

    def getGuildMember(self, guildId: str, userId: str, /) -> Member: ...

    def getGuildMemberList(self, guildId: str, next: Optional[str] = None, /) -> PageResult[Member]: ...

    def getGuildMemberIter(self, guildId: str, /) -> Iterable[Member]: ...

    def kickGuildMember(self, guildId: str, userId: str, permanent: bool = False, /) -> None: ...

    def muteGuildMember(
        self, guildId: str, userId: str, duration: float, reason: Optional[str] = None, /
    ) -> None: ...

    def setGuildMemberRole(self, guildId: str, userId: str, roleId: str, /) -> None: ...

    def unsetGuildMemberRole(self, guildId: str, userId: str, roleId: str, /) -> None: ...

    def getGuildRoleList(self, guildId: str, next: Optional[str] = None, /) -> PageResult[Role]: ...

    def getGuildRoleIter(self, guildId: str, /) -> Iterable[Role]: ...

    def createGuildRole(self, guildId: str, data: dict, /) -> Role: ...

    def updateGuildRole(self, guildId: str, roleId: str, data: dict, /) -> Role: ...

    def deleteGuildRole(self, guildId: str, roleId: str, /) -> None: ...

    def getChannel(self, channelId: str, /) -> Channel: ...

    def getChannelList(
        self, guildId: Optional[str] = None, next: Optional[str] = None, /
    ) -> PageResult[Channel]: ...

    def getChannelIter(self, guildId: Optional[str] = None, /) -> Iterable[Channel]: ...

    def createDirectChannel(self, userId: str, guildId: Optional[str] = None, /) -> Channel: ...

    def createChannel(self, guildId: str, data: dict, /) -> Channel: ...

    def updateChannel(self, channelId: str, data: dict, /) -> Channel: ...

    def deleteChannel(self, channelId: str, /) -> None: ...

    def muteChannel(self, channelId: str, guildId: Optional[str] = None, enable: bool = True, /) -> None: ...

    def handleFriendRequest(
        self, messageId: str, approve: bool, comment: Optional[str] = None, /
    ) -> None: ...

    def handleGuildRequest(self, messageId: str, approve: bool, comment: Optional[str] = None, /) -> None: ...

    def handleGuildMemberRequest(
        self, messageId: str, approve: bool, comment: Optional[str] = None, /
    ) -> None: ...

    def broadcast(
        self,
        channels: list[Union[str, tuple[str, str], "Session"]],
        content: Fragment,
        delay: Optional[float] = None,
        /,
    ) -> list[str]: ...
