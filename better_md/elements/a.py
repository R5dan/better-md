from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML
import typing as t

class MD(CustomMarkdown):
    def to_md(self, inner:'Symbol', symbol:'A', parent:'Symbol'):
        return f"[{" ".join([e.to_md() for e in inner])}]({symbol.get_prop("href")})"

class HTML(CustomHTML):
    def to_html(self, inner:'Symbol', symbol:'A', parent:'Symbol'):
        return f"<a href={symbol.get_prop('href')}>{" ".join([e.to_html() for e in inner])}</a>"
    
class A(Symbol):
    props = ["href"]
    md = MD()
    html = HTML()