from .symbol import Symbol
from ..html import CustomHTML
from ..markdown import CustomMarkdown

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
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
    def to_md(self, inner, symbol, parent):
        if symbol.get_prop("type") == "checkbox":
            return f"- [{'x' if symbol.get_prop('checked', '') else ''}] {inner.to_md()}"
        return symbol.to_html()

class Input(Symbol):
    # Common input attributes
    props = [
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
    md = ""  # No markdown equivalent 