# For documentation, see comments in Module/LDAPObject.c and the
# ldap.sasl module documentation.

import ldap,ldap.sasl

ldap.sasl._trace_level=0

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

for ldap_uri,sasl_mech,sasl_cb_value_dict in [
  (
    "ldap://localhost:1390/",
    'CRAM-MD5',
    {
      ldap.sasl.CB_AUTHNAME    :'fred',
      ldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://localhost:1390/",
    'PLAIN',
    {
      ldap.sasl.CB_AUTHNAME    :'fred',
      ldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://localhost:1390/",
    'LOGIN',
    {
      ldap.sasl.CB_AUTHNAME    :'fred',
      ldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldapi://%2Ftmp%2Fopenldap-socket/",
    'EXTERNAL',
    { }
  ),
  (
    "ldap://localhost:1390/",
    'GSSAPI',
    { }
  ),
  (
    "ldap://localhost:1390/",
    'NTLM',
    {
      ldap.sasl.CB_AUTHNAME    :'fred',
      ldap.sasl.CB_PASS        :'secret',
    }
  ),
  (
    "ldap://localhost:1390/",
    'DIGEST-MD5',
    {
      ldap.sasl.CB_AUTHNAME    :'fred',
      ldap.sasl.CB_PASS        :'secret',
    }
  ),
]:
  sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict,sasl_mech)
  print 20*'*',sasl_auth.mech,20*'*'
  # Open the LDAP connection
  l = ldap.initialize(ldap_uri,trace_level=0)
  # Set protocol version to LDAPv3 to enable SASL bind!
  l.protocol_version = 3
  try:
    l.sasl_interactive_bind_s("", sasl_auth)
  except ldap.LDAPError,e:
    print 'Error using SASL mechanism',sasl_auth.mech,str(e)
  else:
    print 'Sucessfully bound using SASL mechanism',sasl_auth.mech,'as',repr(l.whoami_s())
  l.unbind()
