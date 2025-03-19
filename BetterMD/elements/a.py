from .symbol import Symbol
from ..rst import CustomRst
from ..markdown import CustomMarkdown
import re
import typing as t

if t.TYPE_CHECKING:
    from ..parse import Collection

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return f"[{" ".join([e.to_md() for e in inner])}]({symbol.get_prop("href")})"
    
    def verify(self, text:'str'):
        if re.findall("\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)", text):
            # Case 1: Inline link
            return True
        
        elif re.findall("<(https?:\/\/[^\s>]+)>", text):
            # Case 2: Automatic Links
            return True
        
        elif re.findall("\[([^\]]+)\]\[([^\]]+)\]\s*\n?\[([^\]]+)\]:\s*(https?:\/\/[^\s]+)", text):
            # Case 3: Reference Links
            return True

        return False

    
class RST(CustomRst['A']):
    def to_rst(self, inner, symbol, parent):
        return f"`{' '.join([e.to_rst() for e in inner])} <{symbol.get_prop('href')}>`_"

class A(Symbol):
    prop_list = ["href"]

    refs = {}
    md = MD()
    html = "a"
    rst = RST()

    @classmethod
    def md_refs(cls, references: 'list[str]' = None):
        pass

    @classmethod
    def rst_refs(cls, references: 'list[str]' = None):
        pass

    @classmethod
    def html_refs(cls, references: 'list[str]' = None):
        pass