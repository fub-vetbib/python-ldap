import sys,ldap,ldap.schema

schema_attrs = ldap.schema.SCHEMA_ATTRS

ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

ldap._trace_level = 0

subschemasubentry_dn,schema = ldap.schema.urlfetch(sys.argv[-1])

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'
  sys.exit(1)

print '*** Schema from',repr(subschemasubentry_dn)

# Display schema
for attr_type,schema_class in ldap.schema.SCHEMA_CLASS_MAPPING.items():
  print '*'*66
  for oid,se in schema.items():
    if isinstance(se,schema_class):
      print attr_type,str(se)
print '*** Testing object class inetOrgPerson ***'
inetOrgPerson = schema[schema.name2oid[ldap.schema.ObjectClass]['inetOrgPerson']]
print inetOrgPerson.must,inetOrgPerson.may
print '*** person,organizationalPerson,inetOrgPerson ***'
print schema.attribute_types(
  ['person','organizationalPerson','inetOrgPerson']
)
print schema.attribute_types(
  ['person','organizationalPerson','inetOrgPerson'],
  attr_type_filter = [
#    ('no_user_mod',[0]),
    ('usage',range(2)),
  ]  
)
try:
  drink = schema[schema.name2oid[ldap.schema.AttributeType]['favouriteDrink']]
except KeyError:
  pass
else:
  print '*** drink ***'
  print drink.names


print schema.ldap_entry()

schema.listall(ldap.schema.ObjectClass)

schema.listall(ldap.schema.AttributeType)
