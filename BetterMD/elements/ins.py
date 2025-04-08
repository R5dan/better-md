from .symbol import Symbol

class Ins(Symbol):
    prop_list = ["cite", "datetime"]
    
    md = ""
    html = "ins"
    rst = "" 