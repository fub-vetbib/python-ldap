"""
Performes various tests for module ldapurl
"""

import ldapurl
from ldapurl import *

print '\nTesting function isLDAPUrl():'
is_ldap_url_tests = {
  # Examples from RFC2255
  'ldap:///o=University%20of%20Michigan,c=US':1,
  'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,c=US':1,
  'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,':1,
  'ldap://host.com:6666/o=University%20of%20Michigan,':1,
  'ldap://ldap.itd.umich.edu/c=GB?objectClass?one':1,
  'ldap://ldap.question.com/o=Question%3f,c=US?mail':1,
  'ldap://ldap.netscape.com/o=Babsco,c=US??(int=%5c00%5c00%5c00%5c04)':1,
  'ldap:///??sub??bindname=cn=Manager%2co=Foo':1,
  'ldap:///??sub??!bindname=cn=Manager%2co=Foo':1,
  # More examples from various sources
  'ldap://ldap.nameflow.net:1389/c%3dDE':1,
  'ldap://root.openldap.org/dc=openldap,dc=org':1,
  'ldap://root.openldap.org/dc=openldap,dc=org':1,
  'ldap://x500.mh.se/o=Mitthogskolan,c=se????1.2.752.58.10.2=T.61':1,
  'ldp://root.openldap.org/dc=openldap,dc=org':0,
  'ldap://localhost:1389/ou%3DUnstructured%20testing%20tree%2Cdc%3Dstroeder%2Cdc%3Dcom??one':1,
}
for ldap_url in is_ldap_url_tests.keys():
  result_is_ldap_url = isLDAPUrl(ldap_url)
  if result_is_ldap_url !=is_ldap_url_tests[ldap_url]:
    print 'isLDAPUrl("%s") returns %d instead of %d.' % (
      repr(ldap_url),result_is_ldap_url,is_ldap_url_tests[ldap_url]
    )

print '\nTesting class LDAPUrl:'
parse_ldap_url_tests = {
  'ldap://root.openldap.org/dc=openldap,dc=org':(
    'ldap',
    u'root.openldap.org', u'dc=openldap,dc=org',None,LDAP_SCOPE_BASE,'(objectclass=*)',[]
  ),
  'ldap://localhost/dc=stroeder,dc=com??sub?':(
    'ldap',
    u'localhost', u'dc=stroeder,dc=com',None,LDAP_SCOPE_SUBTREE,'(objectclass=*)',[]
  ),
  'ldap://localhost??one?':(
    'ldap',
    u'localhost', u'',None,LDAP_SCOPE_ONELEVEL,'(objectclass=*)',[]
  ),
  'ldap://x500.mh.se/o=Mitthogskolan,c=se????1.2.752.58.10.2=T.61':(
    'ldap',
    u'x500.mh.se',
    u'o=Mitthogskolan,c=se',None,
    LDAP_SCOPE_BASE,
    u'(objectclass=*)',
    [u'1.2.752.58.10.2=T.61']
  ),
  'ldap://ldap.openldap.org/uid%3dkurt%2cdc%3dboolean%2cdc%3dnet??base?%28objectclass%3d%2a%29':(
    'ldap',
    'ldap.openldap.org',
    u'uid=kurt,dc=boolean,dc=net',
    None,
    LDAP_SCOPE_BASE,
    u'(objectclass=*)',
    []
  ),
  'ldap://localhost:12345/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
    'ldap',
    'localhost:12345',
    u'dc=stroeder,dc=com',
    None,
    LDAP_SCOPE_BASE,
    u'(objectclass=*)',
    [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
  ),
  'ldaps://localhost:12345/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
    'ldaps',
    'localhost:12345',
    u'dc=stroeder,dc=com',
    None,
    LDAP_SCOPE_BASE,
    u'(objectclass=*)',
    [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
  ),
  'ldapi://%2ftmp%2fopenldap2-1389/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
    'ldapi',
    '/tmp/openldap2-1389',
    u'dc=stroeder,dc=com',
    None,
    LDAP_SCOPE_BASE,
    u'(objectclass=*)',
    [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
  ),
}
for ldap_url in parse_ldap_url_tests.keys():
  print 72*'#','\nTesting LDAP URL:',ldap_url
  ldapUrl = LDAPUrl(ldapUrl=ldap_url)
  print 'Unparsed LDAP URL',ldapUrl.unparse()
  if (
       ldapUrl.urlscheme,ldapUrl.hostport,ldapUrl.dn,ldapUrl.attrs,
       ldapUrl.scope,ldapUrl.filterstr,map(str,ldapUrl.extensions.values())
     ) != \
     parse_ldap_url_tests[ldap_url]:
    print 'Attributes of LDAPUrl(%s) are:\n%s\ninstead of:\n%s\n' % (
      repr(ldap_url),
      (
       ldapUrl.urlscheme,ldapUrl.hostport,ldapUrl.dn,ldapUrl.attrs,
       ldapUrl.scope,ldapUrl.filterstr,map(str,ldapUrl.extensions.values())
      ),
      repr(parse_ldap_url_tests[ldap_url])
    )
