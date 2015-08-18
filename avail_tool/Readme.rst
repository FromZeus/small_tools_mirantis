====================
Availability Checker
====================

Description
-----------

This utility is designed for checking if packages with 
their dependencies is in reposytories. At this moment only 
"yum". This tool could be used when you need to check packets in a list of repositories. Just add your repos before run script.

How to use
----------

python check_avail.py -c `config.yaml`_

config.yaml
^^^^^^^^^^^

* ListPath - Location of .json file with packages and their dependencies

* WriteMissed - If "True" then "is Missed" will be written against unexisting packages in repos