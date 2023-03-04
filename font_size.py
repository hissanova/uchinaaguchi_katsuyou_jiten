from itertools import islice
from collections import Counter
from csv import DictWriter

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

path = r'./20210312Uchinaaguchi_e.pdf'
page_start = 17
page_end = 577

output_path = "extracted_text.tsv"

with open(output_path, 'w') as fp:
    tsv_writer = DictWriter(fp, ["Page", "Head_Coord", "Height", "Text"], delimiter="\t")
    tsv_writer.writeheader()
    h_coord_counter = Counter()
    height_counter = Counter()
    mid_pos = []
    right_outliers = []
    for page_num, page_layout in enumerate(islice(extract_pages(path),
                                        page_start,
                                        page_end), page_start):
        left_col = []
        right_col = []
        for h_box in islice(page_layout, 1, None):
            if isinstance(h_box, LTTextContainer):
                head_x_coord = round(h_box.x0)
                height = round(h_box.height, 1)
                line = {"Page": page_num,
                        "Head_Coord": head_x_coord,
                        "Height": height,
                        "Text": h_box.get_text().replace("\n", "")}
                h_coord_counter.update([head_x_coord])
                height_counter.update([height])
                if head_x_coord < 100:
                    left_col.append(line)
                elif 280 < head_x_coord < 300:
                    mid_pos.append(line)
                else:
                    if 400 < head_x_coord and page_num != 433:
                        right_outliers.append(line)
                    else:
                        right_col.append(line)
        for line in left_col + right_col:
            tsv_writer.writerow(line)
print(sorted(h_coord_counter.items()))
print(sorted(height_counter.items()))
# print(all(l["Text"].strip("\n").isdigit() for l in mid_pos))
for entry in right_outliers:
    print(entry)
