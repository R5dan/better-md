# Better-md

## Insallation

```bash
pip install better-md

# Extras

pip install better-md[tables] # For pandas support
```

## Usage

<details>
    <summary><h3>HTML</h3></summary>

```python
import BetterMD as md

html = md.H1("Hello, world!").to_html()
md = md.H1("Hello, world!")..to_md()
rst = md.H1("Hello, world!").to_rst()
```
</details>

<details>
    <summary><h3>Tables</h3></summary>

```python
import BetterMD as md

t = md.Table(
    inner=[
        md.THead(
            inner=[
                md.Tr(
                    inner=[
                        md.Th(inner=[md.Text("Header 1")], styles={"text-align":"left"}),
                        md.Th(inner=[md.Text("Header 2")], styles={"text-align":"center"}),
                        md.Th(inner=[md.Text("Header 3")], styles={"text-align":"right"}),
                        md.Th(inner=[md.Text("Header 4")])
                    ],
                ),
            ]
        ),
        md.TBody(
            inner=[
                md.Tr(
                    inner=[
                        md.Td(inner=[md.Text("Row 1 Cell 1")]),
                        md.Td(inner=[md.Text("Row 1 Cell 2")]),
                        md.Td(inner=[md.Text("Row 1 Cell 3")]),
                        md.Td(inner=[md.Text("Row 1 Cell 4")]),
                    ],
                ),
                md.Tr(
                    inner=[
                        md.Td(inner=[md.Text("Row 2 Cell 1")]),
                        md.Td(inner=[md.Text("Row 2 Cell 2")]),
                        md.Td(inner=[md.Text("Row 2 Cell 3")]),
                        md.Td(inner=[md.Text("Row 2 Cell 4")]),
                    ]
                )
            ]
        )
    ]
)

t.to_md()
t.to_rst()
t.to_html()
t.to_pandas() # Requires `tables` extra
```
</details>