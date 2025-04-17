from .symbol import Symbol
from ..utils import List
from ..markdown import CustomMarkdown
from ..rst import CustomRst
from .text import Text
import logging
import typing as t
import itertools as it

if t.TYPE_CHECKING:
    # Wont be imported at runtime
    import pandas as pd # If not installed, will not affect anything at runtime


logger = logging.getLogger("BetterMD")
T = t.TypeVar("T")

class TableMD(CustomMarkdown['Table']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        logger.debug("Converting Table element to Markdown")
        head = symbol.head.to_md() if symbol.head else None
        body = symbol.body.to_md() if symbol.body else None
        foot = symbol.foot.to_md() if symbol.foot else None

        logger.debug(f"Table conversion complete. Has header: {head is not None}")
        return f"{f"{head}\n" if head else ""}{f"{body}\n" if body else ""}{f"{foot}\n" if foot else ""}"

class THeadMD(CustomMarkdown['THead']):
    def to_md(self, inner, symbol, parent, experiments=None, **kwargs):

        if experiments is None:
            experiments = {}

        multi_head = experiments.get("multiheader", False)

        logger.debug("Converting THead element to RST")
        logger.debug(f"THead has {len(inner)} children: {[e.to_rst() for e in inner]}")

        if not multi_head and len(symbol.data) > 1:
            raise ValueError("THead with multiple rows is not supported when `experiments.multiheader` is `False` as it is not standard markdown")

        rows = [
            [
                e.to_md().replace("\n", "<br />") for e in row.data
            ] for row in symbol.data
        ]

        def op_get(list:'list', i:'int', d):
            try:
                return list[i]
            except:
                return d

        def handle_col(row:'list[list[str]]', i, w:'int') -> 'str':
            col:'list[str]' = []

            for r in row:
                col.append(op_get(r, i, "").center(w))
            ret = "<hr />".join([e for e in col])
            return ret

        widths = symbol.table.widths

        left  = [True if c.styles.get("text-align", "justify") in ["center", "left"] else False for c in symbol.table.cols.keys()]
        right = [True if c.styles.get("text-align", "justify") in ["center", "right"] else False for c in symbol.table.cols.keys()]

        medium = f"| {" | ".join([f"{":" if l else "-"}{'-'*(w-2)}{":" if r else "-"}" for l,r,w in zip(left, right, widths)])} |"

        return f"| {" | ".join([handle_col(rows, i, w) for i, w in zip(range(len(max(rows, key=len, default=""))), widths)])} |\n{medium}"  

class TBodyMD(CustomMarkdown['TBody']):
    def to_md(self, inner, symbol, parent, pretty=True, **kwargs):
        content = [e.to_md() for e in symbol.data]
        logger.debug(f"TBody content: {content}")
        return "\n".join(content)

class TrMD(CustomMarkdown['Tr']):
    def to_md(self, inner, symbol, parent, **kwargs):
        return f"| {" |\n| ".join(" | ".join([e.to_md().center(w) for e, w in zip(symbol.data, symbol.table.widths)]).split("\n"))} |"

class TdMD(CustomMarkdown['Td']):
    def to_md(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_md() for e in inner])
        width = len(max(symbol.table.cols[symbol.header], key=len).data)
        return content.center(width)
class ThMD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        contents = " ".join([e.to_md() for e in inner])

        if contents.strip() == "":
            return ""

        return f"**{contents}**"
