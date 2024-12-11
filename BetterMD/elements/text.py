from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML


# This is not equivelant to the base span or p tags but instead just raw text

class Text(Symbol):
    md = "{t}"
    html = "{t}"
    rst = "{t}"

    def __init__(self, text:str, dom = True, **props):
        self.text = text
        return super().__init__(dom=dom, **props)

    def to_html(self):
        return self.text
    
    def to_md(self):
        return self.text
    
    def __str__(self):
        return f"<Text object>{self.text}</Text>"

    __repr__ = __str__