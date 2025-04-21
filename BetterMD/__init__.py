from .elements import *
from .html import CustomHTML
from .markdown import CustomMarkdown
from .rst import CustomRst
from .parse import HTMLParser, MDParser, Collection
from .utils import enable_debug_mode
import typing as _t

if _t.TYPE_CHECKING:
    class Readable(_t.Protocol):
        def read(self) -> 'str': ...

class HTML:
    @staticmethod
    def from_string(html:'str'):
        return Symbol.from_html(html)

    @staticmethod
    def from_file(file: 'Readable'):
        return Symbol.from_html(file.read())

    @staticmethod
    def from_url(url:'str'):
        import requests as r
        text = r.get(url).text

        if text.startswith("<!DOCTYPE html>"):
            text = text[15:]

        ret = Symbol.from_html(text)

        if len(ret) == 1:
            return ret[0]

        return ret

class MD:
    @staticmethod
    def from_string(md:'str'):
        return Symbol.from_md(md)

    @staticmethod
    def from_file(file: 'Readable'):
        return Symbol.from_md(file.read())

    @staticmethod
    def from_url(url):
        import requests as r
        text = r.get(url).text
        return Symbol.from_md(text)

__all__ = ["HTML", "MD", "Symbol", "Collection", "HTMLParser", "MDParser", "CustomHTML", "CustomMarkdown", "CustomRst", "enable_debug_mode"]
