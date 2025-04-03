from .symbol import Symbol

class P(Symbol):
    html = "p"
    md = ""
    rst = "\n\n"
    block = True

class Pre(Symbol):
    html = "pre"
    md = ""
    rst = ""
