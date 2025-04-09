from .symbol import Symbol

class Frame(Symbol):
    prop_list = [
        "src", "name", "noresize", "scrolling", "marginheight", "marginwidth", "frameborder"
    ]
    
    md = ""
    html = "frame"
    rst = ""