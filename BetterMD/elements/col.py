from .symbol import Symbol

class Colgroup(Symbol):
    prop_list = ["span", "align", "bgcolor", "char", "charoff", "valign", "width"]

    md = ""
    html = "colgroup"
    rst = ""

class Col(Symbol):
    prop_list = ["span", "align", "bgcolor", "char", "charoff", "valign", "width"]

    md = ""
    html = "col"
    rst = ""
    self_closing = True