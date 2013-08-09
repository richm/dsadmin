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

brookers
========

With this structure, the DSAdmin functions will be available under
various small specific classes, like brooks flow to a river ;)
All the replication/changelog/agreement stuff have been moved
into dsadmin.brooker.Replica. Ex. 

conn = DSAdmin(**auth)
- conn.setupChangelog() -> conn.replica.changelog()
- conn.findAgreementDNs() -> conn.replica.agreements(dn=True)
- conn.getReplStatus()	-> conn.replica.status()


Quickstart
==========
- Define your credentials (by default host='localhost', port=389)

auth = {'binddn': 'cn=directory manager','bindpw':'password'}
ds = DSAdmin(**auth)


 # Config
 
 * set error-loglevel
 ds.config.loglevel( vals = [LOG_ENTRY_PARSER,LOG_REPLICA])

 * set access-loglevel
 ds.config.loglevel( vals = [LOG_DEFAULT], level='access')

 * get config from "cn=config"
 ds.config.get('passwordMaxAge')

 * set config
 ds.config.set('passwordGraceLimit', '3')


 # Backends 

 
 *  List backends
backends = ds.backend.list()

 *  Get first backend DN
backends[0].dn

 *  Add a new LDBM backend and setup its suffix
e = ds.backend.add(suffix="o=addressbook1", benamebase="AB1", setup_mt=True)

 *  Set a db in readonly
ds.backend.readonly("AB1")

 *  Set a db in read-write
ds.backend.readonly("AB1", readonly="off")



 # Replica


 *  Get replica entries or agreements dn
replica_e = ds.replica.list()
agreement_dn = ds.replica.agreements()
ruv = ds.replica.ruv(suffix="o=addressbook1")

 *  Enable changelog
ds.replica.changelog()

