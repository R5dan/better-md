from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return f"*{''.join([e.to_md() for e in inner])}*"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return f"*{''.join([e.to_rst() for e in inner])}*"

class I(Symbol):
    html = "i"
    md = MD()
    rst = RST() 