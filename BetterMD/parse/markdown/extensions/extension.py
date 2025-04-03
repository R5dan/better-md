import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from ..typing import ELM_TYPE_W_END, ELM_TYPE_WO_END, ELM_TEXT, ELEMENT, TEXT
    from ..parser import MDParser

class Extension(ABC):
    def __init__(self, parser_class:'type[MDParser]'):
        self.parser_class = parser_class

    def init(self, parser:'MDParser'):
        self.parser = parser
        self.dom = parser.dom

    @property
    @abstractmethod
    def name(self) -> 'str': ...
    
    @property
    @abstractmethod
    def top_level_tags(self) -> 'dict[str, ELM_TYPE_W_END | ELM_TYPE_WO_END]':
        ...

    @property
    @abstractmethod
    def text_tags(self) -> 'dict[str, ELM_TEXT]':
        ...

    @property
    def buffer(self) -> 'str':
        return self.parser.buffer
    
    @buffer.setter
    def buffer(self, value:'str'):
        self.parser.buffer = value

    @property
    def block(self) -> 't.Optional[str]':
        return self.parser.block
    
    @block.setter
    def block(self, value:'str'):
        self.parser.block = value
    
    @property
    def parsing(self) -> 'tuple[bool, list[str]]':
        return self.parser.parsing
    
    @parsing.setter
    def parsing(self, value:'tuple[bool, list[str]]'):
        self.parser.parsing = value

    def create_text(self, content:'str'):
        return self.parser.create_text(content)

    def create_element(self, name:'str', attrs:'dict[str, t.Union[str, bool, int, float, list, dict]]'=None, children:'list[ELEMENT|TEXT]'=None):
        return self.parser.create_element(name, attrs, children)

    def start_block(self, block:'str', end_func:'t.Optional[t.Callable[[], None]]'=None):
        self.parser.start_block(block, end_func)

    def end_block(self, parse=True):
        self.parser.end_block(parse)

    def handle_text(self, line:'str'):
        self.parser.handle_text(line)

    def parse(self, text:'str'):
        return self.parser.parse(text)

    def parse_text(self, text:'str'):
        return self.parser.parse_text(text)
