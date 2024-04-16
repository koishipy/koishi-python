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
ctx.command('echo1 <message:text> 输出收到的信息')\
  .option('timeout', '-t <seconds> 设定延迟发送的时间')\
  .usage('注意：参数请写在最前面，不然会被当成 message 的一部分！')\
  .example('echo -t 300 Hello World  五分钟后发送 Hello World')\
  .action(lambda cmd, _, *args: args[-1])


async def main():
    await ctx.start()

asyncio.run(main())
