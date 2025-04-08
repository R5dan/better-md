from .symbol import Symbol

class Frameset(Symbol):
    prop_list = ["cols", "rows"]
    
    md = ""
    html = "frameset"
    rst = "" 