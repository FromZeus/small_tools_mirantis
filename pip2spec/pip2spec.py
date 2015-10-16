import argparse
import require_utils
import re
import pdb
from fuzzywuzzy import fuzz
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument(
  '-f', '--file', dest='config', help='Path to requirements.txt file')
args = parser.parse_args()

after_last_dot = re.compile("\..*$")
first_in_yum_list = re.compile("^[\S]+")


def get_compare(pip_pack, rpm_pack_list):
  result = ""
  max_ratio = 0
  for el in rpm_pack_list:
    name = "{0}".format(el)
    if name.startswith("python-"):
      new_name = re.sub("python-", "", name)
      ratio = fuzz.ratio(pip_pack, new_name)
      if ratio > max_ratio:
        max_ratio = ratio
        result = name
  return (pip_pack, result)


def process_yum_list(yum_list):
  out_list = []
  for el in yum_list:
    found_first_in_yum_list = first_in_yum_list.search(el)
    if found_first_in_yum_list:
      buf_found = found_first_in_yum_list.group(0)
      clear_pack_name = re.sub(after_last_dot, "", buf_found)
      out_list.append(clear_pack_name)
  return out_list


def main():
  try:
    #pdb.set_trace()
    req_file = open(args.config, 'r')
    requirements = require_utils.Require.parse_req(req_file)
    req_file.close()
    compared = dict()

    p = subprocess.Popen(['yum', 'list'], stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)
    out, err = p.communicate()

    for el in requirements.keys():
      comp = get_compare(el, process_yum_list(out.split('\n')))
      compared[comp[0]] = comp[1]

    with open("pip-spec.json", "w+") as output_json:
      json.dump(compared, output_json, indent=4, sort_keys=True, separators=(',', ':'))

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit


if __name__ == '__main__':
  main()