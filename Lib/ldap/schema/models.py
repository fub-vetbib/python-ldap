"""
schema.py - support for subSchemaSubEntry information
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$
"""

import ldap.cidict

from ldap.schema.tokenizer import split_tokens,extract_tokens


NOT_HUMAN_READABLE_LDAP_SYNTAXES = {
  '1.3.6.1.4.1.1466.115.121.1.4':None,  # Audio
  '1.3.6.1.4.1.1466.115.121.1.5':None,  # Binary
  '1.3.6.1.4.1.1466.115.121.1.6':None,  # Bit String
  '1.3.6.1.4.1.1466.115.121.1.8':None,  # Certificate
  '1.3.6.1.4.1.1466.115.121.1.9':None,  # Certificate List
  '1.3.6.1.4.1.1466.115.121.1.10':None, # Certificate Pair
  '1.3.6.1.4.1.1466.115.121.1.23':None, # G3 FAX
  '1.3.6.1.4.1.1466.115.121.1.28':None, # JPEG
  '1.3.6.1.4.1.1466.115.121.1.40':None, # Octet String
  '1.3.6.1.4.1.1466.115.121.1.49':None, # Supported Algorithm
}


class SchemaElement:
  """
  Base class for all schema element classes. Not used directly!
  """
  token_defaults = {
    'DESC':[None],
  }
  
  def __init__(self,schema_element_str=None):
    if schema_element_str:
      l = split_tokens(schema_element_str)
      self.oid = l[1]
      assert type(self.oid)==type('')
      d = extract_tokens(l,self.token_defaults)
      self._set_attrs(l,d)

  def _set_attrs(self,l,d):
    self.desc = d['DESC'][0]
    return # SchemaElement.__init__()

  def key_attr(self,key,value,quoted=0):
    assert value is None or type(value)==type(''),TypeError("value has to be of StringType, was %s" % repr(value))
    if value:
      if quoted:
        return ' %s %s' % (key,repr(value))
      else:
        return ' %s %s' % (key,value)
    else:
      return ''

  def key_list(self,key,values,sep=' ',quoted=0):
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

  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    return '( %s )' % ''.join(result)


class ObjectClass(SchemaElement):
  """
  ObjectClassDescription = "(" whsp
      numericoid whsp      ; ObjectClass identifier
      [ "NAME" qdescrs ]
      [ "DESC" qdstring ]
      [ "OBSOLETE" whsp ]
      [ "SUP" oids ]       ; Superior ObjectClasses
      [ ( "ABSTRACT" / "STRUCTURAL" / "AUXILIARY" ) whsp ]
                           ; default structural
      [ "MUST" oids ]      ; AttributeTypes
      [ "MAY" oids ]       ; AttributeTypes
  whsp ")"
  """
  schema_attribute = 'objectClasses'
  token_defaults = {
    'NAME':[],
    'DESC':[None],
    'OBSOLETE':None,
    'SUP':[],
    'STRUCTURAL':None,
    'AUXILIARY':None,
    'ABSTRACT':None,
    'MUST':[],
    'MAY':[]
  }

  def _set_attrs(self,l,d):
    self.obsolete = d['OBSOLETE']!=None
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.sup = [ v for v in d['SUP'] if v!="$"]
    self.must = [ v for v in d['MUST'] if v!="$" ]
    self.may = [ v for v in d['MAY'] if v!="$" ]
    # Default is STRUCTURAL, see RFC2552 or draft-ietf-ldapbis-syntaxes
    self.kind = 0
    if d['ABSTRACT']!=None:
      self.kind = 1
    elif d['AUXILIARY']!=None:
      self.kind = 2
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (self.obsolete==0 or self.obsolete==1)
    assert type(self.sup)==type([])
    assert type(self.kind)==type(0)
    assert type(self.must)==type([])
    assert type(self.may)==type([])
    return # ObjectClass.__init__()

  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_list('NAME',self.names,quoted=1))
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    result.append(self.key_list('SUP',self.sup))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append({0:' STRUCTURAL',1:' ABSTRACT',2:' AUXILIARY'}[self.kind])
    result.append(self.key_list('MUST',self.must,sep=' $ '))
    result.append(self.key_list('MAY',self.may,sep=' $ '))
    return '( %s )' % ''.join(result)


AttributeUsage = ldap.cidict.cidict({
  'userApplication':0,
  'userApplications':0,
  'directoryOperation':1,
  'distributedOperation':2,
  'dSAOperation':3,
})


