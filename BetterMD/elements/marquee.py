from .symbol import Symbol

class Marquee(Symbol):
    prop_list = ["behavior", "bgcolor", "direction", "height", "hspace", "loop", "scrollamount", "scrolldelay", "truespeed", "vspace", "width"]

    md = ""
    html = "marquee"
    rst = ""