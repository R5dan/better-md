from .symbol import Symbol
from .text import Text
from ..markdown import CustomMarkdown
from ..html import CustomHTML

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        language = symbol.get_prop("language", "")
        if isinstance(inner, Text):
            inner = inner.to_md()
        
        # If it's a code block (has language or multiline)
        if language or "\n" in inner:
            return f"```{language}\n{inner}\n```\n"
        
        # Inline code
        return f"`{inner}`"

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
        language = symbol.get_prop("language", "")
        if isinstance(inner, Text):
            inner = inner.to_html()
        
        if language:
            return f'<pre><code class="language-{language}">{inner}</code></pre>'
        
        return f"<code>{inner}</code>"

class Code(Symbol):
    props = ["language"]
    html = HTML()
    md = MD()
    rst = "``"
    nl = True 