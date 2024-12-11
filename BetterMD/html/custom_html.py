import typing as t

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

class CustomHTML:
    def to_html(self, inner:'Symbol', symbol:'Symbol', parent:'Symbol') -> str: ...

    def prepare(self, inner:'Symbol', symbol:'Symbol', parent:'Symbol'):...