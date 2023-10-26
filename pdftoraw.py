from pdfreader import SimplePDFViewer

b4_file = open("pdfs/BlackLaw4th.pdf", "rb")
b4_viewer = SimplePDFViewer(b4_file)
b4_raw_file = open("pdfs/BlacksLaw4thRaw.txt", "w", encoding="utf-8")

b4_viewer.navigate(77)  # page 77, first page of definitions
i = 0
for canvas in b4_viewer:
    if i % 25 == 0:
        print(str(i) + " pages processed.")
    page_text = canvas.text_content
    b4_raw_file.write(page_text)
    i += 1

b4_raw_file.close()
