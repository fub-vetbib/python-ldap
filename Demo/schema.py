import ldap,ldap.schema

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

# Connect and bind as LDAPv3
l=ldap.initialize('ldap://localhost:1389',trace_level=0)
l.version = ldap.VERSION3
l.simple_bind_s('','')

# Search for DN of sub schema sub entry
subschemasubentry_dn = l.search_subschemasubentry_s('')

subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn
)

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'

else:

  print '*** Schema from',repr(subschemasubentry_dn)

  # Read the schema entry
  schema = ldap.schema.subSchema(subschemasubentry_entry)

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
  print repr(inetOrgPerson.must),repr(inetOrgPerson.may)
