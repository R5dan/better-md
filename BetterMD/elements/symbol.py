import typing as t

from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst
from ..parse import HTMLParser, MDParser, ELEMENT, TEXT, Collection
from ..utils import List, set_recursion_limit
from ..typing import ATTR_TYPES

set_recursion_limit(10000)

class Symbol:
    html: 't.Union[str, CustomHTML]' = ""
    prop_list: 'list[str]' = []
    md: 't.Union[str, CustomMarkdown]' = ""
    rst: 't.Union[str, CustomRst]' = ""
    nl:'bool' = False
    block: 'bool' = False
    self_closing: 'bool' = False

    collection = Collection()
    html_parser = HTMLParser()
    md_parser = MDParser()

    def __init_subclass__(cls, **kwargs) -> None:
        cls.collection.add_symbols(cls)
        super().__init_subclass__(**kwargs)

    def __init__(self, styles:'dict[str,str]'=None, classes:'list[str]'=None, inner:'list[Symbol]'=None, **props:'ATTR_TYPES'):
        self.parent:'Symbol' = None
        self.prepared:'bool' = False
        self.html_written_props = ""

        if styles is None:
            styles = {}
        if classes is None:
            classes = []
        if inner is None:
            inner = []

        self.styles: 'dict[str, str]' = styles
        self.classes: 'list[str]' = classes
        self.children:'list[Symbol]'  = list(inner) or []
        self.props: 'dict[str, ATTR_TYPES]' = props

    def copy(self, styles:'dict[str,str]'=None, classes:'list[str]'=None, inner:'list[Symbol]'=None):
        if inner is None:
            inner = []
        if styles is None:
            styles = {}
        if classes is None:
            classes = []

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

    def handle_props(self, p):
        props = {**({"class": self.classes} if self.classes else {}), **({"style": self.styles} if self.styles else {}), **self.props}
        prop_list = []
        for k, v in props.items():
            if isinstance(v, bool) or v == "":
                prop_list.append(f"{k}" if v else "")
            elif isinstance(v, (int, float, str)):
                prop_list.append(f'{k}="{v}"')
            elif isinstance(v, list):
                prop_list.append(f'{k}="{" ".join(v)}"')
            elif isinstance(v, dict):
                prop_list.append(f'{k}="{"; ".join([f"{k}:{v}" for k,v in v.items()])}"')
            else:
                raise TypeError(f"Unsupported type for prop {k}: {type(v)}")
        return (" " + " ".join(filter(None, prop_list))) if prop_list else ""

    def to_html(self, indent=0) -> 'str':
        if isinstance(self.html, CustomHTML):
            return self.html.to_html(self.children, self, self.parent)

        inner_HTML = "\n".join([
            e.to_html(0) if not (len(self.children) == 1 and isinstance(e.html, str) and e.html == "text") 
            else e.to_html(0) for e in self.children
        ])

        if inner_HTML or not self.self_closing:
            return f"<{self.html}{self.handle_props(False)}>{inner_HTML}</{self.html}>"
        else:
            return f"<{self.html}{self.handle_props(False)} />"


    def to_md(self) -> 'str':
        if isinstance(self.md, CustomMarkdown):
            return self.md.to_md(self.children, self, self.parent)

        inner_md = ""
        
        for e in self.children:
            if e.block:
                inner_md += f"\n{e.to_md()}\n"
            elif e.nl:
                inner_md += f"{e.to_md()}\n"
            else:
                inner_md += f"{e.to_md()}"

        return f"{self.md}{inner_md}"

    def to_rst(self) -> 'str':
        if isinstance(self.rst, CustomRst):
            return self.rst.to_rst(self.children, self, self.parent)

        inner_rst = " ".join([e.to_rst() for e in self.children])
        return f"{self.rst}{inner_rst}{self.rst}\n"

    @classmethod
    def from_html(cls, text:'str') -> 'List[Symbol]':
        parsed = cls.html_parser.parse(text)
        import json as j
        def handle(dict:'dict'):
            if dict['type'] == 'element':
                dict.pop("parent")

                for c in dict['children']:
                    handle(c)

            return dict

        with open("t2.json", "w") as f:
            
            d = j.dumps([handle(elm) for elm in parsed.copy()])
            f.write(d)
        return List([cls.collection.find_symbol(elm['name'], raise_errors=True).parse(elm) for elm in parsed])



    @classmethod
    def from_md(cls, text: str) -> 'List[Symbol]':
        parsed = cls.md_parser.parse(text)
        return List([cls.collection.find_symbol(elm['name'] , raise_errors=True).parse(elm) for elm in parsed])

    @classmethod
    def parse(cls, text:'ELEMENT|TEXT') -> 'Symbol':
        def handle_element(element:'ELEMENT|TEXT'):
            if element['type'] == 'text':
                text = cls.collection.find_symbol("text", raise_errors=True)
                assert text is not None, "`collection.find_symbol` is broken"
                return text(element['content'])

            symbol_cls = cls.collection.find_symbol(element['name'], raise_errors=True)
            assert symbol_cls is not None, "`collection.find_symbol` is broken"

            return symbol_cls.parse(element)
        
        if text["type"] == "text":
            return cls.collection.find_symbol("text", raise_errors=True)(text["content"])

        # Extract attributes directly from the attributes dictionary
        attributes = text["attributes"]
        
        # Handle class attribute separately if it exists
        classes = []
        if "class" in attributes:
            classes = attributes["class"].split() if isinstance(attributes["class"], str) else attributes["class"]
            del attributes["class"]
        
        # Handle style attribute separately if it exists
        styles = {}
        if "style" in attributes:
            style_str = attributes["style"]
            if isinstance(style_str, str):
                styles = dict(item.split(":") for item in style_str.split(";") if ":" in item)
            elif isinstance(style_str, dict):
                styles = style_str
            del attributes["style"]

        inner=[handle_element(elm) for elm in text["children"]]

        return cls(
            styles=styles,
            classes=classes,
            inner=inner,
            **attributes
        )

    def get_prop(self, prop, default=""):
        return self.props.get(prop, default)

    def set_prop(self, prop, value):
        self.props[prop] = value

    def __contains__(self, item):
        if callable(item):
            return any(isinstance(e, item) for e in self.children)
        return item in self.children
    
    def __str__(self):
        return f"<{self.html}{self.handle_props()} />"

    __repr__ = __str__