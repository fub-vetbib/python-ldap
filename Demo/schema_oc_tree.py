import sys,ldap,ldap.schema,ldapurl

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

# Search for DN of sub schema sub entry
subschemasubentry_dn = l.search_subschemasubentry_s(ldap_url.dn.encode('utf-8'))

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'
  sys.exit(1)

# Read the sub schema sub entry
subschemasubentry_entry = l.read_subschemasubentry_s(
  subschemasubentry_dn,attrs=schema_attrs
)
print '*** Read schema from',repr(subschemasubentry_dn)
print

# Parse the schema entry
schema = ldap.schema.SubSchema(
  subschemasubentry_entry,
  schema_allow=schema_allow,
  ignore_errors=schema_ignore_errors
)

def PrintObjectclassTree(schema,oc_tree,oc_name,level):
#  oc_obj = schema.get_schema_element(oc_name)
#  assert oc_obj!=None
  print '    '*level,'+---'*(level>0),oc_name
  for sub_oc_name in oc_tree[oc_name]:
    print '    '*(level+1),'|'
    PrintObjectclassTree(schema,oc_tree,sub_oc_name,level+1)

objectclass_tree = schema.objectclass_tree(ignore_errors=0)
print '*** Object class tree ***'
print

PrintObjectclassTree(schema,objectclass_tree,'top',0)
