from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML
import typing as t

class MD(CustomMarkdown['A']):
    def to_md(self, inner, symbol, parent):
        return f"[{" ".join([e.to_md() for e in inner])}]({symbol.get_prop("href")})"

class HTML(CustomHTML['A']):
    def to_html(self, inner, symbol, parent):
        return f"<a href={symbol.get_prop('href')}>{" ".join([e.to_html() for e in inner])}</a>"
    
class RST(CustomRst['A']):
    def to_rst(self, inner, symbol, parent):
        return f"`{' '.join([e.to_rst() for e in inner])} <{symbol.get_prop('href')}>`_"

class A(Symbol):
    prop_list = ["href"]
    md = MD()
    html = HTML()
    rst = RST()