import json
from pdfreader import SimplePDFViewer

b4_file = open("pdfs/BlackLaw4th.pdf", "rb")
b4_viewer = SimplePDFViewer(b4_file)
print(b4_viewer.metadata)



# some JSON:
x =  '{ "word1":"foo", "word2":"bar", "word3":"bat"}'

# parse x:
y = json.loads(x)


f = open("words.json", "w")
f.write(x)
f.close()
