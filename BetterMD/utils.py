import typing as t
import sys

if t.TYPE_CHECKING:
    from .elements import Symbol

class List(list['Symbol']):
    def to_html(self):
        return [elm.to_html() for elm in self]

    def to_md(self):
        return [elm.to_md() for elm in self]

    def to_rst(self):
        return [elm.to_rst() for elm in self]
    
def set_recursion_limit(limit):
    sys.setrecursionlimit(limit)

def get_recursion_limit():
    return sys.getrecursionlimit()