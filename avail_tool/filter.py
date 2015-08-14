import sys
import subprocess
import argparse
import pdb
import yaml
import json

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

pdb.set_trace()
def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      list_path = line["ListPath"]

    pack_list_file = open(list_path, "r+")
    pack_list = json.load(pack_list_file)

    filtered = set()

    with open(list_path, "r") as inp:
      for line in inp:
        filtered.add(line)

    sorted(filtered)
    with open("output", "w") as out:
      for el in filtered:
        bashCommand = "yum search {0}".format(el)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        result = process.communicate()[0]
        if result != "":
          out.write(el)

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

if __name__ == '__main__':
  main()