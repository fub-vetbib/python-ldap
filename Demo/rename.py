import ldap
from getpass import getpass

# Create LDAPObject instance
l = ldap.initialize('ldap://localhost:1389')

print l.rename_s.__doc__

print 'Password:'
cred = getpass()

try:

  # Set LDAP protocol version used
  l.set_option(ldap.OPT_PROTOCOL_VERSION,3)

  # Try a bind to provoke failure if protocol version is not supported
  l.bind_s('cn=root,dc=stroeder,dc=com',cred,ldap.AUTH_SIMPLE)

  print 'Using rename_s():'

  l.rename_s(
    'uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com',
    'cn=Fred Feuerstein',
    'dc=stroeder,dc=com',
    0
  )
  print 'uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com'
  print '=> cn=Fred Feuerstein,dc=stroeder,dc=com'

  l.rename_s(
    'cn=Fred Feuerstein,dc=stroeder,dc=com',
    'uid=fred',
    'ou=Unstructured testing tree,dc=stroeder,dc=com',
    0
  )
  print 'cn=Fred Feuerstein,dc=stroeder,dc=com'
  print '=> uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com'

  print 'Using rename():'

  m = l.rename(
    'uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com',
    'cn=Fred Feuerstein',
    'dc=stroeder,dc=com',
    0
  )
  r = l.result(m,1)
  print 'uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com'
  print '=> cn=Fred Feuerstein,dc=stroeder,dc=com'

  m = l.rename(
    'cn=Fred Feuerstein,dc=stroeder,dc=com',
    'uid=fred',
    'ou=Unstructured testing tree,dc=stroeder,dc=com',
    0
  )
  r = l.result(m,1)

  print 'cn=Fred Feuerstein,dc=stroeder,dc=com'
  print '=> uid=fred,ou=Unstructured testing tree,dc=stroeder,dc=com'

finally:

  l.unbind_s()
