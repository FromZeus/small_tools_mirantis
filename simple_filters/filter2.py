import sys

def main():
  try:
    filtered = set()
    with open(sys.argv[1], "r") as inp_list:
      for line in inp_list:
        filtered.add(line)
    with open("filtered_list", "w") as out_list:
      for el in inp_list:
        out_list.write(el)
  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit