"""
Outputs the object class tree read from LDAPv3 schema
of a given server

Usage: schema_oc_tree.py [--html] [LDAP URL]
"""

import sys,getopt,ldap,ldap.schema


def PrintSchemaTree(schema,se_class,se_tree,se_oid,level):
  """ASCII text output for console"""
  se_obj = schema.schema_element.get(se_oid,None)
  if se_obj!=None:
    print '|    '*(level-1)+'+---'*(level>0), \
          ', '.join(se_obj.names), \
          '(%s)' % se_obj.oid
  for sub_se_oid in se_tree[se_oid]:
    print '|    '*(level+1)
    PrintSchemaTree(schema,se_class,se_tree,sub_se_oid,level+1)


def HTMLSchemaTree(schema,se_class,se_tree,se_oid,level):
  """HTML output for browser"""
  se_obj = schema.get_schema_element(se_class,se_oid)
  if se_obj!=None:
    print """
    <dt><strong>%s</strong></dt>
    <dd>
      OID: %s<br>
      Description: &quot;%s&quot;
    """ % (se_oid,se_obj.oid,se_obj.desc)
  if se_tree[se_oid]:
    print '<dl>'
    for sub_se_oid in se_tree[se_oid]:
      HTMLSchemaTree(schema,se_class,se_tree,sub_se_oid,level+1)
    print '</dl>'
  print '</dd>'


ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)

ldap._trace_level = 0

subschemasubentry_dn,schema = ldap.schema.urlfetch(sys.argv[-1])

if subschemasubentry_dn is None:
  print 'No sub schema sub entry found!'
  sys.exit(1)

try:
  options,args=getopt.getopt(sys.argv[1:],'',['html'])
except getopt.error,e:
  print 'Error: %s\nUsage: schema_oc_tree.py [--html] [LDAP URL]'

html_output = options and options[0][0]=='--html'

oc_tree = schema.schema_element_tree(ldap.schema.ObjectClass)
at_tree = schema.schema_element_tree(ldap.schema.AttributeType)

#for k,v in oc_tree.items():
#  print k,'->',v
#for k,v in at_tree.items():
#  print k,'->',v

if html_output:

  print """<html>
<head>
  <title>Object class tree</title>
</head>
<body bgcolor="#ffffff">
<h1>Object class tree</h1>
<dl>
"""
  HTMLSchemaTree(schema,ldap.schema.ObjectClass,oc_tree,'2.5.6.0',0)
  print """</dl>
<h1>Attribute type tree</h1>
<dl>
"""
  HTMLSchemaTree(schema,ldap.schema.AttributeType,at_tree,'_',0)
  print """</dl>
</body>
</html>
"""

else:

  print '*** Object class tree ***\n'
  print
  PrintSchemaTree(schema,ldap.schema.ObjectClass,oc_tree,'2.5.6.0',0)

  print '\n*** Attribute types tree ***\n'
  PrintSchemaTree(schema,ldap.schema.AttributeType,at_tree,'_',0)
