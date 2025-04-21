from .symbol import Symbol

class Meta(Symbol):
    prop_list = ["charset", "content", "httpequiv", "media", "name"]

    md = ""
    html = "meta"
    rst = ""
    type = "void"