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
        t = r.get(url).text[15:]
        print(t[:1000])
        return Symbol.from_html(t)

class MD:
    @staticmethod
    def from_string(md:'str'):
        return Symbol.from_md(md)
