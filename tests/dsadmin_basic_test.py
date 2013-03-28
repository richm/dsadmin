""" Testing basic functionalities of DSAdmin


"""
import dsadmin
from dsadmin import DSAdmin, Entry
import ldap

from nose import SkipTest
from nose.tools import *
import config
from config import *

conn = None
added_entries = None


def setup():
    global conn
    conn = DSAdmin(**config.auth)
    conn.verbose = True
    conn.added_entries = []


def tearDown():
    global conn
    
    # reduce log level
    conn.setLogLevel(0)
    conn.setAccessLogLevel(0)
    
    for e in conn.added_entries:
        try:
            conn.delete_s(e)
        except ldap.NO_SUCH_OBJECT:
            log.warn("entry not found %r" % e)


def bind_test():
    print "conn: %s" % conn


def setupBindDN_UID_test():
    # TODO change returning the entry instead of 0
    user = {
        'binddn': 'uid=rmanager1,cn=config',
        'bindpw': 'password'
    }
    e = conn.setupBindDN(**user)
    conn.added_entries.append(e.dn)

    assert e.dn == user['binddn'], "Bad entry: %r " % e
    expected = conn.getEntry(user['binddn'], ldap.SCOPE_BASE)
    assert entry_equals(
        e, expected), "Mismatching entry %r vs %r" % (e, expected)


def setupBindDN_CN_test():
    # TODO change returning the entry instead of 0
    user = {
        'binddn': 'cn=rmanager1,cn=config',
        'bindpw': 'password'
    }
    e = conn.setupBindDN(**user)
    conn.added_entries.append(e.dn)
    assert e.dn == user['binddn'], "Bad entry: %r " % e
    expected = conn.getEntry(user['binddn'], ldap.SCOPE_BASE)
    assert entry_equals(
        e, expected), "Mismatching entry %r vs %r" % (e, expected)


def setupChangelog_default_test():
    e = conn.setupChangelog()
    conn.added_entries.append(e.dn)
    assert e.dn, "Bad changelog entry: %r " % e
    assert e.getValue('nsslapd-changelogdir').endswith("changelogdb"), "Mismatching entry %r " % e.data.get('nsslapd-changelogdir')
    conn.delete_s("cn=changelog5,cn=config")


def setupChangelog_test():
    e = conn.setupChangelog(dbname="mockChangelogDb")
    conn.added_entries.append(e.dn)
    assert e.dn, "Bad changelog entry: %r " % e
    assert e.getValue('nsslapd-changelogdir').endswith("mockChangelogDb"), "Mismatching entry %r " % e.data.get('nsslapd-changelogdir')
    conn.delete_s("cn=changelog5,cn=config")


def setupChangelog_full_test():
    e = conn.setupChangelog(dbname="/tmp/mockChangelogDb")
    conn.added_entries.append(e.dn)

    assert e.dn, "Bad changelog entry: %r " % e
    expect(e, 'nsslapd-changelogdir', "/tmp/mockChangelogDb")
    conn.delete_s("cn=changelog5,cn=config")


def setLogLevel_test():
    vals = 1 << 0, 1 << 1, 1 << 5
    assert conn.setLogLevel(*vals) == sum(vals)


def setAccessLogLevel_test():
    vals = 1 << 0, 1 << 1, 1 << 5
    assert conn.setAccessLogLevel(*vals) == sum(vals)
