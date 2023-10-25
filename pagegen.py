import json

# Opening JSON file
f = open('json/words.json')
f1 = open('definitions/template_definition.html')
 
# returns JSON object as dict
data = json.load(f)
 
# Iterating through the json list
for i in data:
    f2 = open("definitions/" + str(i) + ".html", "w")
    f2.write(f1.read().format(i + " - BLD", i, data[i]))
    f2.close()
    #print(str(i) +": " + str(data[i]))
 
# Closing file
f.close()
