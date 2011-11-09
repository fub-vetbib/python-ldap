url = "ldap://localhost:1390/"
base = "dc=stroeder,dc=de"
search_flt = r'(objectClass=*)'

searchreq_attrlist=['cn','entryDN','entryUUID','mail','objectClass']

from ldap.ldapobject import LDAPObject

import ldap,pprint
from ldap.controls import SimplePagedResultsControl


class PagedResultsSearchObject:
  page_size = 50

  def paged_search_ext_s(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,serverctrls=None,clientctrls=None,timeout=-1,sizelimit=0):
    """
    Behaves exactly like LDAPObject.search_ext_s() but internally uses the
    simple paged results control to retrieve search results in chunks.
    
    This is non-sense for really large results sets which you would like
    to process one-by-one
    """
    req_ctrl = SimplePagedResultsControl(True,size=self.page_size,cookie='')

    # Send first search request
    msgid = self.search_ext(
      base,
      ldap.SCOPE_SUBTREE,
      search_flt,
      attrlist=searchreq_attrlist,
      serverctrls=(serverctrls or [])+[req_ctrl]
    )

    result_pages = 0
    all_results = []
    
    while True:
      rtype, rdata, rmsgid, rctrls = self.result3(msgid)
      all_results.extend(rdata)
      result_pages += 1
      # Extract the simple paged results response control
      pctrls = [
        c
        for c in rctrls
        if c.controlType == SimplePagedResultsControl.controlType
      ]
      if pctrls:
        if pctrls[0].cookie:
            # Copy cookie from response control to request control
            req_ctrl.cookie = pctrls[0].cookie
            msgid = self.search_ext(
              base,
              ldap.SCOPE_SUBTREE,
              search_flt,
              attrlist=searchreq_attrlist,
              serverctrls=(serverctrls or [])+[req_ctrl]
            )
        else:
            break
    return result_pages,all_results


class MyLDAPObject(LDAPObject,PagedResultsSearchObject):
  pass


#ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)
ldap.set_option(ldap.OPT_REFERRALS, 0)
l = MyLDAPObject(url,trace_level=2)
l.protocol_version = 3
l.simple_bind_s("", "")
l.page_size=10

# Send search request
result_pages,all_results = l.paged_search_ext_s(
  base,
  ldap.SCOPE_SUBTREE,
  search_flt,
  attrlist=searchreq_attrlist,
  serverctrls=None
)

l.unbind_s()

print 'Received %d results in %d pages.' % (len(all_results),result_pages)
