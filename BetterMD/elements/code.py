from .symbol import Symbol
from .text import Text
from ..markdown import CustomMarkdown
from ..html import CustomHTML

class MD(CustomMarkdown['Code']):
    def to_md(self, inner, symbol, parent, **kwargs):
        language = symbol.get_prop("language", "")
        
        content = " ".join([e.to_md(**kwargs) for e in inner])
        
        # If it's a code block (has language or multiline)
        if language or "\n" in inner:
            return f"```{language}\n{content}\n```\n"
        
        # Inline code
        return f"`{content}`"

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent, **kwargs):
        language = symbol.get_prop("language", "")
        
        content = " ".join([e.to_html(**kwargs) for e in inner])
        
        if language:
            return f'<pre><code class="language-{language}">{content}</code></pre>'
        
        return f"<code>{content}</code>"

class Code(Symbol):
    prop_list = ["language"]
    html = HTML()
    md = MD()
    rst = "``"
    nl = True 