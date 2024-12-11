import typing as t

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

class CustomRst:
    prop = ""
    rst: 'dict[str, str]' = {}

    def to_rst(self, inner: 'list[Symbol]', symbol:'Symbol', parent:'Symbol') -> str: ...

    def prepare(self, inner:'list[Symbol]', symbol:'Symbol', parent:'Symbol'): ...

    def verify(self, text) -> bool: ...