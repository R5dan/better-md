import typing as t

if t.TYPE_CHECKING:
    from .elements import Symbol

class List(list['Symbol']):
    def to_html(self, indent=1):
        return [elm.to_html(indent) for elm in self]

    def to_md(self):
        return [elm.to_md() for elm in self]

    def to_rst(self):
        return [elm.to_rst() for elm in self]