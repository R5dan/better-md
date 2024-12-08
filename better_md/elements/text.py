from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML


# This is not equivelant to the base span or p tags but instead just raw text

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
        return symbol.vars.get("t")

class Text(Symbol):
    md = "{t}"
    html = "{t}"

    def __init__(self, text:str, dom = True, **props):
        self.text = text

    def to_html(self):
        return self.text
    
    def to_md(self):
        return self.text