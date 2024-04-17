from typing import Any, Final, Optional, Union, overload
from typing_extensions import TypeAlias

import javascript

_Element = javascript.require("@satorijs/core").Element


class Element:
    type: str
    attrs: dict[str, Any]
    children: list["Element"] = []

    @staticmethod
    def text(content: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element":
        return _Element["text"](content, attrs)

    @staticmethod
    def at(uid: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element":
        return _Element["at"](uid, attrs)

    @staticmethod
    def sharp(cid: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element":
        return _Element["sharp"](cid, attrs)

    @staticmethod
    def quote(mid: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element":
        return _Element["quote"](mid, attrs)

    @staticmethod
    @overload
    def image(data: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    @overload
    def image(data: bytes, dtype: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    def image(*args) -> "Element":
        return _Element["image"](*args)

    @staticmethod
    @overload
    def img(data: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    @overload
    def img(data: bytes, dtype: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    def img(*args) -> "Element":
        return _Element["img"](*args)

    @staticmethod
    @overload
    def video(data: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    @overload
    def video(data: bytes, dtype: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    def video(*args) -> "Element":
        return _Element["video"](*args)

    @staticmethod
    @overload
    def audio(data: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    @overload
    def audio(data: bytes, dtype: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    def audio(*args) -> "Element":
        return _Element["audio"](*args)

    @staticmethod
    @overload
    def file(data: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    @overload
    def file(data: bytes, dtype: str, attrs: Optional[dict[str, Any]] = None, /) -> "Element": ...

    @staticmethod
    def file(*args) -> "Element":
        return _Element["file"](*args)

    @staticmethod
    def i18n(path: Union[str, dict[str, Any]], children: Optional[list] = None, /) -> "Element":
        return _Element["i18n"](path, children)


h: Final = Element
Fragment: TypeAlias = Union[str, Element, list[Union[str, Element]]]
