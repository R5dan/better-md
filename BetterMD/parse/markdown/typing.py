import typing as t

if t.TYPE_CHECKING:
    from .parser import MDParser
    from ..typing import ELEMENT, TEXT

class ELM_TYPE_W_END(t.TypedDict):
    pattern: 't.Union[str, list[str]]'
    handler: 't.Callable[[str], None | t.NoReturn]'
    end: 't.Callable[[], None]'


class ELM_TYPE_WO_END(t.TypedDict):
    pattern: 't.Union[str, list[str]]'
    handler: 't.Callable[[str], ELEMENT]'
    end: 'None'

class ELM_TEXT(t.TypedDict):
    pattern: 't.Union[str, list[str]]'
    handler: 't.Callable[[str], tuple[TEXT | ELEMENT, int]]'

class OL_LIST(t.TypedDict):
    list: 't.Literal["ol"]'
    input: 'bool'
    checked: 'bool'
    indent: 'int'
    contents: 'str'
    type: 't.Literal[")", "."]'
    num: 'int'

class UL_LIST(t.TypedDict):
    list: 't.Literal["ul"]'
    input: 'bool'
    checked: 'bool'
    indent: 'int'
    contents: 'str'
    type: 't.Literal["-", "*", "+"]'

class LIST_ITEM(t.TypedDict):
    data: 'OL_LIST | UL_LIST'
    dataType: 't.Literal["item"]'

class OL_TYPE(t.TypedDict):
    value: 'list[LIST_TYPE | LIST_ITEM]'
    parent: 'dict[str, LIST_TYPE]'
    type: 't.Literal["ol"]'
    key: 't.Literal["-", "*", "+", ")", "."]'
    dataType: 't.Literal["list"]'
    start: 'int'

class UL_TYPE(t.TypedDict):
    value: 'list[LIST_TYPE | LIST_ITEM]'
    parent: 'dict[str, LIST_TYPE]'
    type: 't.Literal["ul"]'
    key: 't.Literal["-", "*", "+", ")", "."]'
    dataType: 't.Literal["list"]'

LIST_TYPE = t.Union[OL_TYPE, UL_TYPE]