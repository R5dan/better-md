from .symbol import Symbol
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        content = " ".join([e.to_md() for e in inner])
        if isinstance(symbol, Strong):
            return f"**{content}**"
        elif isinstance(symbol, Em):
            return f"*{content}*"
        elif isinstance(symbol, Code):
            return f"`{content}`"
        return content

class Strong(Symbol):
    html = "strong"
    md = MD()

class Em(Symbol):
    html = "em"
    md = MD()

class Code(Symbol):
    html = "code"
    md = MD() 