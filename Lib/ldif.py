"""
ldif.py - generate and parse LDIF data

$Id$
"""

__version__ = '0.3.0'

import os,string,base64,re

try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

attrtype_pattern = r'[\w;.]+(;[\w_-]+)*'
data_pattern = r'(([^,]|\\,)+|".*?")'
rdn_pattern = attrtype_pattern + r'[ ]*=[ ]*' + data_pattern
dn_pattern   = rdn_pattern + r'([ ]*,[ ]*' + rdn_pattern + r')*[ ]*'
dn_regex   = re.compile('^%s$' % dn_pattern)

ldif_pattern = '^((dn(:|::) %(dn_pattern)s)|(%(attrtype_pattern)s(:|::) .*)$)+' % vars()
ldif_regex   = re.compile('^%s$' % ldif_pattern,re.M)


def is_dn(s):
  """
  returns 1 if s is a LDAP DN
  """
  rm = dn_regex.match(s)
  return rm!=None and rm.group(0)==s


SAFE_STRING = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
SAFE_STRING_re = re.compile(SAFE_STRING)


def needs_base64(s):
  """
  returns 1 if s has to be base-64 encoded because of special chars
  """
  return not SAFE_STRING_re.search(s) is None


def CreateLDIFLine(attr_type,attr_value,base64_attrs=[],cols=66):
  """
  Write a single attribute to one or many folded LDIF line(s).
  
  attr_type
        attribute type
  attr_value
        attribute value
  base64_attrs
        list of attribute types to be base64-encoded in any case
  cols
        Specifies how many columns a line may have before it's
        folded into many lines.
  """
  # Encode with base64 if necessary
  if (attr_type in base64_attrs) or needs_base64(attr_value):
    line = '%s:: %s' % (
      attr_type,
      string.replace(base64.encodestring(attr_value),'\n','')
    )
  else:
    line = '%s: %s' % (attr_type,attr_value)
  # Check maximum line length
  line_len = len(line)
  if line_len<=cols:
    return line
  # Fold line
  pos = cols
  result = [line[0:min(line_len,cols)]]
  while pos<line_len:
    result.append(line[pos:min(line_len,pos+cols-1)])
    pos = pos+cols-1
  return string.join(result,os.linesep+' ')


def CreateLDIF(dn,entry={},base64_attrs=[],cols=66):
  """
  Create LDIF formatted entry including trailing empty line.
  
  dn
        string-representation of distinguished name
  entry
        dictionary holding the LDAP entry {attrtype:data}
  base64_attrs
        list of attribute types to be base64-encoded in any case
  cols
        Specifies how many columns a line may have before it's
        folded into many lines.
  """
  # At first prepare line with distinguished name
  result = [CreateLDIFLine('dn',dn,cols=cols)]
  attr_types = entry.keys()[:]
  attr_types.sort()
  for attr_type in attr_types:
    for attr_value in entry[attr_type]:
      result.append(CreateLDIFLine(attr_type,attr_value,base64_attrs,cols))
  result.append('')
  return string.join(result,os.linesep)


def StripLineSep(s):
  """
  Strip trailing line separators but no other whitespaces
  """
  if s[-2:]=='\r\n':
    return s[:-2]
  elif s[-1]=='\n':
    return s[:-1]
  else:
    return s


def ParseLDIF(f,ignore_attrs=[],maxentries=0):
  """
  Parse LDIF data read from file object f

  f
        file-object for reading LDIF input
  ignore_attrs
        list of attributes to be ignored
  maxentries
        if non-zero specifies the maximum number of
  	entries to be read from f
  """
  
  result = []

  # lower-case all
  ignore_attrs = map(string.lower,ignore_attrs)

  # Read very first line
  s = f.readline()

  entries_read = 0

  while s and (not maxentries or entries_read<maxentries):

    # Reading new entry

    # Reset entry data
    dn = None; entry = {};

    while s:
    
      # Reading new attribute line
      attr,data=string.split(s,':',1)
      if data[0]==':':
        # Read attr:: data line => binary data assumed
        data = data[1:]
        binary = 1
      elif data[0]=='<' or data[:1]==' <':
        raise ValueError,'File importing not supported'
      else:
        # Read attr: data line
        binary = 0

      # Strip the line separators 
      data = StripLineSep(data[1:])
      s = f.readline()

      # Reading continued multi-line data
      while s and s[0]==' ':
        data = data + string.strip(s)
        # Read next line
        s = f.readline()

      attr = string.strip(attr)

      if not string.lower(attr) in ignore_attrs:

	if binary:
          # binary data has to be BASE64 decoded
          data = base64.decodestring(data)

        # Add attr: data to entry
	if attr=='dn':
          dn = string.strip(data) ; attr = None ; data = None
          if not is_dn(dn):
	    raise ValueError, 'No valid string-representation of distinguished name.'
	else:
          if entry.has_key(attr):
            entry[attr].append(data)
          else:
            entry[attr]=[data]

    # end of entry reached marked by newline character(s)

    if entry:
      # append entry to result list
      result.append((dn,entry))
      entries_read = entries_read+1

    # Start reading next entry
    s = f.readline()

  return result


def test():
  test_entry = {
    'objectClass':['test'],
    'cn;lang-de':['Michael Str\303\266der'],
    'cn;lang-en':['Michael Stroeder'],
    'bin':['\000\001\002'*200],
    'leadingspace':[' bla'],
    'trailingspace':['bla '],
  }
  ldif = CreateLDIF(
    'cn=Michael Str\303\266der,dc=stroeder,dc=com',test_entry,['bin']
  )
  print ldif
  test_result = ParseLDIF(StringIO(ldif))
  print test_result
  for a in test_entry.keys():
    if test_entry[a]!=test_result[0][1][a]:
      print 'Error in attribute %s: "%s"!="%s"' % (
        a,repr(test_entry[a]),repr(test_result[0][1][a])
      )


if __name__ == '__main__':
  test()
