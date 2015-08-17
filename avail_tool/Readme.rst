======================
Availability checker
======================

Description
-----------

This utility is designed for checking if packages with 
their dependencies is in reposytories. At this moment only 
"yum".

How to use
----------

python check_avail.py -c `config.yaml`_

config.yaml
^^^^^^^^^^^

* ListPath - location of .json file with packages and 
their dependencies
* WriteMissed - if "True" then "is Missed" will be
written against unexisting packages in repos