import json

json1 = open("json1.json", "r")
json2 = open("json2.json", "r")

json1_data = json.load(json1)
json2_data = json.load(json2)

json1.close()
json2.close()

merged = dict(json1_data.items() + json2_data.items())

with open("merged.json", "w+") as output_json:
		json.dump(merged, output_json, indent=4, sort_keys=True, separators=(',', ':'))