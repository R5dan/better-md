from .symbol import Symbol
from ..html import CustomHTML

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
        return f"<!--{inner[-1].to_html()}-->"

    def verify(self, text: str) -> bool:
        return text.lower() == "!--"

class Comment(Symbol):
    md = ""
    html = HTML()
    rst = ""