from .elements import *
from .elements import Symbol
from .parse import Collection, HTMLParser, MDParser

class HTML:
    @staticmethod
    def from_string(html:'str'):
        return Symbol.from_html(html)

    @staticmethod
    def from_file(file):
        return Symbol.from_html(file)
    
    @staticmethod
    def from_url(url):
        import requests as r
        text = r.get(url).text

        if text.startswith("<!DOCTYPE html>"):
            text = text[15:]

        return Symbol.from_html(text)

class MD:
    @staticmethod
    def from_string(md:'str'):
        return Symbol.from_md(md)

    @staticmethod
    def from_file(file):
        return Symbol.from_md(file)
    
    @staticmethod
    def from_url(url):
        import requests as r
        text = r.get(url).text
        return Symbol.from_md(text)

__all__ = ["HTML", "MD", "Symbol", "Collection", "HTMLParser", "MDParser"]
