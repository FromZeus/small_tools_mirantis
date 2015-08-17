import sys
import subprocess
import argparse
import pdb
import yaml
import json
import report
from treelib import Node, Tree
from email.utils import formatdate

cur_time = formatdate(timeval=None, localtime=True)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

pdb.set_trace()

def check(pkg_lst, write_missed):
  checked = dict()

  for el in pkg_lst.iteritems():
    pkg_name = el[0]
    bashCommand = "yum search {0}".format(pkg_name)
    process = subprocess.Popen(bashCommand.split(),
      stdout=subprocess.PIPE)
    result = process.communicate()[0]

    found = False if "No matches found" in result else True
    if write_missed:
      pkg_name = "{0} is Missed".format(pkg_name)
    if found or write_missed:
      checked[pkg_name] = check(el[1], write_missed)

  return checked


def generate_tree(pkgs, tree, pred):
  #rst_out_file = open("report.rst", "w")
  for el in pkgs.iteritems():
    pkg_name = el[0]
    tree.create_node(pkg_name, pkg_name, parent = pred)
    generate_tree(el[1], tree, pkg_name)

def main():
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      list_path = line["ListPath"]
      write_missed = line["WriteMissed"]

    pack_list_file = open(list_path, "r+")
    pack_list = json.load(pack_list_file)

    checked = check(pack_list, write_missed)

    tree = Tree()
    tree.create_node(cur_time, "root")
    generate_tree(checked, tree, "root")

    print "\n"
    tree.show()
    print "\n"

    #filtered = list(checked.keys())
    #sorted(filtered)

    #with open("output", "w") as out:
    #  for el in filtered:
    #    out.writeline(el)

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

if __name__ == '__main__':
  main()