import json
import re
from pprint import pprint


chapters = [{"title": "名詞･動詞編", "range": [17, 413]},
            {"title": "形容詞編", "range": [415, 495]},
            {"title": "副詞編", "range": [497, 577]},
            ]

items = []
with open("preliminary-decomposition.jsonl", 'r') as fp:
    for line in fp:
        items.append(json.loads(line))

# print(all(item["entry"].endswith("〉") for item in items))
dictionary = []
for item in items:
    dict_item = {}
    entry = item["entry"]
    print(entry)
    split_point = entry.index("〈")
    okinawago, yamato = entry[:split_point], entry[split_point:]
    dict_item["okinawan"] = okinawago
    dict_item["japanese"] = yamato
    contents = item["contents"]
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
        dict_item[key] = section_head + split_contents[i + 1]
    dictionary.append(dict_item)


for dict_item in dictionary[:5]:
    pprint(dict_item)
