from better_md import H1, H2, Text, Div, LI, OL, UL

print(H1(inner=[Text("Hi")]).to_html())
print(H1(inner=[Text("Hi")]).to_md())


print(
    Div(
        inner=[Div(
            inner=[H1(inner=[Text("Hi this is a H1")])]
        ),
        Div(
            inner=[
                OL(
                    inner=[
                        LI(inner=[Text("LI1")]),
                        LI(inner=[Text("LI2")]),
                        LI(inner=[Text("LI3")])
                    ]
                )
            ]
        )
        ]
    ).prepare(None).to_md()
)