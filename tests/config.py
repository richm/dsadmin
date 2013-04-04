import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


auth = {'host': 'localhost',
        'port': 389,
        'binddn': 'cn=directory manager',
        'bindpw': 'password'}


class MockDSAdmin(object):
    host = 'localhost'
    port = 389
    sslport = 0

    def __str__(self):
        if self.sslport:
            return 'ldaps://%s:%s' % (self.host, self.sslport)
        else:
            return 'ldap://%s:%s' % (self.host, self.port)


def expect(entry, name, value):
    assert entry, "Bad entry %r " % entry
    assert entry.getValue(name) == value, "Bad value for entry %s. Expected %r vs %r" % (entry, entry.getValue(name), value)


def entry_equals(e1, e2):
    return str(e1) == str(e2)


def dfilter(my_dict, keys):
    return dict([(k, v) for k, v in my_dict.iteritems() if k in keys])
