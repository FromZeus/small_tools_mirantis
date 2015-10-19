#!/usr/bin/env python
# -- coding: utf-8 --

__author__ = 'mivanov'

import getpass
import glob
import json
import lan
import os
import re
import readline


req_url_spec = ['https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=rpm/SPECS/{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=rpm/SPECS/python-django-{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=centos7/rpm/SPECS/{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=centos7/rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=centos7/rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}',

                'https://review.fuel-infra.org/gitweb?'
                'p=openstack-build/{0}-build.git;a=blob_plain;'
                'f=centos7/rpm/SPECS/python-django-{0}.spec;hb=refs/heads/{1}']

oslo_req_url_spec = ['https://review.fuel-infra.org/gitweb?'
                     'p=openstack-build/{0}-build.git;a=blob_plain;'
                     'f=rpm/SPECS/python-{1}.spec;hb=refs/heads/{2}',

                     'https://review.fuel-infra.org/gitweb?'
                     'p=openstack-build/{0}-build.git;a=blob_plain;'
                     'f=centos7/rpm/SPECS/python-{1}.spec;hb=refs/heads/{2}']

exceptions = ['httpd',
              'mod_wsgi',
              'fontawesome-fonts-web',
              'openssl',
              'logrotate',
              'openstack-dashboard']

packageName = re.compile("[a-zA-Z0-9-_.]+")


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


def printer(missed_in, missed_out):
    if len(missed_in) > len(missed_out):
        max_value = len(missed_in)
    else:
        max_value = len(missed_out)

    print '+' + '-'*41 + '+' + '-'*41 + '+'
    print '|' + 'We are missed it!' + ' '*24 +\
          '|' + 'We are really use it?' + ' '*20 + '|'
    print '+' + '-'*41 + '+' + '-'*41 + '+'

    for index in xrange(0, max_value):
        try:
            missed_in_element = missed_in[index]
        except IndexError:
            missed_in_element = ''

        try:
            missed_out_element = missed_out[index]
        except IndexError:
            missed_out_element = ''

        print '|' + missed_in_element + ' '*(41-len(missed_in_element)) + \
              '|' + missed_out_element + ' '*(41-len(missed_out_element)) + '|'

        print '+' + '-'*41 + '+' + '-'*41 + '+'


def forming_project_list(filename):

    project_list_array = []

    with open(filename, 'r') as project_list_file:
        for line_with_project_name in project_list_file:
            project_list_array.append(line_with_project_name.strip())

    return project_list_array


def main():
    branch_name = ''

    launchpad_login = raw_input('Enter your launchpad login: ')
    launchpad_password = getpass.getpass('Enter your launchpad password: ')

    gerrit = lan.login_to_launchpad(launchpad_login, launchpad_password)

    while branch_name.lower() not in ['master', '8.0', '7.0', '6.1', '6.0.1']:
                branch_name = raw_input(
                    'At the what branch we should check requirements? ')

                if branch_name == 'master':
                    branch = 'master'

                elif branch_name == '8.0':
                    branch = 'openstack-ci/fuel-8.0/liberty'

                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-7.0/2015.1.0'

                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-6.1/2014.2'

                elif branch_name == '6.0.1':
                    branch = 'openstack-ci/fuel-6.0.1/2014.2'

    file_name = os.path.abspath(raw_input('Specify the name of files with projects: '))

    with open('spec-base.json', 'r') as spec_json:
        json_spec = json.load(spec_json)

    project_list = forming_project_list(file_name)

    for project in project_list:

        print '='*len(project)
        print project
        print '='*len(project)
        list_with_pypi_names_of_requires = []

        try:
            req_file = lan.get_requirements_from_url(
                'https://review.fuel-infra.org/gitweb?p=openstack/{0}.git;'
                'a=blob_plain;f=requirements.txt;'
                'hb=refs/heads/{1}'.format(project, branch), gerrit)

        except KeyError:
            print project + " doesn't have requirements.txt"+'\n'*3
            continue

        if project.startswith('glance'):
            project = '-'.join(project.split('_'))

        if project.startswith('oslo') and len(project) > 4:
            if '.' in project:
                oslo_project = '-'.join(project.split('.'))
            else:
                oslo_project = '-'.join([project[0:4], project[4::]])

            try:
                spec_file = lan.get_requirements_from_url(
                    oslo_req_url_spec[0].format(
                        project, oslo_project, branch), gerrit)

            except KeyError:
                spec_file = lan.get_requirements_from_url(
                    oslo_req_url_spec[0].format(project, project, branch),
                    gerrit)

        else:
            idx = 0
            while idx < len(req_url_spec):
                try:
                    spec_file = lan.get_requirements_from_url(
                        req_url_spec[idx].format(project, branch), gerrit)
                except KeyError:
                    spec_file = None
                idx += 1
                if spec_file is not None:
                    break

        if spec_file is None:
            print project + " hasn't builded before"+'\n'*3
            continue

        for i in spec_file:
            if i.startswith('Requires:'):
                package_name = i.split(':')[1].strip()
                if not package_name.startswith('%{'):
                    if package_name.split(' ')[0] not in exceptions:
                        try:
                            list_with_pypi_names_of_requires.append(
                                json_spec[package_name.split(' ')[0]])
                        except KeyError as e:
                            pass
                            # print 'MISSED IN SPEC-BASE MATRIX!'
                            # print '~~~~~~~~~~~~~~~~~~~~~~~~'
                            # print e
                            # print '~~~~~~~~~~~~~~~~~~~~~~~~'

        result = []
        for i in req_file:
            line = i.strip()
            if line == '' or line[0] == '#':
                    continue
            res_name = packageName.search(line)
            if res_name:
                name = res_name.group(0)
                result.append(name)

        spec_missed_in = list(set(result)
                              - set(list_with_pypi_names_of_requires))
        spec_missed_out = list(set(list_with_pypi_names_of_requires)
                               - set(result))

        if spec_missed_in == spec_missed_out == []:
            print 'All OK with this project'
        else:
            printer(spec_missed_in, spec_missed_out)
        print "\n"*2


if __name__ == "__main__":
    try:
        main()
    except IOError as e:
        print e
    #    print 'Sorry, no such file or directory!'
    except KeyboardInterrupt:
        print '\n' + 'Interrupted by user'
