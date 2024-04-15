import asyncio
from koishi_python import init

init()

from koishi_python import Context, plugin_require, plugins_require

console = plugins_require("@koishijs/plugin-console")
sandbox = plugin_require("@koishijs/plugin-sandbox")
echo = plugin_require("@koishijs/plugin-echo")
server = plugins_require('@koishijs/plugin-server')


ctx = Context()
ctx.plugin(console["default"])
ctx.plugin(sandbox)
ctx.plugin(echo)
ctx.plugin(server["default"], {"port": 5140})


def test(x: Context, *_):
    def handle(session, *args):
        if session.content == "天王盖地虎":
            session.send("宝塔镇河妖")
    x.on("message", handle)


ctx.plugin({"apply": test})
# ctx.command("天王盖地虎").action(lambda *args: "宝塔镇河妖")


async def main():
    ctx.start()
    while True:
        await asyncio.sleep(0.1)


asyncio.run(main())
