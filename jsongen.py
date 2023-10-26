import json
from pdfreader import SimplePDFViewer
import re


def compare_to(str1, str2):
    for i in range(min(len(str1), len(str2))):
        diff = ord(str1[i]) - ord(str2[i])
        if diff != 0:
            return diff

    return len(str1) - len(str2)



b4_file = open("pdfs/BlackLaw4th.pdf", "rb")
b4_viewer = SimplePDFViewer(b4_file)
b4_dict = {}
b4_raw_file = open("pdfs/BlacksLaw4thRaw.txt", "r")

b4_viewer.navigate(77) # page 77, first page of definitions

# matches any number of capital letters with optional spaces in-between with a period at the end
word_ptrn = re.compile("^\\b[A-Z ]+[.,]{1,2}")
current_word = ""
buffer = ""
for canvas in b4_viewer:
    page_strings = canvas.strings
    page_text = canvas.text_content
    for string in page_strings:
        result = word_ptrn.match(string)
        if result:
            word = result.group(0)
            l_dist = compare_to(word[:len(word) - 1], current_word[:len(current_word) - 1])
            #print(l_dist)
            if 0 < l_dist < 2:
                regex = "\\n\\(" + str(word).replace('.', "\\.") + " "
                result2 = re.search(regex, page_text)
                if result2:
                    print(buffer)
                    print(result2.group(0))
                    print(word)
                    b4_dict[current_word] = buffer
                    buffer = ""
                    current_word = word
            #else:
                #print('nope: "' + regex + '"')
                #print(page_text)
        else:
            buffer += string + " "


b4_raw_file.close()

# parse dict as json
y = json.loads(b4_dict)


f = open("words.json", "w")
f.write(str(b4_dict))
f.close()
