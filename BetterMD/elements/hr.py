from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return f"---\n"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return "----\n"

class Hr(Symbol):
    prop_list = ["align", "color", "noshade", "size", "width"]

    html = "hr"
    md = MD()
    rst = RST()
    type = "void"  # Changed from block=True and self_closing=True