"""
Demo using the ldap.async module for retrieving partial results
even though the exception ldap.SIZELIMIT_EXCEEDED was raised.
"""

import sys,ldap,ldap.async

s = ldap.async.CollectResults(
  ldap.open('localhost:1389'),
)

s.startSearch(
  'dc=stroeder,dc=com',
  ldap.SCOPE_SUBTREE,
  '(objectClass=*)',
)

try:
  partial = s.processResults()
except ldap.SIZELIMIT_EXCEEDED:
  sys.stderr.write('Warning: Server-side size limit exceeded.\n')
else:
  if partial:
    sys.stderr.write('Warning: Only partial results received.\n')

sys.stderr.write(
  '%d results received.\n' % (
    len(s.allResults)
  )
)
