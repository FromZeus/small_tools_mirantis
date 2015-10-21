import require_utils
import argparse
import re
#import pdb
import json
import yaml
import sys


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


parser = argparse.ArgumentParser()
parser.add_argument(
  '-rf', '--requirements', dest='req', help='Path to requirements.txt file')
parser.add_argument(
  '-sf', '--spec', dest='spec', help='Path to .spec file')
parser.add_argument(
  '-ps', '--pipspec', dest='pipspec', help='Path to pip-spec.json file')
parser.add_argument(
  '-sp', '--specpip', dest='specpip', help='Path to spec-pip.json file')
parser.add_argument(
  '-c', '--config', dest='config', help='Configuration YAML')
parser.add_argument(
  '-m', '--missed', dest='missed', help='Show missed requirements (True|False)')
parser.add_argument(
  '-e', '--extra', dest='extra', help='Show extra requirements (True|False)')
parser.add_argument(
  '-cb','--cutbounds', dest='cutbounds', nargs='+', help='Update without this bounds')
args = parser.parse_args()


pipspec = specpip = project_reqs = spec_reqs = {}


def update_line(packs, used, space):
  new_lines = []
  for pack_name in packs.keys():
    if specpip.has_key(pack_name):
      pip_name = specpip[pack_name]
      if pack_name not in used and project_reqs.has_key(pip_name):
        new_lines.append(convert_to_spec(pip_name, project_reqs[pip_name], space))
        used.add(pack_name)
  return new_lines


def convert_to_spec(pip_name, pip_bounds, space):
  result_require = "Requires:{0}".format(space)
  spec_name = pipspec[pip_name]
  for el in pip_bounds:
    if el[0] == "!=":
      result_require += "{0} < {1}, ".format(spec_name, el[1])
      result_require += "{0} > {1}, ".format(spec_name, el[1])
    else:
      result_require += "{0} {1} {2}, ".format(spec_name, el[0], el[1])
  result_require = "{0}\n".format(result_require[:-2])
  return result_require


def show_missed_packs():
  trans_reqs = set()
  for el in project_reqs.keys():
    if pipspec.has_key(el):
      trans_reqs.add(pipspec[el])
  diff = sorted(list(trans_reqs - set(spec_reqs.keys())))
  return diff


def show_extra_packs():
  trans_reqs = set()
  for el in project_reqs.keys():
    if pipspec.has_key(el):
      trans_reqs.add(pipspec[el])
  diff = sorted(list(set(spec_reqs.keys()) - trans_reqs))
  return diff


def filter_bounds(cut_bounds):
  global project_reqs
  for pack_name, bounds in project_reqs.iteritems():
    new_bounds = {el for el in bounds
      if el[0] not in cut_bounds}
    project_reqs[pack_name] = new_bounds


def main():
  try:
    #pdb.set_trace()

    if len(sys.argv) == 1:
      raise ValueError("Epmty argument list")

    if args.config:
      conf_file = open(args.config, 'r')
      config = yaml.load_all(conf_file)

      for line in config:
        req_file_path = args.req if args.req else line["Requirements"]
        spec_file_path = args.spec if args.spec else line["Spec"]
        pipspec_file_path = args.pipspec if args.pipspec else line["PipSpec"]
        specpip_file_path = args.specpip if args.specpip else line["SpecPip"] 
        show_missed = args.missed if args.missed else line["Missed"]
        show_extra = args.extra if args.extra else line["Extra"]
        cut_bounds = args.cutbounds if args.cutbounds else line["CutBounds"]


    pipspec_file = open(pipspec_file_path, 'r')
    specpip_file = open(specpip_file_path, 'r')
    req_file = open(req_file_path, 'r')
    spec_file = open(spec_file_path, 'r+')
    
    global pipspec
    pipspec = json.load(pipspec_file)
    pipspec_file.close()

    global specpip
    specpip = json.load(specpip_file)
    specpip_file.close()
    
    global project_reqs
    project_reqs = require_utils.Require.parse_req(req_file)
    req_file.close()
    filter_bounds(cut_bounds)
    if show_missed or show_extra:
      global spec_reqs
      spec_reqs = require_utils.Require.parse_requires_spec(spec_file)
      if show_extra:
        print color.BOLD + color.YELLOW + "\nExtra packages:" + color.END
        for el in show_extra_packs():
          print el
      if show_missed:
        print color.BOLD + color.RED + "\nMissed packages" + color.END
        for el in show_missed_packs():
          print el
        

    used = set()

    spec_file.seek(0)
    data = spec_file.readlines()
    spec_file.seek(0)

    for idx, line in enumerate(data):
      if "%package" in line:
        used = {}
      if line.startswith("Requires:"):

        space = re.search("\s+", line[9:])
        if space:
          space = space.group(0)
        else:
          space = ""

        packs = require_utils.Require.parse_line_spec(line[9:])
        new_lines = update_line(packs, used, space)
        if len(new_lines) > 0:
          del data[idx]
          for el in new_lines:
            data.insert(idx, el)
    
    spec_file.writelines(data)
    spec_file.truncate()

    spec_file.close()

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

if __name__ == '__main__':
  main()