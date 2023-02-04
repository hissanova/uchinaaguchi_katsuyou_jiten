import re


import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams

path = r'./20210312Uchinaaguchi_e.pdf'

Extract_Data = []

for i, page_layout in enumerate(extract_pages(path)):
    if 17 <= i <= 577:
        # print(page_layout)
        for j, element in enumerate(page_layout):
            # print(j, element)
            if isinstance(element, LTTextContainer):
                font_sizes = []
                for text_line in element:
                    for character in text_line:
                        # print(character, end="")
                        if isinstance(character, LTChar):
                            font_sizes.append(round(character.size, 2))
                Extract_Data.append([font_sizes, element.get_text()])
    # if 18 < i:
    #     break


# print(len(Extract_Data))
indices = []
for line in Extract_Data:
    # print(len(line[0]), len(line[1]))
    # print(line[1])
    refined = re.sub('[\n\ ]', '', line[1])
    # print(len(refined), refined)
    # print(line)
    index = ""
    for size, char in zip(line[0], refined):
        if 20 > size > 10:
            index += char
    if index:
        indices.append((index, line[1]))

with open("index_words.txt", 'w') as fp:
    for index, line in indices:
        line = line.replace('\n', '')
        fp.write(f"{index}\t{line}\n")
