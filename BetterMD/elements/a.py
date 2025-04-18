from .symbol import Symbol
from ..rst import CustomRst
from ..markdown import CustomMarkdown

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return f"[{" ".join([e.to_md() for e in inner])}]({symbol.get_prop("href")})"

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
    def get_ref(cls, name):
        return cls.refs[name]

    @classmethod
    def email(cls, email):
        return cls(href=f"mailto:{email}")