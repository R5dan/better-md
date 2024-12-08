from .symbol import Symbol
from ..html import CustomHTML
import typing as t

class HTML(CustomHTML):
    def __init__(self, t:'OLi|ULi'):
        self.t = t
        super().__init__()

    def prepare(self, inner, symbol, parent):
        if not isinstance(parent, (UL, OL)):
            if isinstance(self.t, OLi): l = parent.has_child(OL) or OL()
            else: l = parent.has_child(UL) or UL()
            
            parent.add_child(l)

            symbol.change_parent(l)


    def to_html(self, inner:'Symbol', symbol:'Symbol', parent:'Symbol'):
        return f"<li value={symbol.vars.get("i", "")} >{inner.to_html()}</li>"

class UL(Symbol):
    md = ""
    html = "ul"

class OL(Symbol):
    md = ""
    html = "ol"

class ULi(Symbol):
    md = "-"
    html = "li"

class OLi(Symbol):
    md = "{i}."
    html = HTML(OL)


class LI(Symbol):
    def prepare(self, parent):
        if self.vars.get("l"):
            parent.replace_child(self, OL())
        else:
            parent.replace_child(self, UL())