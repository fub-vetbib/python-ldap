"""
ldap.schema.subentry -  subschema subentry
written by Michael Stroeder <michael@stroeder.com>

\$Id$
"""

import ldap.cidict,ldap.schema

from ldap.schema.models import *

from UserDict import UserDict

SCHEMA_CLASS_MAPPING = ldap.cidict.cidict()

for _name in dir():
  o = eval(_name)
  if hasattr(o,'schema_attribute'):
    SCHEMA_CLASS_MAPPING[o.schema_attribute] = o

SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()

# Create the reverse of SCHEMA_CLASS_MAPPING
SCHEMA_ATTR_MAPPING = {}
for k in SCHEMA_ATTRS:
  SCHEMA_ATTR_MAPPING[SCHEMA_CLASS_MAPPING[k]] = k


class SubSchema(UserDict):
    
    def __init__(self,sub_schema_sub_entry):
        """
        sub_schema_sub_entry
            Dictionary containing the sub schema sub entry
        """
        # Initialize all dictionaries
        UserDict.__init__(self,{})
        self.name2oid = {}
        self.sed_class = {}
        for c in SCHEMA_CLASS_MAPPING.values():
          self.name2oid[c] = ldap.cidict.cidict()
          self.sed_class[c] = {}

        e = ldap.cidict.cidict(sub_schema_sub_entry)

        # Build the schema registry
        for attr_type in SCHEMA_ATTRS:
          if not e.has_key(attr_type) or \
             not e[attr_type]:
            continue
          for attr_value in e[attr_type]:
            se_class = SCHEMA_CLASS_MAPPING[attr_type]
            se_instance = se_class(attr_value)
            self[se_instance.oid] = se_instance
            if hasattr(se_instance,'names'):
              for name in se_instance.names:
                self.name2oid[se_class][name] = se_instance.oid
        return # subSchema.__init__()        

    def __setitem__(self,oid,element_instance):
      self.data[oid] = element_instance
      self.sed_class[element_instance.__class__][oid] = None

    def ldap_entry(self):
      """
      Returns a dictionary containing the sub schema sub entry
      """
      # Initialize the dictionary with empty lists
      entry = {}
      # Collect the schema elements and store them in
      # entry's attributes
      for se in self.values():
        se_str = str(se)
        try:
          entry[SCHEMA_ATTR_MAPPING[se.__class__]].append(se_str)
        except KeyError:
          entry[SCHEMA_ATTR_MAPPING[se.__class__]] = [ se_str ]
      return entry

    def listall(self,schema_element_class):
      """
      Returns a list of OIDs of all available schema
      elements of a given schema element class.
      
      """
      return self.sed_class[schema_element_class].keys()

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
        se_obj = self[se_oid]
        if se_obj.__class__!=schema_element_class:
          # Ignore schema elements not matching schema_element_class.
          # This helps with falsely assigned OIDs.
          continue
        assert se_obj.__class__==schema_element_class, \
          "Schema element referenced by %s must be of class %s but was %s" % (
            se_oid,schema_element_class.__name__,se_obj.__class__
          )
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

    def get_obj(self,se_class,nameoroid,default=None):
      """
      Get a schema element by name or OID
      """
      return self.get(self.getoid(se_class,nameoroid),default)

    def get_syntax(self,nameoroid):
      """
      Get the syntax of an attribute type specified by name or OID
      """
      at_oid = self.getoid(AttributeType,nameoroid)
      try:
        at_obj = self[at_oid]
      except KeyError:
        return None
      if at_obj.syntax:
        return at_obj.syntax
      elif at_obj.sup:
        for sup in at_obj.sup:
          syntax = self.get_syntax(sup)
          if syntax:
            return syntax
      return None

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
          object_class = self[object_class_oid]
        except KeyError:
          if raise_keyerror:
            raise
          # Ignore this object class
          continue
        if object_class.__class__!=ObjectClass:
          # Check if we really have an ObjectClass instance
          continue
        assert hasattr(object_class,'must'),ValueError(object_class_oid)
        assert hasattr(object_class,'may'),ValueError(object_class_oid)
        for a in object_class.must:
          try:
            at_obj = self[self.name2oid[AttributeType][a]]
          except KeyError:
            if raise_keyerror:
              raise
          r_must[at_obj.oid] = at_obj
        for a in object_class.may:
          try:
            at_obj = self[self.name2oid[AttributeType][a]]
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
            if self.has_key(a):
              for afk,afv in attr_type_filter:
                schema_attr_type = self[a]
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
