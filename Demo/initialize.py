"""
Various examples how to connect to a LDAP host with the new
factory function ldap.initialize() introduced in OpenLDAP 2 API.

Assuming you have LDAP servers running on
ldap://localhost:1389 (LDAP with StartTLS)
ldaps://localhost:1636 (LDAP over SSL)
ldapi://%2ftmp%2fopenldap2 (domain socket /tmp/openldap2)
"""

import sys,ldap

# Set debugging level
ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)
ldapmodule_trace_level = 1
ldapmodule_trace_file = sys.stderr

# Set path name of file containing all CA certificates
# needed to validate server certificates
ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,'/etc/httpd/ssl.crt/myCA-cacerts.pem')

print """##################################################################
# LDAPv3 connection with StartTLS
##################################################################
"""

# Create LDAPObject instance
l = ldap.initialize('ldap://localhost:1390',trace_level=ldapmodule_trace_level,trace_file=ldapmodule_trace_file)
# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3
l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
# Now try StartTLS extended operation
l.start_tls_s()
# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)
# Close connection
l.unbind_s()

print """##################################################################
# LDAPv3 connection over SSL
##################################################################
"""

# Create LDAPObject instance
l = ldap.initialize('ldaps://localhost:1636',trace_level=ldapmodule_trace_level,trace_file=ldapmodule_trace_file)
# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3
# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)
# Close connection
l.unbind_s()

print """##################################################################
# LDAPv3 connection over Unix domain socket
##################################################################
"""

# Create LDAPObject instance
l = ldap.initialize('ldapi://%2ftmp%2fopenldap2',trace_level=ldapmodule_trace_level,trace_file=ldapmodule_trace_file)
# Set LDAP protocol version used
l.protocol_version=ldap.VERSION3
# Try a bind to provoke failure if protocol version is not supported
l.bind_s('','',ldap.AUTH_SIMPLE)
# Close connection
l.unbind_s()

