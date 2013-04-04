
from nose import *
import dsadmin
from dsadmin.utils import *

def normalizeDN_test():
    test = [ 
        (r'dc=example,dc=com', r'dc=example,dc=com'),
        (r'dc=example, dc=com', r'dc=example,dc=com'),
        (r'cn="dc=example,dc=com",cn=config', 'cn=dc\\=example\\,dc\\=com,cn=config'),
        ]
    for k,v in test:
        r = normalizeDN(k)
        assert r == v, "Mismatch %r vs %r" % (r,v)


def escapeDNValue_test():
    test = [ (r'"dc=example, dc=com"', r'\"dc\=example\,\ dc\=com\"') ]
    for k,v in test:
        r = escapeDNValue(k)
        assert r == v, "Mismatch %r vs %r" % (r,v)
        
def escapeDNFiltValue_test():
    test = [ (r'"dc=example, dc=com"', '\\22dc\\3dexample\\2c\\20dc\\3dcom\\22') ]
    for k,v in test:
        r = escapeDNFiltValue(k)
        assert r == v, "Mismatch %r vs %r" % (r,v)

#
# socket related functions
#
import socket
def isLocalHost_test():
    test = [ 
        ('localhost', True), 
        ('localhost.localdomain', True),
        (socket.gethostname(), True),
        ('www.google.it', False) ]
    for k,v in test:
        r = isLocalHost(k)
        assert r == v, "Mismatch %r vs %r on %r" % (r,v, k)

   
def update_newhost_with_fqdn_test():
    test = [ 
        ({'newhost':'localhost'}, ('localhost.localdomain', True) ), 
        ({'newhost': 'remote'}, ('remote', False) ), 
        ]
    for k,v in test:
        old = k.copy()
        expected_host, expected_r = v
        r = update_newhost_with_fqdn(k)
        assert expected_r == r, "Mismatch %r vs %r for %r" % (r,expected_r, old)
        assert expected_host == k['newhost'], "Mismatch %r vs %r for %r" % (k['newhost'],expected_host, old)

def formatInfData_test():
    formatInfData({})
