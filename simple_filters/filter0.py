import re
import sys

packageNameFilter = re.compile("/[a-zA-Z0-9-_.]+$")
packageName = re.compile("[a-zA-Z0-9-_.]+$")

with open('input', 'r') as req:
	filtered = open('filtered_requirements_ubuntu', 'w+')
	lib = set()
	for line in req:
		resNameFilter = packageNameFilter.search(line)
		if resNameFilter:
			resName = packageName.search(resNameFilter.group(0))
			if resName:
				name = resName.group(0)
				if name not in lib:
					lib.add(name)
					filtered.write(name + "\n")
	filtered.close()
