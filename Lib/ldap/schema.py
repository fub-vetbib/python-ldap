"""
schema.py - support for subSchemaSubEntry information
written by Hans Aschauer <Hans.Aschauer@Physik.uni-muenchen.de>,
modified by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.
"""

__version__ = '0.1.0'


import ldap,ldap.cidict,ldap.functions,_ldap


class SchemaError(Exception):
  """
  Base class for exceptions raised if a schema error is detected.
  """


StringType=type('')

NOT_HUMAN_READABLE_LDAP_SYNTAXES = {
  '1.3.6.1.4.1.1466.115.121.1.4':None,
  '1.3.6.1.4.1.1466.115.121.1.5':None,
  '1.3.6.1.4.1.1466.115.121.1.6':None,
  '1.3.6.1.4.1.1466.115.121.1.8':None,
  '1.3.6.1.4.1.1466.115.121.1.9':None,
  '1.3.6.1.4.1.1466.115.121.1.10':None,
  '1.3.6.1.4.1.1466.115.121.1.28':None,
  '1.3.6.1.4.1.1466.115.121.1.40':None,
  '1.3.6.1.4.1.1466.115.121.1.49':None,
}

def split_tokens(s):
  """
  Returns list of syntax elements with quotes and spaces
  stripped.
  """
  result = []
  s_len = len(s)
  i = 0
  while i<s_len:
    start = i
    while i<s_len and s[i]!="'":
      if s[i]=="(" or s[i]==")":
        result.append(s[i])
        i +=1 # Consume parentheses
        start = i
      elif s[i]==" ":
        if i>start:
          result.append(s[start:i])
        # Consume space chars
        while i<s_len and s[i]==" ":
          i +=1
        start = i
      else:
        i +=1
    if i>start:
      result.append(s[start:i])
    i +=1
    if i>=s_len:
      break
    start = i
    while i<s_len and s[i]!="'":
      i +=1
    if i>=start:
      result.append(s[start:i])
    i +=1
  return result # split_tokens()


def extract_tokens(l,known_tokens={}):
  """
  Returns dictionary of known tokens with all values
  """
  assert l[0].strip()=="(" and l[-1].strip()==")",ValueError(repr(s),l)
  result = known_tokens
  i = 0
  l_len = len(l)
  while i<l_len:
    if result.has_key(l[i]):
      token = l[i]
      i += 1 # Consume token
      if i<l_len:
        if result.has_key(l[i]):
          # non-valued
          result[token] = []
        elif l[i]=="(":
          # multi-valued
          i += 1 # Consume left parentheses
          start = i
          while i<l_len and l[i]!=")":
            i += 1
          result[token] = l[start:i]
          i += 1 # Consume right parentheses
        else:
          # single-valued
          result[token] = [l[i]]
          i += 1 # Consume single value
    else:
      i += 1 # Consume unrecognized item
  return result


