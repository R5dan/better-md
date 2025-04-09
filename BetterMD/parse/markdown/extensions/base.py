import re
import typing as t
from .extension import Extension

if t.TYPE_CHECKING:
    from ..parser import MDParser
    from ...typing import ELEMENT, TEXT
    from ..typing import ELM_TYPE_W_END, ELM_TYPE_WO_END, OL_LIST, UL_LIST, LIST_ITEM, LIST_TYPE, OL_TYPE, UL_TYPE


def unescape(text: str) -> 'str':
    """Unescape text."""
    for i in range(len(text)):
        m = re.match(r'^\\(.)', text[i:])
        if m:
            text = text[:i] + m.group(1) + text[i + m.end(0):]
    return text

def dequote(text: str) -> str:
    """Remove quotes from text."""
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    elif text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    return text

def count(text: 'str', char: 'str') -> 'int':
    return len(re.findall(r"(?<!\\)"+char, text))

def char_isin(text, pattern):
    return bool(count(text, pattern))


class BaseExtension(Extension):
    @property
    def name(self):
        return "Base Extension"

    def init(self, parser:'MDParser'):
        super().init(parser)
        self.table = []
        self.thead = ""
        self.tcols = []
        self.had_thead = False
        self.list_stack:'list[t.Union[OL_LIST, UL_LIST]]' = []
        self.code_index = 0
        self.pre_dom = []

    @property
    def top_level_tags(self) -> 'dict[str, ELM_TYPE_W_END | ELM_TYPE_WO_END]':
        return {
            "blockquote": {
                "pattern": r"^> (.*)$",
                "handler": self.handle_blockquote,
                "end": self.end_blockquote
            },
            "code": {
                "pattern": r"^```([A-Za-z]*)?$",
                "handler": self.handle_code,
                "end": self.end_code
            },
            "h": {
                "pattern": r"^(#{1,6})(?: (.*))?$",
                "handler": self.handle_h,
                "end": None
            },
            "hr": {
                "pattern": r"^---+$",
                "handler": self.handle_hr,
                "end": None
            },
            "br": {
                "pattern": r"^\s*$",
                "handler": self.handle_br,
                "end": None
            },
            "ul": {
                "pattern": r"^(\s*)(-|\+|\*)(?: +(?:\[( |x|X)\])?(.*))?$",
                "handler": self.handle_ul,
                "end": self.end_list
            },
            "ol": {
                "pattern": r"^(\s*)(\d)(\.|\))(?: +(?:\[( |x|X)\] *)?(.*)?)?$",
                "handler": self.handle_ol,
                "end": self.end_list
            },
            "thead": {
                "pattern": r"^\|(?::?-+:?\|)+$",
                "handler": self.handle_thead,
                "end": self.end_table
            },
            "tr": {
                "pattern": r"^\|(?:[^|\n]+\|)+$",
                "handler": self.handle_tr,
                "end": self.end_table
            },
            "title": {
                "pattern": r"^title:(?: (.+))?$",
                "handler": self.handle_title,
                "end": None
            }
        }

    @property
    def text_tags(self):
        return {
            "inline_link": {
                "pattern": r"(?<!!)\[",
                "handler": self.inline_link
            },
            "automatic_link": {
                "pattern": r"^<([^>]+)>",
                "handler": self.automatic_link
            },
            "reference_definition": {
                "pattern": r"^\[([^\]]+)\]:\s*([^\s]+)",
                "handler": self.reference_definition
            },
            "reference": {
                "pattern": r"^\[([^\]]+)\]\[([^\]]+)\]\s*",
                "handler": self.reference
            },
            "image": {
                "pattern": r"^!\[",
                "handler": self.image
            },
            "bold_and_italic": {
                "pattern": [r"^([\*_])([\*_]){2}([^\*\n\r]+?)\2{2}\1", r"^([\*_]){2}([\*_])([^\*\n\r]+?)\2\1{2}"],
                "handler": self.bold_and_italic
            },
            "bold": {
                "pattern": r"^([\*_])\1{1}(.+?)\1{2}",
                "handler": self.bold
            },
            "italic": {
                "pattern": r"^([\*_])([^\*\n\r]+?)\1",
                "handler": self.italic
            },
            "code": {
                "pattern": r"^(`+)([\s\S]*?)\1",
                "handler": self.code
            }
        }

    #################### Handlers ####################

    ########## Paragraph Handlers ##########

    def inline_link(self, text:'str'):
        def handle_alt(text:'str'):
            ob = 0
            alt = ""
            i = 0

            for i, char in enumerate(text):
                if char == "[":
                    ob += 1
                elif char == "]":
                    ob -= 1
                    if ob == 0:
                        break

                alt += char

            return alt[1:], i+1

        def handle_link(text:'str'):
            i = 1
            link = ""
            link_mode = None # True - <>, False - " "
            obs = 0
            esc = False
            while i < len(text):
                char = text[i]
                if link_mode is None:
                    if char == "<":
                        link_mode = True
                        obs = 1
                    else:
                        link_mode = False
                        link = char

                elif esc:
                    esc = False
                    link += char

                elif char == "\\":
                    esc = True

                elif link_mode:
                    if char == "<":
                        obs += 1
                        if obs != 1:
                            link += char
                    elif char == ">":
                        obs -= 1
                        if obs == 0:
                            return link, i+1
                        else:
                            link += char
                    else:
                        link += char

                elif char == " ":
                    return link, i

                elif char == ")":
                    return link, i

                else:
                    link += char

                i += 1
            return link, i

        def handle_title(text:'str'):
            i = text[1:].index(text[0])
            return text[1:i+1], i+1

        assert len(text) >= 4

        if text[1] != "]":
            alt, i = handle_alt(text)
        else:
            alt = None
            i = 2
        if text[i+1] in ["'", '"']:
            href = None
            index = 0

        elif text[i+1] != ")":
            href, index = handle_link(text[i:])
        else:
            href = None
            index = 1
        i += index

        if len(text)-1 <= i or text[i+1] not in ['"', "'"]:
            title = None

        else:
            title, index = handle_title(text[i+1:])
            i += index + 2

        el = self.create_element("a", {"class": "inline-link", **({"href": href} if href else {}), **({"title": title} if title is not None else {})}, [self.create_text(alt)] if alt else [])
        return el, i

    def automatic_link(self, text:'str'):
        match = re.match(self.text_tags["automatic_link"]["pattern"], text)

        assert match is not None, "Automatic link not found"

        url = match.group(1)
        return self.create_element("a", {"class": "automatic-link", "href": url}, [self.create_text(url)]), match.end() - match.start()

    def reference_definition(self, text:'str'):
        match = re.match(self.text_tags["reference_definition"]["pattern"], text)
        assert match is not None, "Reference definition not found"

        label = match.group(1)
        url = match.group(2)
        return self.create_element("a", {"class": ["ref-def"], "href": url, "ref": True, "refId":label}, [self.create_text(label)])

    def reference(self, text:'str'):
        match = re.match(self.text_tags["reference"]["pattern"], text)
        assert match is not None, "Reference not found"

        label = match.group(1)
        ref = match.group(2)
        return self.create_element("a", { "class": ["ref"], "ref": True, "refId":ref }, [self.create_text(label)])

    def image(self, text:'str'):
        def handle_alt(text:'str'):
            ob = 0
            alt = ""
            i = 0

            for i, char in enumerate(text):
                if char == "[":
                    ob += 1
                elif char == "]":
                    ob -= 1
                    if ob == 0:
                        break

                alt += char

            return alt[1:], i+1

        def handle_link(text:'str'):
            i = 1
            link = ""
            link_mode = None # True - <>, False - " "
            obs = 0
            esc = False
            while i < len(text):
                char = text[i]
                if link_mode is None:
                    if char == "<":
                        link_mode = True
                        obs = 1
                    else:
                        link_mode = False
                        link = char

                elif esc:
                    esc = False
                    link += char

                elif char == "\\":
                    esc = True

                elif link_mode:
                    if char == "<":
                        obs += 1
                        if obs != 1:
                            link += char
                    elif char == ">":
                        obs -= 1
                        if obs == 0:
                            return link, i+1
                        else:
                            link += char
                    else:
                        link += char

                elif char == " ":
                    return link, i

                elif char == ")":
                    return link, i

                else:
                    link += char

                i += 1
            return link, i

        def handle_title(text:'str'):
            i = text[1:].index(text[0])
            return text[1:i+1], i+1

        assert len(text) >= 5

        if text[1] != "]":
            alt, i = handle_alt(text)
        else:
            alt = None
            i = 2
        if text[i+1] in ["'", '"']:
            href = None
            index = 0

        elif text[i+1] != ")":
            href, index = handle_link(text[i:])
        else:
            href = None
            index = 1
        i += index

        if len(text)-1 <= i or text[i+1] not in ['"', "'"]:
            title = None

        else:
            title, index = handle_title(text[i+1:])
            i += index + 2

        el = self.create_element("img", {**({"href": href} if href else {}), **({"title": title} if title is not None else {})}, [self.create_text(alt)] if alt else [])
        return el, i

    def bold(self, text:'str'):
        match = re.match(self.text_tags["bold"]["pattern"], text)
        assert match is not None, "Bold not found"

        content = match.group(2)
        return self.create_element("strong", children=self.parse_text(content)), match.end() - match.start()

    def italic(self, text:'str'):
        match = re.match(self.text_tags["italic"]["pattern"], text)
        assert match is not None, "Italic not found"

        content = match.group(2)
        return self.create_element("em", children=self.parse_text(content)), match.end() - match.start()

    def bold_and_italic(self, text:'str'):
        m1 = re.match(self.text_tags["bold_and_italic"]["pattern"][0], text)
        m2 = re.match(self.text_tags["bold_and_italic"]["pattern"][1], text)
        match = m1 or m2
        assert match is not None, "Bold and italic not found"

        content = match.group(3)
        return self.create_element("strong", {"class": ["italic-bold" if m1 else "bold-italic"]}, children=[self.create_element("em", children=self.parse_text(content))]), match.end() - match.start()

    def code(self, text:'str'):
        match = re.match(self.text_tags["code"]["pattern"], text)
        assert match is not None, "Code not found"

        return self.create_element("code", {"class": ["codespan"]}, [self.create_text(match.group(2))]), match.end() - match.start()

    ########## Top Level Handlers ##########

    # Blockquote

    def handle_blockquote(self, line: 'str'):
        if self.block != "BLOCKQUOTE":
            self.start_block("BLOCKQUOTE", self.end_blockquote)

        match = re.match(self.top_level_tags["blockquote"]["pattern"], line)
        assert match is not None, "Blockquote not found"

        self.handle_text(match.group(1))

    def end_blockquote(self):
        subparser = self.parser_class()
        children = subparser.parse(self.buffer)
        return self.create_element("blockquote", children=children)

    # Code

    def handle_code(self, line: 'str'):
        if not self.parsing[0]:
            self.end_block(parse=False)
        else:
            self.parsing = False, ["code"]

        if self.block is None or not self.block.startswith("CODE:"):
            match = re.match(self.top_level_tags["code"]["pattern"], line)
            assert match is not None, "Code block not found"
            lang = match.group(1) or ""
            self.start_block(f"CODE:{lang}", self.end_code)
        else:
            self.end_block()

    def end_code(self):
        lang = self.block[5:]
        elm = self.create_element("code", {"class": ["codeblock"], "language": lang}, [self.create_element("pre", children=[self.create_text(self.buffer)])])
        self.buffer = ""
        return elm

    # List

    def handle_ul(self, line: 'str'):
        match = re.match(self.top_level_tags["ul"]["pattern"], line)
        assert match is not None, "UL not found"

        indent = len(match.group(1))
        type = match.group(2)
        input = match.group(3) != None
        checked = match.group(3) != " "
        contents = match.group(4) or ""

        if self.block != "UL":
            self.start_block("UL", self.end_list)
            self.list_stack = []

        # Store the indent level and content for proper nesting
        self.list_stack.append({"list":"ul", "input":input, "checked": checked, "indent": indent, "contents": contents, "type": type})

    def handle_ol(self, line: 'str'):
        match = re.match(self.top_level_tags["ol"]["pattern"], line)
        assert match is not None, "OL not found"

        indent = len(match.group(1))
        num = int(match.group(2))
        type = match.group(3)
        input = match.group(4) != None
        checked = match.group(4) != " "
        contents = match.group(5) or ""
        input = False

        if self.block != "OL":
            self.start_block("OL", self.end_list)
            self.list_stack = []

        # Store the indent level and content for proper nesting
        self.list_stack.append({"list":"ol", "input":input, "checked": checked, "indent": indent, "contents": contents, "type": type, "num": num})


    def end_list(self):
        def data2li(item: 'UL_LIST|OL_LIST') -> 'LIST_ITEM':
            return {
                "data": item,
                "dataType": "item"
            }

        lists:'list[LIST_TYPE]' = [{
            "value": [],
            "parent": None,
            "type": "ul" if self.block == "UL" else "ol",
            "key": self.list_stack[0]["type"],
            "dataType": "list",
            **({"start": self.list_stack[0]["num"]} if self.block == "OL" else {})
        }]
        
        cur_indent = -1
        cur_list = lists[0]

        list_modes:'dict[str, t.Literal["ul", "ol"]]' = {
            "-": "ul", "*": "ul", "+": "ul",
            ")": "ol", ".": "ol"
        }

        for item in self.list_stack:
            indent = item["indent"]
            mode = list_modes[item["type"]]

            if indent > cur_indent:
                # Create new nested list
                new_list:'LIST_TYPE' = {
                    "value": [data2li(item)],
                    "parent": cur_list,
                    "type": mode,
                    "key": item["type"],
                    "dataType": "list",
                    **({"start": item["num"]} if mode == "ol" else {})
                }
                cur_list["value"].append(new_list)
                cur_list = new_list
                cur_indent = indent

            elif indent < cur_indent:
                # Go back up the tree
                while cur_indent > indent and cur_list["parent"] is not None:
                    cur_list = cur_list["parent"]
                    cur_indent -= 1
                cur_list["value"].append(data2li(item))

            else:
                # Same level
                cur_list["value"].append(data2li(item))

        def handle_item(item:'LIST_ITEM'):
            if item["data"]["input"]:
                return self.create_element(
                    "li",
                    children=[
                        self.create_element(
                            "input",
                            {
                                "class": ["checklist"],
                                "type": "checkbox",
                                "checked": item["data"]["checked"]
                            }
                        ),
                        self.create_text(item["data"]["contents"])
                    ]
                )
            return self.create_element(
                "li",
                children=[self.create_text(item["data"]["contents"])]
            )

        def handle_child_list(child_list:'LIST_TYPE'):
            return self.create_element(
                child_list["type"],
                {
                    "class": [f"list-{child_list['key']}"],
                    **({"start": child_list["start"]} if child_list["type"] == "ol" else {})
                },
                [
                    handle_child_list(child) if child.get("dataType") == "list" 
                    else handle_item(child) 
                    for child in child_list["value"]
                ]
            )

        return [handle_child_list(list) for list in lists]

    # Table

    # TR

    def handle_tr(self, line: 'str'):
        if self.had_thead:
            self.table.append(line)
            return

        if self.thead:
            self.handle_text(self.thead)

        self.thead = line


    def handle_thead(self, line: 'str'):
        if not self.thead:
            self.handle_text(line)
        elif self.had_thead:
            self.table.append(line)
        else:
            self.start_block("TABLE", self.end_table)
            self.had_thead = True
            self.tcols = []
            for col in line.split("|"):
                if col == "":
                    continue
                if col.startswith(":") and col.endswith(":"):
                    self.tcols.append("center")
                elif col.startswith(":"):
                    self.tcols.append("left")
                elif col.endswith(":"):
                    self.tcols.append("right")
                else:
                    self.tcols.append("justify")

    def end_table(self):
        head = [h.strip() for h in self.thead.removeprefix("|").removesuffix("|").split("|")]

        body = [
            [
                cell.strip() for cell in row.removeprefix("|").removesuffix("|").split("|")
            ] for row in self.table
        ]

        return self.create_element(
                "table",
                children=[
                    self.create_element(
                        "thead",
                        children=[
                            self.create_element(
                                "tr",
                                children=[
                                    self.create_element("th", {"class": [f"list-{style}"]}, [self.create_text(cell.strip())]) for cell, style in zip(head, self.tcols)
                                ]
                            )
                        ]
                    ),
                    self.create_element(
                        "tbody",
                        children=[
                            self.create_element(
                                "tr",
                                children=[
                                    self.create_element("td", {"class": [f"list-{style}"]},[self.create_text(cell.strip())]) for cell, style in zip(row, self.tcols)
                                ]
                            ) for row in body
                        ]
                    )
                ]
            )

    # Br

    def handle_br(self, line: 'str'):
        self.end_block()
        return self.create_element("br")

    # Header

    def handle_h(self, line: 'str'):
        self.end_block()
        match = re.match(self.top_level_tags["h"]["pattern"], line)
        assert match is not None, "Header not found"

        level = len(match.group(1))
        content = match.group(2)

        return self.create_element(f"h{level}", {"id": content.replace(" ", "-")}, children=[self.create_text(content)])

    # Horizontal rule

    def handle_hr(self, line: 'str'):
        self.end_block()
        return self.create_element("hr", {})

    def handle_title(self, line: 'str'):
        self.end_block()
        match = re.match(self.top_level_tags["title"]["pattern"], line)
        assert match is not None, "Title not found"

        title = match.group(1)
        self.head = self.create_element("head", children=[self.create_element("title", children=[self.create_text(title)])])
