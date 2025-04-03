# BetterMD

## Insallation

```bash
pip install better-md
```

## Usage

```python
from better_md import md

html = md.H1("Hello, world!").prepare().to_html()
md = md.H1("Hello, world!").prepare().to_md()
```