from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        if inner:
            raise ValueError("Hr element must not have any children")
        return f"---\n"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs):
        if inner:
            raise ValueError("Hr element must not have any children")
        return "----\n"

class Hr(Symbol):
    html = "hr"
    md = MD()
    rst = RST()
    nl = True 