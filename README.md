dsadmin
=======

dsadmin python module for 389 directory server administration


Test with:

 # cd /path/to/module

 # export PYTHONPATH+=:$PWD:

 # nosetests -w tests

 # sudo PYTHONPATH=$PYTHONPATH nosetests -w tests/


Debian/Ubuntu users may need to align their setup
to the redhat one to run all tests (or edit test configuration)

for file in setup-ds setup-ds-admin remove-ds; do 
	sudo ln -s /usr/sbin/${file}{,.pl};
done

structure
=========
```python
dsadmin/
|-- _entry.py 		- the Entry class 
|-- __init__.py	- core module, involving only ldap commands
|-- tools.py		- methods involving stuff outside ldap (eg. copy, start/stop, ...)
|-- utils.py		- static methods for mangling strings, formatting text and so on
```
