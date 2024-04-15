import os
import javascript
from pathlib import Path
from typing import TYPE_CHECKING
from .typing import PluginType

_init = False


def init():
    global koishi, Context, _init
    main_path = Path.cwd()
    js_path = Path(javascript.__file__)
    node_src = js_path.parent / "js" / "node_modules"
    node_src.mkdir(parents=True, exist_ok=True)
    node_dst = main_path / "node_modules"
    os.symlink(node_src.as_posix(), node_dst.as_posix(), target_is_directory=True)
    package_src = js_path.parent / "js" / "package.json"
    package_lock_src = js_path.parent / "js" / "package-lock.json"
    package_dst = main_path / "package.json"
    package_lock_dst = main_path / "package-lock.json"
    os.symlink(package_src.as_posix(), package_dst.as_posix())
    os.symlink(package_lock_src.as_posix(), package_lock_dst.as_posix())

    if TYPE_CHECKING:
        from .typing import TKoishi as koishi
        from .typing import Context as Context
    else:
        koishi = javascript.require("koishi")
        Context = koishi['Context']
    _init = True


def plugin_require(name: str) -> PluginType:
    return javascript.require(name)  # type: ignore


def plugins_require(name: str) -> dict[str, PluginType]:
    return javascript.require(name)  # type: ignore


def __getattr__(name):
    if name == "init":
        return init
    if not _init:
        raise RuntimeError("Not Initialize Environment yet!\nPlease Calling `koishi_python.init()` first")
    return globals()[name]


__all__ = [
    "Context",
    "koishi",
    "plugin_require",
    "plugins_require"
]
