from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return "---\n"

class Hr(Symbol):
    html = "hr"
    md = MD()
    nl = True 