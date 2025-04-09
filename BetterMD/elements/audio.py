from .symbol import Symbol

class Audio(Symbol):
    prop_list = ["autoplay", "controls", "crossorigin", "disableremoteplayback", "loop", "muted", "preload", "src"]

    md = ""
    html = "audio"
    rst = ""