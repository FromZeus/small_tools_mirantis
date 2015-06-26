import argparse
import re
import json
from os import listdir
from os.path import join, isdir

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

re_import = re.compile("(import)+\s+\S")
re_from = re.compile("(from)+\s+\S")
re_tail = re.compile("\S$")

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      py_file_path = line["PyFilePath"]



  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

def get_pack(line):
  from_line = re_from.search(line)
  import_line = re_import.search(line)
  if from_line:


def search_py(name, path):
  for _file in listdir(path):
    if is 

def parse_py(path):
  with open(path) as py_file:
    for line in py_file:
      if "import" in line:
        if 

def build_init_dir_tree(path):
  tree = dict()
  for _file in listdir(path):
    new_path = join(path, _file)
    if isdir(_file) and "__init__.py" in listdir(new_path):
      tree[new_path].add(build_init_dir_tree(new_path))
  return tree

if __name__ == '__main__':
  main()