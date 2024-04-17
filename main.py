from koishi import Context, Session, ctx, h

ctx.requires(
    "@koishijs/plugin-console",
    "@koishijs/plugin-sandbox",
    "@koishijs/plugin-echo",
    "@koishijs/plugin-help",
    "@koishijs/plugin-server",
    config={
        "@koishijs/plugin-server": {"port": 5140},
    },
)


def test(x: Context, *_):
    def handle(session: Session, *args):
        if session.content == "天王盖地虎":
            session.send(["宝塔镇河妖", h.at(session.event.user.id, {"name": session.event.user.name})])

    x.on("message", handle)


ctx.plugin({"apply": test})
ctx.command("echo1 <message:text>", "输出收到的信息", {"checkArgCount": True}).option(
    "timeout", "-t <seconds> 设定延迟发送的时间"
).usage("注意：参数请写在最前面，不然会被当成 message 的一部分！").example(
    "echo -t 300 Hello World  五分钟后发送 Hello World"
).action(
    lambda cmd, _, *args: args[0]
)

ctx.command("test").option("alpha", "-a").option("beta", "-b [beta]").option("gamma", "-c <gamma>").action(
    lambda cmd, argv, *args: str(argv.get("options"))
)


ctx.run()
