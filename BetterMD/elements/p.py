from .symbol import Symbol

class P(Symbol):
    html = "p"
    md = ""
    rst = "\n\n"
    type = "block"

class Pre(Symbol):
    html = "pre"
    md = ""
    rst = ""
