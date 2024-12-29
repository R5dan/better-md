from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        if isinstance(parent, OL):
            return f"\n1. {" ".join([e.to_md() for e in inner])}"
        return f"\n- {" ".join([e.to_md() for e in inner])}"
    
class RST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs) -> str:
        content = " ".join([e.to_rst() for e in inner])
        if isinstance(parent, OL):
            if v := symbol.props.get("value", None):
                return f"{v}. {content}" 
            return f"#. {content}"
        return f"* {content}"
    
class LMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs) -> str:
        if isinstance(parent, LI):
            return "    \n".join([e.to_md() for e in inner])
        return " ".join([e.to_md() for e in inner])

class LRST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs) -> str:
        if isinstance(parent, LI):
            return "    \n".join([e.to_rst() for e in inner])
        return " ".join([e.to_rst() for e in inner])


class LI(Symbol):
    html = "li"
    md = MD()
    rst = RST()

class OL(Symbol):
    html = "ol"
    md = LMD()
    rst = LRST()

class UL(Symbol):
    html = "ul"
    md = LMD()
    rst = LRST()