from BetterMD import H1, H2, Text, Div, LI, OL, UL, A, Strong, Table, Tr, Td, Th, Blockquote, Em, Input, CustomRst, CustomHTML, CustomMarkdown

print(H1(inner=[Text("Hi")]).to_html())
print(H1(inner=[Text("Hi")]).to_md())


print(
    Div(
        inner=[Div(
            inner=[H1(inner=[Text("Hi this is a H1")])]
        ),
        A(inner=[Text("Link")], href="https://www.google.com"),
        Div(
            inner=[
                OL(
                    inner=[
                        LI(inner=[Text("LI1")]),
                        LI(inner=[Text("LI2")]),
                        LI(inner=[Text("LI3")])
                    ]
                ),
                A(inner=[Text("Link")], href="https://www.google.com")
            ]
        ),
        UL(
            inner=[
                LI(inner=[Text("LI1")]),
                LI(inner=[Text("LI2")]),
                LI(inner=[Text("LI3")])
            ]
        )
        ]
    ).prepare(None).to_md()
)

# Bold text
print(Strong(inner=[Text("Bold text")]).prepare(None).to_md())  # **Bold text**

# Table example
print("RST",
    Table(
        inner=[
            Tr(
                inner=[
                    Th(inner=[Text("Header 1")]),
                    Th(inner=[Text("Header 2")])
                ],
                is_header=True
            ),
            Tr(
                inner=[
                    Td(inner=[Text("Cell 1")]),
                    Td(inner=[Text("Cell 2")])
                ]
            )
        ]
    ).prepare(None).to_rst(), sep="\n"
)
"""
|Header 1|Header 2|
|---|---|
|Cell 1|Cell 2|
"""

# Blockquote with formatting
print(
    Blockquote(
        inner=[
            Text("A quote with "),
            Strong(inner=[Text("bold")]),
            Text(" and "),
            Em(inner=[Text("italic")]),
            Text(" text.")
        ]
    ).prepare(None).to_md()
)
"A quote with **bold** and *italic* text."

# Text input
print(Input(type="text", placeholder="Enter your name", required=True).prepare(None).to_html())
# <input type="text" placeholder="Enter your name" required />

# Password input
print(Input(type="password", name="password", autocomplete="off").prepare(None).to_html())
# <input type="password" name="password" autocomplete="off" />

# Checkbox
print(Input(type="checkbox", name="subscribe", checked=True).prepare(None).to_html())
# <input type="checkbox" name="subscribe" checked />

# Number input
print(Input(type="number", min="0", max="100", step="5").prepare(None).to_html())
# <input type="number" min="0" max="100" step="5" />

