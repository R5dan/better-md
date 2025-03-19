import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from ..elements.symbol import Symbol

T = t.TypeVar("T", default='Symbol')

class CustomRst(t.Generic[T], ABC):
    prop = ""
    rst: 'dict[str, str]' = {}

    @abstractmethod
    def to_rst(self, inner: 'list[Symbol]', symbol:'T', parent:'Symbol') -> 'str': ...

    def prepare(self, inner:'list[Symbol]', symbol:'T', parent:'Symbol'): ...

    def verify(self, text) -> 'bool': ...