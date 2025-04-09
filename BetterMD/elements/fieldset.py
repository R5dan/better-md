from .symbol import Symbol

class Fieldset(Symbol):
    prop_list = ["disabled", "form", "name"]
    
    md = ""
    html = "fieldset"
    rst = ""