"""
schema.py - support for subSchemaSubEntry information
written by Hans Aschauer <Hans.Aschauer@Physik.uni-muenchen.de>
modified by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.
"""

__version__ = '0.0.4'


import ldap,ldap.cidict,ldap.functions,_ldap


# Flags that control how liberal the parsing routines are.

# Allow missing oid
ALLOW_NO_OID = 0x01
# Allow bogus extra quotes
ALLOW_QUOTED = 0x02
# Allow descr instead of OID
ALLOW_DESCR = 0x04
# Allow descr as OID prefix    
ALLOW_DESCR_PREFIX = 0x08
# Allow OID macros in slapd    
ALLOW_OID_MACRO = 0x10

# Combined constants
# Strict parsing
ALLOW_NONE = 0x00
# Be very liberal in parsing
ALLOW_ALL = 0x1f


# Wrapper functions to serialize calls into OpenLDAP libs with
# a module-wide thread lock
def str2objectclass(schema_element_str,schema_allow=0):
    return ldap.functions._ldap_function_call(_ldap.str2objectclass,schema_element_str,schema_allow)

def str2attributetype(schema_element_str,schema_allow=0):
    return ldap.functions._ldap_function_call(_ldap.str2attributetype,schema_element_str,schema_allow)

def str2syntax(schema_element_str,schema_allow=0):
    return ldap.functions._ldap_function_call(_ldap.str2syntax,schema_element_str,schema_allow)

def str2matchingrule(schema_element_str,schema_allow=0):
    return ldap.functions._ldap_function_call(_ldap.str2matchingrule,schema_element_str,schema_allow)


class objectClass:

    def __init__(
      self,schema_element_str=None,schema_allow=0,
      oid=None,#REQUIRED
      names=None,#OPTIONAL
      desc=None,#OPTIONAL
      obsolete=0,#0=no, 1=yes
      sup=[],#OPTIONAL
      kind=1,#0=ABSTRACT
      must=[],#OPTIONAL
      may=[],#OPTIONAL
      ext=None,#OPTIONAL
    ):
      if schema_element_str:
        (
          self.oid,self.names,self.desc,self.obsolete,self.sup,
          self.kind,self.must,self.may,self.ext,
        ) = str2objectclass(schema_element_str,schema_allow)
      else:
        self.oid = oid
        self.names = names
        self.desc = desc
        self.obsolete = obsolete
        self.sup = sup
        self.kind = kind
        self.must = must
        self.may = may
        self.ext = ext

    def all_attrs(self,schema):
      """
      Return a 2-tuple of all must and may attributes including
      all inherited attributes of superior object classes.
      by walking up classes which the SUP
      """
      r_must,r_may = self.must,self.may
      for sup_item in self.sup:
        sup_oid = schema.name2oid.get(sup_item,sup_item)
        sup_all_must,sup_all_may = schema.schema_element[sup_oid].all_attrs(schema)
        r_must = ldap.cidict.strlist_union(
          r_must,sup_all_must
        )
        r_may = ldap.cidict.strlist_union(
          r_may,sup_all_may
        )
      r_may = ldap.cidict.strlist_minus(r_may,r_must)
      return r_must,r_may


class attributeType:

    def __init__(self, schema_element_str,schema_allow=0):
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
         ) = str2attributetype(schema_element_str,schema_allow)


class ldapSyntax:

    def __init__(self, schema_element_str,schema_allow=0):
        (self.oid,    #REQUIRED
         self.names,  #OPTIONAL
         self.desc,   #OPTIONAL
         self.ext     #OPTIONAL
         ) = str2syntax(schema_element_str,schema_allow)


class matchingRule:

    def __init__(self, schema_element_str,schema_allow=0):
        (self.oid,         #REQUIRED
         self.names,       #OPTIONAL
         self.desc,        #OPTIONAL
         self.obsolete,    #OPTIONAL
         self.syntax_oid,  #REQUIRED
         self.ext          #OPTIONAL
         ) = str2matchingrule(schema_element_str,schema_allow)


SCHEMA_CLASS_MAPPING = {
  'objectClasses':objectClass,
  'attributeTypes':attributeType,
  'ldapSyntaxes':ldapSyntax,
  'matchingRules':matchingRule
}
SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()


class subSchema:
    
    def __init__(self,sub_schema_sub_entry,schema_allow=0):
        """
        sub_schema_sub_entry
            Dictionary containing the sub schema sub entry
        schema_allow
            Integer with flags defining workarounds for
            broken schema data
        """
        self.schema_element = {}
        self.name2oid = ldap.cidict.cidict()

        # Build the schema registry
        for attr_type in SCHEMA_ATTRS:
          if not sub_schema_sub_entry.has_key(attr_type) or \
             not sub_schema_sub_entry[attr_type]:
            continue
          for attr_value in sub_schema_sub_entry[attr_type]:
            se = SCHEMA_CLASS_MAPPING[attr_type](attr_value,schema_allow)
            assert not self.schema_element.has_key(se.oid), ValueError
            self.schema_element[se.oid] = se
            for name in se.names:
              self.name2oid[name] = se.oid

        return # subSchema.__init__()        
