====================
pip2spec
====================

Description
-----------

This utility is designed for comparing pip based dependencies against spec based packages names. You can add more repositories to /etc/yum.repos.d/ if you need in wider search for packages names.

How to use
----------

python pip2spec.py -f `requirements.txt`_

requirements.txt
^^^^^^^^^^^^^^^^

This is path to any file with pip-like dependencies.