from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..html import CustomHTML


# This is not equivalent to the html span or p tags but instead just raw text
# Should be ported over to use standard str objects

class Text(Symbol):
    md = "raw_text"
    html = "raw_text"
    rst = "raw_text"

    def __init__(self, text:'str'="", **props):
        self._text = text
        return super().__init__(**props)

    @property
    def text(self):
        return self._text

    def to_html(self, indent=0):
        return f"{'    '*indent}{self.text}"

    def to_md(self):
        return self.text

    def to_rst(self):
        return self.text

    def __str__(self):
        return self.text

    __repr__ = __str__
