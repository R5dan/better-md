import typing as t

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

class CustomMarkdown:
    prop = ""
    md: 'dict[str, str]' = {}

    def to_md(self, inner: 'list[Symbol]', symbol:'Symbol', parent:'Symbol') -> str: ...

    def prepare(self, inner:'list[Symbol]', symbol:'Symbol', parent:'Symbol'): ...

    def verify(self, text) -> bool: ...