# For documentation, see comments in Module/LDAPObject.c and the
# ldap.sasl module documentation.

import ldap, ldap.sasl

l = ldap.initialize("ldap://localhost:1389/")
auth = ldap.sasl.digest_md5("aschauer","secret")
l.sasl_bind_s("", auth)
    

res = l.search_s("",ldap.SCOPE_BASE,"(objectClass=*)")
print res

l.unbind()
