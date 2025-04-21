from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        alt = symbol.get_prop("alt", "")
        return f"![{alt}]({symbol.get_prop('src')})"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return f".. image:: {symbol.get_prop('src')}\n   :alt: {symbol.get_prop("alt", "")}\n"

class Img(Symbol):
    prop_list = ["alt", "attributionsrc", "crossorigin", "decoding", "elementtiming", "fetchpriority", "height", "ismap", "loading", "referrerpolicy", "sizes", "src", "srcset",  "width", "usemap", "align", "border", "hspace", "longdesc", "name", "vspace"]
    md = MD()
    html = "img"
    rst = RST()
    type = "void"