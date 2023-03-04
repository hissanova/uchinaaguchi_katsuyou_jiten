from itertools import islice
from collections import Counter

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextContainer, LTChar, LTLine

path = r'./20210312Uchinaaguchi_e.pdf'
page_start = 17
page_end = 577

h_coord_counter = Counter()
height_counter = Counter()
for page_layout in islice(extract_pages(path), 17, 577):
    left_col = []
    right_col = []
    for h_box in islice(page_layout, 1, None):
        # print(h_box)
        # print(h_box.x0, h_box.x1 - h_box.x0, h_box.y1 - h_box.y0)
        if isinstance(h_box, LTTextContainer):
            head_x_coord = round(h_box.x0)
            height = round(h_box.height, 1)
            line = (head_x_coord, height, h_box.get_text())
            h_coord_counter.update([head_x_coord])
            height_counter.update([height])
            if head_x_coord < 100:
                left_col.append(line)
            else:
                right_col.append(line)
    # for line in left_col + right_col:
    #     print(line)

print(sorted(h_coord_counter.items()))
print(sorted(height_counter.items()))
