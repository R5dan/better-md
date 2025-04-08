from .symbol import Symbol

class Meter(Symbol):
    prop_list = ["value", "min", "max", "low", "high", "optimum", "form"]

    md = ""
    html = "meter"
    rst = ""