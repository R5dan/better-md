# Better-md

## Insallation

```bash
pip install better-md
```

## Usage

```python
import BetterMD as md

html = md.H1("Hello, world!").prepare().to_html()
md = md.H1("Hello, world!").prepare().to_md()
rst = md.H1("Hello, world!").prepare().to_rst()
```