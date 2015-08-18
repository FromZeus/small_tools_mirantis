import lan
import require_utils
import argparse
import yaml
import json
#import pdb

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()

def main():
  pdb.set_trace()
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
      launchpad_id = line["Login"]
      launchpad_pw = line["Password"]

      project_type = line["ProjectType"]

    gerrit_account = lan.login_to_launchpad(launchpad_id, launchpad_pw)
    req_url = \
      "https://review.fuel-infra.org/#/admin/projects/?filter={0}".format(project_type)

    requested_file = lan.get_requirements_from_url(req_url, gerrit_account)

    for line in requested_file:
      print line

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user' 
    raise SystemExit

if __name__ == '__main__':
  main()
