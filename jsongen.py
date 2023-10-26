import json
from pdfreader import SimplePDFViewer
import re

non_alpha_regex = re.compile('[,\.!? ]')

def compare_to(str1, str2):
    str1 = non_alpha_regex.sub('', str1)
    str2 = non_alpha_regex.sub('', str2)
    for i in range(min(len(str1), len(str2))):
        diff = ord(str1[i]) - ord(str2[i])
        if diff != 0:
            return diff / (10 ** i)

    if len(str1) < len(str2):
        return -1
    if len(str1) != len(str2):
        return 1
    return 0

def acceptable_dist(str1, str2):
    if len(str1) == 0:
        return False
    if len(str2) == 0 and str1 == "A.":
        return True
    if 0 < compare_to(str1, str2) < 2:
        return True
    if ord(str1[0]) - ord(str2[0]) == 1:
        return True;
    return False;

str2 = "A. A. C. N."
str1 = "A AVER ET TENER."
print(compare_to(str1, str2))
print(acceptable_dist(str1, str2))



b4_file = open("pdfs/BlackLaw4th.pdf", "rb")
b4_viewer = SimplePDFViewer(b4_file)
b4_dict = {}
b4_raw_file = open("pdfs/BlacksLaw4thRaw.txt", "r")

b4_viewer.navigate(77) # page 77, first page of definitions

# matches any number of capital letters with optional spaces in-between with a period at the end
word_ptrn = re.compile("^\\b[A-Z .,]+[.,]{1,2}")
current_word = ""
buffer = ""
for canvas in b4_viewer:
    page_strings = canvas.strings
    page_text = canvas.text_content
    for string in page_strings:
        result = word_ptrn.match(string)
        if result:
            word = result.group(0)
            if acceptable_dist(word, current_word):
                regex = "\\n\\(" + str(word).replace('.', "\\.") + " "
                result2 = re.search(regex, page_text)
                if result2:
                    #print(buffer)
                    #print(result2.group(0))
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
