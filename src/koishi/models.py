from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, List, Optional


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
    parent_id: Optional[str] = None


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
    is_bot: Optional[bool] = None


@dataclass
class Member:
    user: Optional[User] = None
    nick: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    joined_at: Optional[int] = None


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
    self_id: Optional[str] = None
    platform: Optional[str] = None


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
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


@dataclass
class Event:
    id: int
    type: str
    platform: str
    self_id: str
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


class Session:
    id: int
    event: Event
    locales: List[str] = []
    user: Optional[User] = None
    channel: Optional[Channel] = None
    guild: Optional[Guild] = None
    permissions: List[str] = []
    scope: Optional[str] = None
    response: Optional[Any] = None

    @property
    def content(self) -> str:
        return self.event.message.content  # type: ignore

    def send(self, msg: str): ...
