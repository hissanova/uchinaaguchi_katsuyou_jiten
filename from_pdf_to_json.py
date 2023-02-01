import json
from pprint import pprint


import PyPDF2

chapters = [{"title": "名詞･動詞編", "range": [17, 413]},
            {"title": "形容詞編", "range": [415, 495]},
            {"title": "副詞編", "range": [497, 577]},
            ]

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

    items = []
    current_entry = ""
    current_contents = ""
    for page_text in get_pages(17, 577):
        lines = page_text.split("\n")
        # lines[1: -1] なのは、ページタイトルとページ数を除くため
        for i, line in enumerate(lines[1:-1]):
            if "〈" in line:
                if current_contents:
                    items.append({"entry": current_entry, "contents": current_contents})
                if "〉" in line:
                    closing_pos = line.index("〉") + 1
                    current_entry = line[:closing_pos]
                    current_contents = line[closing_pos:]
                else:
                    current_entry = line
                    current_contents = ""
            else:
                if "〉" in line:
                    closing_pos = line.index("〉") + 1
                    current_entry += line[:closing_pos]
                    current_contents = line[closing_pos:]
                else:
                    current_contents += line


with open("preliminary-decomposition.jsonl", 'w') as fp:
    for item in items:
        json.dump(item, fp, ensure_ascii=False)
        fp.write("\n")
