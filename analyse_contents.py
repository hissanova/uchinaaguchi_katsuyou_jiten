from pprint import pprint
import json

dict_items = []
with open("./dict_items.jsonl") as tsv_fp:
    for row in tsv_fp:
        dict_items.append(json.loads(row))


for item in dict_items:
    if not item['contents'].startswith("〈"):
        pprint(item)
