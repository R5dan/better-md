from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .h import H1, H2, H3, H4, H5, H6
from .text import Text
import itertools as it

class TableMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        result = []
        thead_content = ""
        tbody_rows = []
        
        # Process inner elements
        for section in inner:
            if isinstance(section, THead):
                thead_content = section.to_md()
            elif isinstance(section, TBody):
                tbody_content = section.to_md()
                if tbody_content:
                    tbody_rows.append(tbody_content)
        
        # Combine all parts
        if thead_content:
            result.append(thead_content)
        
        if tbody_rows:
            result.append("\n".join(tbody_rows))
        
        return "\n".join(result)
   
class TableRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        if not inner:
            return ""
        
        # First pass: collect all cell widths from both thead and tbody
        col_widths = []
        all_rows = []
        
        for section in inner:
            if isinstance(section, THead) or isinstance(section, TBody):
                for row in section.children:
                    cells = [cell.to_rst() for cell in row.children]
                    all_rows.append((cells, isinstance(section, THead)))
                    
                    # Update column widths
                    if not col_widths:
                        col_widths = [len(cell) for cell in cells]
                    else:
                        col_widths = [max(old, len(new)) for old, new in zip(col_widths, cells + [''] * (len(col_widths) - len(cells)))]
        
        if not all_rows:
            return ""
        
        # Second pass: generate RST with consistent widths
        result = []
        
        # Top border
        top_border = "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+"
        result.append(top_border)
        
        for i, (cells, is_header) in enumerate(all_rows):
            # Create row with proper spacing using consistent column widths
            row = "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, col_widths)) + " |"
            result.append(row)
            
            # Add separator after each row
            if is_header:
                separator = "+" + "+".join(["=" * (width + 2) for width in col_widths]) + "+"
            else:
                separator = "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+"
            result.append(separator)
        
        return "\n".join(result)

class THeadMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if not inner:
            return ""
            
        rows = []
        widths = []
        
        # First pass: collect all rows and calculate column widths
        for row in inner:
            row_cells = [cell.to_md() for cell in row.children]
            if not widths:
                widths = [len(cell) for cell in row_cells]
            else:
                widths = [max(old, len(new)) for old, new in zip(widths, row_cells)]
            rows.append(row_cells)
        
        if not rows:
            return ""
        
        # Second pass: generate properly formatted markdown
        result = []
        for row_cells in rows:
            row = "|" + "|".join(row_cells) + "|"
            result.append(row)
        
        # Add separator row
        separator = "|" + "|".join(["-" * width for width in widths]) + "|"
        result.append(separator)
        
        return "\n".join(result)

class THeadRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        # This is now handled by TableRST
        return ""

class TBodyMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        if not inner:
            return ""
        
        rows = []
        for row in inner:
            rows.append(row.to_md())
        
        return "\n".join(rows)

class TrMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        cells = [cell.to_md() for cell in inner]
        return f"|{'|'.join(cells)}|"

class TrRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        # This is now handled by TableRST
        return ""

class TdMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return " ".join([e.to_md() for e in inner])

class TdRST(CustomRst):
    def to_rst(self, inner: list[Symbol], symbol: Symbol, parent: Symbol) -> str:
        if not inner:
            return ""
            
        if len(inner) > 1 or not isinstance(inner[0], (Text, H1, H2, H3, H4, H5, H6)):
            return " ".join([e.to_rst() for e in inner])  # Fallback to join instead of raising error
        return inner[0].to_rst()

class ThRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        return " ".join([e.to_rst() for e in inner])

class TBodyRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        # This is now handled by TableRST
        return ""

class Table(Symbol):
    html = "table"
    md = TableMD()
    rst = TableRST()
    nl = True

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    rst = TrRST()

class Td(Symbol):
    html = "td"
    md = TdMD()
    rst = TdRST()

class Th(Symbol):
    html = "th"
    md = TdMD()
    rst = ThRST()

class THead(Symbol):
    html = "thead"
    md = THeadMD()
    rst = THeadRST()

class TBody(Symbol):
    html = "tbody"
    md = TBodyMD()
    rst = TBodyRST()