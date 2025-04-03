from .symbol import Symbol

class Script(Symbol):
    prop_list = ["async", "attributionsrc", "blocking", "crossorigin", "defer", "fetchpriority", "integrity", "nomodule", "none", "referrerpolicy", "src", "type", "charset", "language"]

    md = ""
    html = "script"
    rst = ""