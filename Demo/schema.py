import sys,time,ldap,ldap.schema,ldapurl

schema_allow = ldap.schema.ALLOW_ALL

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

print 'Time elapsed search sub schema sub entry: %0.3f' % (time_mark1-time_mark0)

subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn
)

time_mark2 = time.time()

print 'Time elapsed reading sub schema sub entry: %0.3f' % (time_mark2-time_mark1)

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'

else:

  print '*** Schema from',repr(subschemasubentry_dn)

  # Read the schema entry
  schema = ldap.schema.subSchema(
    subschemasubentry_entry,schema_allow=schema_allow
  )

  time_mark3 = time.time()

  print 'Time elapsed parsing sub schema sub entry: %0.3f' % (time_mark3-time_mark2)

  # Display schema
  for attr_type,schema_class in ldap.schema.SCHEMA_CLASS_MAPPING.items():
    print '***',repr(attr_type),'***'
    for oid,se in schema.schema_element.items():
      if isinstance(se,schema_class):
        print repr(oid),repr(se)
  schema_element_names = schema.name2oid.keys()
  schema_element_names.sort()
  for name in schema_element_names:
    print repr(name),'->',repr(schema.name2oid[name])
  print '*** inetOrgPerson ***'
  inetOrgPerson = schema.schema_element[schema.name2oid['inetOrgPerson']]
  print inetOrgPerson.must,inetOrgPerson.may
  print '*** person,organizationalPerson,inetOrgPerson ***'
  print schema.all_attrs(['person','organizationalPerson','inetOrgPerson'])