class AttributeType(SchemaElement):
  """
      AttributeTypeDescription = "(" whsp
            numericoid whsp              ; AttributeType identifier
          [ "NAME" qdescrs ]             ; name used in AttributeType
          [ "DESC" qdstring ]            ; description
          [ "OBSOLETE" whsp ]
          [ "SUP" woid ]                 ; derived from this other
                                         ; AttributeType
          [ "EQUALITY" woid              ; Matching Rule name
          [ "ORDERING" woid              ; Matching Rule name
          [ "SUBSTR" woid ]              ; Matching Rule name
          [ "SYNTAX" whsp noidlen whsp ] ; see section 4.3
          [ "SINGLE-VALUE" whsp ]        ; default multi-valued
          [ "COLLECTIVE" whsp ]          ; default not collective
          [ "NO-USER-MODIFICATION" whsp ]; default user modifiable
          [ "USAGE" whsp AttributeUsage ]; default userApplications
          whsp ")"

      AttributeUsage =
          "userApplications"     /
          "directoryOperation"   /
          "distributedOperation" / ; DSA-shared
          "dSAOperation"          ; DSA-specific, value depends on server
  """
  schema_attribute = 'attributeTypes'
  token_defaults = {
    'NAME':[],
    'DESC':[None],
    'OBSOLETE':None,
    'SUP':[],
    'EQUALITY':[None],
    'ORDERING':[None],
    'SUBSTR':[None],
    'SYNTAX':[None],
    'SINGLE-VALUE':None,
    'COLLECTIVE':None,
    'NO-USER-MODIFICATION':None,
    'USAGE':['userApplications']
  }

  def _set_attrs(self,l,d):
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.obsolete = d['OBSOLETE']!=None
    self.sup = [ v for v in d['SUP'] if v!="$"]
    self.equality = d['EQUALITY'][0]
    self.ordering = d['ORDERING'][0]
    self.substr = d['SUBSTR'][0]
    syntax = d['SYNTAX'][0]
    if syntax is None:
      self.syntax = None
      self.syntax_len = None
    else:
      try:
        self.syntax,syntax_len = d['SYNTAX'][0].split("{")
      except ValueError:
        self.syntax = d['SYNTAX'][0]
        self.syntax_len = None
        for i in l:
          if i.startswith("{") and i.endswith("}"):
            self.syntax_len=long(i[1:-1])
      else:
        self.syntax_len = long(syntax_len[:-1])
    self.single_value = d['SINGLE-VALUE']!=None
    self.collective = d['COLLECTIVE']!=None
    self.no_user_mod = d['NO-USER-MODIFICATION']!=None
    try:
      self.usage = AttributeUsage[d['USAGE'][0]]
    except KeyError:
      raise
    self.usage = AttributeUsage.get(d['USAGE'][0],0)
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.sup)==type([])
    assert type(self.obsolete)==type(0) and (self.obsolete==0 or self.obsolete==1)
    assert type(self.single_value)==type(0) and (self.single_value==0 or self.single_value==1)
    assert type(self.no_user_mod)==type(0) and (self.no_user_mod==0 or self.no_user_mod==1)
    assert self.syntax is None or type(self.syntax)==type('')
    assert self.syntax_len is None or type(self.syntax_len)==type(0L)
    return # AttributeType.__init__()

  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_list('NAME',self.names,quoted=1))
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    result.append(self.key_list('SUP',self.sup))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(self.key_attr('EQUALITY',self.equality))
    result.append(self.key_attr('ORDERING',self.ordering))
    result.append(self.key_attr('SUBSTR',self.substr))
    result.append(self.key_attr('SYNTAX',self.syntax))
    if self.syntax_len!=None:
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


class LDAPSyntax(SchemaElement):
  """
  SyntaxDescription = "(" whsp
      numericoid whsp
      [ "DESC" qdstring ]
      whsp ")"
  """
  schema_attribute = 'ldapSyntaxes'
  token_defaults = {
    'DESC':[None],
    'X-NOT-HUMAN-READABLE':[None],
  }

  def _set_attrs(self,l,d):
    self.desc = d['DESC'][0]
    self.not_human_readable = \
      NOT_HUMAN_READABLE_LDAP_SYNTAXES.has_key(self.oid) or \
      d['X-NOT-HUMAN-READABLE'][0]=='TRUE'
    assert self.desc is None or type(self.desc)==type('')
    return # LDAPSyntax.__init__()
                                  
  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    result.append(
      {0:'',1:" X-NOT-HUMAN-READABLE 'TRUE'"}[self.not_human_readable]
    )
    return '( %s )' % ''.join(result)


class MatchingRule(SchemaElement):
  """
  MatchingRuleDescription = "(" whsp
      numericoid whsp  ; MatchingRule identifier
      [ "NAME" qdescrs ]
      [ "DESC" qdstring ]
      [ "OBSOLETE" whsp ]
      "SYNTAX" numericoid
  whsp ")"
  """
  schema_attribute = 'matchingRules'
  token_defaults = {
    'NAME':[],
    'DESC':[None],
    'OBSOLETE':None,
    'SYNTAX':[None],
    'APPLIES':[None],
  }

  def _set_attrs(self,l,d):
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.obsolete = d['OBSOLETE']!=None
    self.syntax = d['SYNTAX'][0]
    self.applies = d['APPLIES'][0]
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (self.obsolete==0 or self.obsolete==1)
    assert self.syntax is None or type(self.syntax)==type('')
    return # MatchingRule.__init__()

  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_list('NAME',self.names,quoted=1))
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(self.key_attr('SYNTAX',self.syntax))
    return '( %s )' % ''.join(result)


