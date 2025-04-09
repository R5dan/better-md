from .symbol import Symbol

class Details(Symbol):
    prop_list = ["open", "name"]
    event_list = ["toggle"]

    md = ""
    html = "details"
    rst = ""