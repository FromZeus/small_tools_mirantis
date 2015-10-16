#!/usr/bin/env python
# -- coding: utf-8 --
__author__ = 'michael'

import json
import re
import lan
import require_utils
from pprint import pprint


def print_funct(project_name, missed_in, missed_out):
    if len(missed_in) > len(missed_out):
        max_value = len(missed_in)
    else:
        max_value = len(missed_out)

    print '+' + '-'*41 + '+' + '-'*41 + '+'
    print '|'+'We are missed it!'+' '*24+'|'+'We are really use it?'+' '*20+'|'
    print '+' + '-'*41 + '+' + '-'*41 + '+'

    for index in xrange(0, max_value):
        try:
            min_element = missed_in[index]
        except IndexError:
            min_element = ''
        try:
            mout_element = missed_out[index]
        except IndexError:
            mout_element = ''
        print '|'+min_element+' '*(41-len(min_element))+'|'+mout_element+' '*(41-len(mout_element))+'|'

        print '+' + '-'*41 + '+' + '-'*41 + '+'

project_list = []

with open('req', 'r') as project_list_file:
    for i in project_list_file:
        project_list.append(i.strip())

ll = None
lp = None
branch = None

if ll is None:
    print "You missed your launchpad login"
if lp is None:
    print "You missed your launchpad password"
if branch is None:
    print "You must specify branch"


req_url_spec = ['https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=rpm/SPECS/{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=rpm/SPECS/python-django-{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=centos7/rpm/SPECS/{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=centos7/rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=centos7/rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}',
                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                'a=blob_plain;f=centos7/rpm/SPECS/python-django-{0}.spec;hb=refs/heads/{1}']

oslo_req_url_spec = ['https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                     'a=blob_plain;f=centos7/rpm/SPECS/python-{1}.spec;hb=refs/heads/{2}']

gerrit = lan.login_to_launchpad(ll, lp)

exceptions = ['httpd', 'mod_wsgi', 'fontawesome-fonts-web', 'openssl', 'logrotate', 'openstack-dashboard']

packageName = re.compile("[a-zA-Z0-9-_.]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.a-z-~:]+")

with open('spec-base.json', 'r') as spec_json:
    json_spec = json.load(spec_json)

for project in project_list:
    print '='*len(project)
    print project
    print '='*len(project)
    list_with_pypi_names_of_requires = []
    try:
        req_file = lan.get_requirements_from_url('https://review.fuel-infra.org/gitweb?p=openstack/{0}.git;'
                                                 'a=blob_plain;f=requirements.txt;hb=refs/heads/master'.format(project),
                                                 gerrit)
    except KeyError:
        print project + " doesn't have requirements.txt"+'\n'*3
        continue

    if project.startswith('glance'):
        project = '-'.join(project.split('_'))

    if project.startswith('oslo') and len(project) > 4:
        if '.' in project:
            osloproject = '-'.join(project.split('.'))
        else:
            osloproject = '-'.join([project[0:4], project[4::]])

        try:
            spec_file = lan.get_requirements_from_url(oslo_req_url_spec[0].format(project, osloproject, branch), gerrit)
        except KeyError:
            spec_file = lan.get_requirements_from_url(oslo_req_url_spec[0].format(project, project, branch), gerrit)

    else:
        idx = 0
        while idx < len(req_url_spec):
            try:
                spec_file = lan.get_requirements_from_url(req_url_spec[idx].format(project, branch), gerrit)
            except KeyError:
                spec_file = None
            idx += 1
            if spec_file is not None:
                break

    if spec_file is None:
        print project + " hasn't builded before"+'\n'*3
        continue

    for i in spec_file:
        strlen = 85
        if i.startswith('Requires:'):
            package_name = i.split(':')[1].strip()
            if not package_name.startswith('%{'):
                if package_name.split(' ')[0] not in exceptions:
                    try:
                        list_with_pypi_names_of_requires.append(json_spec[package_name.split(' ')[0]])
                    except KeyError as e:
                        pass
                        #print 'MISSED IN SPEC-BASE MATRIX!'
                        #print '~~~~~~~~~~~~~~~~~~~~~~~~'
                        #print e
                        #print '~~~~~~~~~~~~~~~~~~~~~~~~'


    res = []
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

    missed_in = list(set(res)-set(list_with_pypi_names_of_requires))

    missed_out = list(set(list_with_pypi_names_of_requires)-set(res))
    if missed_in == missed_out == []:
        print 'All OK with this project'
    else:
        print_funct(project, missed_in, missed_out)
    print "\n"*2
