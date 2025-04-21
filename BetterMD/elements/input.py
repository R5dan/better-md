from .symbol import Symbol
from ..html import CustomHTML
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if symbol.get_prop("type") == "checkbox":
            return f"- [{'x' if symbol.get_prop('checked', '') else ' '}] {" ".join([elm.to_md() for elm in inner])}"
        return symbol.to_html()

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        if symbol.get_prop("type") == "checkbox":
            return f"[{'x' if symbol.get_prop('checked', '') else ' '}] {" ".join([elm.to_md() for elm in inner])}"
        return ""  # Most input types don't have RST equivalents

class Input(Symbol):
    # Common input attributes
    prop_list = [
        "accept",
        "alt",
        "autocapitalize",
        "autocomplete",
        "autofocus",
        "capture",
        "checked",
        "dirname",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "height",
        "list",
        "max",
        "maxlength",
        "min",
        "minlength",
        "multiple",
        "name",
        "pattern",
        "placeholder",
        "popovertarget",
        "popovertargetaction",
        "readonly",
        "required",
        "size",
        "src",
        "step",
        "type",
        "value",
        "width",
    ]

    html = "input"
    md = MD()
    rst = RST()
    type = "void"