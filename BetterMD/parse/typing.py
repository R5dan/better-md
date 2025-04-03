import typing as t

from ..typing import ATTR_TYPES, ATTRS

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