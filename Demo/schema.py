import sys,time,ldap,ldap.schema,ldapurl

schema_allow = ldap.schema.ALLOW_ALL
schema_ignore_errors = 1
schema_attrs = ldap.schema.SCHEMA_ATTRS

ldap_url = ldapurl.LDAPUrl(sys.argv[1])

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

ldap._trace_level = 0

# Connect and bind as LDAPv3
l=ldap.initialize(ldap_url.initializeUrl(),trace_level=0)
l.protocol_version = ldap.VERSION3
l.simple_bind_s('','')

time_mark0 = time.time()

# Search for DN of sub schema sub entry
subschemasubentry_dn = l.search_subschemasubentry_s(ldap_url.dn.encode('utf-8'))

time_mark1 = time.time()

print 'Result of search for sub schema sub entry:',repr(subschemasubentry_dn)
print 'Time elapsed search sub schema sub entry: %0.3f' % (time_mark1-time_mark0)


if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'
  sys.exit(1)

# Read the sub schema sub entry
subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn,attrs=schema_attrs
)
time_mark2 = time.time()
print 'Time elapsed reading sub schema sub entry: %0.3f' % (time_mark2-time_mark1)

print '*** Schema from',repr(subschemasubentry_dn)

# Parse the schema entry
schema = ldap.schema.SubSchema(
  subschemasubentry_entry,
  schema_allow=schema_allow,
  ignore_errors=schema_ignore_errors
)

time_mark3 = time.time()

print 'Time elapsed parsing sub schema sub entry: %0.3f' % (time_mark3-time_mark2)

schema_element_names = schema.name2oid.keys()
schema_element_names.sort()
for name in schema_element_names:
  print repr(name),'->',repr(schema.name2oid[name])

# Display schema
for attr_type,schema_class in ldap.schema.SCHEMA_CLASS_MAPPING.items():
  print '***',repr(attr_type),'***'
  for oid,se in schema.schema_element.items():
    if isinstance(se,schema_class):
      print repr(oid),repr(se)
      print str(se)
print '*** Testing object class inetOrgPerson ***'
inetOrgPerson = schema.schema_element[schema.name2oid['inetOrgPerson']]
print inetOrgPerson.must,inetOrgPerson.may
print '*** person,organizationalPerson,inetOrgPerson ***'
print schema.all_attrs(
  ['person','organizationalPerson','inetOrgPerson']
)
print schema.all_attrs(
  ['person','organizationalPerson','inetOrgPerson'],
  attr_type_filter = [
    ('no_user_mod',[0]),
    ('usage',range(2)),
  ]  
)

schema.ldap_entry()

schema.avail_objectclasses()
