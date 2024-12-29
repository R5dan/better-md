from BetterMD.rst.custom_rst import CustomRst
from .symbol import Symbol

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs):
        return "    \n".join([e.to_rst(**kwargs) for e in inner])
        

class Blockquote(Symbol):
    html = "blockquote"
    md = ">"
    rst = RST()
    nl = True 