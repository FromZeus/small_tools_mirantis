import require_utils
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
  '-rf', '--requirements', dest='req', help='Path to requirements.txt file')
parser.add_argument(
  '-sf', '--spec', dest='spec', help='Path to .spec file')
args = parser.parse_args()


def main():
  try:
    #pdb.set_trace()
    req_file = open(args.req, 'r')
    spec_file = open(args.spec, 'r')

    req_file.close()
    spec_file.close()

  except KeyboardInterrupt:
    print '\nThe process was interrupted by the user'
    raise SystemExit

if __name__ == '__main__':
  main()