from .markdown.custom_markdown import CustomMarkdown

class Symbol:
    styles: 'dict[str, str]' = {}
    classes: 'list[str]' = []
    inner: 'Symbol|str' = ""
    html: 'str'
    md: 'str'

    def to_html(self):
        if isinstance(self.inner, Symbol):
            inner_HTML = self.inner.to_html()
        else:
            inner_HTML = self.inner
        return f"<{self.html} classes={' '.join(self.classes)} styles={' '.join([f'{k}:{v}' for k,v in self.styles.items()])}{inner_HTML}</{self.html}>"
    
    def to_md(self):
        if isinstance(self.inner, Symbol):
            inner_md = self.inner.to_md()
        else:
            inner_md = self.inner
        if isinstance(self.md, CustomMarkdown):
            return self.md.to_md(inner_md)
        return f"{self.md} {inner_md}"