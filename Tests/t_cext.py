
import unittest, slapd
import _ldap
import logging

class TestLdapCExtension(unittest.TestCase):

    def _init(self):
        self.slapd = s = slapd.Slapd()
        #s.set_debug()  # enables verbose messages
        s.start()
        ldap = _ldap.initialize(s.get_url())
        #-- slapd wants v3 so that adds are properly authenticated
        ldap.set_option(_ldap.OPT_PROTOCOL_VERSION, _ldap.VERSION3)
        ldap.simple_bind(s.get_root_dn(), s.get_root_password())
        return ldap

    def test_simple_bind(self):
        l = self._init()
        l.unbind_ext()

    def test_search_ext_individual(self):
        l = self._init()
        base = self.slapd.get_dn_suffix()
        m = l.search_ext(base, _ldap.SCOPE_SUBTREE, '(objectClass=dcObject)')
        result,pmsg,msgid,ctrls = l.result3(m, 0)

        # Expect to get just one object
        self.assertEquals(result, 100)
        self.assertEquals(len(pmsg), 1)
        self.assertEquals(len(pmsg[0]), 2)
        self.assertEquals(pmsg[0][0], self.slapd.get_dn_suffix())
        self.assertEquals(pmsg[0][0], self.slapd.get_dn_suffix())
        self.assertTrue('dcObject' in pmsg[0][1]['objectClass'])
        self.assertTrue('organization' in pmsg[0][1]['objectClass'])
        self.assertEquals(msgid, m)
        self.assertEquals(ctrls, [])

        result,pmsg,msgid,ctrls = l.result3(m, 0) # all=0
        self.assertEquals(result, 101)
        self.assertEquals(pmsg, [])
        self.assertEquals(msgid, m)
        self.assertEquals(ctrls, [])

    def test_search_ext_all(self):
        l = self._init()
        base = self.slapd.get_dn_suffix()
        m = l.search_ext(base, _ldap.SCOPE_SUBTREE, '(objectClass=*)')
        result,pmsg,msgid,ctrls = l.result3(m, 1) # all=1

        # Expect to get the objects
        self.assertEquals(result, 101)
        self.assertEquals(len(pmsg), 2)
        self.assertEquals(msgid, m)
        self.assertEquals(ctrls, [])

    def test_add(self):
        l = self._init()
        dn = "cn=Foo," + self.slapd.get_dn_suffix()
        obj = [('objectClass','organizationalRole'), ('cn', 'Foo')]
        m = l.add_ext(dn, obj)

        result,pmsg,msgid,ctrls = l.result3(m, 1) # all=1

if __name__ == '__main__':
    unittest.main()
