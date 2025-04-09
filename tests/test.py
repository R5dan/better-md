from BetterMD import H1, H2, Text, Div, LI, OL, UL, A, B, Table, Tr, Td, Th, THead, TBody, Blockquote, I, Input, CustomRst, CustomHTML, CustomMarkdown, enable_debug_mode

# enable_debug_mode()

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
print(B(inner=[Text("Bold text")]).prepare(None).to_md())  # **Bold text**

# Table example
t=Table(
        inner=[
            THead(
                inner=[
                    Tr(
                        inner=[
                            Th(inner=[Text("Header 1")], styles={"text-align":"left"}),
                            Th(inner=[Text("Header 2 WIDER")], styles={"text-align":"center"}),
                            Th(inner=[Text("Header 3")], styles={"text-align":"right"}),
                            Th(inner=[Text("SMALL")]),
                            Th()
                        ],
                    ),
                ]
            ),
            TBody(
                inner=[
                    Tr(
                        inner=[
                            Td(inner=[Text("Row 1 Cell 1 EXTRA LONG")]),
                            Td(inner=[Text("Row 1 Cell 2")]),
                            Td(inner=[Text("Row 1 Cell 3")]),
                            Td(inner=[Text("SMALL")]),
                            Td()
                        ],
                    ),
                    Tr(
                        inner=[
                            Td(inner=[Text("Row 2 Cell 1")]),
                            Td(inner=[Text("Row 2 Cell 2")]),
                            Td(inner=[Text("Row 2 Cell 3 EXTRA LONG")]),
                            Td(inner=[Text("SMALL")]),
                            Td(inner=[Text("2")])
                        ]
                    )
                ]
            )
        ]
    ).prepare()

print(
    "\n",
    t.to_rst(),
    sep=""
)


# Blockquote with formatting
print(
    Blockquote(
        inner=[
            Text("A quote with "),
            B(inner=[Text("bold")]),
            Text(" and "),
            I(inner=[Text("italic")]),
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

