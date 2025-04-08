from .symbol import Symbol
from ..utils import List
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .text import Text
import logging
import typing as t

if t.TYPE_CHECKING:
    # Wont be imported at runtime
    import pandas as pd # If not installed, will not affect anything at runtime


logger = logging.getLogger("BetterMD")
T = t.TypeVar("T")

class TrMD(CustomMarkdown['Tr']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        logger.debug("Converting Tr element to Markdown")
        contents = "\n".join([e.to_md() for e in inner])
        split_content = contents.splitlines()
        logger.debug(f"Split content: {split_content}")
        ret = f"| {" | ".join(split_content)} |"
        return ret


class THeadMD(CustomMarkdown['THead']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        md = []
        for child in symbol.head.children:
            e = child.to_md()

            md.append({"len":len(e), "style":child.styles.get("text-align", "justify")})

        def parse_md(data: 'dict') -> 'str':
            start = " :" if data["style"] in ["left", "center"] else " "
            middle = "-"*(data["len"]-2) if data["style"] == "center" else "-"*(data["len"]-1) if data["style"] in ["left", "right"] else "-"*(data["len"])
            end = ": " if data["style"] in ["right", "center"] else " "

            return f"{start}{middle}{end}"

        return f"{inner[0].to_md()}\n|{"|".join([parse_md(item) for item in md])}|"
        
class TBodyMD(CustomMarkdown['TBody']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        content = [e.to_md() for e in inner if isinstance(e, Tr)]
        logger.debug(f"TBody conent: {content}")
        return "\n".join(content)

class TdMD(CustomMarkdown['Td']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        if not pretty:
            return " ".join([e.to_md() for e in inner])
        
        length = len(max(symbol.table.cols[symbol.header], key=len).data)
        logger.debug(f"Td length: {len(symbol)}")
        logger.debug(f"Column length: {length}")
        return " ".join([e.to_md() for e in inner]).center(length)

class ThMD(CustomMarkdown['Th']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        if not pretty:
            return " ".join([e.to_md() for e in inner])
        
        width = len(max(symbol.table.cols[symbol.header], key=len).data)

        
        if symbol.data == "":
            return "".center(width)
        
        return f"**{" ".join([e.to_md() for e in inner]).center(width)}**"
    
class TableMD(CustomMarkdown['Table']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        logger.debug("Converting Table element to Markdown")
        head = symbol.head.to_md() if symbol.head else None
        body = symbol.body.to_md()

        logger.debug(f"Table conversion complete. Has header: {head is not None}")
        return f"{f"{head}\n" if head else ""}{body}"


class TableRST(CustomRst['Table']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        logger.debug("Converting Table element to RST")
        head = symbol.head.to_rst() if symbol.head else None
        body = symbol.body.to_rst()

        return f"{f"{head}\n" if head else ""}{body}"

class THeadRST(CustomRst['THead']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        logger.debug("Converting THead element to RST")
        logger.debug(f"THead has {len(inner)} children: {[e.to_rst() for e in inner]}")
        top = [len(max(symbol.table.cols[child.header], key=len).data) for child in symbol.head.children]
        content = "\n".join([e.to_rst() for e in inner])
        return f"+-{"-+-".join([t*"-" for t in top])}-+\n{content}\n+={"=+=".join([t*"=" for t in top])}=+"
    
class TBodyRST(CustomRst['TBody']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        bottom = [len(max(symbol.table.cols[child.header], key=len).data) for child in symbol.table.head.head.children]
        return f'{f"\n+-{"-+-".join(["-"*b for b in bottom])}-+\n".join([e.to_rst() for e in inner if isinstance(e, Tr)])}\n+-{"-+-".join(["-"*b for b in bottom])}-+'

class TrRST(CustomRst['Tr']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        return f'| {" |\n| ".join(" | ".join([e.to_rst() for e in inner]).split("\n"))} |'


class TdRST(CustomRst['Td']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_rst() for e in inner])
        width = len(max(symbol.table.cols[symbol.header], key=len).data)
        return content.center(width)

class ThRST(CustomRst['Th']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_rst() for e in inner])
        width = len(max(symbol.table.cols[symbol.header], key=len).data)
        if content == "":
            return "".center(width)
        return f"**{content}**".center(width)

class Table(Symbol):
    html = "table"
    md = TableMD()
    rst = TableRST()
    head:'THead' = None
    body:'TBody' = None
    foot:'TFoot' = None

    cols: 'dict[Th, list[Td]]' = {}
    headers: 'list[Th]' = []

    def to_pandas(self):
        if not self.prepared:
            self.prepare()

        logger.debug("Converting Table to pandas DataFrame")
        try:
            import pandas as pd
            df = pd.DataFrame([e.to_pandas() for e in self.body.children], columns=self.head.to_pandas())
            logger.debug(f"Successfully converted table to DataFrame with shape {df.shape}")
            return df
        except ImportError:
            logger.error("pandas not installed - tables extra required")
            raise ImportError("`tables` extra is required to use `to_pandas`")
        except Exception as e:
            logger.error(f"Error converting table to pandas: {str(e)}")
            raise
        
    @classmethod
    def from_pandas(cls, df:'pd.DataFrame'):
        logger.debug(f"Creating Table from pandas DataFrame with shape {df.shape}")
        try:
            import pandas as pd
            self = cls()
            head = THead.from_pandas(df.columns)
            body = TBody.from_pandas(df)
            
            self.head = head
            self.body = body
            
            self.add_child(head)
            self.add_child(body)
            
            logger.debug("Successfully created Table from DataFrame")
            logger.debug(f"Table has {len(self.head.children)} columns and {len(self.body.children)} rows with shape {df.shape}")
            logger.debug(f"Table head: {self.head.to_list()}")
            logger.debug(f"Table body: {self.body.to_list()}")
            logger.debug(f"Table foot: {self.foot.to_list()}")
            return self
        except ImportError:
            logger.error("pandas not installed - tables extra required")
            raise ImportError("`tables` extra is required to use `from_pandas`")
        except Exception as e:
            logger.error(f"Error creating table from pandas: {str(e)}")
            raise
    
    def prepare(self, parent = None, *args, **kwargs):
        return super().prepare(parent, table=self, *args, **kwargs)

class THead(Symbol):
    html = "thead"
    rst = THeadRST()
    md = THeadMD()

    table:'Table' = None
    data:'list[Tr]' = None


    def to_pandas(self) -> 'pd.Index':
        import pandas as pd
        if len(self.data) == 0:
            pass # Return undefined

        elif len(self.data) == 1:
            return pd.Index([d.data for d in self.data])

    def to_list(self) -> 'list[list[str]]':
        if not self.prepared:
            self.prepare()

        return [
            [
                d.data for d in row.data
            ] for row in self.data
        ]

    @classmethod
    def from_pandas(cls, data:'pd.Index | pd.MultiIndex'):
        self = cls()

        self.add_child(Tr.from_pandas(data))

    @classmethod
    def from_list(cls, data:'list[str]|list[list[str]]'):
        self = cls()
        if isinstance(data[0], list):
            self.extend_children([Tr.from_list(d, head=True) for d in data])
        else:
            self.add_child(Tr.from_list(data))

        return self

    def prepare(self, parent = None, table=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.table.head = self
        return super().prepare(parent, table=table, head=self, *args, **kwargs)

class TBody(Symbol):
    html = "tbody"
    rst = TBodyRST()
    md = TBodyMD()

    table:'Table' = None
    data :'list[Tr]' = []

    def to_pandas(self):
        if not self.prepared:
            self.prepare()

        logger.debug("Converting TBody to pandas format")
        data = [e.to_pandas() for e in self.children]
        logger.debug(f"Converted {len(data)} rows from TBody")
        return data
    
    @classmethod
    def from_pandas(cls, df:'pd.DataFrame'):
        logger.debug(f"Creating TBody from DataFrame with {len(df)} rows")
        try:
            self = cls()

            for i, row in df.iterrows():
                tr = Tr.from_pandas(row)
                self.children.append(tr)
                logger.debug(f"Added row {i} to TBody")

            return self
        except ImportError:
            logger.error("pandas not installed - tables extra required")
            raise ImportError("`tables` extra is required to use `from_pandas`")
        
    @classmethod
    def from_list(cls, data:'list[list[str]]'):
        try:
            self = cls()

            for row in data:
                self.add_child(Tr.from_list(row))

        except Exception as e:
            logger.error(f"Exception occurred in `from_list`: {e}")

    def to_list(self):
        return [
            row.to_list() for row in self.data
        ]

    def prepare(self, parent = None, table=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.table.body = self
        return super().prepare(parent, table=table, head=self, *args, **kwargs)

class TFoot(Symbol):
    html = "tfoot"
    md = TBodyMD()
    rst = TBodyRST()

    table:'Table' = None
    data :'list[Tr]' = []

    def to_pandas(self):
        if not self.prepared:
            self.prepare()

        logger.debug("Converting TFoot to pandas format")
        data = [e.to_pandas() for e in self.children]
        logger.debug(f"Converted {len(data)} rows from TFoot")
        return data

    @classmethod
    def from_pandas(cls, df:'pd.DataFrame'):
        logger.debug(f"Creating TFoot from DataFrame with {len(df)} rows")
        try:
            self = cls()

            for i, row in df.iterrows():
                tr = Tr.from_pandas(row)
                self.children.append(tr)
                logger.debug(f"Added row {i} to TFoot")

            return self
        except ImportError:
            logger.error("pandas not installed - tables extra required")
            raise ImportError("`tables` extra is required to use `from_pandas`")

    def prepare(self, parent = None, table=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.table.foot = self
        return super().prepare(parent, table=table, head=self, *args, **kwargs)

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    rst = TrRST()

    head:'THead|TBody|TFoot' = None
    table:'Table' = None
    data:'list[t.Union[Td, Th]]' = []


    def to_pandas(self):
        if not self.prepared:
            self.prepare()

        if isinstance(self.head, THead):
            raise ValueError("This `Tr` is a header row and cannot be converted to a pandas `Series`")

        try:
            import pandas as pd

            return pd.Series(
                [d for d in self.data],
                self.table.head.to_pandas()
            )

        except ImportError:
            raise ImportError("`tables` extra is required to use `to_pandas`")

    @t.overload
    @classmethod
    def from_pandas(cls, series:'pd.Series', head:'t.Literal[False]'=False): ...

    @t.overload
    @classmethod
    def from_pandas(cls, series:'pd.Index', head:'t.Literal[True]'): ...

    @classmethod
    def from_pandas(cls, series:'pd.Series | pd.Index', head:'bool'=False):
        try:
            self = cls()

            if head:
                self.extend_children([Th(inner=[Text(d)]) for d in series])

            self.extend_children([Td(inner=[Text(d)]) for d in series])

            return self
        except ImportError:
            raise ImportError("`tables` extra is required to use `from_pandas`")


    def to_list(self):
        if not self.prepared:
            self.prepare()

        return [e.data for e in self.data]

    @classmethod
    def from_list(cls, data:'list[str]', head:'bool'=False):
        self = cls()
        for value in data:
            td = Td(inner=[Text(value)]) if not head else Th(inner=[Text(value)])
            self.children.append(td)

        return self

    def prepare(self, parent = None, table=None, head:'THead|TBody|TFoot'=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        if head: self.head = head
        return super().prepare(parent, table=table, row=self, *args, **kwargs)

class Td(Symbol):
    html = "td"
    md = TdMD()
    rst = TdRST()

    children:'List[Text]' = List()
    row:'Tr' = None

    @property
    def data(self):
        return self.children.get(0, Text("")).text

    @property
    def width(self):
        return len(self.data)

    def prepare(self, parent = None, table=None, row=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.row = row

        self.row.data.append(self)
        self.header = self.table.headers[self.row.children.index(self)]
        self.table.cols[self.header].append(self)
        return super().prepare(parent, table=table, data=self, *args, **kwargs)

    def __len__(self):
        return len(self.data)

class Th(Symbol):
    html = "th"
    md = ThMD()
    rst = ThRST()

    children:'List[Text]' = List()
    row:'Tr' = None  

    def __init__(self, styles: dict[str, str] = {}, classes: list[str] = [], dom: bool = True, inner: list[Symbol] = [], **props):
        super().__init__(styles, classes, dom, inner, **props)

    @property
    def data(self):
        contents = self.children.get(0, Text("")).text
        logger.debug(f"Th data: {contents}")
        if contents == "":
            logger.debug("Th data is empty")
            return ""
        logger.debug("Th data is not empty")
        return f"**{contents}**"

    @property
    def width(self):
        """Width of the data"""
        if self.data == "":
            return 0
        return len(self.data)-4

    def prepare(self, parent = None, table=None, row=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.row = row

        self.row.data.append(self)
        self.header = self
        self.table.cols[self] = [self]
        return super().prepare(parent, table=table, data=self, *args, **kwargs)

    def __len__(self):
        """Width of the element (data + bolding)"""
        return len(self.data)