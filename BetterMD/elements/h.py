from ..rst.custom_rst import CustomRst
from .symbol import Symbol

class RST(CustomRst):
    def __init__(self, character:'str') -> None:
        self.character = character
        super().__init__()

    def to_rst(self, inner: list[Symbol], symbol: Symbol, parent: Symbol, **kwargs) -> str:
        list_rst = [e.to_rst(**kwargs) for e in inner]
        content = "\n".join(list_rst)
        max_length = len(max(list_rst, key=lambda l: len(l)))

        return f"{self.character * max_length}\n{content}\n{self.character * max_length}"

class H1(Symbol):
    html = "h1"
    md = "#"
    rst = RST("=")
    nl = True

class H2(Symbol):
    html = "h2"
    md = "##"
    rst = RST("-")
    nl = True

class H3(Symbol):
    html = "h3"
    md = "###"
    rst = RST("~")
    nl = True

class H4(Symbol):
    html = "h4"
    md = "####"
    rst = RST("+")
    nl = True

class H5(Symbol):
    html = "h5"
    md = "#####"
    rst = RST("^")
    nl = True

class H6(Symbol):
    html = "h6"
    md = "######"
    rst = RST('"')
    nl = True