from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class SMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_md() for e in inner])
        return f"**{content}**"

class EMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_md() for e in inner])
        return f"*{content}*"

class Strong(Symbol):
    html = "strong"
    md = SMD()
    rst = "**"

class Em(Symbol):
    html = "em"
    md = EMD()
    rst = "*"