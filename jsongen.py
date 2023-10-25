import json


# some JSON:
x =  '{ "word1":"foo", "word2":"bar", "word3":"bat"}'

# parse x:
y = json.loads(x)


f = open("words.json", "w")
f.write(x)
f.close()
