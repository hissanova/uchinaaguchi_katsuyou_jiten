import json
import re
from pprint import pprint


chapters = [{"title": "名詞･動詞編", "range": [17, 413]},
            {"title": "形容詞編", "range": [415, 495]},
            {"title": "副詞編", "range": [497, 577]},
            ]

items = []
with open("dict_items.jsonl", 'r') as fp:
    for line in fp:
        items.append(json.loads(line))

dictionary = []
for item in items:
    original_contents = item["contents"]
    split_point = original_contents.index("〉")
    yamato, contents = original_contents[:split_point+1], original_contents[split_point+1:]
    if len(contents) == 0:
        print(item)
    item["yamato"] = yamato
    split_contents = re.split(r"(【\w】)", contents)[1:]
    if len(split_contents) % 2 == 1:
        raise Exception(f"{split_contents}")
    for i in range(0, len(split_contents), 2):
        section_head = split_contents[i]
        if section_head == "【活】":
            key = "conjugation"
        elif section_head == "【例】":
            key = "sample_setences"
        elif section_head == "【参】":
            key = "reference"
        else:
            raise NotImplementedError
        item[key] = section_head + split_contents[i + 1]
    item.pop("contents")
    dictionary.append(item)


for dict_item in dictionary[:5]:
    pprint(dict_item)

print(all(item["yamato"].count("〈") == 1 for item in dictionary))
print(all(item["yamato"].endswith("〉") for item in dictionary))
