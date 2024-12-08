from ..markdown import CustomMarkdown
from ..html import CustomHTML

class Symbol:
    styles: 'dict[str, str]' = {}
    classes: 'list[str]' = []
    html: 'str'
    props: 'dict[str, str]'
    prop_list: 'list[str]' = []
    vars:'dict[str,str]' = {}
    children:'list[Symbol]' = []
    md: 'str'
    parent:'Symbol'
    prepared:'bool' = False

    html_written_props = ""

    def __init__(self, styles:'dict[str,str]'={}, classes:'list[str]'=[], dom:'bool'=True, inner:'Symbol'=[], **props):
        self.styles = styles
        self.classes = classes
        self.children = list(inner) or []
        self.props = props
        self.dom = dom
        
    def copy(self, styles:'dict[str,str]'={}, classes:'list[str]'=[], inner:'Symbol'=""):
        return Symbol(self.styles+styles, self.classes+classes, self.inner or inner)
    
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
        for symbol in self.children:
            symbol.prepare(self)

    def replace_child(self, old:'Symbol', new:'Symbol'):
        i = self.children.index(old)
        self.children.remove(old)

        self.children[i] = new
        

    def to_html(self):
        if not self.prepared: self.prepare(self)

        if isinstance(self.html, CustomHTML):
            return self.html.to_html(self.children, self, self.parent)

        inner_HTML = "\n".join([e.to_html() for e in self.children])
        return f"<{self.html} classes={' '.join(self.classes) or '""'} style={' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or '""'} {' '.join([f'{k}={v}'for k,v in self.props.items()])}>{inner_HTML}</{self.html}>"
    
    def to_md(self):
        if not self.prepared: self.prepare()

        if isinstance(self.md, CustomMarkdown):
            return self.md.to_md(self.children, self, self.parent)
        
        inner_md = " ".join([e.to_md() for e in self.children])
        return f"{self.md} {inner_md}"
    
    def get_prop(self, prop, default=""):
        return self.props.get(prop, default)

    def set_prop(self, prop, value):
        self.props[prop] = value
