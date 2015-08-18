=====================
Fast Projects Checker
=====================

Description
-----------

This utility is designed for fast checking (by forming) dependencies of projects. This is useful when you need to check if some package is in dependencies of another.

How to use
----------

Specify `config.yaml`_ and `repos_list`_ as list of repositories, then run "python fast_check.py -c config.yaml"

Examples of lists and config are in the directory of this project.

config.yaml
^^^^^^^^^^^

* PyFilePath - location of .py file which will be processed
* StartDirPath - location of directory from which .py file will be started

Specify "config.yaml" and "repos_list" as list of repositories, then run "python fast_check.py -c config.yaml"

repos_list
^^^^^^^^^^

* Login - Your launchpad login (email)
* Password - Your password
* Branch - Branch that you want to check
* RepoNames - Print names of repositories before printing list of its dependencies
* IgnoreUnknown - Ignore unknown packages with "python-" prefix
* Templates - Templates of repos in python form (example applied).