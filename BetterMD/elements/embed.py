from .symbol import Symbol

class Embed(Symbol):
    prop_list = ["height", "src", "type", "width"]

    md = ""
    html = "embed"
    rst = ""
    type = "void"