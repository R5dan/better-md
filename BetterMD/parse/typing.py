import typing as t

from ..typing import ATTRS

ELEMENT_TYPES:'dict[t.Literal["block", "inline", "void"], list[str]]' = {
    "block": [
        "address", "article", "aside", "blockquote", "canvas", "dd", "div",
        "dl", "dt", "fieldset", "figcaption", "figure", "footer", "form",
        "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "hr",
        "li", "main", "nav", "noscript", "ol", "p", "pre", "section",
        "table", "tfoot", "thead", "tbody", "tr", "ul", "video"
    ],
    "inline": [
        "a", "abbr", "acronym", "b", "bdi", "bdo", "big", "cite", "code",
        "data", "dfn", "em", "i", "kbd", "mark", "q", "ruby", "s", "samp",
        "small", "span", "strong", "sub", "sup", "time", "tt", "u", "var"
    ],
    "void": [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    ]
}

class TEXT(t.TypedDict):
    type: 't.Literal["text"]'
    content: 'str'
    name: 't.Literal["text"]'

class ELEMENT(t.TypedDict):
    type: 't.Literal["element"]'
    name: 'str'
    attributes: 'ATTRS'
    children: 'list[t.Union[ELEMENT, TEXT]]'

@t.runtime_checkable
class Parser(t.Protocol):
    def parse(self, html:'str') -> 'list[ELEMENT]': ...