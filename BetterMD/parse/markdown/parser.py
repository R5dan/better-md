import re
from ..typing import ELEMENT, TEXT
import typing as t

if t.TYPE_CHECKING:
    from .typing import ELM_TYPE_W_END, ELM_TYPE_WO_END, ELM_TEXT
    from . import Extension

class MDParser:
    extensions:'list[type[Extension]]' = []
    top_level_tags:'dict[str, t.Union[ELM_TYPE_W_END, ELM_TYPE_WO_END]]' = {}
    text_tags:'dict[str, ELM_TEXT]' = {}

    @classmethod
    def add_extension(cls, extension: 'type[Extension]'):
        cls.extensions.append(extension)

    @classmethod
    def remove_extension(cls, extension: 'type[Extension]'):
        cls.extensions.remove(extension)

    @classmethod
    def get_extension(cls, name: 'str') -> 't.Union[type[Extension], None]':
        for extension in cls.extensions:
            if extension.name == name:
                return extension

    def refresh_extensions(self):
        self.top_level_tags = {}
        self.text_tags = {}

        for extension in self.extensions:
            ext = extension(MDParser)
            ext.init(self)
            self.top_level_tags.update(ext.top_level_tags)
            self.text_tags.update(ext.text_tags)
            self.exts.append(ext)

    def __init__(self):
        self.exts:'list[Extension]' = []
        self.reset()

    def reset(self):
        self.dom:'list[ELEMENT|TEXT]' = []
        self.buffer = ""
        self.end_func:'t.Optional[t.Callable[[], None]]' = None
        self.dom_stack = []
        self.head = []
        self.block = None
        self.parsing:'tuple[bool, list[str]]' = True, [] # bool - is parsing, list[str] - tags

        for extension in self.exts:
            extension.init(self)

    @staticmethod
    def create_element(name:'str', attrs:'dict[str, t.Union[str, bool, int, float]]'=None, children:'list[ELEMENT|TEXT]'=None) -> 'ELEMENT':
        if children is None:
            children = []

        if attrs is None:
            attrs = {}

        return {
            "type": "element",
            "name": name,
            "attributes": attrs,
            "children": children
        }

    @staticmethod
    def create_text(content:'str') -> 'TEXT':
        return {
            "type": "text",
            "content": content,
            "name": "text"
        }

    def end_block(self, parse=True):
        if self.buffer and parse:
            self.dom.append(self.parse_text(self.buffer))

        if self.end_func is None:
            return

        self.dom.append(self.end_func())
        self.end_func = None
        self.block = None
        self.parsing = True, []

    def start_block(self, block, end_func=None):
        self.end_block()
        self.block = block
        self.end_func = end_func

    # Text

    def handle_text(self, line: 'str'):
        # Buffer text content for paragraph handling
        if self.buffer:
            self.buffer += '\n' + line
        else:
            self.buffer = line

    def parse(self, markdown: 'str') -> 'list[ELEMENT]':
        self.refresh_extensions()

        for line in markdown.splitlines():
            # Check for block-level elements
            for tag, handler in self.top_level_tags.items():
                if (not self.parsing[0]) and (tag not in self.parsing[1]):
                    continue
                if re.search(handler["pattern"], line):
                    if handler["end"] is not None:
                        handler["handler"](line)
                    else:
                        self.dom.append(handler["handler"](line))
                    break

            else:
                # Regular text gets buffered for paragraph handling
                self.handle_text(line)

        # End any remaining block
        self.end_block()

        dom:'list[ELEMENT]' = []

        for item in self.dom:
            if isinstance(item, list):
                dom.extend(item)
            else:
                dom.append(item)

        return dom

    def parse_text(self, text: 'str') -> 'list[ELEMENT | TEXT]':
        self.refresh_extensions()
        plain_text = ""
        dom = []
        i = 0

        def handle(pattern, handler):
            if re.match(pattern, text[i:]):
                return True, *handler(text[i:])

            return False, None, 0

        while i < len(text):
            for tag, handler in self.text_tags.items():
                if not self.parsing[0] and tag not in self.parsing[1]:
                    continue

                if isinstance(handler["pattern"], list):
                    b = False
                    for pattern in handler["pattern"]:
                        v, elm, l = handle(pattern, handler["handler"])
                        if v:
                            if plain_text:
                                dom.append(self.create_text(plain_text))
                                plain_text = ""

                            dom.append(elm)
                            i += l
                            b = True
                            break
                    if b:
                        break
                else:
                    v, elm, l = handle(handler["pattern"], handler["handler"])
                    if v:
                        if plain_text:
                            dom.append(self.create_text(plain_text))
                            plain_text = ""
                        
                        dom.append(elm)
                        i += l
                        break

            else:
                plain_text += text[i]

            i += 1

        if plain_text:
            dom.append(self.create_text(plain_text))
            plain_text = ""

        return dom

    def from_file(self, file):
        with open(file, "r") as f:
            self.parse(f.read())

        head = self.create_element("head", children=self.head)
        body = self.create_element("body", children=self.dom)

        return self.create_element("html", children=[head, body])