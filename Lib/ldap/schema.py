"""
schema.py - support for subSchemaSubEntry information
written by Hans Aschauer <Hans.Aschauer@Physik.uni-muenchen.de>

\$Id$

License:
Public domain. Do anything you want with this module.
"""

__version__ = '0.0.2'


import ldap,ldap.functions,_ldap


# Wrapper functions to serialize calls into OpenLDAP libs with
# a module-wide thread lock
def str2objectclass(schema_element_str):
    return ldap.functions._ldap_function_call(_ldap.str2objectclass,schema_element_str)
def str2attributetype(schema_element_str):
    return ldap.functions._ldap_function_call(_ldap.str2attributetype,schema_element_str)
def str2syntax(schema_element_str):
    return ldap.functions._ldap_function_call(_ldap.str2syntax,schema_element_str)
def str2matchingrule(schema_element_str):
    return ldap.functions._ldap_function_call(_ldap.str2matchingrule,schema_element_str)


class objectClass:
    def __init__(self, schema_element_str):
        (self.oid,           #REQUIRED
         self.names,         #OPTIONAL
         self.desc,          #OPTIONAL
         self.obsolete,      #0=no, 1=yes
         self.sup_oids,      #OPTIONAL
         self.kind,          #0=ABSTRACT
         self.oids_must,     #OPTIONAL
         self.oids_may,      #OPTIONAL
         self.ext,           #OPTIONAL
         ) = str2objectclass(schema_element_str)

class attributeType:
    def __init__(self, schema_element_str):
        (self.oid,             #REQUIRED
         self.names,           #OPTIONAL
         self.desc,            #OPTIONAL
         self.obsolete,        #0=no, 1=yes
         self.sup_oid,         #OPTIONAL
         self.equality_oid,    #OPTIONAL
         self.ordering_oid,    #OPTIONAL
         self.substr_oid,      #OPTIONAL
         self.syntax_oid,      #OPTIONAL
         self.syntax_len,      #OPTIONAL
         self.single_value,    #0=no, 1=yes		    
         self.collectiove,     #0=no, 1=yes			    
         self.no_user_mod,     #0=no, 1=yes 			    
         self.usage,           #0=userApplications, 1=directoryOperation,
                               #2=distributedOperation, 3=dSAOperation
         self.ext              #OPTIONAL
         ) = str2attributetype(schema_element_str)

class ldapSyntax:
    def __init__(self, schema_element_str):
        (self.oid,    #REQUIRED
         self.names,  #OPTIONAL
         self.desc,   #OPTIONAL
         self.ext     #OPTIONAL
         ) = str2syntax(schema_element_str)

class matchingRule:
    def __init__(self, schema_element_str):
        (self.oid,         #REQUIRED
         self.names,       #OPTIONAL
         self.desc,        #OPTIONAL
         self.obsolete,    #OPTIONAL
         self.syntax_oid,  #REQUIRED
         self.ext          #OPTIONAL
         ) = str2matchingrule(schema_element_str)


SCHEMA_CLASS_MAPPING = {
  'objectClasses':objectClass,
  'attributeTypes':attributeType,
  'ldapSyntaxes':ldapSyntax,
  'matchingRules':matchingRule
}
SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()


class subSchema:
    
    def __init__(self,l,schema_dn):
        """
        l
                LDAPObject instance
        schema_dn
                Distinguished name of sub schema sub entry to read
        """
        self.schema_element = {}
        self.name2oid = {}
        result = l.search_s(
          schema_dn,
          ldap.SCOPE_BASE,"(objectClass=*)",
          SCHEMA_ATTRS
        )

        if not result:
          # Nothing to do for empty search result
          return

        # Sub schema sub entry's data
        sub_schema_sub_entry = result[0][1]
        # Build the schema registry
        for attr_type in SCHEMA_ATTRS:
          if not sub_schema_sub_entry[attr_type]:
            continue
          for attr_value in sub_schema_sub_entry[attr_type]:
            se = SCHEMA_CLASS_MAPPING[attr_type](attr_value)
            assert not self.schema_element.has_key(se.oid), ValueError
            self.schema_element[se.oid] = se
            for name in se.names:
              self.name2oid[name] = se.oid

        return # subSchema.__init__()        


if __name__ == '__main__':
    l=ldap.initialize('ldap://localhost:1389')
    l.simple_bind_s('','')

    schema = subSchema(l,'cn=Subschema')
    for attr_type,schema_class in SCHEMA_CLASS_MAPPING.items():
      print '***',repr(attr_type),'***'
      for oid,se in schema.schema_element.items():
        if isinstance(se,schema_class):
          print repr(oid),repr(se)
    schema_element_names = schema.name2oid.keys()
    schema_element_names.sort()
    for name in schema_element_names:
      print repr(name),'->',repr(schema.name2oid[name])

