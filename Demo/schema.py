import sys,ldap,ldap.schema,ldapurl

ldap_url = ldapurl.LDAPUrl(sys.argv[1])

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

# Connect and bind as LDAPv3
l=ldap.initialize(ldap_url.initializeUrl(),trace_level=0)
l.version = ldap.VERSION3
l.simple_bind_s('','')

# Search for DN of sub schema sub entry
subschemasubentry_dn = l.search_subschemasubentry_s(ldap_url.dn.encode('utf-8'))

subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn
)

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'

else:

  print '*** Schema from',repr(subschemasubentry_dn)

  # Read the schema entry
  schema = ldap.schema.subSchema(subschemasubentry_entry,schema_allow=31)

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
  all_must,all_may = inetOrgPerson.all_attrs(schema)
  print all_must,all_may
