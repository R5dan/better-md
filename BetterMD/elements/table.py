from .symbol import Symbol
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .h import H1, H2, H3, H4, H5, H6
from .text import Text

class TableMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return "\n".join([e.to_md() for e in inner]) + "\n"

class TrMD(CustomMarkdown['Tr']):
    def to_md(self, inner, symbol, parent):
        if symbol.is_header:
            cells = [e.to_md() for e in inner]
            separator = ["---" for _ in cells]
            return f"|{'|'.join(cells)}|\n|{'|'.join(separator)}|"
        return f"|{'|'.join([e.to_md() for e in inner])}|"

class TdMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        return " ".join([e.to_md() for e in inner])
    
class TableRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        if not inner:
            return ""
            
        # Get all rows and their cells
        rows = [[cell.to_rst() for cell in row.children] for row in inner]
        
        # Calculate max width for each column
        num_cols = max(len(row) for row in rows)
        col_widths = [0] * num_cols
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))
        
        # Create the table string
        table = []
        
        # Create top border
        border = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
        table.append(border)
        
        # Add rows with proper formatting
        for i, row in enumerate(inner):
            cells = [cell.to_rst() for cell in row.children]
            row_str = "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, col_widths)) + " |"
            table.append(row_str)
            
            # Add header separator or row separator
            if row.is_header:
                separator = "+" + "+".join("=" * (width + 2) for width in col_widths) + "+"
            else:
                separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
            table.append(separator)
            
        return "\n".join(table)

class ThRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        content = " ".join([e.to_rst() for e in inner])
        return content

class TrRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        # Get cell contents
        cells = [c.to_rst() for c in inner]
        
        # Calculate column widths
        widths = [len(cell) for cell in cells]
        
        # Create row with proper spacing
        row = "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)) + " |"
        
        # For header rows, create separator
        if symbol.is_header:
            separator = "+" + "+".join("="*(width + 2) for width in widths) + "+"
        else:
            separator = "+" + "+".join("-"*(width + 2) for width in widths) + "+"
            
        return f"{row}\n{separator}"

class TdRST(CustomRst):
    def to_rst(self, inner: list[Symbol], symbol: Symbol, parent: Symbol) -> str:
        if len(inner) > 1 or not isinstance(inner[0], (Text, H1, H2, H3, H4, H5, H6)):
            raise TypeError("Table Data may only contain text as inner")

        return inner[0].to_rst()

class Table(Symbol):
    html = "table"
    md = TableMD()
    rst = TableRST()
    nl = True

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    
    def __init__(self, is_header=False, **kwargs):
        super().__init__(**kwargs)
        self.is_header = is_header

class Td(Symbol):
    html = "td"
    md = TdMD()
    rst = TdRST()

class Th(Symbol):
    html = "th"
    md = TdMD() 
    rst = ThRST()