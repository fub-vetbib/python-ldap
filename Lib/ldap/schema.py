"""
schema.py - support for subSchemaSubEntry information
written by Hans Aschauer <Hans.Aschauer@Physik.uni-muenchen.de>
modified by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.
"""

__version__ = '0.1.0'


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


class SchemaError(Exception): pass

class SCHERR_OUTOFMEM(SchemaError): pass

class SCHERR_UNEXPTOKEN(SchemaError): pass

class SCHERR_NOLEFTPAREN(SchemaError): pass

class SCHERR_NORIGHTPAREN(SchemaError): pass

class SCHERR_NODIGIT(SchemaError): pass

class SCHERR_BADNAME(SchemaError): pass

class SCHERR_BADDESC(SchemaError): pass

class SCHERR_BADSUP(SchemaError): pass

class SCHERR_DUPOPT(SchemaError): pass

class SCHERR_EMPTY(SchemaError): pass


ERRCODE2SCHERR = {
    1:SCHERR_OUTOFMEM,
    2:SCHERR_UNEXPTOKEN,
    3:SCHERR_NOLEFTPAREN,
    4:SCHERR_NORIGHTPAREN,
    5:SCHERR_NODIGIT,
    6:SCHERR_BADNAME,
    7:SCHERR_BADDESC,
    8:SCHERR_BADSUP,
    9:SCHERR_DUPOPT,
   10:SCHERR_EMPTY
}


def schema_func_wrapper(func,schema_element_str,schema_allow=0):
  """
  Wrapper functions to serialize calls into OpenLDAP libs with       
  a module-wide thread lock and correct error handling. The schema   
  parsing functions return an integer in case of an error; in this   
  case we raise the appropriate exception. If everything is ok, they 
  return a tuple, which we return to the caller.
  """

  def parse_oid(schema_element_str):
    name_pos = schema_element_str.find('NAME',1)
    if name_pos==-1:
      SCHERR_UNEXPTOKEN(2,schema_element_str)
    oid = schema_element_str[1:name_pos].strip()
    s = '( 0.0.0.0.0.0.0.0.0.0.0.0.0 '+schema_element_str[name_pos:]
    return oid,s

  if schema_allow==ALLOW_ALL:
    # This is a work-around as long as OpenLDAP libs
    # does not accept non-numeric OID
    oid, fake_str = parse_oid(schema_element_str)
    res = ldap.functions._ldap_function_call(
      func,fake_str,schema_allow
    )
    if type(res)==type(0):
      raise ERRCODE2SCHERR.get(res,SchemaError)(res,schema_element_str)
    else:
      assert type(res)==type([])
      res[0] = oid
      return res
  else:
    # This is the normal code
    res = ldap.functions._ldap_function_call(
      func,schema_element_str,schema_allow
    )
    if type(res)==type(0):
      raise ERRCODE2SCHERR.get(res,SchemaError)(res,schema_element_str)
    else:
      assert type(res)==type([])
      return res


# Wrapper functions to serialize calls into OpenLDAP libs with
# a module-wide thread lock
def str2objectclass(schema_element_str,schema_allow=0):
  return schema_func_wrapper(_ldap.str2objectclass,schema_element_str,schema_allow)

def str2attributetype(schema_element_str,schema_allow=0):
  return schema_func_wrapper(_ldap.str2attributetype,schema_element_str,schema_allow)

def str2syntax(schema_element_str,schema_allow=0):
  return schema_func_wrapper(_ldap.str2syntax,schema_element_str,schema_allow)

def str2matchingrule(schema_element_str,schema_allow=0):
  return schema_func_wrapper(_ldap.str2matchingrule,schema_element_str,schema_allow)


def key_attr(key,value,quoted=0):
  assert type(value)==type(''),TypeError("value has to be of StringType")
  if value:
    if quoted:
      return ' %s %s' % (key,repr(value))
    else:
      return ' %s %s' % (key,value)
  else:
    return ''

def key_list(key,values,sep=' ',quoted=0):
  assert type(values)==type([]),TypeError("values has to be of ListType")
  if quoted:
    quoted_values = [repr(n) for n in values]
  else:
    quoted_values = values
  if not values:
    return ''
  elif len(values)==1:
    return ' %s %s' % (key,quoted_values[0])
  else:
    return ' %s ( %s )' % (key,sep.join(quoted_values))


class ObjectClass:

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
      assert self.oid!=None,ValueError("%s.oid is None" % (self.__class__.__name__))
      assert self.names,ValueError("%s.names empty" % (self.__class__.__name__))
      return # ObjectClass.__init__()

    def __str__(self):
      result = [str(self.oid)]
      result.append(key_list('NAME',self.names,quoted=1))
      result.append(key_attr('DESC',self.desc,quoted=1))
      result.append(key_list('SUP',self.sup))
      result.append({0:'',1:' OBSOLETE'}[self.obsolete])
      result.append({0:' ABSTRACT',1:' STRUCTURAL',2:' AUXILIARY'}[self.kind])
      result.append(key_list('MUST',self.must,sep=' $ '))
      result.append(key_list('MAY',self.may,sep=' $ '))
      return '( %s )' % ''.join(result)


