from typing import Any, Callable, Optional, TypedDict, Awaitable
from typing_extensions import Unpack

from .models import Session

class CommandConfig(TypedDict, total=False):
    hidden: bool


class OptionConfig(TypedDict, total=False):
    hidden: bool
    fallback: Any
    value: Any
    type: Any


class AliasConfig(TypedDict, total=False):
    args: list[str]


class Message:
    rest: str
    source: str
    root: bool
    session: Session
    command: "Command"
    args: list[str]
    options: dict[str, Any]
    error: str
    next: Callable[..., Awaitable[Any]]


class Command:
    def option(self, name: str, decl: str, config: Optional[OptionConfig] = None, /) -> "Command": ...
    def action(self, callback: Callable[["Command", Message, Unpack[tuple]], Any]) -> "Command": ...
    def alias(self, name: str, config: Optional[AliasConfig] = None, /) -> "Command": ...
    def usage(self, text: str) -> "Command": ...
    def example(self, text: str) -> "Command": ...
    def subcommand(self, name: str, config: Optional[CommandConfig] = None, /) -> "Command": ...
