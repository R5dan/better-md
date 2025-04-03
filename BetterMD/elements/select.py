from . import Symbol

class Select(Symbol):
    prop_list = ["autocomplete", "autofocus", "disabled", "form", "multiple", "name", "required", "size"]

    md = ""
    html = "select"
    rst = ""

class Option(Symbol):
    prop_list = ["disabled", "label", "selected", "value"]

    md = ""
    html = "option"
    rst = ""

class Optgroup(Symbol):
    prop_list = ["disabled", "label"]

    md = ""
    html = "optgroup"
    rst = ""