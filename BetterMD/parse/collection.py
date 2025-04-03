import typing as t
import logging
from ..html import CustomHTML

if t.TYPE_CHECKING:
    from ..elements import Symbol

class Collection:
    def __init__(self, *symbols:'type[Symbol]'):
        self.symbols = list(symbols)
        self.logger = logging.getLogger("BetterMD")

    def add_symbols(self, symbol:'type[Symbol]'):
        self.symbols.append(symbol)

    def remove_symbol(self, symbol:'type[Symbol]'):
        self.symbols.remove(symbol)

    def find_symbol(self, name:'str', raise_errors:'bool'=False) -> 't.Union[type[Symbol], t.Union[None, t.NoReturn]]':
        print(name)
        print("VALID HTML") if filter(lambda s: isinstance(s.html, str) and s.html.lower() == name.lower(), self.symbols) else print("INVALID HTML")
        for symbol in self.symbols:
            if name == "abbr":
                print(symbol.html)
            if isinstance(symbol.html, str) and symbol.html.lower() == name.lower():
                return symbol
            elif isinstance(symbol.html, CustomHTML) and symbol.html.verify(name):
                return symbol

        if raise_errors:
            raise ValueError(f"Symbol `{name}` not found in collection, if using default symbols it may not be supported.")
        return None