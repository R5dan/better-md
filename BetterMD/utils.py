import typing as t
import sys
import logging

if t.TYPE_CHECKING:
    from .elements import Symbol

T = t.TypeVar("T", default=t.Any)
T2 = t.TypeVar("T2", default=t.Any)

class List(list['Symbol'], t.Generic[T]):
    def on_set(self, key, value): ...

    def on_append(self, object: 'T'): ...

    def append(self, object: 'T') -> 'None':
        self.on_append(object)
        return super().append(object)
    
    def get(self, index, default:'T2'=None) -> 't.Union[T, T2]':
        try:
            return self[index]
        except IndexError:
            return default

    def __setitem__(self, key, value):
        self.on_set(key, value)
        return super().__setitem__(key, value)
    
    def __getitem__(self, item) -> 'T':
        return super().__getitem__(item)
    
    def __iter__(self) -> 't.Iterator[T]':
        return super().__iter__()

    def to_html(self):
        ret = [elm.to_html() for elm in self]
        if len(ret) == 1:
            return ret[0]
        return ret

    def to_md(self):
        ret = [elm.to_md() for elm in self]
        if len(ret) == 1:
            return ret[0]
        return ret

    def to_rst(self):
        ret = [elm.to_rst() for elm in self]
        if len(ret) == 1:
            return ret[0]
        return ret
    
def set_recursion_limit(limit):
    sys.setrecursionlimit(limit)

def get_recursion_limit():
    return sys.getrecursionlimit()

def enable_debug_mode():
    logger = logging.getLogger("BetterMD")
    logger.setLevel(1)

    return logger
