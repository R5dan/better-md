import typing as t

if t.TYPE_CHECKING:
    from ..elements import Symbol

class Collection:
    def __init__(self, *symbols:'type[Symbol]'):
        self.symbols = list(symbols)
        self.cached = False
        self.qual_names_cache = {}

    @property
    def qual_keys(self):
        if self.cached:
            return self.qual_names_cache
        
        self.qual_names_cache = {s.__qualname__.lower(): s for s in self.symbols}
        self.cached = True
        return self.qual_names_cache

    def add_symbols(self, symbol:'type[Symbol]'):
        self.cached = False
        self.symbols.append(symbol)

    def remove_symbol(self, symbol:'type[Symbol]'):
        self.cached = False
        self.symbols.remove(symbol)

    @t.overload
    def find_symbol(self, name:'str', raise_errors:'t.Literal[False]'=False) -> 't.Optional[type[Symbol]]': ...

    @t.overload
    def find_symbol(self, name:'str', raise_errors:'t.Literal[True]') -> 't.Union[type[Symbol], t.NoReturn]': ...

    def find_symbol(self, name:'str', raise_errors:'bool'=False):
        lname = name.lower()
        if lname in self.qual_keys:
            return self.qual_keys[lname]


        if raise_errors:
            raise ValueError(f"Symbol `{name}` not found in collection, if using default symbols it may not be supported.")
        return None