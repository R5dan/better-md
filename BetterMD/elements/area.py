from .symbol import Symbol

class Area(Symbol):
    prop_list = ["alt", "coords", "download", "href", "ping", "referrerpolicy", "rel", "shape", "target"]

    md = ""
    html = "area"
    rst = ""
    type = "void"