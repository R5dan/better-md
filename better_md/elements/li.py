from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if isinstance(parent, OL):
            return f"1. {" ".join([e.to_md() for e in inner])}"
        return f"- {inner.to_md()}\n"


class LI(Symbol):
    html = "li"
    md = MD()

class OL(Symbol):
    html = "ol"
    md = ""

class UL(Symbol):
    html = "ul"
    md = ""