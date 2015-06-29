import argparse
import re
import json
import yaml
from os import listdir
from os.path import join, isdir, abspath
import pdb

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
re_to_last_slash = re.compile("\/*([^\/]+\/)+")
re_to_slash_from_end = re.compile("[^\s\/]+$")
#re_to_backslash_from_end = re.compile("[^\s(\\\\)]$")

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    pdb.set_trace()

    for line in tempConf:
      py_file_path = line["PyFilePath"]

    init_dir_tree = build_init_dir_tree(
      re_to_last_slash.search(py_file_path).group(0))

    print parse_py(py_file_path, init_dir_tree)

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

def get_all_imports(text):
  all_matches = []
  for match in re_all_imports.finditer(text):
    all_matches.append(match.group(0))
  return all_matches

def extract_module(from_module, imp_module, init_dir_tree):
  from_module_start = re_to_dot.search(from_module).group(0)
  from_module_end = from_module[len(module_name_start):]
  dir_modules = []
  for key, tree in init_dir_tree.iteritems():
    if from_module_start in key:
      return extract_module(from_module_end, tree)
    else:
      return from_module_start

def in_pyes(module, path):
  files = listdir(path)
  py_files = [el for el in files if el.endswith(".py")]
  if module in ",".join(py_files):
    return True
  else:
    return False

def parse_py(path, init_dir_tree):
  modules = set()
  cur_dir = re_to_last_slash.search(path).group(0)
  with open(path) as py_file:
    text = py_file.read()
    all_imports = get_all_imports(text)
    for imp in all_imports:
      from_module = re_from.search(imp)
      imp_module = re_to_dot.search(
        re_tail.search(imp).group(0)).group(0)
      if not from_module:
        if not in_pyes(imp_module, cur_dir):
          modules.add(imp_module)
        else:
          modules |= parse_py(
            "{0}/{1}.py".format(cur_dir, imp_module), init_dir_tree)
      else:
        from_module = re_tail.search(from_module.group(0)).group(0)
        modules.add(extract_module(
          from_module, imp_module, init_dir_tree))
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