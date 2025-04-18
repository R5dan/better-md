from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if isinstance(parent, OL):
            return f"\n1. {" ".join([e.to_md() for e in inner])}"
        return f"\n- {" ".join([e.to_md() for e in inner])}"
    
class RST(CustomRst):
    def to_rst(self, inner, symbol, parent) -> str:
        content = " ".join([e.to_rst() for e in inner])
        if isinstance(parent, OL):
            if v := symbol.props.get("value", None):
                return f"{v}. {content}" 
            return f"#. {content}"
        return f"* {content}"
    
class LMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent) -> str:
        if isinstance(parent, LI):
            return "    \n".join([e.to_md() for e in inner])
        return " ".join([e.to_md() for e in inner])

class LRST(CustomRst):
    def to_rst(self, inner, symbol, parent) -> str:
        if isinstance(parent, LI):
            return "    \n".join([e.to_rst() for e in inner])
        return f"\n\n{"\n".join([e.to_rst() for e in inner])}\n\n"


class LI(Symbol):
    prop_list = ["value", "type"]

    html = "li"
    md = MD()
    rst = RST()

class OL(Symbol):
    prop_list = ["reversed", "start", "type"]
    html = "ol"
    md = LMD()
    rst = LRST()

class UL(Symbol):
    prop_list = ["compact", "type"]

    html = "ul"
    md = LMD()
    rst = LRST()