from .symbol import Symbol

class Textarea(Symbol):
    prop_list = ["autocapitalize", "autocomplete", "autocorrect", "autofocus", "cols", "dirname", "disabled", "form", "maxlength", "minlength", "name", "placeholder", "readonly", "required", "rows", "spellcheck", "wrap"]

    html = "textarea"
    md = "" 
    rst = ""