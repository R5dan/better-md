from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .text import Text

class MD(CustomMarkdown):
    def to_md(self, inner: list[Symbol], symbol: Symbol, parent: Symbol, **kwargs) -> str:
        if not inner or not isinstance(inner[0], Text) or len(inner) != 1:
             raise ValueError("Title element must contain a single Text element")

        return f'title: "{inner[0].to_md()}"\n# "{inner[0].to_md()}"'

class RST(CustomRst):
    def to_rst(self, inner: list[Symbol], symbol: Symbol, parent: Symbol, **kwargs) -> str:
        if not inner or not isinstance(inner[0], Text) or len(inner) != 1:
            raise ValueError("Title element must contain a single Text element")

        return f":title: {inner[0].to_rst()}"

class Title(Symbol):
    prop_list = ["align", "bgcolor", "char", "charoff", "valign"]

    html = "title"
    md = MD()
    rst = RST()
