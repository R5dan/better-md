from .symbol import Symbol
from ..markdown import CustomMarkdown
import typing as t

class MD(CustomMarkdown):
    def to_md(self, inner:'Symbol', symbol:'A', parent:'Symbol'):
        return f"[{inner.to_md()}]({symbol.get_prop("href")})"
    
class A(Symbol):
    props = ["href"]
    md = MD()
    html = "a"