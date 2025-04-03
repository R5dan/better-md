from .symbol import Symbol

class Form(Symbol):
    prop_list = [
        "accept", "accept-charset", "autocapitalize", "autocomplete", "name", "rel", 
        "action", "enctype", "method", "novalidate", "target", 
    ]
    
    md = ""
    html = "form"
    rst = "" 