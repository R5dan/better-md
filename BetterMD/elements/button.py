from .symbol import Symbol

class Button(Symbol):
    prop_list = ["autofocus", "command", "commandfor", "disabled", "form", "formaction", "formenctype", "formmethod", "formnovalidate", "formtarget", "name", "popovertarget", "popovertargetaction", "type", "value"]

    md = ""
    html = "button"
    rst = ""