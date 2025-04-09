from .symbol import Symbol

class Iframe(Symbol):
    prop_list = [
        "allow", "allowfullscreen", "allowpaymentrequest", "browsingtopics", "credentialless", "csp",
        "height", "loading", "name", "referrerpolicy", "sandbox",
        "src", "srcdoc", "width"
    ]
    
    md = ""
    html = "iframe"
    rst = "" 