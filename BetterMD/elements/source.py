from .symbol import Symbol

class Source(Symbol):
    prop_list = ["type", "src", "srcset", "sizes", "media", "width"]

    md = ""
    html = "source"
    rst = ""
    type = "void"