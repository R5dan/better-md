from .symbol import Symbol

class Del(Symbol):
    prop_list = ["cite", "datetime"]

    md = ""
    html = "del"
    rst = ""