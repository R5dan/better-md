from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return "\n\n"

class Br(Symbol):
    html = "br"
    md = MD() 