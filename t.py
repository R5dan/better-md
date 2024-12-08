from better_md import H1, H2, Text

print(H1(inner=[Text("Hi")]).to_html())