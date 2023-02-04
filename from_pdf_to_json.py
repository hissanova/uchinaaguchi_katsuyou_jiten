import json
import re
from functools import reduce
from pprint import pprint


import PyPDF2

chapters = [{"title": "名詞･動詞編", "range": [17, 413]},
            {"title": "形容詞編", "range": [415, 495]},
            {"title": "副詞編", "range": [497, 577]},
            ]

with open("./index_words.txt") as indices_file:
    indices = {}
    for row in indices_file:
        index, line = row.split("\t")
        indices[line.strip("\n")] = index



# creating a pdf file object
with open('20210312Uchinaaguchi_e.pdf', 'rb') as pdfFileObj:
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    # print(pdfReader.numPages)
    # creating a page object
    # pageObj = pdfReader.getPage(17)
    # extracting text from page
    # text = pageObj.extractText()

    def get_pages(start: int, end: int):
        pages = []
        for i in range(start, end + 1):
            pageObj = pdfReader.getPage(i)
            pages.append(pageObj.extractText())
        return pages

    def is_index_in_tail(line):
        return indices.get(line.replace("\n", ""), False)
    items = []
    current_entry = ""
    current_contents = ""
    in_definition = False
    for page_text in get_pages(17, 200):
        # print(page_text)
        lines = page_text.split("\n")
        # lines[1: -1] なのは、ページタイトルとページ数を除くため
        for i, line in enumerate(lines[1:-1]):
            index = is_index_in_tail(line)
            # print(index)
            if index:
                pattern = '(' + index + ' *〈[\w（）、]+〉? *)'
                split_contents = re.split(pattern, line)
                print(split_contents)
                tail_of_current_ctnts = split_contents.pop(0)
                next_entry = split_contents.pop(0)
                head_of_next_ctnts = split_contents.pop(0)
                if current_contents:
                    items.append({"entry": current_entry,
                                  "contents": current_contents + tail_of_current_ctnts})
                    print(items[-1])
                current_entry = next_entry
                current_contents = head_of_next_ctnts
                if len(head_of_next_ctnts) == 0:
                    in_definition = True
            else:
                if in_definition:
                    if "〉" in line:
                        closing_pos = line.index("〉") + 1
                        current_entry += line[:closing_pos]
                        current_contents = line[closing_pos:]
                        in_definition = False
                    else:
                        current_entry += line
                else:
                    current_contents += line


with open("preliminary-decomposition.jsonl", 'w') as fp:
    for item in items:
        json.dump(item, fp, ensure_ascii=False)
        fp.write("\n")
