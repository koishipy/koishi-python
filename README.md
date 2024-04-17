# koishi-python

在 python 下运行 koishi 的实例

## 安装

```bash
pip install "koishi-python @ git+https://github.com/koishipy/koishi-python"
```

## 使用

```python
from koishi import ctx

ctx.requires(
    "@koishijs/plugin-console",
    "@koishijs/plugin-sandbox",
    "@koishijs/plugin-server",
    config={
        "@koishijs/plugin-server": {"port": 5140},
    },
)

ctx.command("echo <message:text>", "输出收到的信息", {"checkArgCount": True})\
    .action(lambda _, __, *args: args[0])

ctx.run()
```

## 注意事项

1. 你 require 的 npm 包会自动安装，但是每安装完一次会报错然后退出，这是正常现象，不用担心。
2. 启动后会出现一些警告信息，这些对运行没有影响
3. 目前默认安装 koishi 最新版
4. 因为运行位置在 site-packages 下，`koishi` 会自动在运行目录下建立软链接。
