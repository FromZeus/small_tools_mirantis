import argparse
import re
import json
from os import listdir
from os.path import join, isdir, abspath

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

re_all_imports = re.compile(
  "(from\s+\S+\s+)*((\\\\)+\s*\n\s*)*(import)+\s+\S+",
    re.VERBOSE | re.MULTILINE)
re_import = re.compile("(import)+\s+\S+")
re_from = re.compile("(from)+\s+\S+")
re_tail = re.compile("\S+$")

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      py_file_path = line["PyFilePath"]



  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

def get_all_imports(text):
  all_matches = []
  for match in re_all_imports.finditer(text):
    all_matches.append(match.group(0))
  return all_matches

def search_py(name, path):
  for _file in listdir(path):
    pass

def parse_py(path):
  with open(path) as py_file:
    text = py_file.read()
    get_all_imports(text)
    for line in py_file:
      pass

def build_init_dir_tree(path):
  tree = dict()
  for _file in listdir(path):
    new_path = join(path, _file)
    if isdir(new_path) and "__init__.py" in listdir(new_path):
      if not new_path in tree:
        tree[new_path] = []
      tree[new_path].append(build_init_dir_tree(new_path))
  return tree

if __name__ == '__main__':
  main()