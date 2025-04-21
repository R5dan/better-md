from .symbol import Symbol

class Base(Symbol):
    prop_list = ["href", "target"]

    md = ""
    html = "base"
    rst = ""
    type = "void"