class TableRST(CustomRst['Table']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        logger.debug("Converting Table element to RST")
        head = symbol.head.to_rst() if symbol.head is not None else None
        body = symbol.body.to_rst() if symbol.body is not None else None
        foot = symbol.foot.to_rst() if symbol.foot is not None else None
        return f"{f"{head}\n" if head else ""}{f"{body}\n" if body else ""}{f"{foot}\n" if foot else ""}"

class THeadRST(CustomRst['THead']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        logger.debug("Converting THead element to RST")
        logger.debug(f"THead has {len(inner)} children: {[e.to_rst() for e in inner]}")
    
        rows = [
            [
                e.to_rst().splitlines() for e in row.data
            ] for row in symbol.data
        ]

        def op_get(list:'list', i:'int', d):
            try:
                return list[i]
            except:
                return d

        def handle_row(row:'list[list[str]]', l) -> 'str':
            h = len(max(row, key=len))

            thead = []
            for i in range(h):
                thead.append("| " + " | ".join([op_get(d, i, "").center(w) for w, d in zip(l, row)]) + " |")

            ret = "\n".join(thead)
            return ret
        
        widths = symbol.table.widths

        medium = f"+{"+".join(['-'*(width+2) for width in widths])}+"
        b_medium = f"+{"+".join(['='*(width+2) for width in widths])}+"

        return f"{medium}\n{f"\n{medium}\n".join([handle_row(row, widths) for row in rows])}\n{b_medium}"  

class TBodyRST(CustomRst['TBody']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        rows = [
            [
                e.to_rst().splitlines() for e in row.data
            ] for row in symbol.data
        ]

        def op_get(list:'list', i:'int', d):
            try:
                return list[i]
            except:
                return d

        def handle_row(row:'list[list[str]]', l) -> 'str':
            h = len(max(row, key=len))

            thead = []
            for i in range(h):
                thead.append("| " + " | ".join([op_get(d, i, "").center(w) for w, d in zip(l, row)]) + " |")

            ret = "\n".join(thead)
            return ret
        
        widths = symbol.table.widths

        medium = f"+{"+".join(['-'*(l+2) for l in widths])}+"

        return f"{f"\n{medium}\n".join([handle_row(row, widths) for row in rows])}\n{medium}"  

class TrRST(CustomRst['Tr']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        return f'| {" |\n| ".join(" | ".join([e.to_rst() for e in inner]).split("\n"))} |'


class TdRST(CustomRst['Td']):
    def to_rst(self, inner, symbol, parent, **kwargs):
        content = " ".join([e.to_rst() for e in inner])
        width = len(max(symbol.table.cols[symbol.header], key=len).data)
        return content.center(width)

class ThRST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        contents = " ".join([e.to_rst() for e in inner])

        if contents.strip() == "":
            return ""

        return f"**{contents}**"

class Table(Symbol):
    # All deprecated
    prop_list = ["align", "bgcolor", "border", "cellpadding", "cellspacing", "frame", "rules", "summary", "width"]

    html = "table"
    md = TableMD()
    rst = TableRST()
    def __init__(self, styles: dict[str, str] = None, classes: list[str] = None, inner: list[Symbol] = None, **props: str | bool | int | float | list | dict):
        self.head:'THead' = None
        self.body:'TBody' = None
        self.foot:'TFoot' = None

        self.widths = []
        self.cols: 'dict[Th, list[Td | HeadlessTd]]' = {}
        self.headers: 'list[Th]' = []


        super().__init__(styles, classes, inner, **props)

    def prepare(self, parent:'Symbol'=None, dom:'list[Symbol]' = None, *args, **kwargs):
        if dom is None:
            dom = []
        dom.append(self)

        self.prepared = True
        self.parent = parent
        for symbol in self.children:
            symbol.prepare(self, *args, **kwargs, dom.copy(), table=self)

        return self

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

class THead(Symbol):
    html = "thead"
    rst = THeadRST()
    md = THeadMD()



    def __init__(self, styles: dict[str, str] = None, classes: list[str] = None, inner: list[Symbol] = None, **props: str | bool | int | float | list | dict):
        self.table:'Table' = None
        self.data:'list[Tr]' = []
        super().__init__(styles, classes, inner, **props)

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

    def prepare(self, parent = None, dom=None, table=None, *args, **kwargs):
        assert isinstance(table, Table), table
        print("THEAD")
        self.table = table
        self.table.head = self

        if dom is None:
            dom = []
        dom.append(self)

        self.prepared = True
        self.parent = parent
        for symbol in self.children:
            print("THEAD", symbol)
            symbol.prepare(self, dom.copy(), table=table, head=self, *args, **kwargs)

        return self

class TBody(Symbol):
    html = "tbody"
    rst = TBodyRST()
    md = TBodyMD()

    table:'Table' = None
    data :'list[Tr]' = []

    def to_rst(self) -> 'str':
        if isinstance(self.rst, CustomRst):
            return self.rst.to_rst(self.children, self, self.parent)

        inner_rst = " ".join([e.to_rst() for e in self.children])
        return f"{self.rst}{inner_rst}{self.rst}\n"

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

    def prepare(self, parent = None, dom=None, table=None, *args, **kwargs):
        print("TBODY")
        assert isinstance(table, Table)

        self.table = table
        self.table.body = self
        return super().prepare(parent, dom, table=table, head=self, *args, **kwargs)

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

    def prepare(self, parent = None, dom=None, table=None, *args, **kwargs):
        print("TFOOT")
        assert isinstance(table, Table)

        self.table = table
        self.table.foot = self
        return super().prepare(parent, dom, table=table, head=self, *args, **kwargs)

class Tr(Symbol):
    html = "tr"
    md = TrMD()
    rst = TrRST()

    head:'THead|TBody|TFoot' = None
    table:'Table' = None
    data:'list[t.Union[Td, Th]]' = None

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

    def prepare(self, parent = None, dom=None, table=None, head:'THead|TBody|TFoot'=None, *args, **kwargs):
        print(f"TR {parent} {self.children} {self.data}")
        assert isinstance(table, Table)
        assert isinstance(head, (THead, TBody, TFoot))
        self.data = []
        self.table = table
        self.head = head
        self.head.data.append(self)
        ret = super().prepare(parent, dom, table=table, row=self, head=head, *args, **kwargs)

        self.table.widths = [max(len(max(col.data.splitlines(), key=len, default="")), width, 3) for col, width in it.zip_longest(self.data, self.table.widths,  fillvalue=0)]

        return ret

    def __str__(self):
        return f"<tr />"

    def __repr__(self):
        return f"<tr />"

class Td(Symbol):
    prop_list = ["colspan", "rowspan", "headers"]
    # Deprecated
    prop_list +=  ["abbr", "align", "axis", "bgcolor", "char", "charoff", "height", "scope", "valign", "width"]

    html = "td"
    md = TdMD()
    rst = TdRST()

    def __init__(self, styles: dict[str, str] = None, classes: list[str] = None, inner: list[Symbol] = None, **props: str | bool | int | float | list | dict):
        super().__init__(styles, classes, inner, **props)
        self.row:'Tr' = None

    @property
    def data(self):
        return self.children.get(0, Text("")).text

    @property
    def width(self):
        return len(self.data)

    def prepare(self, parent = None, dom=None, table=None, row=None, *args, **kwargs):
        assert isinstance(table, Table)
        self.table = table
        self.row = row

        self.row.data.append(self)
        print(self.table.headers)

        def op_get(list:'list', i:'int', d):
            try:
                return list[i]
            except:
                return d

        self.header = op_get(self.table.headers, len(self.row.data) - 1, HeadlessTd())
        if isinstance(self.header, HeadlessTd):
            self.table.cols[self.header] = [self]
        else:
            self.table.cols[self.header].append(self)
        return super().prepare(parent, dom, table=table, data=self, *args, **kwargs)

    def __len__(self):
        return len(self.data)

class HeadlessTd: ...

class Th(Symbol):
    prop_list = ["abbr", "colspan","headers", "rowspan", "scope"]
    # Deprecated
    prop_list +=  ["align", "axis", "bgcolor", "char", "charoff", "height", "valign", "width"]


    html = "th"
    md = ThMD()
    rst = ThRST()

    row:'Tr' = None  

    def __init__(self, styles: dict[str, str] = {}, classes: list[str] = [], inner: list[Symbol] = [], **props):
        super().__init__(styles, classes, inner, **props)

    @property
    def data(self):
        contents = self.children.get(0, Text("")).text
        logger.debug(f"Th data: {contents}")
        if not contents:
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

    def prepare(self, parent = None, dom=None, table=None, row=None, *args, **kwargs):
        print("TH PREPARED")
        assert isinstance(table, Table)
        self.table = table
        self.row = row

        self.row.data.append(self)
        self.header = self
        self.table.cols[self] = []
        self.table.headers.append(self)
        print("TH")
        return super().prepare(parent, dom, table=table, data=self, *args, **kwargs)

    def __len__(self):
        """Width of the element (data + bolding)"""
        return len(self.data)
