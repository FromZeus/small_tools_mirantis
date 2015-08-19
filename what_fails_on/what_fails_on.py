import lan
import yaml
import argparse
#import pdb
import re
from email.utils import formatdate

cur_time = formatdate(timeval=None, localtime=True)
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

re_package_name = re.compile("[a-zA-Z0-9-_.()]+")

def check_req_err(page):
  required = set()
  err = False
  no_pack = "No Package found for"
  for line in page:
    if no_pack in line:
      idx = line.index(no_pack)
      pack_name = line[idx + len(no_pack):]
      pack_name = re_package_name.search(pack_name).group(0)
      required.add(pack_name)
    else:
      if err:
        if "Requires:" in line:
          #pack_name = re.sub("\s", "", line) 
          pack_name = re.sub("Requires:", "", line)
          pack_name = re_package_name.search(pack_name).group(0)
          required.add(pack_name)
      err = False
      if "Error: Package:" in line:
        err = True
  return required


def main():
  #pdb.set_trace()
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      launchpad_id = line["Login"]
      launchpad_pw = line["Password"]
      global_list = line["GlobalList"]
      urls = line["URLs"]

    output = open("report from {0}.rst".format(cur_time), "w")
    gerrit_account = lan.login_to_launchpad(launchpad_id, launchpad_pw)

    result = set()

    for url in urls:
      page = lan.get_requirements_from_url(url[0], gerrit_account)

      if global_list:
        result |= check_req_err(page)
      else:
        output.write("**{0}**\n".format(url[1]))
        required = check_req_err(page)
        required = sorted(required)
        for pack in required:
          output.write("{0}\n".format(pack))
        output.write("\n")

    result = sorted(result)
    for pack in result:
      output.write("{0}\n".format(pack))

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

main()