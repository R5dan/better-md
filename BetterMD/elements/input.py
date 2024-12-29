from .symbol import Symbol
from ..html import CustomHTML
from ..markdown import CustomMarkdown
from ..rst import CustomRst

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent, **kwargs):
        # Collect all input attributes
        attrs = []
        for prop in Input.props:
            value = symbol.get_prop(prop)
            if value:
                # Handle boolean attributes like 'required', 'disabled', etc.
                if isinstance(value, bool) and value:
                    attrs.append(prop)
                else:
                    attrs.append(f'{prop}="{value}"')
        
        attrs_str = " ".join(attrs)
        return f"<input {attrs_str} />"

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent, **kwargs):
        if symbol.get_prop("type") == "checkbox":
            return f"- [{'x' if symbol.get_prop('checked', '') else ''}] {inner.to_md()}"
        return symbol.to_html()

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent, **kwargs):
        if symbol.get_prop("type") == "checkbox":
            return f"[ ] {inner.to_rst() if inner else ''}"
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
    html = HTML()
    md = MD()
    rst = RST()