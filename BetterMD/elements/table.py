from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .h import H1, H2, H3, H4, H5, H6
from .text import Text

class TableMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return "\n".join([e.to_md() for e in inner]) + "\n"

class TrMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if symbol.is_header:
            cells = [e.to_md() for e in inner]
            separator = ["---" for _ in cells]
            return f"|{'|'.join(cells)}|\n|{'|'.join(separator)}|"
        return f"|{'|'.join([e.to_md() for e in inner])}|"

class TdMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return " ".join([e.to_md() for e in inner])
    
class Table(Symbol):
    html = "table"
    md = TableMD()
    nl = True

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    
    def __init__(self, is_header=False, **kwargs):
        super().__init__(**kwargs)
        self.is_header = is_header

class Td(Symbol):
    html = "td"
    md = TdMD()

class Th(Symbol):
    html = "th"
    md = TdMD() 
