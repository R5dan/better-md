from .symbol import Symbol

class Dialog(Symbol):
    prop_list = ["open"] # Dont use `tabindex`

    md = ""
    html = "dialog"
    rst = ""