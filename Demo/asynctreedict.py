"""
Demo using the ldap.async module for retrieving partial results
in a hierarchically structured dictionary.
"""

import sys,ldap,ldap.async

class TreeDict(ldap.async.AsyncSearchHandler):
  """
  Class for collecting all search results in a dictionary
  hierarchically structured by distinguished name.
  """

  def __init__(self,l):
    ldap.async.AsyncSearchHandler.__init__(self,l)
    self.resultsTree = {}
    self.resultCounter = 0

  def _processSingleResult(self,resultType,resultItem):
    if ldap.async._entryResultTypes.has_key(resultType):
      dn,entry = resultItem
      self.resultCounter = self.resultCounter+1
      dn_list = ldap.explode_dn(dn)
      branch_dict = self.resultsTree
      for i in range(len(dn_list)-1,-1,-1):
        rdn = dn_list[i]
        if not branch_dict.has_key(rdn):
          branch_dict[rdn]={}
        branch_dict = branch_dict[rdn]

s = TreeDict(
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
  '%d results stored in TreeDict instance.\n' % (
    s.resultCounter
  )
)
