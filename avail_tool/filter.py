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

def check(pkg_seq):
  pkg_name = pkg_seq[0] if type(pkg_seq) is tuple else pkg_seq

  bashCommand = "yum search {0}".format(pkg_name)
  process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
  result = process.communicate()[0]

  if type(pkg_seq) is tuple:
    if result:
      return [pkg_name] + check(pkg_seq[1])
    else:
      return check(pkg_seq[1])
  else:
    if result:
      return [pkg_name]

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      list_path = line["ListPath"]

    pack_list_file = open(list_path, "r+")
    pack_list = json.load(pack_list_file)

    filtered = set()

    for el in pack_list:
      result = check(el)
      if result:
        for el1 in result:
          filtered.add(el1)

    sorted(filtered)
    with open("output", "w") as out:
      for el in filtered:
        out.write(el)

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

if __name__ == '__main__':
  main()