class AttributeType:

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
         self.collective,      #0=no, 1=yes
         self.no_user_mod,     #0=no, 1=yes
         self.usage,           #0=userApplications, 1=directoryOperation,
                               #2=distributedOperation, 3=dSAOperation
         self.ext              #OPTIONAL
         ) = str2attributetype(schema_element_str,schema_allow)

    def __str__(self):
      result = [str(self.oid)]
      result.append(key_list('NAME',self.names,quoted=1))
      result.append(key_attr('DESC',self.desc,quoted=1))
      result.append(key_attr('SUP',self.sup_oid))
      result.append({0:'',1:' OBSOLETE'}[self.obsolete])
      result.append(key_attr('EQUALITY',self.equality_oid))
      result.append(key_attr('ORDERING',self.ordering_oid))
      result.append(key_attr('SUBSTR',self.substr_oid))
      result.append(key_attr('SYNTAX',self.syntax_oid))
      result.append(('{%d}' % (self.syntax_len))*(self.syntax_len>0))
      result.append({0:'',1:' SINGLE-VALUE'}[self.single_value])
      result.append({0:'',1:' COLLECTIVE'}[self.collective])
      result.append({0:'',1:' NO-USER-MODIFICATION'}[self.no_user_mod])
      result.append(
        {
          0:"",
          1:" USAGE directoryOperation",
          2:" USAGE distributedOperation",
          3:" USAGE dSAOperation",
        }[self.usage]
      )
      return '( %s )' % ''.join(result)


class LDAPSyntax:

    def __init__(self, schema_element_str,schema_allow=0):
        (self.oid,    #REQUIRED
         self.names,  #OPTIONAL
         self.desc,   #OPTIONAL
         self.ext     #OPTIONAL
         ) = str2syntax(schema_element_str,schema_allow)

    def __str__(self):
      result = [str(self.oid)]
      result.append(key_list('NAME',self.names,quoted=1))
      result.append(key_attr('DESC',self.desc,quoted=1))
      return '( %s )' % ''.join(result)


class MatchingRule:

    def __init__(self, schema_element_str,schema_allow=0):
        (self.oid,         #REQUIRED
         self.names,       #OPTIONAL
         self.desc,        #OPTIONAL
         self.obsolete,    #OPTIONAL
         self.syntax_oid,  #REQUIRED
         self.ext          #OPTIONAL
         ) = str2matchingrule(schema_element_str,schema_allow)

    def __str__(self):
      result = [str(self.oid)]
      result.append(key_list('NAME',self.names,quoted=1))
      result.append(key_attr('DESC',self.desc,quoted=1))
      result.append({0:'',1:' OBSOLETE'}[self.obsolete])
      result.append(key_attr('SYNTAX',self.syntax_oid))
      return '( %s )' % ''.join(result)


SCHEMA_CLASS_MAPPING = {
  'objectClasses':ObjectClass,
  'attributeTypes':AttributeType,
  'ldapSyntaxes':LDAPSyntax,
  'matchingRules':MatchingRule
}
SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()

# Create the reverse of SCHEMA_CLASS_MAPPING
SCHEMA_ATTR_MAPPING = {}
for k in SCHEMA_ATTRS:
  SCHEMA_ATTR_MAPPING[SCHEMA_CLASS_MAPPING[k]] = k

class SubSchema:
    
    def __init__(self,sub_schema_sub_entry,schema_allow=0,ignore_errors=0):
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
            try:
              se = SCHEMA_CLASS_MAPPING[attr_type](attr_value,schema_allow)
            except SchemaError:
              if not ignore_errors:
                raise
            else:
              self.schema_element[se.oid] = se
              for name in se.names:
                self.name2oid[name] = se.oid

        return # subSchema.__init__()        

    def entryDict(self):
      """
      Returns a dictionary containing the sub schema sub entry
      """
      # Initialize the dictionary with empty lists
      entry = {
        'objectClasses':[],
        'attributeTypes':[],
        'ldapSyntaxes':[],
        'matchingRules':[]
      }
      # Collect the schema elements and store them in
      # entry's attributes
      for se in self.schema_element.values():
        entry[SCHEMA_ATTR_MAPPING[se.__class__]].append(str(se))
      # Remove empty attribute lists
      for k in entry.keys():
        if not entry[k]:
          del entry[k]
      return entry

    def avail_objectclasses(self):
      """
      Returns a list of all available object classes by first name.
      """
      return [
        se.names[0]
        for se in self.schema_element.values()
        if se.__class__==ObjectClass
      ]

    def all_attrs(self,object_class_list,attr_type_filter={}):
      """
      Return a 2-tuple of all must and may attributes including
      all inherited attributes of superior object classes.
      by walking up classes along the SUP attribute

      object_class_list
          list of strings specifying object class names or OIDs
      attr_type_filter
          list of 2-tuples containing lists of class attributes
          which has to be matched
      """
      oid_cache = {}
      object_class_oids = [
        self.name2oid.get(o,o) for o in object_class_list
      ]
      r_must,r_may = ldap.cidict.cidict(),ldap.cidict.cidict()
      while object_class_oids:
        object_class_oid = object_class_oids.pop(0)
        # Check whether the objectClass with this OID
        # has already been processed
        if oid_cache.has_key(object_class_oid):
          continue
        # Cache this OID as already being processed
        oid_cache[object_class_oid] = None
        object_class = self.schema_element[object_class_oid]
        for a in object_class.must:
          r_must[a] = a
        for a in object_class.may:
          r_may[a] = a
        object_class_oids.extend([
          self.name2oid.get(s,s)
          for s in object_class.sup
        ])
      # Removed all mandantory attribute types from
      # optional attribute type list
      for a in r_may.keys():
        if r_must.has_key(a):
          del r_may[a]
      # Apply attr_type_filter to results
      if attr_type_filter:
        for l in [r_must,r_may]:
          for a in l.keys():
            if self.name2oid.has_key(a):
              for afk,afv in attr_type_filter:
                schema_attr_type = self.schema_element[self.name2oid[a]]
                if not getattr(schema_attr_type,afk) in afv:
                  del l[a]
                  break
            else:
              raise KeyError,'No schema element found with name %s' % (a)
      return r_must.values(),r_may.values()

