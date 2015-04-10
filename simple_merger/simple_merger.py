set_filter = set()

with open("input", "r") as input_file:
	for line in input_file:
		set_filter.add(line.strip())

with open("output", "w+") as output_file:
	for el in set_filter:
		output_file.write("{0}\n".format(el))