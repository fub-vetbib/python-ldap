########################################################################
# ldif.py 0.2.3
# Various routines for handling LDIF data
########################################################################
# This module is distributed under the terms of the
# GPL (GNU GENERAL PUBLIC LICENSE) Version 2
# (see http://www.gnu.org/copyleft/gpl.html)
# Author: Michael Ströder
# $Id$
########################################################################

import sys,string,binascii,re

try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

attr_pattern = r'[\w;.]+(;[\w_-]+)*'
data_pattern = '([^,]+|".*?")'
rdn_pattern = attr_pattern + r'[\s]*=[\s]*' + data_pattern
dn_pattern   = rdn_pattern + r'([\s]*,[\s]*' + rdn_pattern + r')*'

#rdn_regex   = re.compile('^%s$' % rdn_pattern)
dn_regex   = re.compile('^%s$' % dn_pattern)

ldif_pattern = '^((dn(:|::) %(dn_pattern)s)|(%(attr_pattern)s(:|::) %(data_pattern)s)$)+' % vars()

ldif_regex   = re.compile('^%s$' % ldif_pattern,re.M)

# returns 1 if s is a LDAP DN
def is_dn(s):
  rm = dn_regex.match(s)
  return rm!=None and rm.group(0)==s

# returns 1 if s is plain ASCII
def is_ascii(s):
  if s:
    pos=0 ; s_len = len(s)
    while ((ord(s[pos]) & 0x80) == 0) and (pos<s_len-1):
      pos=pos+1
    if pos<s_len-1:
      return 0
    else:
      return (ord(s[pos]) & 0x80) == 0
  else:
    return 1

########################################################################
# Convert buf to a binary attribute representation
########################################################################

def BinaryAttribute(attr,buf,col=77):

  b64buf = '%s:: ' % (attr)
  buflen = len(buf)
  pos=0
  while pos<buflen:
    b64buf = '%s%s' % (b64buf,binascii.b2a_base64(buf[pos:min(buflen,pos+57)])[:-1])
    pos = pos+57

  b64buflen = len(b64buf)
  pos=col
  result = b64buf[0:min(b64buflen,col)]
  while pos<b64buflen:
    result = '%s\n %s' % (result,b64buf[pos:min(b64buflen,pos+col-1)])
    pos = pos+col-1

  return '%s\n' % result


########################################################################
# Create LDIF formatted entry without empty line
# dn is the distinguished name as string
# entry is dictionary {attr:data}
########################################################################

def CreateLDIF(dn,entry={},binary_attrs=[]):

  # Write line dn: first
  if is_ascii(dn):
    result = ['dn: %s\n' % (dn)]
  else:
    result = [BinaryAttribute('dn',dn)]

  objectclasses = entry.get('objectclass',entry.get('objectClass',[]))
  for oc in objectclasses:
    result.append('objectclass: %s\n' % oc)
  attrs = entry.keys()[:]
  try:
    attrs.remove('objectclass')
    attrs.remove('objectClass')
  except:
    pass
  attrs.sort()
  for attr in attrs:
    if attr in binary_attrs:
      for data in entry[attr]:
        result.append(BinaryAttribute(attr,data))
    else:
      for data in entry[attr]:
        if is_ascii(data):
  	  result.append('%s: %s\n' % (attr,data))
	else:
          result.append(BinaryAttribute(attr,data))
  return string.join(result,'')


########################################################################
# Parse LDIF data read from file object f
# result is [(dn,{attr:data})]
# maxentries (if non-zero) determines the maximum number of
# entries to be read from f
########################################################################

def ParseLDIF(f=StringIO(),ignore_attrs=[],maxentries=0):

  result = []

  # lower-case all
  ignored_attrs = map(string.lower,ignore_attrs)

  # Read very first line
  s = f.readline()

  entries_read = 0

  while s and (not maxentries or entries_read<maxentries):

    # Reading new entry

    # Reset entry data
    dn = ''; entry = {}; attr = ''; data = ''

    s = string.rstrip(s)

    while s:
    
      # Reading new attribute line
      attr,data=string.split(s,':',1)
      if data[0]==':':
        # Read attr:: data line => binary data assumed
        data = data[1:]
        binary = 1
      else:
        # Read attr: data line
        binary = 0

      s = f.readline()
      s = string.rstrip(s)

      # Reading continued multi-line data
      while s and s[0]==' ':
        data = data + string.strip(s)
        # Read next line
        s = f.readline()
        s = string.rstrip(s)

      attr = string.lower(string.strip(attr))

      if not attr in ignored_attrs:

	if binary:
          # binary data has to be BASE64 decoded
          data = binascii.a2b_base64(data)
	else:
          data = string.strip(data)

        # Add attr: data to entry
	if attr=='dn':
          dn = string.strip(data) ; attr = '' ; data = ''
          if not is_dn(dn):
	    raise ValueError
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
