from nose import *
from nose.tools import *
import config
from config import log
from config import *

from dsadmin import DSAdmin, Entry
from dsadmin import NoSuchEntryError
import dsadmin
import ldap


from subprocess import Popen


conn = None
added_entries = None

def setup():
    global conn
    conn = DSAdmin(**config.auth)
    conn.verbose = True
    conn.added_entries = []

def tearDown():
    global conn
    for e in conn.added_entries:
        conn.delete_s(e)

def drop_backend(suffix, bename=None, maxnum=50):
    global conn
    if not bename:
        bename = [x.dn for x in conn.getBackendsForSuffix(suffix) ]   
    assert bename, "Missing bename for %r" % suffix
    if not hasattr(bename, '__iter__'):
        bename = [ ','.join(['cn=%s' % bename, dsadmin.DN_LDBM]) ]
    for be in bename:
        log.debug("removing entry from %r" % be)
        leaves = [x.dn for x in conn.search_s(be, ldap.SCOPE_SUBTREE, '(objectclass=*)', ['cn']) ]
        # start deleting the leaves - which have the max number of ","
        leaves.sort(key=lambda x:x.count(",")) 
        while leaves and maxnum:        
            # to avoid infinite loops
            # limit the iterations
            maxnum-= 1
            try:
                log.debug("removing %s" % leaves[-1])
                conn.delete_s(leaves[-1])
                leaves.pop()
            except:
                leaves.insert(0, leaves.pop())
        
        if not maxnum:
            raise Exception("BAD")
    

#
# Tests
#




def addbackend_harn(conn, name):
    suffix = "o=%s" % name
    e = Entry((suffix, {
               'objectclass': ['top', 'organization'],
               'o': name
               }))

    ret = conn.addSuffix(suffix, name)
    conn.add(e)

def setupBackend_ok_test():
    be = conn.setupBackend('o=mockbe1', 'mockbe1')
    assert be

@raises(ldap.ALREADY_EXISTS)
def setupBackend_double_test():
    be1 = conn.setupBackend('o=mockbe2', 'mockbe2')
    be11 = conn.setupBackend('o=mockbe2', 'mockbe2')

def addsuffix_test():
    addbackend_harn(conn, 'addressbook16')


def addreplica_write_test():
    name = 'ab3'
    user = {
        'binddn': 'uid=rmanager,cn=config',
        'bindpw': 'password'
    }
    replica = {
        'suffix': 'o=%s' % name,
        'type': dsadmin.MASTER_TYPE,
        'id': 124
    }
    replica.update(user)
    addbackend_harn(conn, name)
    ret = conn.replicaSetupAll(replica)
    assert ret == 0, "Error in setup replica: %s" % ret


@SkipTest
def setupSSL_test():
    ssl_args = {
        'secport': 636,
        'sourcedir': None,
        'secargs': {'nsSSLPersonalitySSL': 'localhost'},
    }
    cert_dir = conn.getDseAttr('nsslapd-certdir')
    assert cert_dir, "Cannot retrieve cert dir"
    
    log.info("Creating a self-signed cert for the server")
    cmd = 'certutil -d %s -S -n localhost  -t CTu,Cu,Cu  -s cn=localhost -x' % cert_dir
    Popen(cmd.split(), stdin=open("/dev/urandom"))
    
    log.info("Testing ssl configuration")
    conn.setupSSL(**ssl_args)




def prepare_master_replica_test():
    user = {
        'binddn': 'uid=rmanager,cn=config',
        'bindpw': 'password'
    }
    conn.enableReplLogging()
    e = conn.setupBindDN(**user)
    conn.added_entries.append(e.dn)

    # only for Writable
    e = conn.setupChangelog()
    conn.added_entries.append(e.dn)



def setupAgreement_test():
    consumer = MockDSAdmin()
    args = {
        'suffix': "o=addressbook6",
        #'bename': "userRoot",
        'binddn': "uid=rmanager,cn=config",
        'bindpw': "password",
        'type': dsadmin.MASTER_TYPE
    }
    conn.setupReplica(args)
    conn.added_entries.append(args['binddn'])

    dn_replica = conn.setupAgreement(consumer, args)
    print dn_replica



@raises(NoSuchEntryError)
def getMTEntry_missing_test():
    e = conn.getMTEntry('o=MISSING')


def getMTEntry_present_test():
    suffix = 'o=addressbook16'
    e = conn.getMTEntry(suffix)
    assert e, "Entry should be present %s" % suffix
