import json

words_json = open('json/words.json', 'r')
words = json.load(words_json)
words_json.close()

template_definition = open('definitions/template_definition.html', 'r')
template_definition_text = template_definition.read()
template_definition.close()

template_index = open('template_index.html', 'r')
template_index_text = template_index.read()
template_index.close()

index = open('index.html', 'w')
write_files = [index]

link_refs: str = ""

for word in words:
    definition = str(words[word])
    word = str(word)
    page_title = word + " - BLD"
    this_word = open("definitions/" + word + ".html", "w")

    # Create definition page based off of template_definition.html
    this_word.write(template_definition_text.format(page_title, word, definition))
    this_word.close()

    link_refs += "<h1><a class=\"definition\" href=\"definitions/" + word + ".html\">" + word + "</a></h1>\n"

# Add word definition links to index.html based off of template_index.html
index.write(template_index_text.format(link_refs.strip()))

for file in write_files:
    file.close()