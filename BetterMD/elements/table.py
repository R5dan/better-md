from .symbol import Symbol, List
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .h import H1, H2, H3, H4, H5, H6
from .text import Text
import logging
import typing as t

logger = logging.getLogger("BetterMD")

class TrMD(CustomMarkdown['Tr']):
    def to_md(self, inner, symbol, parent):
        logger.debug("Converting Tr element to Markdown")
        contents = "\n".join([e.to_md() for e in inner])
        split_content = contents.splitlines()
        logger.debug(f"Split content: {split_content}")
        ret = f"| {" | ".join(split_content)} |"

        return ret
        
class THeadMD(CustomMarkdown['THead']):
    def to_md(self, inner, symbol, parent):
        if len(inner) > 1:
            raise ValueError(f"THead must have exactly 1 element of type {THead.__name__} not {len(inner)} of type {type(inner[0]).__name__}")

        md = []
        for child in inner[0].children:
            child:'Symbol'
            e = child.to_md()

            md.append({"len":len(e), "style":child.styles.get("text-align", "justify")})

        return f"{inner[0].to_md()}\n|{"|".join([f"{" :" if item["style"] in ["left", "center"] else " "}{"-"*(item["len"]-2) if item["style"] == "center" else "-"*(item["len"]-1) if item["style"] in ["left", "right"] else "-"*(item["len"])}{": " if item["style"] in ["right", "center"] else " "}" for item in md])}|"
        
class TBodyMD(CustomMarkdown['TBody']):
    def to_md(self, inner, symbol, parent):
        content = [e.to_md() for e in inner if isinstance(e, Tr)]
        logger.debug(f"TBody conent: {content}")
        return "\n".join(content)

class TdMD(CustomMarkdown['Td']):
    def to_md(self, inner, symbol, parent):
        return " ".join([e.to_md() for e in inner])

class ThMD(CustomMarkdown['Th']):
    def to_md(self, inner, symbol, parent):
        return " ".join([e.to_md() for e in inner])


class TrRST(CustomRst['Tr']):
    def to_rst(self, inner, symbol, parent):
        logger.debug("Converting Tr element to RST")
        split_content = [e.to_rst() for e in inner]
        contents = "\n".join(split_content)
        ret = "\n".join([f"| {' | '.join([c for c in content])}" for content in split_content])
        
        widths = [[len(c) for c in content] for content in split_content]
        
        if symbol.is_header:
            logger.debug(f"Adding RST header separator with widths {widths[0]}")
            return f"{ret}\n| {' | '.join(['-' * width for width in widths[0]])} |"
        
        return ret
    
class TableMD(CustomMarkdown['Table']):
    def to_md(self, inner, symbol, parent):
        i1 = inner[0]
        if isinstance(i1, THead):
            head = i1.to_md()
            if not len(inner) == 2 or not isinstance(inner[1], TBody):
                raise ValueError
            body = inner[1].to_md()
        elif isinstance(i1, TBody):
            head = None
            body = i1.to_md()
        else:
            raise ValueError


        return f"{f"{head}\n" if head else ""}{body}"
    

    


class Table(Symbol):
    html = "table"
    md = TableMD()
    rst = ""

class THead(Symbol):
    html = "thead"
    rst = ""
    md = THeadMD()

class TBody(Symbol):
    html = "tbody"
    rst = ""
    md = TBodyMD()

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    rst = TrRST()

    def __init__(self, styles = {}, classes = [], dom = True, inner = [], **props):
        super().__init__(styles, classes, dom, inner, **props)

        self.is_header = False
        if isinstance(self.parent, THead):
            self.is_header = True
            logger.debug("Tr element identified as header row")


class Td(Symbol):
    html = "td"
    md = TdMD()
    rst = ""

class Th(Symbol):
    html = "th"
    md = TdMD()
    rst = ""