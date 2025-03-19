import re
import typing as t
from .typing import ELEMENT, TEXT
import threading as th

class MDParser:

    top_level_tags = {
        "blockquote": r"^> (.+)$", # Blockquote
        "br": r"\n\n", # Br
        "code": r"^```([A-Za-z]*)[^.](?:([^`]*)[^.])?```$", # Code block

        "h": r"^(#{1,6})(?: (.*))?$",

        "hr": r"^---+$", # Hr

        "ul" : r"^([ |	]*)(?:-|\+|\*)(?: (.*))?$", # Ul Li
        "ol" : r"^([ |	]*)(\d)\.(?: (.*))?$", # Ol Li

        "tr": r"^\|(?:[^|\n]+\|)+$",  # tr - must start and end with | and have at least one |
        "thead": r"^\|(?::?-+:?\|)+$", # thead / tbody

        "title": r"^title: .+$", # Title
    }

    def __init__(self):
        self.reset()

    def reset(self):
        self.dom = []
        self.buffer = ''
        self.list_stack = []
        self.dom_stack = []

    def create_element(self, name:'str', attrs:'dict[str, str]'=None, children:'list[ELEMENT|TEXT]'=None) -> 'ELEMENT':
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

    def create_text(self, content:'str') -> 'TEXT':
        return {
            "type": "text",
            "content": content,
            "name": "text"
        }
    
    def end_block(self):
        # Create paragraph from buffered text
        if self.buffer:
            text = self.buffer.strip()
            if text:
                para = self.create_element("p", children=[self.create_text(text)])
                self.dom.append(para)
            self.buffer = ''

    def start_block(self):
        pass

    def handle_blockquote(self, text: 'list[str]', i):
        elm = self.create_element("blockquote")
        new_text = []
        current_line = []

        for line in text[i:]:
            if re.match(self.top_level_tags["blockquote"], line):
                # Remove blockquote marker and add to current line
                content = line.removeprefix("> ").removeprefix(">").strip()
                if content:
                    current_line.append(content)
            elif line.strip() == "":
                # Empty line marks paragraph break
                if current_line:
                    new_text.append(" ".join(current_line))
                    new_text.append("")
                    current_line = []
            elif not any(re.match(pattern, line) for pattern in self.top_level_tags.values()):
                # Continuation of blockquote without marker
                current_line.append(line.strip())
            else:
                break

        if current_line:
            new_text.append(" ".join(current_line))

        # Parse blockquote content recursively
        elm["children"] = MDParser().parse("\n".join(new_text))
        self.dom.append(elm)
        
        return len(new_text) - 1

    def handle_code(self, text: 'list[str]'):
        self.end_block()
        match = re.match(self.top_level_tags["code"], "\n".join(text))
        assert match is not None, "Code block not found"

        lang = match.group(1)
        content = match.group(2)

        elm = self.create_element("pre", children=[self.create_element("code", {"language": lang}, [self.create_text(content)])])
        self.dom.append(elm)

        return "\n".join(text)["\n".join(text).index("```"):].index("```")


    def handle_br(self, text: 'list[str]'):
        self.end_block()
        if text[0] == "" and text[1] == "":
            self.dom.append(self.create_element("br", {}))
            return 1
        return 0

    def handle_h(self, line: 'str'):
        self.end_block()
        match = re.match(self.top_level_tags["h"], line)
        assert match is not None, "Header not found"

        level = len(match.group(1))
        content = match.group(2)

        self.dom.append(self.create_element(f"h{level}", children=[self.create_text(content)]))

    def handle_hr(self, line: 'str'):
        self.end_block()
        self.dom.append(self.create_element("hr", {}))

    def handle_text(self, line: 'str'):
        # Don't create text nodes for empty lines
        if not line.strip():
            self.handle_br(line)
            return

        # Buffer text content for paragraph handling
        if self.buffer:
            self.buffer += '\n' + line
        else:
            self.buffer = line

    def handle_list(self, text: 'list[str]', i: int, indent_level: int = 0) -> int:
        if re.match(self.top_level_tags["ul"], text[i]):
            list_elm = self.create_element("ul")
            list_pattern = self.top_level_tags["ul"]
        elif re.match(self.top_level_tags["ol"], text[i]):
            list_elm = self.create_element("ol")
            list_pattern = self.top_level_tags["ol"]
        else:
            return 0

        current_item = []
        lines_processed = 0
        
        while i + lines_processed < len(text):
            line = text[i + lines_processed]
            
            if not line.strip():
                if current_item:
                    # Empty line in list item - treat as paragraph break
                    current_item.append("")
                lines_processed += 1
                continue

            list_match = re.match(list_pattern, line)
            if list_match:
                indent = len(list_match.group(1))
                
                if indent < indent_level:
                    # End of current list level
                    break
                elif indent > indent_level:
                    # Nested list
                    nested_lines = lines_processed + self.handle_list(text[i + lines_processed:], 0, indent)
                    lines_processed += nested_lines
                    continue
                
                # Add previous item if exists
                if current_item:
                    content = " ".join(current_item).strip()
                    if content:
                        list_elm["children"].append(
                            self.create_element("li", children=[self.create_text(content)])
                        )
                
                # Start new item
                current_item = [list_match.group(2).strip()]
                
            elif not any(re.match(pattern, line) for pattern in self.top_level_tags.values()):
                # Continuation of list item
                current_item.append(line.strip())
            else:
                break
                
            lines_processed += 1

        # Add final item
        if current_item:
            content = " ".join(current_item).strip()
            if content:
                list_elm["children"].append(
                    self.create_element("li", children=[self.create_text(content)])
                )

        self.dom.append(list_elm)
        return lines_processed

    def handle_table(self, text: 'list[str]', i: int) -> int:
        # First check if this is actually a table
        # A proper table needs at least two rows (header and separator)
        if i + 1 >= len(text) or not re.match(self.top_level_tags["thead"], text[i + 1]):
            # Not a table, treat as regular text
            self.handle_text(text[i])
            return 1
        
        lines_processed = 0
        table = self.create_element("table")
        thead = self.create_element("thead")
        tbody = self.create_element("tbody")
        current_section = thead
        
        while i + lines_processed < len(text):
            line = text[i + lines_processed]
            
            if not line.strip():
                break
                
            if re.match(self.top_level_tags["thead"], line):
                # Alignment row - skip it but switch to tbody
                current_section = tbody
                lines_processed += 1
                continue
                
            if re.match(self.top_level_tags["tr"], line):
                # Process table row
                row = self.create_element("tr")
                cells = [cell.strip() for cell in line.strip('|').split('|')]
                
                for cell in cells:
                    if current_section == thead:
                        cell_type = "th"
                    else:
                        cell_type = "td"
                        
                    row["children"].append(
                        self.create_element(cell_type, children=[self.create_text(cell.strip())])
                    )
                    
                current_section["children"].append(row)
                lines_processed += 1
            else:
                break

        if thead["children"]:
            table["children"].append(thead)
        if tbody["children"]:
            table["children"].append(tbody)
            
        self.dom.append(table)
        return lines_processed
    
    def handle_title(self, line: 'str'):
        self.end_block()
        match = re.match(self.top_level_tags["title"], line)
        assert match is not None, "Title not found"

        title = match.group(1)
        self.head = self.create_element("head", children=[self.create_element("title", children=[self.create_text(title)])])

    def parse(self, markdown: 'str') -> 'ELEMENT':
        self.reset()
        lines = markdown.splitlines()
        i = 0

        while i < len(lines):
            line = lines[i].strip()  # Strip whitespace from each line

            # Empty line ends current block
            if not line:
                self.end_block()
                i += 1
                continue

            # Check for block-level elements
            if re.search(self.top_level_tags["h"], line):
                self.end_block()
                self.handle_h(line)
                i += 1
                continue
            
            elif re.search(self.top_level_tags["blockquote"], line):
                self.end_block()
                lines_processed = self.handle_blockquote(lines, i)
                i += lines_processed + 1
                continue
            
            elif re.search(self.top_level_tags["code"], "\n".join(lines[i:])):
                self.end_block()
                lines_processed = self.handle_code(lines[i:])
                i += lines_processed + 1
                continue
            
            elif re.search(self.top_level_tags["h"], line):
                self.end_block()
                self.handle_h(line)
                i += 1
                continue
            
            elif re.search(self.top_level_tags["hr"], line):
                self.end_block()
                self.handle_hr(line)
                i += 1
                continue
            
            elif re.search(self.top_level_tags["ul"], line) or re.search(self.top_level_tags["ol"], line):
                self.end_block()
                lines_processed = self.handle_list(lines, i)
                i += lines_processed
                continue
            
            elif re.search(self.top_level_tags["tr"], line):
                self.end_block()
                lines_processed = self.handle_table(lines, i)
                i += lines_processed
                continue
            
            elif re.search(self.top_level_tags["title"], line):
                self.end_block()
                self.handle_title(line)
                i += 1
                continue

            elif re.search(self.top_level_tags["br"], line):
                self.end_block()
                lines_processed = self.handle_br(lines[i:])
                i += lines_processed
                continue
            
            else:
                # Regular text gets buffered for paragraph handling
                self.handle_text(line)
                i += 1

        # End any remaining block
        self.end_block()

        head = self.create_element("head") or self.head
        body = self.create_element("body", children=self.dom)

        return self.create_element("html", children=[head, body])