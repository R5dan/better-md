import typing as t

from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst
from ..parse import HTMLParser, MDParser, ELEMENT, TEXT, Collection
from ..utils import List
from ..typing import ATTRS, ATTR_TYPES

class Symbol:
    styles: 'dict[str, str]' = {}
    classes: 'list[str]' = []
    html: 't.Union[str, CustomHTML]' = ""
    props: 'dict[str, t.Union[str, bool, int, float, list, dict]]' = {}
    prop_list: 'list[str]' = []
    vars:'dict[str,str]' = {}
    children:'list[Symbol]' = []
    md: 't.Union[str, CustomMarkdown]' = ""
    rst: 't.Union[str, CustomRst]' = ""
    parent:'Symbol' = None
    prepared:'bool' = False
    nl:'bool' = False
    block: 'bool' = False

    html_written_props = ""

    collection = Collection()
    html_parser = HTMLParser()
    md_parser = MDParser()

    def __init_subclass__(cls, **kwargs) -> None:
        cls.collection.add_symbols(cls)
        super().__init_subclass__(**kwargs)

    def __init__(self, styles:'dict[str,ATTR_TYPES]'=None, classes:'list[str]'=None, inner:'list[Symbol]'=None, **props):
        if styles == None:
            styles = {}
        if classes == None:
            classes = []
        if inner == None:
            inner = []

        self.styles = styles
        self.classes = classes
        self.children = list(inner) or []
        self.props = props

    def copy(self, styles:'dict[str,str]'=None, classes:'list[str]'=None, inner:'list[Symbol]'=None):
        if inner == None:
            inner = []
        if styles == None:
            styles = {}
        if classes == None:
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


    def to_html(self, indent=1) -> 'str':
        if isinstance(self.html, CustomHTML):
            return self.html.to_html(self.children, self, self.parent)

        def handle_props(props):
            props = []
            for k, v in self.props.items():
                if isinstance(v, bool) or v == "":
                    props.append(f"{k}" if v else "")
                elif isinstance(v, (int, float, str)):
                    props.append(f"{k}={'"'}{v}{'"'}")
                elif isinstance(v, list):
                    props.append(f"{k}={'"'}{' '.join(v)}{'"'}")
                elif isinstance(v, dict):
                    props.append(f"{k}={'{'}{' '.join([f'{k}:{v}' for k,v in v.items()])}{'}'}")
                else:
                    raise TypeError(f"Unsupported type for prop {k}: {type(v)}")

            return ' '.join(props)


        inner_HTML = f"\n{"    "*indent}".join([e.to_html(indent+1) if not (len(self.children) == 1 and self.children[0].html == "text") else e.to_html(0) for e in self.children])
        return f"<{self.html}{" " if self.styles or self.classes or self.props else ""}{f"class={'"'}{' '.join(self.classes) or ''}{'"'}" if self.classes else ""}{" " if (self.styles or self.classes) and self.props else ""}{f"style={'"'}{' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or ""}{'"'}" if self.styles else ""}{" " if (self.styles or self.classes) and self.props else ""}{handle_props(self.props)}{f">{"\n" if len(self.children) > 1 else ""}{inner_HTML}{"\n" if len(self.children) > 1 else ""}</{self.html}>" if inner_HTML else f" />"}"

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
        print(parsed)
        return List([cls.collection.find_symbol(elm['name'] , raise_errors=True).parse(elm) for elm in parsed])

    @classmethod
    def from_md(cls, text: str) -> 'List[Symbol]':
        parsed = cls.md_parser.parse(text)
        return List([cls.collection.find_symbol(elm['name'] , raise_errors=True).parse(elm) for elm in parsed])

    @classmethod
    def parse(cls, text:'ELEMENT|TEXT') -> 'Symbol':
        def handle_element(element:'ELEMENT|TEXT') -> 'Symbol':
            if element['type'] == 'text':
                text = cls.collection.find_symbol("text", raise_errors=True)
                assert text is not None, "`collection.find_symbol` is broken"
                return text(element['content'])

            symbol_cls = cls.collection.find_symbol(element['name'], raise_errors=True)
            assert symbol_cls is not None, "`collection.find_symbol` is broken"

            return symbol_cls.parse(element)
        
        if text["type"] == "text":
            return cls.collection.find_symbol("text", raise_errors=True)(text["content"])

        styles = text["attributes"].get("style", {})
        classes = list(filter(lambda c: bool(c), text["attributes"].pop("class", "")))

        return cls(styles, classes, inner=[handle_element(elm) for elm in text["children"]], **text["attributes"])

    def get_prop(self, prop, default="") -> 'str':
        return self.props.get(prop, default)

    def set_prop(self, prop, value):
        self.props[prop] = value

    def __contains__(self, item):
        if callable(item):
            return any(isinstance(e, item) for e in self.children)
        return item in self.children
    
    def __str__(self):
        return f"<{self.html}{" " if self.styles or self.classes or self.props else ""}{f"class={'"'}{' '.join(self.classes) or ''}{'"'}" if self.classes else ""}{" " if (self.styles or self.classes) and self.props else ""}{f"style={'"'}{' '.join([f'{k}:{v}' for k,v in self.styles.items()]) or ""}{'"'}" if self.styles else ""}{" " if (self.styles or self.classes) and self.props else ""}{' '.join([f'{k}={'"'}{v}{'"'}' if v != "" else f'{k}' for k,v in self.props.items()])}{f">{"\n" if len(self.children) > 1 else ""}{"\n" if len(self.children) > 1 else ""}{len(self.children)}</{self.html}>"}"

    __repr__ = __str__