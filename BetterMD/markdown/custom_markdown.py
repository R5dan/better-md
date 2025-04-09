import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

T = t.TypeVar("T", default='Symbol')

class CustomMarkdown(t.Generic[T], ABC):
    prop = ""
    md: 'dict[str, str]' = {}

    @abstractmethod
    def to_md(self, inner: 'list[Symbol]', symbol:'T', parent:'Symbol') -> 'str': ...

    def prepare(self, inner:'list[Symbol]', symbol:'T', parent:'Symbol', *args, **kwargs) -> 'list[Symbol]': ...

    def verify(self, text) -> 'bool': ...
