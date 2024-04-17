from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, Generic, List, Optional, TypeVar


class ChannelType(IntEnum):
    TEXT = 0
    DIRECT = 1
    CATEGORY = 2
    VOICE = 3


@dataclass
class Channel:
    id: str
    type: ChannelType
    name: Optional[str] = None
    parentId: Optional[str] = None


@dataclass
class Guild:
    id: str
    name: Optional[str] = None
    avatar: Optional[str] = None


@dataclass
class User:
    id: str
    name: Optional[str] = None
    nick: Optional[str] = None
    avatar: Optional[str] = None
    isBot: Optional[bool] = None


@dataclass
class Member:
    user: Optional[User] = None
    nick: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    joinedAt: Optional[int] = None


@dataclass
class Role:
    id: str
    name: Optional[str] = None


class LoginStatus(IntEnum):
    OFFLINE = 0
    ONLINE = 1
    CONNECT = 2
    DISCONNECT = 3
    RECONNECT = 4


@dataclass
class Login:
    status: LoginStatus
    user: Optional[User] = None
    selfId: Optional[str] = None
    platform: Optional[str] = None
    hidden: Optional[bool] = None


@dataclass
class ArgvInteraction:
    name: str
    arguments: list
    options: Any


@dataclass
class ButtonInteraction:
    id: str


class Opcode(IntEnum):
    EVENT = 0
    PING = 1
    PONG = 2
    IDENTIFY = 3
    READY = 4


@dataclass
class Identify:
    token: Optional[str] = None
    sequence: Optional[int] = None


@dataclass
class Ready:
    logins: List[Login]


@dataclass
class MessageObject:
    id: str
    content: str
    channel: Optional[Channel] = None
    guild: Optional[Guild] = None
    member: Optional[Member] = None
    user: Optional[User] = None
    createdAt: Optional[int] = None
    updatedAt: Optional[int] = None


@dataclass
class Event:
    id: int
    type: str
    platform: str
    selfId: str
    timestamp: datetime
    argv: Optional[ArgvInteraction] = None
    button: Optional[ButtonInteraction] = None
    channel: Optional[Channel] = None
    guild: Optional[Guild] = None
    login: Optional[Login] = None
    member: Optional[Member] = None
    message: Optional[MessageObject] = None
    operator: Optional[User] = None
    role: Optional[Role] = None
    user: Optional[User] = None

    _type: Optional[str] = None
    _data: Optional[dict] = None


T = TypeVar("T")


@dataclass
class PageResult(Generic[T]):
    data: List[T]
    next: Optional[str] = None
