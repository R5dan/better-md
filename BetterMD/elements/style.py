from .symbol import Symbol
from ..html import CustomHTML
from ..typing import ATTR_TYPES

import typing as t

StyleValue = t.Union[str, int, float, tuple[t.Union[str, int, float], ...]]
StyleDict = dict[str, t.Union[StyleValue, 'StyleDict']]

class HTML(CustomHTML['Style']):
    def verify(self, text) -> bool:
        return text.lower() == "style"

    def _format_value(self, value: 'StyleValue') -> 'str':
        """Format a style value for CSS output"""
        if isinstance(value, tuple):
            return " ".join(str(v) for v in value)
        return str(value)

    def _process_styles(self, selector: 'str', styles: 'StyleDict') -> 'list[str]':
        """Process styles recursively and return CSS rules"""
        result = []
        properties = {}
        nested = {}
        
        # Separate properties from nested selectors
        for key, value in styles.items():
            if isinstance(value, dict):
                nested[key] = value
            else:
                properties[key] = value
        
        # Add properties for current selector if any
        if properties:
            result.append(f"{selector} {{")
            for prop, value in properties.items():
                formatted_value = self._format_value(value)
                result.append(f"  {prop}: {formatted_value};")
            result.append("}")
        
        # Process nested selectors
        for key, value in nested.items():
            if key.startswith(':'):  # Pseudo-class
                nested_selector = f"{selector}{key}"
            elif key.startswith('#'):  # ID
                nested_selector = f"{selector} {key}"
            elif key.startswith('.'):  # Class
                nested_selector = f"{selector} {key}"
            else:  # Element or custom
                nested_selector = f"{selector} {key}"
            
            result.extend(self._process_styles(nested_selector, value))
        
        return result

    def to_html(self, inner, symbol, parent):
        style_str = []
        
        for selector, rules in symbol.style.items():
            style_str.extend(self._process_styles(selector, rules))

        return f"<style>{'\n'.join(style_str)}\n{symbol.raw}\n</style>"


class Style(Symbol):  
    def __init__(self, styles:'dict[str, ATTR_TYPES]'=None, classes:'list[str]'=None, inner:'list[Symbol]'=None, *, style: t.Optional[StyleDict] = None, raw: str = "",**props):
        """
        Styles with intuitive nested structure

        Args:
            style: Dictionary of style rules with nested selectors
            raw: Original raw CSS text
            inner: Child symbols
            **props: Additional properties
        """
        super().__init__(styles, classes, inner, **props)
        self.style: 'StyleDict' = style or {}
        self.raw: 'str' = raw

    prop_list = ["blocking", "media", "nonce", "title", "type"]

    html = HTML()
    md = ""
    rst = ""