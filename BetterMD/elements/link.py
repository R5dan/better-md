from .symbol import Symbol

class Link(Symbol):
    prop_list = ["as", "blocking", "crossorigin", "disabled", "fetchpriority", "href", "hreflang", "imagesizes", "imagesrcset", "integrity", "media", "referrerpolicy", "rel", "sizes", "title", "type", "target", "charset", "rev"]

    md = ""
    html = "link"
    rst = ""
    type = "void"