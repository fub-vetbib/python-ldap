"""
dsml - generate and parse DSMLv1 data (see http://www.dsml.org)
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

$Id$

Python compability note:
Tested with Python 2.0+.
"""

__version__ = '0.5.0'

import string,base64

def list_dict(l):
  """
  return a dictionary with all items of l being the keys of the dictionary
  """
  d = {}
  for i in l:
    d[i]=None
  return d

special_entities = (
  ('&','&amp;'),
  ('<','&lt;'),
  ('"','&quot;'),
  ("'",'&apos;'),
)

def replace_char(s):
  for char,entity in special_entities:
    s = string.replace(s,char,entity)
  return s

class DSMLWriter:

  def __init__(
    self,f,base64_attrs=[],dsml_comment='',indent='    '
  ):
    """
    Parameters:
    f
          File object for output.
    base64_attrs
          Attribute types to be base64-encoded.
    dsml_comment
          Text placed in comment lines behind <dsml:dsml>.
    indent
          String used for indentiation of next nested level.
    """
    self._f = f
    self._base64_attrs = list_dict(map(string.lower,base64_attrs))
    self._dsml_comment = dsml_comment
    self._indent = indent

  def _needs_base64_encoding(self,attr_type,attr_value):
    return self._base64_attrs.has_key(string.lower(attr_type))

  def writeHeader(self):
    """
    Write the header
    """
    self._f.write('\n'.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE root PUBLIC "dsml.dtd" "http://www.dsml.org/1.0/dsml.dtd">',
        '<dsml:dsml xmlns:dsml="http://www.dsml.org/DSML">',
        '%s<dsml:directory-entries>\n' % (self._indent),
      ])
    )
    if self._dsml_comment:
      self._f.write('%s<!--\n' % (self._indent))
      self._f.write('%s%s\n' % (self._indent,self._dsml_comment))
      self._f.write('%s-->\n' % (self._indent))

  def writeFooter(self):
    """
    Write the footer
    """
    self._f.write('%s</dsml:directory-entries>\n' % (self._indent))
    self._f.write('</dsml:dsml>\n')
    
  def writeRecord(self,dn,entry):
    """
    dn
          string-representation of distinguished name
    entry
          dictionary holding the LDAP entry {attr:data}
    """

    # Write line dn: first
    self._f.write(
      '%s<dsml:entry dn="%s">\n' % (
        self._indent*2,replace_char(dn)
      )
    )

    objectclasses = entry.get('objectclass',entry.get('objectClass',[]))

    self._f.write('%s<dsml:objectclass>\n' % (self._indent*3))
    for oc in objectclasses:
      self._f.write('%s<dsml:oc-value>%s</dsml:oc-value>\n' % (self._indent*4,oc))
    self._f.write('%s</dsml:objectclass>\n' % (self._indent*3))

    attr_types = entry.keys()[:]
    try:
      attr_types.remove('objectclass')
      attr_types.remove('objectClass')
    except ValueError:
      pass
    attr_types.sort()
    for attr_type in attr_types:
      self._f.write('%s<dsml:attr name="%s">\n' % (self._indent*3,attr_type))
      for attr_value_item in entry[attr_type]:
        needs_base64_encoding = self._needs_base64_encoding(
          attr_type,attr_value_item
        )
        if needs_base64_encoding:
          attr_value_item = base64.encodestring(attr_value_item)
        else:
          attr_value_item = replace_char(attr_value_item)
  	self._f.write('%s<dsml:value%s>\n' % (
            self._indent*4,
            ' encoding="base64"'*needs_base64_encoding
          )
        )
  	self._f.write('%s%s\n' % (
            self._indent*5,
            attr_value_item
          )
        )
  	self._f.write('%s</dsml:value>\n' % (
            self._indent*4,
          )
        )
      self._f.write('%s</dsml:attr>\n' % (self._indent*3))
    self._f.write('%s</dsml:entry>\n' % (self._indent*2))
    return
