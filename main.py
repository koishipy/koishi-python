import asyncio
from koishi import ctx, Context, Session

console = ctx.require("@koishijs/plugin-console")
sandbox = ctx.require("@koishijs/plugin-sandbox")
echo = ctx.require("@koishijs/plugin-echo")
server = ctx.require('@koishijs/plugin-server', {"port": 5140})


def test(x: Context, *_):
    def handle(session: Session, *args):
        if session.content == "天王盖地虎":
            session.send("宝塔镇河妖")
    x.on("message", handle)


ctx.plugin({"apply": test})
# ctx.command("天王盖地虎").action(lambda *args: "宝塔镇河妖")


async def main():
    await ctx.start()

asyncio.run(main())
