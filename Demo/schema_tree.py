"""
Outputs the object class tree read from LDAPv3 schema
of a given server

Usage: schema_oc_tree.py [--html] [LDAP URL]
"""

import sys,getopt,ldap,ldap.schema,ldapurl


schema_allow = ldap.schema.ALLOW_ALL
schema_ignore_errors = 0


def PrintSchemaTree(schema,se_tree,se_name,level):
  """ASCII text output for console"""
  se_obj = schema.get_schema_element(se_name)
  if se_obj!=None:
    print '|    '*(level-1)+'+---'*(level>0), \
          se_name, \
          '(%s)' % se_obj.oid
  for sub_se_name in se_tree[se_name]:
    print '|    '*(level+1)
    PrintSchemaTree(schema,se_tree,sub_se_name,level+1)


def HTMLSchemaTree(schema,se_tree,se_name,level):
  """HTML output for browser"""
  se_obj = schema.get_schema_element(se_name)
  if se_obj!=None:
    print """
    <dt><strong>%s</strong></dt>
    <dd>
      OID: %s<br>
      Description: &quot;%s&quot;
    """ % (se_name,se_obj.oid,se_obj.desc)
  if se_tree[se_name]:
    print '<dl>'
    for sub_se_name in se_tree[se_name]:
      HTMLSchemaTree(schema,se_tree,sub_se_name,level+1)
    print '</dl>'
  print '</dd>'


ldap_url = ldapurl.LDAPUrl(sys.argv[-1])

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
  subschemasubentry_dn,attrs=['objectClasses','attributeTypes']
)

# Parse the schema entry
schema = ldap.schema.SubSchema(
  subschemasubentry_entry,
  schema_allow=schema_allow,
  ignore_errors=schema_ignore_errors
)

try:
  options,args=getopt.getopt(sys.argv[1:],'',['html'])
except getopt.error,e:
  print 'Error: %s\nUsage: schema_oc_tree.py [--html] [LDAP URL]'

html_output = options and options[0][0]=='--html'

oc_tree = schema.schema_element_tree(
  ldap.schema.ObjectClass,ignore_errors=schema_ignore_errors
)
at_tree = schema.schema_element_tree(
  ldap.schema.AttributeType,ignore_errors=schema_ignore_errors
)

if html_output:


  print """<html>
<head>
  <title>Object class tree</title>
</head>
<body bgcolor="#ffffff">
<h1>Object class tree</h1>
<dl>
"""
  HTMLSchemaTree(schema,oc_tree,'top',0)
  print """</dl>
<h1>Attribute type tree</h1>
<dl>
"""
  HTMLSchemaTree(schema,at_tree,'_',0)
  print """</dl>
</body>
</html>
"""

else:

  print '*** Object class tree ***\n'
  print
  PrintSchemaTree(schema,oc_tree,'top',0)

  print '\n*** Attribute types tree ***\n'
  PrintSchemaTree(schema,at_tree,'_',0)
