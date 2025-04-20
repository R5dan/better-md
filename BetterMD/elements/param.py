from .symbol import Symbol

class Param(Symbol):
    prop_list = ["name", "value", "type", "valuetype"]

    md = ""
    html = "param"
    rst = ""
    self_closing = True