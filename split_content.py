from collections import Counter, defaultdict
import json
import re
# from pprint import pprint
from typing import Dict

chapters = [{"title": "名詞･動詞編", "range": [17, 413]},
            {"title": "形容詞編", "range": [415, 495]},
            {"title": "副詞編", "range": [497, 577]},
            ]


def is_in(val, interval) -> bool:
    return interval[0] <= val <= interval[1]


def add_pos(item):
    if is_in(item["page"], chapters[0]["range"]):
        if item.get("conjugation"):
            item["pos"] = "動"
        else:
            item["pos"] = "名"
    elif is_in(item["page"], chapters[1]["range"]):
        item["pos"] = "形"
    elif is_in(item["page"], chapters[2]["range"]):
        item["pos"] = "副"
    else:
        raise ValueError


items = []
with open("dict_items.jsonl", 'r') as fp:
    for line in fp:
        items.append(json.loads(line))

index_pos_stats: Dict[int, Counter] = defaultdict(Counter)
dictionary = []
prev_main_entry = items[0]
for i, item in enumerate(items):
    original_contents = item["contents"]
    # 大和口での意味、その他の内容に分割する
    split_point = original_contents.index("〉")
    yamato, contents = original_contents[:split_point+1], original_contents[split_point+1:]
    item["yamato"] = yamato
    # 見出し語の位置情報によって、親の語彙エントリーの関連語リストに登録する
    index_x_coord = item["index_x_coord"]
    index_size = item["index_size"]
    index_pos_stats[index_x_coord].update([index_size])
    if 71 <= index_x_coord <= 72 or index_x_coord == 315:
        prev_main_entry = item
    else:
        parent_related_list = prev_main_entry.get("related", [])
        parent_related_list.append({"index": item["index"],
                                    "yamato": item["yamato"],
                                    "id": i})
        prev_main_entry["related"] = parent_related_list
    # if not yamato.startswith("〈"):
    #     print(item['index'], yamato)
    # if len(contents) == 0:
    #     print(item)
    # 活用、例文、参照項に分割して、それぞれアイテムのアトリビュートとする
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
    add_pos(item)
    # 最終的な辞書に要らない項目の削除
    item.pop("contents")
    item.pop("index_x_coord")
    item.pop("index_size")
    # 辞書リストに登録
    dictionary.append(item)

with open("split_contents.jsonl", "w") as fp:
    for dict_item in dictionary:
        json.dump(dict_item, fp, ensure_ascii=False)
        fp.write("\n")

# print(all(item["yamato"].count("〈") == 1 for item in dictionary))
# print(all(item["yamato"].endswith("〉") for item in dictionary))
# pprint(index_pos_stats)
