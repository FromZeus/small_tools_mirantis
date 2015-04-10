import re
import sys

packageName = re.compile("[a-zA-Z0-9-_.]+")

with open('input', 'r') as req:
	filtered = open('filtered_requirements', 'w+')
	for line in req:
		if line[0] != "#":
			resName = packageName.search(line)
			if resName:
				filtered.write(resName.group(0) + "\n")
	filtered.close()
