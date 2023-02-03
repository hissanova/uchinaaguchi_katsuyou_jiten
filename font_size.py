import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams

path = r'./20210312Uchinaaguchi_e.pdf'

Extract_Data = []

for page_layout in extract_pages(path):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            font_sizes = []
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):
                        font_sizes.append(character.size)
                        Extract_Data.append([font_sizes, element.get_text()])
