dsadmin
=======

dsadmin python module for 389 directory server administration


Test with:

 # cd /path/to/module

 # export PYTHONPATH+=:$PWD:

 # nosetests -w tests

 # sudo PYTHONPATH=$PYTHONPATH nosetests -w tests/


structure
=========

dsadmin/
|-- \_entry.py 		- the Entry class 
|-- \_\_init\_\_.py	- core module, involving only ldap commands
|-- tools.py		- methods involving stuff outside ldap (eg. copy, start/stop, ...)
|-- utils.py		- static methods for mangling strings, formatting text and so on

