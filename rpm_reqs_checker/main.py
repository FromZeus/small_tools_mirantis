__author__ = 'michael'

import json
import require_utils
import re

packageName = re.compile("[a-zA-Z0-9-_.]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.a-z-~:]+")

list_with_pypi_names_of_requires = []
with open('spec-base.json', 'r') as spec_json:
    json_spec = json.load(spec_json)

with open('murano.spec', 'r') as spec_file:
    for i in spec_file:
        if i.startswith('Requires:'):
            package_name = i.split(':')[1].strip()
            if not package_name.startswith('%{'):
                #pass
                list_with_pypi_names_of_requires.append(json_spec[package_name.split(' ')[0]])


with open('requirements.txt', 'r') as req_file:
    res = [] # dict()
    for i in req_file:
        line = i.strip()
        if line == '' or line[0] == '#':
                continue
        resName = packageName.search(line)
        resEq = packageEq.findall(line)
        it = next(re.finditer('>=|<=|>|<|==|!=', line), None)
        if it:
            resVers = packageVers.findall(line[it.start():])
        if resName:
            name = resName.group(0)
            res.append(name)


print list(set(res)-set(list_with_pypi_names_of_requires))
