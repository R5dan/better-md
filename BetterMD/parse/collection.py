import typing as t
import logging

if t.TYPE_CHECKING:
    from ..elements import Symbol

logger = logging.getLogger("BetterMD")

class Collection:
    def __init__(self, *symbols:'type[Symbol]'):
        self.symbols = list(symbols)

    def add_symbols(self, symbol:'type[Symbol]'):
        self.symbols.append(symbol)

    def remove_symbol(self, symbol:'type[Symbol]'):
        self.symbols.remove(symbol)

    def find_symbol(self, name:'str', raise_errors:'bool'=False) -> 't.Optional[type[Symbol]]':
        for symbol in self.symbols:
            if symbol.__qualname__.lower() == name.lower():
                return symbol


        if raise_errors:
            raise ValueError(f"Symbol `{name}` not found in collection, if using default symbols it may not be supported.")
        return None