def key_attr(key,value,quoted=0):
  assert value is None or type(value)==type(''),TypeError("value has to be of StringType, was %s" % repr(value))
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

  def __init__(
    self,schema_element_str=None,
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
      l = ldap.schema.split_tokens(schema_element_str)
      d = ldap.schema.extract_tokens(
        l,
        {'NAME':[],'DESC':[None],'OBSOLETE':None,'SUP':[],
         'STRUCTURAL':None,'AUXILIARY':None,'ABSTRACT':None,
         'MUST':[],'MAY':[]}
      )
      self.oid = l[1]
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
    result.append(key_list('NAME',self.names,quoted=1))
    result.append(key_attr('DESC',self.desc,quoted=1))
    result.append(key_list('SUP',self.sup))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append({0:' STRUCTURAL',1:' ABSTRACT',2:' AUXILIARY'}[self.kind])
    result.append(key_list('MUST',self.must,sep=' $ '))
    result.append(key_list('MAY',self.may,sep=' $ '))
    return '( %s )' % ''.join(result)


AttributeUsage = ldap.cidict.cidict({
  'userApplication':0,
  'userApplications':0,
  'directoryOperation':1,
  'distributedOperation':2,
  'dSAOperation':3,
})


class AttributeType:
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

  def __init__(self, schema_element_str):
    if schema_element_str:
      l = ldap.schema.split_tokens(schema_element_str)
      d = ldap.schema.extract_tokens(
        l,
        {
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
      )
      self.oid = l[1]
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
      self.usage = AttributeUsage[d['USAGE'][0]]
    assert self.oid!=None,ValueError("%s.oid is None" % (self.__class__.__name__))
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (self.obsolete==0 or self.obsolete==1)
    assert type(self.sup)==type([])
    assert self.syntax is None or type(self.syntax)==type('')
    assert self.syntax_len is None or type(self.syntax_len)==type(0L)

  def __str__(self):
    result = [str(self.oid)]
    result.append(key_list('NAME',self.names,quoted=1))
    result.append(key_attr('DESC',self.desc,quoted=1))
    result.append(key_list('SUP',self.sup))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(key_attr('EQUALITY',self.equality))
    result.append(key_attr('ORDERING',self.ordering))
    result.append(key_attr('SUBSTR',self.substr))
    result.append(key_attr('SYNTAX',self.syntax))
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


class LDAPSyntax:
  """
      SyntaxDescription = "(" whsp
          numericoid whsp
          [ "DESC" qdstring ]
          whsp ")"
  """

  def __init__(self, schema_element_str):
    if schema_element_str:
      l = ldap.schema.split_tokens(schema_element_str)
      d = ldap.schema.extract_tokens(
        l,
        {
          'DESC':[None],
          'X-NOT-HUMAN-READABLE':[None],
        }
      )
      self.oid = l[1]
      self.desc = d['DESC'][0]
      self.not_human_readable = \
        NOT_HUMAN_READABLE_LDAP_SYNTAXES.has_key(self.oid) or \
        d['X-NOT-HUMAN-READABLE'][0]=='TRUE'
                                  
  def __str__(self):
    result = [str(self.oid)]
    result.append(key_attr('DESC',self.desc,quoted=1))
    result.append(
      {0:'',1:" X-NOT-HUMAN-READABLE 'TRUE'"}[self.not_human_readable]
    )
    return '( %s )' % ''.join(result)


class MatchingRule:
  """
      MatchingRuleDescription = "(" whsp
          numericoid whsp  ; MatchingRule identifier
          [ "NAME" qdescrs ]
          [ "DESC" qdstring ]
          [ "OBSOLETE" whsp ]
          "SYNTAX" numericoid
      whsp ")"
  """

  def __init__(self, schema_element_str):
    l = ldap.schema.split_tokens(schema_element_str)
    d = ldap.schema.extract_tokens(
      l,
      {
         'NAME':[],
         'DESC':[None],
         'OBSOLETE':None,
         'SYNTAX':[None],
         'APPLIES':[None],
      }
    )
    self.oid = l[1]
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.obsolete = d['OBSOLETE']!=None
    self.syntax = d['SYNTAX'][0]
    self.applies = d['APPLIES'][0]
    assert self.oid!=None,ValueError("%s.oid is None" % (self.__class__.__name__))
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (self.obsolete==0 or self.obsolete==1)
    assert self.syntax is None or type(self.syntax)==type('')

  def __str__(self):
    result = [str(self.oid)]
    result.append(key_list('NAME',self.names,quoted=1))
    result.append(key_attr('DESC',self.desc,quoted=1))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(key_attr('SYNTAX',self.syntax))
    return '( %s )' % ''.join(result)


class MatchingRuleUse:
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

  def __init__(self, schema_element_str):
    l = ldap.schema.split_tokens(schema_element_str)
    d = ldap.schema.extract_tokens(
      l,
      {
         'NAME':[],
         'DESC':[None],
         'OBSOLETE':None,
         'APPLIES':[],
      }
    )
    self.oid = l[1]
    self.names = d['NAME']
    self.desc = d['DESC'][0]
    self.obsolete = d['OBSOLETE']!=None
    self.applies = d['APPLIES']
    assert self.oid!=None,ValueError("%s.oid is None" % (self.__class__.__name__))
    assert type(self.names)==type([])
    assert self.desc is None or type(self.desc)==type('')
    assert type(self.obsolete)==type(0) and (type(self.obsolete)==0 or type(self.obsolete)==1)
    assert type(self.self.applies)==type([])

  def __str__(self):
    result = [str(self.oid)]
    result.append(key_list('NAME',self.names,quoted=1))
    result.append(key_attr('DESC',self.desc,quoted=1))
    result.append({0:'',1:' OBSOLETE'}[self.obsolete])
    result.append(key_attr('SYNTAX',self.syntax))
    return '( %s )' % ''.join(result)


class Entry(ldap.cidict.cidict):

  def __init__(self,sub_schema,entry={}):
    ldap.cidict.cidict.__init__(self)
    for k,v in entry.items():
      try:
        self[sub_schema.name2oid[AttributeType][k]] = v
      except KeyError:
        self[k] = v


SCHEMA_CLASS_MAPPING = {
  'objectClasses':ObjectClass,
  'attributeTypes':AttributeType,
  'ldapSyntaxes':LDAPSyntax,
  'matchingRules':MatchingRule,
  'matchingRulesUse':MatchingRuleUse,
}
SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()

# Create the reverse of SCHEMA_CLASS_MAPPING
SCHEMA_ATTR_MAPPING = {}
for k in SCHEMA_ATTRS:
  SCHEMA_ATTR_MAPPING[SCHEMA_CLASS_MAPPING[k]] = k


class SubSchema:
    
    def __init__(self,sub_schema_sub_entry):
        """
        sub_schema_sub_entry
            Dictionary containing the sub schema sub entry
        """
        self.sed = {}
        self.name2oid = {
          ObjectClass:ldap.cidict.cidict(),
          AttributeType:ldap.cidict.cidict(),
          LDAPSyntax:ldap.cidict.cidict(),
          MatchingRule:ldap.cidict.cidict(),
        }
        e = ldap.cidict.cidict(sub_schema_sub_entry)

        # Build the schema registry
        for attr_type in SCHEMA_ATTRS:
          if not e.has_key(attr_type) or \
             not e[attr_type]:
            continue
          for attr_value in e[attr_type]:
            se_class = SCHEMA_CLASS_MAPPING[attr_type]
            se_instance = se_class(attr_value)
            self.sed[se_instance.oid] = se_instance
            if hasattr(se_instance,'names'):
              for name in se_instance.names:
                self.name2oid[se_class][name] = se_instance.oid
        return # subSchema.__init__()        

    def ldap_entry(self):
      """
      Returns a dictionary containing the sub schema sub entry
      """
      # Initialize the dictionary with empty lists
      entry = {}
      # Collect the schema elements and store them in
      # entry's attributes
      for se in self.sed.values():
        se_str = str(se)
        try:
          entry[SCHEMA_ATTR_MAPPING[se.__class__]].append(se_str)
        except KeyError:
          entry[SCHEMA_ATTR_MAPPING[se.__class__]] = [ se_str ]
      return entry

    def listall(self,schema_element_class):
      """
      Returns a list of all available schema elements by first name
      of a given class.
      """
      result = [
        oid
        for oid in self.sed.keys()
        if isinstance(self.sed[oid],schema_element_class)
      ]
      return result

    def tree(self,schema_element_class):
      """
      Returns a ldap.cidict.cidict dictionary representing the
      tree structure of the schema elements.
      """
      assert schema_element_class in [ObjectClass,AttributeType]
      avail_se = self.listall(schema_element_class)
      top_node = {0:'_',1:'2.5.6.0'}[schema_element_class==ObjectClass]
      tree = ldap.cidict.cidict({top_node:[]})
      # 1. Pass: Register all nodes
      for se in avail_se:
        tree[se] = []
      # 2. Pass: Register all sup references
      for se_oid in avail_se:
        se_obj = self.sed[se_oid]
        for s in se_obj.sup:
          sup_oid = self.name2oid[schema_element_class].get(s,s)
          tree[sup_oid].append(se_oid)
      return tree

    def getoid(self,se_class,nameoroid):
      """
      Get an OID by name or OID
      """
      se_oid = nameoroid.split(';')[0].strip()
      return self.name2oid[se_class].get(se_oid,se_oid)

    def get(self,se_class,nameoroid,default=None):
      """
      Get a schema element by name or OID
      """
      return self.sed.get(self.getoid(se_class,nameoroid),default)

    def attribute_types(
      self,object_class_list,attr_type_filter={},strict=1,raise_keyerror=1
    ):
      """
      Returns a 2-tuple of all must and may attributes including
      all inherited attributes of superior object classes
      by walking up classes along the SUP attribute.
      
      The attributes are stored in a ldap.cidict.cidict dictionary.

      object_class_list
          list of strings specifying object class names or OIDs
      attr_type_filter
          list of 2-tuples containing lists of class attributes
          which has to be matched
      """
      # Map object_class_list to object_class_oids (list of OIDs)
      object_class_oids = [
        self.name2oid[ObjectClass].get(o,o)
        for o in object_class_list
      ]
      # Initialize
      oid_cache = {}
      r_must,r_may = ldap.cidict.cidict(),ldap.cidict.cidict()
      while object_class_oids:
        object_class_oid = object_class_oids.pop(0)
        # Check whether the objectClass with this OID
        # has already been processed
        if oid_cache.has_key(object_class_oid):
          continue
        # Cache this OID as already being processed
        oid_cache[object_class_oid] = None
        try:
          object_class = self.sed[object_class_oid]
        except KeyError:
          if raise_keyerror:
            raise
          # Ignore this object class
          continue
        assert hasattr(object_class,'must'),ValueError(object_class_oid)
        assert hasattr(object_class,'may'),ValueError(object_class_oid)
        for a in object_class.must:
          try:
            at_obj = self.sed[self.name2oid[AttributeType][a]]
          except KeyError:
            if raise_keyerror:
              raise
          r_must[at_obj.oid] = at_obj
        for a in object_class.may:
          try:
            at_obj = self.sed[self.name2oid[AttributeType][a]]
          except KeyError:
            if raise_keyerror:
              raise
            else:
              continue
          r_may[at_obj.oid] = at_obj
        object_class_oids.extend([
          self.name2oid[ObjectClass].get(o,o)
          for o in object_class.sup
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
            if self.sed.has_key(a):
              for afk,afv in attr_type_filter:
                schema_attr_type = self.sed[a]
                try:
                  if not getattr(schema_attr_type,afk) in afv:
                    del l[a]
                    break
                except AttributeError:
                  if raise_keyerror:
                    raise
                  else:
                    try: del l[a]
                    except KeyError: pass
            else:
              raise KeyError,'No schema element found with name %s' % (a)
      return r_must,r_may


def urlfetch(uri,trace_level=0):
  """
  Fetches a parsed schema entry by uri.
  
  If uri is a LDAP URL the LDAP server is queried directly.
  Otherwise uri is assumed to point to a LDIF file which
  is loaded with urllib.
  """
  uri = uri.strip()
  if uri.startswith('ldap:') or uri.startswith('ldaps:') or uri.startswith('ldapi:'):
    import ldapurl
    ldap_url = ldapurl.LDAPUrl(uri)
    l=ldap.initialize(ldap_url.initializeUrl(),trace_level)
    l.protocol_version = ldap.VERSION3
    l.simple_bind_s('','')
    subschemasubentry_dn = l.search_subschemasubentry_s(ldap_url.dn)
    if subschemasubentry_dn is None:
      subschemasubentry_entry = None
    else:
      if ldap_url.attrs is None:
        schema_attrs = SCHEMA_ATTRS
      else:
        schema_attrs = ldap_url.attrs
      subschemasubentry_entry = l.read_subschemasubentry_s(
        subschemasubentry_dn,attrs=schema_attrs
      )
    l.unbind_s()
    del l

  else:
    import urllib,ldif
    ldif_file = urllib.urlopen(uri)
    ldif_parser = ldif.LDIFRecordList(ldif_file,max_entries=1)
    ldif_parser.parse()
    subschemasubentry_dn,subschemasubentry_entry = ldif_parser.all_records[0]

  if subschemasubentry_dn!=None:
    parsed_sub_schema = ldap.schema.SubSchema(subschemasubentry_entry)
  else:
    parsed_sub_schema = None

  return subschemasubentry_dn, parsed_sub_schema
