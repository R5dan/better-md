from .symbol import Symbol
from ..html import CustomHTML
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if symbol.get_prop("type") == "checkbox":
            return f"- [{'x' if symbol.get_prop('checked', '') else ' '}] {inner.to_md()}"
        return symbol.to_html()

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        if symbol.get_prop("type") == "checkbox":
            return f"[{'x' if symbol.get_prop('checked', '') else ' '}] {inner.to_rst() if inner else ''}"
        return ""  # Most input types don't have RST equivalents

class Input(Symbol):
    # Common input attributes
    prop_list = [
        "type",
        "name",
        "value",
        "placeholder",
        "required",
        "disabled",
        "readonly",
        "min",
        "max",
        "pattern",
        "autocomplete",
        "autofocus",
        "checked",
        "multiple",
        "step"
    ]
    html = "input"
    md = MD()
    rst = RST()