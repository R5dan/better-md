from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        alt = symbol.get_prop("alt", "")
        return f"![{alt}]({symbol.get_prop('src')})"

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
        return f"<img src={symbol.get_prop('src')} alt={symbol.get_prop('alt', '')} />"

class Img(Symbol):
    props = ["src", "alt"]
    md = MD()
    html = HTML() 