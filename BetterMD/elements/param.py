from .symbol import Symbol

class Param(Symbol):
    prop_list = ["name", "value", "type", "valuetype"]

    md = ""
    html = "param"
    rst = ""
    type = "void"