class MatchingRuleUse(SchemaElement):
  """
  MatchingRuleUseDescription = "(" whsp
     numericoid 
     [ space "NAME" space qdescrs ]
     [ space "DESC" space qdstring ]
     [ space "OBSOLETE" ]
     space "APPLIES" space oids    ;  AttributeType identifiers
     extensions
     whsp ")" 
  """
  schema_attribute = 'matchingRuleUses'
  token_defaults = {
       'NAME':[],
       'DESC':[None],
       'OBSOLETE':None,
       'APPLIES':[],
  }

  def _set_attrs(self,l,d):
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.obsolete = d['OBSOLETE']!=None
    self.applies = d['APPLIES']
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (type(self.obsolete)==0 or type(self.obsolete)==1)
    assert type(self.self.applies)==type([])
    return # MatchingRuleUse.__init__()

  def __str__(self):
    result = [str(self.oid)]
    result.append(self.key_list('NAME',self.names,quoted=1))
    result.append(self.key_attr('DESC',self.desc,quoted=1))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(self.key_attr('SYNTAX',self.syntax))
    return '( %s )' % ''.join(result)


class DITStructureRule(SchemaElement):
  """
  DITStructureRuleDescription = LPAREN WSP
      ruleid                     ; rule identifier
      [ SP "NAME" SP qdescrs ]   ; short names
      [ SP "DESC" SP qdstring ]  ; description
      [ SP "OBSOLETE" ]          ; not active
      SP "FORM" SP oid           ; NameForm
      [ SP "SUP" ruleids ]       ; superior rules
      extensions WSP RPAREN      ; extensions

  ruleids = ruleid / LPAREN WSP ruleidlist WSP RPAREN

  ruleidlist = [ ruleid *( SP ruleid ) ]

  ruleid = number
  """
  schema_attribute = 'dITStructureRules'


class DITContentRule(SchemaElement):
  """
  DITContentRuleDescription = LPAREN WSP
      numericoid                 ; object identifer
      [ SP "NAME" SP qdescrs ]   ; short names
      [ SP "DESC" SP qdstring ]  ; description
      [ SP "OBSOLETE" ]          ; not active
      [ SP "AUX" SP oids ]       ; auxiliary object classes
      [ SP "MUST" SP oids ]      ; attribute types
      [ SP "MAY" SP oids ]       ; attribute types
      [ SP "NOT" SP oids ]       ; attribute types
      extensions WSP RPAREN      ; extensions
  """
  schema_attribute = 'dITContentRules'


class NameForm(SchemaElement):
  """
  NameFormDescription = LPAREN WSP
      numericoid                 ; object identifer
      [ SP "NAME" SP qdescrs ]   ; short names
      [ SP "DESC" SP qdstring ]  ; description
      [ SP "OBSOLETE" ]          ; not active
      SP "OC" SP oid             ; structural object class
      SP "MUST" SP oids          ; attribute types
      [ SP "MAY" SP oids ]       ; attribute types
      extensions WSP RPAREN      ; extensions
  """
  schema_attribute = 'nameForms'


class Entry(ldap.cidict.cidict):
  """
  Schema-aware implementation of an LDAP entry class.
  
  Mainly it holds the attributes in a string-keyed dictionary with
  the OID as key.
  """

  def __init__(self,schema,entry=None):
    self._at_oid2name = {}
    self._s = schema
    ldap.cidict.cidict.__init__(self,(entry or {}))

  def _at_oid(self,nameoroid):
    """
    Return OID of attribute type specified in nameoroid or
    nameoroid itself if nameoroid was not found in schema's
    name->OID registry (self._s.name2oid).
    """
    return self._s.getoid(ldap.schema.AttributeType,nameoroid)

  def __getitem__(self,nameoroid):
    return ldap.cidict.cidict.__getitem__(self,self._at_oid(nameoroid))

  def __setitem__(self,nameoroid,schema_obj):
    oid = self._at_oid(nameoroid)
    self._at_oid2name[oid] = nameoroid
    ldap.cidict.cidict.__setitem__(self,oid,schema_obj)

  def __delitem__(self,nameoroid):
    del self.data[self._at_oid(nameoroid)]

  def has_key(self,nameoroid):
    return ldap.cidict.cidict.has_key(self,self._at_oid(nameoroid))

  def get(self,nameoroid,failobj):
    try:
      return self[self._at_oid(nameoroid)]
    except KeyError:
      return failobj

  def keys(self):
    return self._at_oid2name.values()

  def items(self):
    result = []
    for k in self._at_oid2name.values():
      result.append((k,self[k]))
    return result

  def attribute_types(
    self,attr_type_filter=None,strict=1,raise_keyerror=1
  ):
    """
    Convenience wrapper around SubSchema.attribute_types() which
    passes object classes of this particular entry as argument to
    SubSchema.attribute_types()
    """
    return self._s.attribute_types(
      self['objectClass'],attr_type_filter,strict,raise_keyerror
    )
