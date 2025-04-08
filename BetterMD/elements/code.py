from .symbol import Symbol
from .text import Text
from ..markdown import CustomMarkdown
from ..html import CustomHTML
from ..rst import CustomRst

class MD(CustomMarkdown):
    def to_md(self, inner, symbol, parent):
        language = symbol.get_prop("language", "")
        if isinstance(inner, Text):
            inner = inner.to_md()
        
        # If it's a code block (has language or multiline)
        if language or "\n" in inner:
            return f"\n```{language}\n{inner}\n```\n" # Cant use block as inline code isn't a block

        # Inline code
        return f"`{inner}`"

class HTML(CustomHTML):
    def to_html(self, inner, symbol, parent):
        language = symbol.get_prop("language", "")
        inner = "\n".join([i.to_html() for i in inner])
        
        if language:
            return f'<code class="language-{language}">{inner}</code>'
        
        return f"<code>{inner}</code>"
    
    def verify(self, text: str) -> bool:
        return text.lower() == "code"

class RST(CustomRst):
    def to_rst(self, inner, symbol, parent):
        language = symbol.get_prop("language", "")
        
        # Handle inner content
        if isinstance(inner, list):
            content = "".join([
                i.to_rst() if isinstance(i, Symbol) else str(i)
                for i in inner
            ])
        else:
            content = inner.to_rst() if isinstance(inner, Symbol) else str(inner)
        
        # If it's a code block (has language or multiline)
        if language or "\n" in content:
            # Use code-block directive for language-specific blocks
            if language:
                # Indent the content by 3 spaces (RST requirement)
                indented_content = "\n".join(f"   {line}" for line in content.strip().split("\n"))
                return f".. code-block:: {language}\n\n{indented_content}\n\n"
            
            # Use simple literal block for language-less blocks
            # Indent the content by 3 spaces (RST requirement)
            indented_content = "\n".join(f"   {line}" for line in content.strip().split("\n"))
            return f"::\n\n{indented_content}\n\n"
        
        # Inline code
        # Escape backticks if they exist in content
        if "`" in content:
            return f"``{content}``"
        return f"`{content}`"

class Code(Symbol):
    html = HTML()
    md = MD()
    rst = RST()