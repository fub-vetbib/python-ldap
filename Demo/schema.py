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
  for oid in schema.listall(schema_class):
    se = schema.get_obj(schema_class,oid)
    print attr_type,str(se)
print '*** Testing object class inetOrgPerson ***'
inetOrgPerson = schema.get_obj(ldap.schema.ObjectClass,'inetOrgPerson')
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
  drink = schema.get_obj(ldap.schema.AttributeType,'favouriteDrink')
except KeyError:
  pass
else:
  print '*** drink ***'
  print drink.names


print schema.ldap_entry()

print str(schema.get_obj(ldap.schema.MatchingRule,'2.5.13.11'))

print str(schema.get_obj(ldap.schema.MatchingRuleUse,'2.5.13.11'))

print schema.ldap_entry()
