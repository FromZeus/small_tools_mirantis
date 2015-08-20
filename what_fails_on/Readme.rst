=============
What Fails On
=============

Description
-----------

This utility is designed for scanning console output of jenkins jobs by subject of errors with missed packages. As result returns a list of missed packages.

How to use
----------

./`what_fails_on.sh`_

what_fails_on.sh
^^^^^^^^^^^^^^^^
This file contains:
ruby gerrit.rb & python what_fails_on.py -c `config.yaml`_

config.yaml
^^^^^^^^^^^

* Login - Your launchpad login (email)
* Password - Your password
* GlobalList - Return all missed packages as one list or separate by dependent packages names.
* URLs - List of consoles URLs