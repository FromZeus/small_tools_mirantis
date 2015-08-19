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
  #pdb.set_trace()
  try:
    conf = open(args.config, 'r')
    tempConf = yaml.load_all(conf)

    for line in tempConf:
  
      launchpad_id = line["Login"]
      launchpad_pw = line["Password"]
      branch = line["Branch"]
      repo_names = line["RepoNames"]
      ignore_unknown = line["IgnoreUnknown"]
      req_urls = line["Templates"]
  
      gerrit_account = lan.login_to_launchpad(launchpad_id, launchpad_pw)
  
      with open("repos_list", "r") as input_list:
        for repo in input_list:
          for url in req_urls:
            with open(url[2], "a") as templ:
              req_url = url[0].format(repo.strip(), branch, url[1])
              try:
                requested_file = lan.get_requirements_from_url(req_url, gerrit_account)
              except:
                print req_url + " is absent!"
                continue

              if url[1] == "control":
                sec_list = ["Build-Depends-Indep:", "Build-Depends:", "Depends:", "Suggests:", "Recommends:",
"Pre-Depends:", "Conflicts:", "Provides:", "Breaks:", "Replaces:"]
                packs_list = require_utils.Require.get_packs_control(requested_file)
              elif url[1] == "spec":
                sec_list = ["Requires:"]
                packs_list = require_utils.Require.get_packs_spec(packs_request)
              else:
                print "Warning: Wrong file name!"
                raise SystemExit
  
              with open("{0}-base.json".format(url[1]), 'r') as b:
                base = json.load(b)
  
              if repo_names:
                templ.write("{0}\n----\n\n".format(repo.strip()))
              for sec in sec_list:
                for el in packs_list[sec]:
                  if (base.has_key(el)) or (ignore_unknown and el.startswith("python-")):
                    templ.write("{0}\n".format(el))
                  else:
                    print "Unknown: " + el

              templ.write("\n" * 3)

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
        raise SystemExit

main()