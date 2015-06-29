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
re_to_dot = re.compile("^[^\s.]+")
re_to_backslash_from_end = re.compile("[^\s(\\\\)]$")

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      py_file_path = line["PyFilePath"]

    init_dir_tree = build_init_dir_tree(
      "{0}/..".format(py_file_path))



  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

def get_all_imports(text):
  all_matches = []
  for match in re_all_imports.finditer(text):
    all_matches.append(match.group(0))
  return all_matches

def extract_module(module_name, init_dir_tree):
  module_name_start = re_to_dot.search(module_name).group(0)
  module_name_end = module_name[len(module_name_start):]
  dir_modules = []
  for key in init_dir_tree.keys():
    dir_modules.append(
      re_to_backslash_from_end.search(key).group(0))
  if init_dir_tree in dir_modules:
    return extract_module(module_name_end, )
  else:
    return module_name_start

def parse_py(path, init_dir_tree):
  modules = set()
  with open(path) as py_file:
    text = py_file.read()
    all_imports = get_all_imports(text)
    for imp in all_imports:
      from_module = re_from(imp)
      if not from_module:
        imp_module = re_to_dot.search(
          re_tail.search(imp).group(0)).group(0)
        modules.add(imp_module)
      else:
        from_module = re_tail.search(from_module.group(0)).group(0)
        modules.add(extract_module(from_module, init_dir_tree))
  return modules

def build_init_dir_tree(path):
  tree = dict()
  for _file in listdir(path):
    new_path = join(path, _file)
    if isdir(new_path) and "__init__.py" in listdir(new_path):
      tree[new_path] = build_init_dir_tree(new_path)
  return tree

if __name__ == '__main__':
  main()