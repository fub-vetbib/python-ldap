"""
Do a search with the LDAP URL specified at command-line.

No output of LDAP data is produced except trace output.
"""

import sys,getpass,ldap,ldapurl

try:
  ldapUrl = ldapurl.LDAPUrl(ldapUrl=sys.argv[1])
except IndexError:
  print 'Usage: %s [LDAP URL]' % (sys.argv[0])
  sys.exit(1)

for a in [
  'urlscheme','hostport','dn','attrs','scope',
  'filterstr','extensions','charset','who','cred'
]:
  print a,repr(getattr(ldapUrl,a))

l = ldap.open(ldapUrl.hostport,trace_level=1)
l.search_s(ldapUrl.dn,ldapUrl.scope,ldapUrl.filterstr,ldapUrl.attrs)
