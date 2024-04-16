import os
import javascript
from pathlib import Path

from .models import Session as Session
from .context import Context as Context

_koishi = javascript.require("koishi")
_Context = _koishi['Context']
main_path = Path.cwd()
js_path = Path(javascript.__file__)
node_src = js_path.parent / "js" / "node_modules"
node_src.mkdir(parents=True, exist_ok=True)
node_dst = main_path / "node_modules"
if node_src.exists() and not node_dst.exists():
    os.symlink(node_src.as_posix(), node_dst.as_posix(), target_is_directory=True)
package_src = js_path.parent / "js" / "package.json"
package_lock_src = js_path.parent / "js" / "package-lock.json"
package_dst = main_path / "package.json"
package_lock_dst = main_path / "package-lock.json"
if package_src.exists() and not package_dst.exists():
    os.symlink(package_src.as_posix(), package_dst.as_posix())
if package_lock_src.exists() and not package_lock_dst.exists():
    os.symlink(package_lock_src.as_posix(), package_lock_dst.as_posix())

ctx = Context(_Context)
