from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML

import typing as t

class Str(t.Protocol):
    def __str__(self) -> str: ...


# This is not equivelant to the html span or p tags but instead just raw text

class Text(Symbol):
    md = "{t}"
    html = "{t}"
    rst = "{t}"

    def __init__(self, text:'Str', dom = True, **props):
        self.text = str(text)
        return super().__init__(dom=dom, **props)

    def to_html(self) -> 'str':
        return self.text
    
    def to_md(self) -> 'str':
        return self.text
    
    def to_rst(self) -> 'str':
        return self.text
    
    def __str__(self):
        return f"<Text object>{self.text}</Text>"

    __repr__ = __str__