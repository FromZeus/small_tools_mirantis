====================
reqspec
====================

Description
-----------

This utility is designed for updating requirements in "Requires" sections of .spec files. Also highlight of missed or extra dependencies could be switch on.

How to use
----------

python reqspec.py -c `config.yaml`_

config.yaml
^^^^^^^^^^^

* Requirements - Path to requirements.txt file of project
* Spec - Path to .spec file of project
* PipSpec - Path to pip-spec.json library file
* SpecPip - Path to spec-pip.json library file
* Missed - True to show missed requirements
* Extra - True to show extra requirements
* CutBounds - List of bounds which will be cutted while update