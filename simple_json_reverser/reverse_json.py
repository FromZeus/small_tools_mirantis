import json

with open("input.json", "r") as input_json:
	json_data = json.load(input_json)
	with open("reversed.json", "w+") as output_json:
		json.dump(dict([(val, key) for key, val in json_data.items()]),
			output_json, indent=4, sort_keys=True, separators=(',', ':'))