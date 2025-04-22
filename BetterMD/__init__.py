from . import elements
from .html import CustomHTML
from .markdown import CustomMarkdown
from .rst import CustomRst
from .parse import HTMLParser, MDParser, Collection
from .utils import enable_debug_mode
import typing as _t

if _t.TYPE_CHECKING:
    class Readable(_t.Protocol):
        def read(self) -> str: ...

class HTML:
    @staticmethod
    def from_string(html:'str'):
        return elements.Symbol.from_html(html)

    @staticmethod
    def from_file(file: 'Readable'):
        try:
            text = file.read()
        except Exception as e:
            raise IOError(f"Error reading HTML file: {e}")

        return elements.Symbol.from_html(text)

    @staticmethod
    def from_url(url:'str'):
        try:
            import requests as r
            text = r.get(url).text

            if text.startswith("<!DOCTYPE html>"):
                text = text[15:]
        except Exception as e:
            raise IOError(f"Error reading HTML from URL: {e}")

        ret = elements.Symbol.from_html(text)

        if len(ret) == 1:
            return ret[0]

        return ret

class MD:
    @staticmethod
    def from_string(md:'str'):
        return elements.Symbol.from_md(md)

    @staticmethod
    def from_file(file: 'Readable'):
        try:
            text = file.read()
        except Exception as e:
            raise IOError(f"Error reading Markdown file: {e}")

        return elements.Symbol.from_md(text)

    @staticmethod
    def from_url(url):
        try:
            import requests as r
            text = r.get(url).text
        except Exception as e:
            raise IOError(f"Error reading Markdown from URL: {e}")

        return elements.Symbol.from_md(text)


__all__ = ["HTML", "MD", "elements", "Collection", "HTMLParser", "MDParser", "CustomHTML", "CustomMarkdown", "CustomRst", "enable_debug_mode"]
