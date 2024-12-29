import typing as t

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

T = t.TypeVar("T", default='Symbol')

class CustomRst(t.Generic[T]):
    prop = ""
    rst: 'dict[str, str]' = {}

    def to_rst(self, inner: 'list[Symbol]', symbol:'T', parent:'Symbol', **kwargs) -> str: ...

    def prepare(self, inner:'list[Symbol]', symbol:'T', parent:'Symbol', *args, **kwargs) -> 'list[Symbol]': ...

    def verify(self, text) -> bool: ...