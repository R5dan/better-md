import typing as t

from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst

class Symbol:
    styles: 'dict[str, str]' = {}
    classes: 'list[str]' = []
    html: 't.Union[str, CustomHTML]' = ""
    props: 'dict[str, str]' = {}
    prop_list: 'list[str]' = []
    vars:'dict[str,str]' = {}
    children:'list[Symbol]' = []
    md: 't.Union[str, CustomMarkdown]' = ""
    rst: 't.Union[str, CustomRst]' = ""
    parent:'Symbol' = None
    prepared:'bool' = False
    nl:'bool' = False

    html_written_props = ""

    def __init__(self, styles:'dict[str,str]'={}, classes:'list[str]'=[], dom:'bool'=True, inner:'list[Symbol]'=[], **props):
        self.styles = styles
        self.classes = classes
        self.children = list(inner) or []
        self.props = props
        self.dom = dom
        
    def copy(self, styles:'dict[str,str]'={}, classes:'list[str]'=[], inner:'list[Symbol]'=None):
        if inner == None:
            inner = [Symbol()]
        styles.update(self.styles)
        return Symbol(styles, classes, inner = inner)
    
    
    def set_parent(self, parent:'Symbol'):
        self.parent = parent
        self.parent.add_child(self)

    def change_parent(self, new_parent:'Symbol'):
        self.set_parent(new_parent)
        self.parent.remove_child(self)

    def add_child(self, symbol:'Symbol'):
        self.children.append(symbol)

    def remove_child(self, symbol:'Symbol'):
        self.children.remove(symbol)

    def has_child(self, child:'type[Symbol]'):
        for e in self.children:
            if isinstance(e, child):
                return e
            
        return False

    def prepare(self, parent:'Symbol'):
        self.prepared = True
        self.parent = parent
        for symbol in self.children:
            symbol.prepare(self)
        
        return self

    def replace_child(self, old:'Symbol', new:'Symbol'):
        i = self.children.index(old)
        self.children.remove(old)

        self.children[i-1] = new
        

    def to_html(self):
        if isinstance(self.html, CustomHTML):
            return self.html.to_html(self.children, self, self.parent)

        inner_HTML = "\n".join([e.to_html() for e in self.children])
        return f"<{self.html} class={' '.join(self.classes) or '""'} style={' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or '""'} {' '.join([f'{k}={v}'for k,v in self.props.items()])}>{inner_HTML}</{self.html}>"
    
    def to_md(self):
        if isinstance(self.md, CustomMarkdown):
            return self.md.to_md(self.children, self, self.parent)
        
        inner_md = " ".join([e.to_md() for e in self.children])
        return f"{self.md} {inner_md}" + ("\n" if self.nl else "")

    
    def get_prop(self, prop, default=""):
        return self.props.get(prop, default)

    def set_prop(self, prop, value):
        self.props[prop] = value

    def __contains__(self, item):
        if callable(item):
            return any(isinstance(e, item) for e in self.children)
        return item in self.children
