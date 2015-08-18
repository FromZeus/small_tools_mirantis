import argparse
import re
import yaml
from os import listdir
from os.path import join, isdir, abspath
#import pdb

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


def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    #pdb.set_trace()

    for line in tempConf:
      py_file_path = line["PyFilePath"]
      start_dir_path = line["StartDirPath"]
    py_file_path = abspath(py_file_path)
    start_dir_path = abspath(start_dir_path)

    init_dir_tree = build_init_dir_tree(start_dir_path)

    imports = \
      sorted(parse_py(py_file_path, start_dir_path, init_dir_tree))
    print imports
    with open("imports for {0} file".format(
        re_to_slash_from_end.search(py_file_path).group(0)), "w+") \
        as imports_file:
      for imp in imports:
        imports_file.write(imp + "\n")

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit


def get_all_imports(text):
  all_matches = []
  for match in re_all_imports.finditer(text):
    all_matches.append(match.group(0))
  return all_matches


def extract_module(from_module, imp_module, init_dir_tree, cur_dir):
  imp_module_start = re_to_dot.search(imp_module).group(0)
  imp_module_end = imp_module[len(imp_module_start) + 1:]
  if imp_module == "*":
    return ["{0}/{1}".format(cur_dir, el) \
      for el in list_only_endswith(cur_dir, ".py")]
  if from_module:
    from_module_start = re_to_dot.search(from_module).group(0)
    from_module_end = from_module[len(from_module_start) + 1:]
    for key, tree in init_dir_tree.iteritems():
      if from_module_start in key:
        return extract_module(from_module_end, imp_module, tree, key)
    if in_pyes(from_module_start, cur_dir):
      return ["{0}/{1}.py".format(cur_dir, from_module_start)]
    else:
      return from_module
  else:
    for key, tree in init_dir_tree.iteritems():
      if imp_module_start in key:
        if not imp_module_end:
          return ["{0}/{1}.py".format(cur_dir, "__init__")]
        return extract_module(from_module, imp_module_end, tree, key)
    if in_pyes(imp_module_start, cur_dir):
      return ["{0}/{1}.py".format(cur_dir, imp_module_start)]
    else:
      return imp_module


def list_only_endswith(path, ends):
  files = listdir(path)
  py_files = [el for el in files if el.endswith(ends)]
  return py_files


def in_pyes(module, path):
  py_files = list_only_endswith(path, ".py")
  if module in ",".join(py_files):
    return True
  else:
    return False


def parse_py(py_path, dir_path, init_dir_tree):
  modules = set()
  with open(py_path) as py_file:
    text = py_file.read()
    all_imports = get_all_imports(text)
    for imp in all_imports:
      from_module = re_from.search(imp)
      imp_module = re_tail.search(re_import.search(imp).group(0)).group(0)
      if from_module:
        from_module = re_tail.search(from_module.group(0)).group(0)
      else:
        from_module = ""
      extracted = extract_module(
        from_module, imp_module, init_dir_tree, dir_path)
      if isinstance(extracted, list):
        for el in extracted:
          modules |= parse_py(el, dir_path, init_dir_tree)
      else:
        modules.add(extracted)
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