from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return "    \n".join([e.to_rst() for e in inner])


class Blockquote(Symbol):
    html = "blockquote"
    md = "> "
    rst = RST()
    nl = True
    type = "block"