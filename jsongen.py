import json
from pdfreader import SimplePDFViewer
import re

non_alpha_regex = re.compile('[^A-Z ]')
exception_list = ['AAA.', 'A. A. C.', 'A. A. C. N.', 'A. C.,', 'A/C', 'A CANCELLIS,', 'A CANCELLIS CURIAE EXPLODI.',
                  'A CAPELLA OR A LA CAPELLA.', 'A CAUSA DE CY.', 'A. C. C.', 'AB. ABR.', 'AB AGENDO.', 'AB EPISTOLIS.', 'AB EXTRA.',
                  'AB INCONVENIENT!.', 'A DIE CONFECTIONIS.', 'AB JUDICATIO.', 'AB IRATO.']
exception_index = 0
json_file_location = "json/words.json"

def dehyphenateAndSpace(str):
    if len(str) > 1 and str[len(str) - 1] == '-':
        return str[:len(str) - 1]
    return str + ' '

def matches_exception(str1):
    if exception_index < len(exception_list):
        ex = exception_list[exception_index]
        if ex in str1 and str1.index(ex) == 0:
            return True
    return False

def compare_to(str1, str2):
    str1 = non_alpha_regex.sub('', str1)
    str2 = non_alpha_regex.sub('', str2)
    parts1 = str1.split(' ')
    parts2 = str2.split(' ')
    #print(str(parts1) + " " + str(parts2))
    pointer = 0
    for part in range(min(len(parts1), len(parts2))):
        for i in range(min(len(parts1[part]), len(parts2[part]))):
            diff = ord(parts1[part][i]) - ord(parts2[part][i])
            if diff != 0:
                out = (diff / 10.0 * 26) / (10 ** pointer)
                #print(out)
                return out
        pointer += 1

    if len(str1) < len(str2):
        return -1
    if len(str1) > len(str2):
        return 1
    return 0

def acceptable_dist(str1, str2):
    if len(str1) == 0:
        return False
    if len(str2) == 0 and str1 == "A.":
        return True
    if 0 < compare_to(str1, str2) <= 1:
        return True
    if ord(str1[0]) - ord(str2[0]) == 1:
        return True;
    return False;

def get_user_choice(prompt=": "):
    while True:
        try:
            val = input(prompt)
            if str(val) == "":
                return 0
            return int(val)
        except ValueError:
            print("Invalid input. Please try again!")

def get_int(prompt=": "):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please try again!")

def saveJSONToFile(data, file_name):
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    b4_file = open("pdfs/BlackLaw4th.pdf", "rb")
    b4_viewer = SimplePDFViewer(b4_file)
    b4_raw_file = open("pdfs/BlacksLaw4thRaw.txt", "r")
    b4_dict = json.load(open(json_file_location, 'r'))

    b4_viewer.navigate(77) # page 77, first page of definitions

    strict_word_ptrn = re.compile("(^\\b([A-Z]\\. )+)|(^\\b([A-Z]+)([A-Z ]*)\\b(\\.))")
    loose_word_ptrn = re.compile("^\\b([A-Z]+)([A-Z .]*)([.,]{1,2})")
    current_word = "A."
    exception_index = 0
    page_strings_list = []
    last_word_index = 3
    last_word_char_index = 0
    for canvas in b4_viewer:
        page_strings = canvas.strings

        #remove header & footer
        page_strings = page_strings[1:len(page_strings) - 1]

        page_strings_list.append(page_strings)
        page_text = canvas.text_content
        if len(page_strings_list) > 20:
            print("Unable to find definition after " + current_word)
            exit(1)
        for string_index in range(len(page_strings)):
            string = page_strings[string_index]
            is_word = False
            word = ""
            end_pos = 0
            if matches_exception(string):
                is_word = True
                word = exception_list[exception_index]
                end_pos = len(word)
                exception_index += 1
            else:
                strict_match = strict_word_ptrn.match(string)
                if strict_match and not strict_match.group(0)[len(strict_match.group(0)) - 2]== 'L':
                    word = strict_match.group(0)
                    end_pos = strict_match.end()
                    if acceptable_dist(word, current_word):
                        regex = "\\n\\(" + str(word).replace('.', "\\.") + " "
                        beg_of_line = re.search(regex, page_text)
                        if beg_of_line:
                            is_word = True
                else:
                    loose_match = loose_word_ptrn.match(string)
                    if loose_match and acceptable_dist(loose_match.group(0), current_word):
                        while not is_word:
                            regex = "\\n\\(" + str(string).replace('.', "\\.") + " "
                            beg_of_line = re.search(regex, page_text)
                            print(f"Current string: \"{string}\" | Is strict match: {strict_match} | Is loose match: {loose_match} | Is acceptable distance: {acceptable_dist(string, current_word)} | Is beginning of line: {beg_of_line}")
                            response = get_user_choice(prompt="Is \"" + string + "\" the next word? (enter=yes, 1=no-last string, 2=modify, 3=no-next string, 4=no-next match, 9=save&quit): ")
                            if response == 0:
                                is_word = True
                            elif response == 1:
                                string_index -= 1
                                string = page_strings[string_index]
                                continue
                            elif response == 2:
                                print(string.split(' '))
                                val = get_int("Please indicate the last section included in the word (1-indexed): ")
                                last_known_space_pos = 0
                                for i in range(val):
                                    last_known_space_pos = string.index(' ', last_known_space_pos + 1)
                                word = string[:last_known_space_pos]
                                end_pos = last_known_space_pos
                                is_word = True
                            elif response == 3:
                                string_index += 1
                                string = page_strings[string_index]
                                continue
                            elif response == 4:
                                break
                            elif response == 9:
                                saveJSONToFile(b4_dict, json_file_location)
                                quit(0)

            if is_word:
                buffer = ""
                for i in range(len(page_strings_list)):
                    if len(page_strings_list) == 1:
                        for def_index in range(last_word_index, string_index):
                            if def_index == last_word_index:
                                buffer += dehyphenateAndSpace(page_strings[def_index][len(current_word):])
                            else:
                                buffer += dehyphenateAndSpace(page_strings[def_index])
                    else:
                        if i == 0:
                            for def_index in range(last_word_index, len(page_strings_list[i])):
                                if def_index == last_word_index:
                                    buffer += dehyphenateAndSpace(page_strings_list[i][def_index][len(current_word):])
                                else:
                                    buffer += dehyphenateAndSpace(page_strings_list[i][def_index])
                        elif i < len(page_strings_list) - 1:
                            for def_index in range(len(page_strings_list[i])):
                                buffer += dehyphenateAndSpace(page_strings_list[i][def_index])
                        elif i == len(page_strings_list) - 1:
                            for def_index in range(string_index):
                                buffer += dehyphenateAndSpace(page_strings[def_index])

                b4_dict[current_word] = buffer
                last_word_index = string_index
                last_word_char_index = end_pos
                print(current_word + ": " + b4_dict[current_word])
                buffer = string[end_pos:]
                current_word = word
                page_strings_list = [page_strings_list[len(page_strings_list) - 1]]
            else:
                continue


    b4_raw_file.close()
    saveJSONToFile(b4_dict, json_file_location)
