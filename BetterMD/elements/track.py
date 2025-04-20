from .symbol import Symbol

class Track(Symbol):
    prop_list = ["default", "kind", "label", "src", "srclang"]

    html = "track"
    md = "" 
    rst = ""
    self_closing = True