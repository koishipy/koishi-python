from typing import Any, Awaitable, Callable, Optional, TypedDict, Union, overload
from typing_extensions import Unpack

from .session import Session


class CommandBaseConfig(TypedDict, total=False):
    strictOptions: bool


class CommandConfig(CommandBaseConfig, total=False):
    checkUnknown: bool
    checkArgCount: bool
    showWarning: bool
    handleError: Union[bool, Callable[[Exception, Any], Awaitable[Any]]]
    slash: bool

    hidden: Union[bool, Callable[..., bool]]
    hideOptions: bool
    params: dict[str, Any]


class PermissionConfig(TypedDict, total=False):
    authority: float
    permissions: list[str]
    dependencies: list[str]


class OptionConfig(PermissionConfig, total=False):
    aliases: list[str]
    symbols: list[str]
    fallback: Any
    value: Any
    type: Any
    descPath: str

    hidden: Union[bool, Callable[..., bool]]
    params: dict[str, Any]


class AliasConfig(TypedDict, total=False):
    options: dict[str, Any]
    args: list[str]
    filter: Union[bool, Callable[..., bool]]


class Argv(TypedDict, total=False):
    args: list
    options: dict[str, Any]
    error: str
    source: str
    initiator: str
    terminator: str
    session: Session
    command: "Command"
    rest: str
    pos: int
    root: bool
    tokens: list
    name: str
    next: Callable[..., Awaitable[Any]]


class Command:
    def option(self, name: str, desc: str, config: Optional[OptionConfig] = None, /) -> "Command": ...
    def action(
        self, callback: Callable[["Command", Argv, Unpack[tuple]], Any], prepend: bool = False
    ) -> "Command": ...
    @overload
    def alias(self, *names: str) -> "Command": ...
    @overload
    def alias(self, name: str, config: Optional[AliasConfig] = None, /) -> "Command": ...
    def alias(self, *args) -> "Command": ...
    def usage(self, text: str) -> "Command": ...
    def example(self, text: str) -> "Command": ...

    @overload
    def subcommand(self, name: str, config: Optional[CommandConfig] = None, /) -> "Command": ...
    @overload
    def subcommand(self, name: str, desc: str, config: Optional[CommandConfig] = None, /) -> "Command": ...
    def subcommand(self, *args) -> "Command": ...
