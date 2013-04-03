""" Test creation and deletion of instances
"""
import ldap
from dsadmin import DSAdmin, DN_CONFIG

def default_test():
    host = 'localhost'
    port = 10200
    binddn = "cn=directory manager"
    bindpw = "secret12"

    basedn = DN_CONFIG
    scope = ldap.SCOPE_BASE
    filt = "(objectclass=*)"

    try:
        m1 = DSAdmin(host, port, binddn, bindpw)
#        filename = "%s/slapd-%s/ldif/Example.ldif" % (m1.sroot, m1.inst)
#        m1.importLDIF(filename, "dc=example,dc=com", None, True)
#        m1.exportLDIF('/tmp/ldif', "dc=example,dc=com", False, True)
        print m1.sroot, m1.inst, m1.errlog
        ent = m1.getEntry(basedn, scope, filt, None)
        if ent:
            print ent.passwordmaxage
        m1 = DSAdmin.createInstance({
                                    'cfgdshost': host,
                                    'cfgdsport': port,
                                    'cfgdsuser': 'admin',
                                    'cfgdspwd': 'admin',
                                    'newrootpw': 'password',
                                    'newhost': host,
                                    'newport': port + 10,
                                    'newinst': 'm1',
                                    'newsuffix': 'dc=example,dc=com',
                                    'verbose': 1
                                    })
#     m1.stop(True)
#     m1.start(True)
        cn = m1.setupBackend("dc=example2,dc=com")
        rc = m1.setupSuffix("dc=example2,dc=com", cn)
        entry = m1.getEntry(DN_CONFIG, ldap.SCOPE_SUBTREE, "(cn=" + cn + ")")
        print "new backend entry is:"
        print entry
        print entry.getValues('objectclass')
        print entry.OBJECTCLASS
        results = m1.search_s("cn=monitor", ldap.SCOPE_SUBTREE)
        print results
        results = m1.getBackendsForSuffix("dc=example,dc=com")
        print results

    except ldap.LDAPError, e:
        print e

    print "done"


