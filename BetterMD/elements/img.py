from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        alt = symbol.get_prop("alt", "")
        return f"![{alt}]({symbol.get_prop('src')})"

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent, **kwargs):
        return f"<img src={symbol.get_prop('src')} alt={symbol.get_prop('alt', '')} />"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs):
        return f".. image:: {symbol.get_prop('src')}\n   :alt: {symbol.get_prop("alt", "")}\n"

class Img(Symbol):
    prop_list = ["src", "alt"]
    md = MD()
    html = HTML()
    rst = RST()