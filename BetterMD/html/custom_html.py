import typing as t

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

T = t.TypeVar("T", default='Symbol')

class CustomHTML(t.Generic[T]):
    def to_html(self, inner:'list[Symbol]', symbol:'T', parent:'Symbol') -> str: ...

    def prepare(self, inner:'list[Symbol]', symbol:'T', parent:'Symbol', *args, **kwargs) -> 'list[Symbol]': ...

    def verify(self, text) -> bool: ...