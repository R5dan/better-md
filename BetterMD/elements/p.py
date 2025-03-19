from .symbol import Symbol

class P(Symbol):
    html = "p"
    md = ""
    rst = "\n\n"
    nl = True

class Pre(Symbol):
    html = "pre"
    md = ""
    rst = ""
