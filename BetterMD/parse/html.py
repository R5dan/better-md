from .typing import ELEMENT, TEXT
from ..typing import ATTRS
import typing as t

class HTMLParser:
    NON_PARSING_TAGS = ['script', 'style', 'textarea']

    def __init__(self):
        self.reset()

    @property
    def children(self):
        return self.current_tag["children"]

    def reset(self):
        self.dom:'list[ELEMENT|TEXT]' = []
        self.buffer = ""
        self.state = ""
        self.current_tag = {
            "type": "element",
            "name": "dom",
            "attributes": {},
            "children": self.dom,
            "parent": None
        }
        self.tag = ""
        self.non_parsing_content = ""
        self.in_non_parsing_tag = False
        self.current_non_parsing_tag = None

    def create_element(self, name:'str', attrs:'ATTRS'=None, children:'list[ELEMENT|TEXT]'=None) -> 'ELEMENT':
        if children is None:
            children = []

        if attrs is None:
            attrs = {}

        return {
            "type": "element",
            "name": name,
            "attributes": attrs,
            "children": children,
            "parent": self.current_tag
        }

    @staticmethod
    def create_text(content:'str') -> 'TEXT':
        return {
            "type": "text",
            "content": content,
            "name": "text"
        }

    def parse(self, html:'str') -> 'list[ELEMENT]':
        self.reset()
        i = 0
        
        while i < len(html):
            char = html[i]
            if self.in_non_parsing_tag:
                closing_tag = f"</{self.current_non_parsing_tag}>"
                if html[i:i+len(closing_tag)].lower() == closing_tag.lower():
                    # Found closing tag, create element with unparsed content
                    self.children.append(self.create_text(self.non_parsing_content))
                    self.current_tag = self.current_tag["parent"]

                    self.in_non_parsing_tag = False
                    self.current_non_parsing_tag = None
                    self.non_parsing_content = ""
                    i += len(closing_tag)
                else:
                    self.non_parsing_content += char
                    i += 1
                continue

            elif char == '<':
                if self.buffer:
                    self.children.append(self.create_text(self.buffer))
                    self.buffer = ""

                # Check for comment
                if html[i:i+4] == '<!--':
                    i = self.handle_comment(html, i+4)
                elif html[i + 1] == '/':
                    # Closing tag
                    i = self.handle_closing_tag(html, i + 2)
                    if self.current_tag["parent"] is not None:
                        self.current_tag = self.current_tag["parent"]
                else:
                    # Opening tag
                    i = self.handle_opening_tag(html, i + 1)
                    # Check if we entered a non-parsing tag
                    if self.tag.lower() in self.NON_PARSING_TAGS:
                        self.in_non_parsing_tag = True
                        self.current_non_parsing_tag = self.tag
            else:
                self.buffer += char
                i += 1

        if self.buffer:
            self.dom.append(self.create_text(self.buffer))
        
        return self.dom

    def handle_opening_tag(self, html:'str', start:'int') -> 'int':
        i = start
        self.tag = ""
        attrs:'dict[str, t.Union[str, bool, int, float]]' = {}

        # Get tag name
        while i < len(html) and not html[i].isspace() and html[i] != '>':
            self.tag += html[i]
            i += 1

        # Skip whitespace
        while i < len(html) and html[i].isspace():
            i += 1

        # Parse attributes
        while i < len(html) and html[i] != '>' and html[i:i+1] != '/>':
            if html[i].isspace():
                i += 1
                continue

            # Get attribute name
            attr = ""
            while i < len(html) and not html[i].isspace() and html[i] != '=' and html[i] != '>':
                attr += html[i]
                i += 1
            
            if attr == "/" and html[i-1:i+1] == "/>":
                break

            # Skip whitespace
            while i < len(html) and html[i].isspace():
                i += 1

            value = True  # Default for boolean attributes

            # Get attribute value if it exists
            if i < len(html) and html[i] == '=':
                i += 1
                # Skip whitespace
                while i < len(html) and html[i].isspace():
                    i += 1

                quote = html[i] if html[i] in '"\'`' else None
                if quote:
                    i += 1
                    value = ""
                    while i < len(html) and html[i] != quote:
                        value += html[i]
                        i += 1
                    i += 1  # Skip closing quote
                else:
                    value = ""
                    while i < len(html) and not html[i].isspace() and html[i] != '>':
                        value += html[i]
                        i += 1

            if attr:
                attrs[attr] = value

            # Skip whitespace
            while i < len(html) and html[i].isspace():
                i += 1

        # Handle self-closing tags
        tag = self.create_element(self.tag, attrs)
        is_self_closing = html[i-1] == '/'
        if is_self_closing:
            self.children.append(tag)
        else:
            self.children.append(tag)
            self.current_tag = tag

        return i + 1

    def handle_closing_tag(self, html:'str', start:'int') -> 'int':
        i = start
        tag = ""
        
        # Get tag name
        while i < len(html) and html[i] != '>':
            tag += html[i]
            i += 1
        self.tag = tag
        return i + 1

    def handle_comment(self, html:'str', start:'int') -> 'int':
        i = start
        comment = ""
        
        # Get comment content until -->
        while i < len(html) - 2:
            if html[i:i+3] == '-->':
                break
            comment += html[i]
            i += 1
        
        # Create comment element
        self.children.append(self.create_element("comment", children=[self.create_text(comment)]))
        
        return i + 3  # Skip past -->
