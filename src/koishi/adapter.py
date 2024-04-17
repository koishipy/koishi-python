from typing import TYPE_CHECKING, Generic, TypeVar

from .bot import Bot

if TYPE_CHECKING:
    from .context import Context

B = TypeVar("B", bound=Bot)


class Adapter(Generic[B]):
    schema = False

    bots: list[B]

    def __init__(self, ctx: "Context"):
        self.context = ctx
        self.bots = []

    def connect(self, bot: B):
        self.bots.append(bot)

    def disconnect(self, bot: B):
        self.bots.remove(bot)

    def fork(self, ctx: "Context", bot: B):
        bot.adapter = self
        self.bots.append(bot)
        ctx.on("dispose", lambda: self.disconnect(bot))
