import requests
import json
import re
from StringIO import StringIO
import base64
import yaml
import argparse

re_spec = re.compile("[a-zA-Z0-9-_]+\.spec")
re_epoch = re.compile("\d+")


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()


def get_spec_name(url):
  page = requests.get(url, stream = True)
  for line in page.text.split('\n'):
    spec = re_spec.search(line)
    if spec:
      return spec.group(0)
  return None


def main():
  try:
    username = password = ""
    
    if args.config:
      conf = open(args.config, 'r')
      tempConf = yaml.load_all(conf)

      for line in tempConf:
        username = line["Username"]
        password = line["Password"]

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    if username and password:
      headers["Authorization"] = "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password))

    repos_trash = \
      requests.get("https://api.github.com/orgs/openstack-packages/repos?per_page=9999",
        stream = True, headers = headers)
    repos_info_list = json.loads(repos_trash.text)
  
    for el in repos_info_list:
      buf_repos_info = json.dumps(el)
      repos_info = json.loads(buf_repos_info)
      if repos_info["default_branch"] == "rpm-master":
        spec_name = get_spec_name("https://github.com/openstack-packages/{0}".format(repos_info["name"]))
        for line in requests.get(
          "https://raw.githubusercontent.com/openstack-packages" \
          "/{0}/rpm-master/{1}".format(repos_info["name"], spec_name), stream = True).text.split('\n'):
          if "Epoch:" in line:
            epoch = re_epoch.search(line)
            if epoch:
              print "{0} : {1}".format(repos_info["name"], epoch.group(0))
  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit


if __name__ == '__main__':
  main()
