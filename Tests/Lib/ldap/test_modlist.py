"""
Tests for module ldap.modlist
"""

import ldap

from ldap.modlist import addModlist,modifyModlist
  
print '\nTesting function addModlist():'
addModlist_tests = [
  (
    {
      'objectClass':['person','pilotPerson'],
      'cn':['Michael Str\303\266der','Michael Stroeder'],
      'sn':['Str\303\266der'],
      'dummy':[],
      'dummy':[''],
      'dummy':['2'],
      'dummy2':[],
      'dummy2':[''],
    },
    [
      ('objectClass',['person','pilotPerson']),
      ('cn',['Michael Str\303\266der','Michael Stroeder']),
      ('sn',['Str\303\266der']),
      ('dummy',['2']),
    ]
  ),
]
for entry,test_modlist in addModlist_tests:
  test_modlist.sort()
  result_modlist = addModlist(entry)
  result_modlist.sort()
  if test_modlist!=result_modlist:
    print 'addModlist(%s) returns\n%s\ninstead of\n%s.' % (
      repr(entry),repr(result_modlist),repr(test_modlist)
    )

print '\nTesting function modifyModlist():'
modifyModlist_tests = [
  (
    {
      'objectClass':['person','pilotPerson'],
      'cn':['Michael Str\303\266der','Michael Stroeder'],
      'sn':['Str\303\266der'],
      'c':['DE'],
    },
    {
      'objectClass':['person','inetOrgPerson'],
      'cn':['Michael Str\303\266der','Michael Stroeder'],
      'sn':[],
      'mail':['michael@stroeder.com'],
    },
    [
      (ldap.MOD_DELETE,'objectClass',['pilotPerson']),
      (ldap.MOD_ADD,'objectClass',['inetOrgPerson']),
      (ldap.MOD_DELETE,'c',None),
      (ldap.MOD_DELETE,'sn',None),
      (ldap.MOD_ADD,'mail',['michael@stroeder.com']),
    ]
  ),

  # Now a weird test-case for catching all possibilities
  # of removing an attribute with MOD_DELETE,attr_type,None
  (
    {
      'objectClass':['person'],
      'cn':[],
      'sn':[''],
      'c':['DE'],
    },
    {
      'objectClass':[],
      'cn':[],
      'sn':[''],
    },
    [
      (ldap.MOD_DELETE,'c',None),
      (ldap.MOD_DELETE,'cn',None),
      (ldap.MOD_DELETE,'objectClass',None),
      (ldap.MOD_DELETE,'sn',None),
    ]
  ),
]
for old_entry,new_entry,test_modlist in modifyModlist_tests:
  test_modlist.sort()
  result_modlist = modifyModlist(old_entry,new_entry)
  result_modlist.sort()
  if test_modlist!=result_modlist:
    print 'modifyModlist(%s,%s) returns\n%s\ninstead of\n%s.' % (
      repr(old_entry),
      repr(new_entry),
      repr(result_modlist),
      repr(test_modlist)
    )
