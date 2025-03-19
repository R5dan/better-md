from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML


# This is not equivelant to the html span or p tags but instead just raw text

class Text(Symbol):
    md = "text"
    html = "text"
    rst = "text"

    def __init__(self, text:str, **props):
        self.text = text
        return super().__init__(**props)

    def to_html(self, indent=0, parent=None):
        return f"{'    '*indent}{self.text}"

    def to_md(self):
        return self.text
    
    def to_rst(self):
        return self.text
