import typing as t
import logging

from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst

T = t.TypeVar("T", default=t.Any)
T2 = t.TypeVar("T2", default=t.Any)
logger = logging.getLogger("BetterMD")

class List(list, t.Generic[T]):
    def on_set(self, key, value): ...

    def on_ammend(self, object: 'T'): ...


    def append(self, object: 'T') -> 'None':
        self.on_ammend(object)
        return super().append(object)
    
    def get(self, index, default:'T2'=None) -> 't.Union[T, T2]':
        try:
            return self[index]
        except IndexError:
            return default

    def __setitem__(self, key, value):
        self.on_set(key, value)
        return super().__setitem__(key, value)
    
    def __getitem__(self, item) -> 'T':
        return super().__getitem__(item)
    
    def __iter__(self) -> 't.Iterator[T]':
        return super().__iter__()

class Symbol:
    styles: 'dict[str, str]' = {}
    classes: 'list[str]' = []
    html: 't.Union[str, CustomHTML, CustomHTML[Symbol]]' = ""
    props: 'dict[str, t.Union[str, list[str], dict[str, str]]]' = {}
    prop_list: 'list[str]' = []
    vars:'dict[str,str]' = {}
    children:'List[Symbol]' = List()
    md: 't.Union[str, CustomMarkdown, CustomMarkdown[Symbol], None]' = None
    rst: 't.Union[str, CustomRst, CustomRst[Symbol], None]' = None
    parent:'Symbol' = None
    prepared:'bool' = False
    nl:'bool' = False

    html_written_props = ""

    def __init__(self, styles:'dict[str,str]'={}, classes:'list[str]'=[], dom:'bool'=True, inner:'list[Symbol]'=[], **props):
        logger.debug(f"Creating new Symbol with {styles=} {classes=} {dom=} {inner=} {props=}")
        self.styles = styles
        self.classes = classes
        self.children = List(inner) or List()
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

    def prepare(self, parent:'t.Union[Symbol, None]'=None, *args, **kwargs):
        self.prepared = True
        self.parent = parent
        
        [symbol.prepare(self, *args, **kwargs) for symbol in self.children]
        
        return self

    def replace_child(self, old:'Symbol', new:'Symbol'):
        i = self.children.index(old)
        self.children.remove(old)

        self.children[i-1] = new
        

    def to_html(self) -> 'str':
        if not self.prepared:
            self.prepare()
        
        if isinstance(self.html, CustomHTML):
            return self.html.to_html(self.children, self, self.parent)
        
        props = []
        for prop, value in self.props.items():
            if isinstance(value, list):
                props.append(f"{prop}={'"'}{' '.join(value)}{'"'}")
            elif isinstance(value, dict):
                props.append(f"{prop}={'"'}{' '.join([f'{k}:{v}' for k,v in value.items()])}{'"'}")
            else:
                props.append(f"{prop}={value}")

        inner_HTML = "\n".join([e.to_html() for e in self.children])
        logger.debug(f"{inner_HTML=} {self.html=} {self.classes=} {self.styles=} {props=}")
        return f"<{self.html} class={'"'}{' '.join(self.classes) or ''}{'"'} style={'"'}{' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or ''}{'"'} {' '.join(props)}>{inner_HTML}</{self.html}>"
    
    def to_md(self, **kwargs) -> 'str':
        if not self.prepared:
            self.prepare(**kwargs)
        
        if isinstance(self.md, CustomMarkdown):
            return self.md.to_md(self.children, self, self.parent, **kwargs)
        
        if self.md == None:
            return self.to_html(**kwargs)
        
        inner_md = " ".join([e.to_md() for e in self.children])
        return f"{self.md} {inner_md}" + ("\n" if self.nl else "")
    
    def to_rst(self, **kwargs) -> 'str':
        if not self.prepared:
            self.prepare(**kwargs)

        if isinstance(self.rst, CustomRst):
            return self.rst.to_rst(self.children, self, self.parent)
        
        if self.rst == None:
            return self.to_html()
        
        inner_rst = " ".join([e.to_rst() for e in self.children])
        return f"{self.rst}{inner_rst}{self.rst}\n"
    
    def get_prop(self, prop, default="") -> 't.Union[str, list[str], dict[str, str]]':
        return self.props.get(prop, default)

    def set_prop(self, prop:'str', value:'t.Union[str, list[str], dict[str, str]]'):
        self.props[prop] = value

    def __contains__(self, item):
        if callable(item):
            return any(isinstance(e, item) for e in self.children)
        return item in self.children
    
    def __str__(self):
        return f"<{self.html} class={'"'}{' '.join(self.classes) or ''}{'"'} style={'"'}{' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or ''}{'"'} {' '.join(self.props)}/>"
