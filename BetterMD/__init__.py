from .elements import *
from .elements import Symbol
from .parse import Collection, HTMLParser, MDParser, RSTParser

def from_html(html:'str'):
    return Symbol.from_html(html)

def from_md(md:'str'):
    return Symbol.from_md(md)