"""
ldapurl - handling of LDAP URLs as described in RFC 2255
written by Michael Stroeder <michael@stroeder.com>

\$Id$

This module is part of the python-ldap project:
http://python-ldap.sourceforge.net

License:
Public domain. Do anything you want with this module.

Python compability note:
This module only works with Python 2.0+ since all string parameters
are assumed to be Unicode objects, string methods are used instead of
module string and list comprehensions are used.
"""

__version__ = '0.4.0'

__all__ = [
  # constants
  'SEARCH_SCOPE','SEARCH_SCOPE_STR',
  # functions
  'isLDAPUrl',
  # classes
  'LDAPUrlExtension','LDAPUrl'
]

import re

from urllib import quote,quote_plus,unquote_plus

host_pattern = r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|[a-zA-Z]+[a-zA-Z0-9-]*(\.[a-zA-Z]+[a-zA-Z0-9-]*)*)+(:[0-9]*)*'
host_regex = re.compile('^%s$' % host_pattern)

# Some widely used types
StringType = type('')
UnicodeType = type(u'')

LDAP_SCOPE_BASE = 0
LDAP_SCOPE_ONELEVEL = 1
LDAP_SCOPE_SUBTREE = 2

SEARCH_SCOPE_STR = ['base','one','sub']

SEARCH_SCOPE = {
  # the search scope strings defined in RFC22xx(?)
  'base':LDAP_SCOPE_BASE,
  'one':LDAP_SCOPE_ONELEVEL,
  'sub':LDAP_SCOPE_SUBTREE
}


def isLDAPUrl(s):
  """
  Returns 1 if s is a LDAP URL, 0 else
  """
  if type(s)==UnicodeType:
    s=s.encode('utf-8')
  return \
    s.startswith('ldap://') or \
    s.startswith('ldaps://') or \
    s.startswith('ldapi://')


def decode_dn(dn,charset,relaxed_charset_handling):
  dn = unquote_plus(dn)
  try:
    result_dn = unicode(dn,charset)
  except UnicodeError:
    if relaxed_charset_handling:
      result_dn = None
      for c in ['utf-8','iso-8859-1']:
        if c!=charset:
          try:
            result_dn = unicode(dn,c)
          except UnicodeError:
            pass
          else:
            break
      if result_dn is None:
        raise ValueError,'Invalid character set used in DN part of LDAP URL.'
    else:
      raise ValueError,'Invalid character set used in DN part of LDAP URL.'
  return result_dn


class LDAPUrlExtension:
  """
  Class for parsing and unparsing LDAP URL extensions
  as described in RFC 2255.

  BNF definition of LDAP URL extensions:

       extensions = extension *("," extension)
       extension  = ["!"] extype ["=" exvalue]
       extype     = token / xtoken
       exvalue    = LDAPString from section 4.1.2 of [2]
       token      = oid from section 4.1 of [3]
       xtoken     = ("X-" / "x-") token

  Usable class attributes:
  critical
        Boolean integer marking the extension as critical
  extype    
        Type of extension
  exvalue
        Value of extension
  """

  def __init__(self,extensionStr=None,critical=0,extype=None,exvalue=None):
    if extensionStr is None:
      self.critical = critical
      self.extype = extype
      self.exvalue = exvalue
    else:
      self._parse(extensionStr)

  def _parse(self,extension):
    extension = extension.strip()
    if not extension:
      # Don't parse empty strings
      self.extype,self.exvalue = None,None
      return
    self.critical = extension[0]=='!'
    if extension[0]=='!':
      extension = extension[1:].strip()
    self.extype,self.exvalue = extension.split('=',1)
    self.extype = self.extype.strip()
    self.exvalue = unquote_plus(self.exvalue.strip())

  def __str__(self):
    return '%s%s=%s' % (
      '!'*(self.critical>0),
      self.extype,self.exvalue.replace(',',r'%2C')
    )
    

class LDAPUrl:
  """
  Class for parsing and unparsing LDAP URLs
  as described in RFC 2255.

  BNF definition of LDAP URL:

    hostport     host:port
    dn           distinguished name
    attributes   list with attributes
    scope        search scope string
    filter       LDAP search filter
    ldapurl    = scheme "://" [hostport] ["/"
                     [dn ["?" [attrs] ["?" [scope]
                     ["?" [filter] ["?" extensions]]]]]]

  Usable class attributes:
    urlscheme
        URL scheme (either ldap, ldaps or ldapi)
    hostport
        LDAP host (default '')
    dn
        Unicode string holding distinguished name (default '')
    attrs
        list of attribute types (default None)
    scope
        integer search scope for ldap-module
    filterstr
        Unicode string representation of LDAP Search Filters
        (see RFC 2254)
    extensions
        Dictionary used as extensions store
    charset
        Character set to be assumed for LDAP data
    who
        Maps automagically to bindname LDAP URL extension
    cred
        Maps automagically to X-BINDPW LDAP URL extension
  """

  attr2extype = {'who':'bindname','cred':'X-BINDPW'}

  def __init__(
    self,
    ldapUrl=None,
    urlscheme='ldap',
    hostport='',
    dn=None,
    attrs=None,
    scope=LDAP_SCOPE_BASE,
    filterstr='(objectclass=*)',
    extensions = {},
    charset='utf-8',
    who=None,
    cred=None,
  ):
    self.urlscheme=urlscheme
    self.hostport=hostport
    self.dn=dn
    self.attrs=attrs
    self.scope=scope
    self.filterstr=filterstr
    self.extensions=extensions
    self.charset=charset
    self.who = who
    self.cred = cred
    if ldapUrl!=None:
      self._parse(ldapUrl)

  def __getattr__(self,name):
    if self.attr2extype.has_key(name):
      extype = self.attr2extype[name]
      if self.extensions.has_key(extype):
        return unquote_plus(
          self.extensions[extype].exvalue
        )
      else:
        return None
    else:
      raise AttributeError,'No attribute %s in instance of %s.' % (
        name,self.__class__.__name__
      )
    return None # __getattr__()

  def __setattr__(self,name,value):
    if (name=='who' or name=='cred'):
      extype = self.attr2extype[name]
      if value is None and self.extensions.has_key(extype):
        # A value of None means that extension is deleted
        del self.extensions[extype]
      elif value!=None:
        # Add appropriate extension
        self.extensions[extype] = LDAPUrlExtension(
          extype=extype,exvalue=unquote_plus(value)
        )
    else:
      self.__dict__[name] = value

  def __delattr__(self,name):
    if (name=='who' or name=='cred'):
      extype = self.attr2extype[name]
      del self.extensions[extype]
    else:
      del self.__dict__[name]

  def _parse(self,ldap_url,relaxed_charset_handling=1):
    """
    parse a LDAP URL and set the class attributes
    urlscheme,host,dn,attrs,scope,filterstr,extensions
    """
    if not isLDAPUrl(ldap_url):
      raise ValueError,'Parameter ldap_url does not seem to be a LDAP URL.'
    scheme,rest = ldap_url.split('://',1)
    self.urlscheme = scheme.strip()
    if not self.urlscheme in ['ldap','ldaps','ldapi']:
      raise ValueError,'LDAP URL contains unsupported URL scheme %s.' % (self.urlscheme)
    slash_pos = rest.find('/')
    qemark_pos = rest.find('?')
    if (slash_pos==-1) and (qemark_pos==-1):
      # No / and ? found at all
      self.hostport = unquote_plus(rest)
      self.dn = u''
      return
    else:
      if slash_pos!=-1 and (qemark_pos==-1 or (slash_pos<qemark_pos)):
        # Slash separates DN from hostport
        self.hostport = unquote_plus(rest[:slash_pos])
        # Eat the slash from rest
        rest = rest[slash_pos+1:]
      elif qemark_pos!=1 and (slash_pos==-1 or (slash_pos>qemark_pos)):
        # Question mark separates hostport from rest, DN is assumed to be empty
        self.hostport = unquote_plus(rest[:qemark_pos])
        # Do not eat question mark
        rest = rest[qemark_pos:]
      else:
        raise ValueError,'Something completely weird happened!'
    paramlist=rest.split('?')
    paramlist_len = len(paramlist)
    if paramlist_len>=1:
      self.dn = decode_dn(paramlist[0],self.charset,relaxed_charset_handling)
    if (paramlist_len>=2) and (paramlist[1]):
      self.attrs = unquote_plus(paramlist[1].strip()).split(',')
    if paramlist_len>=3:
      scope = paramlist[2].strip()
      if not scope:
        scope = 'base'
      try:
        self.scope = SEARCH_SCOPE[scope]
      except KeyError:
        raise ValueError,"Search scope must be either one of base, one or sub. LDAP URL contained %s" % (repr(scope))
    if paramlist_len>=4:
      filterstr = unquote_plus(paramlist[3].strip())
      if not filterstr:
        filterstr='(objectclass=*)'
      try:
        self.filterstr = unicode(filterstr,self.charset)
      except:
        self.filterstr = unicode(filterstr,'iso-8859-1')
    if paramlist_len>=5:
      extensions = [
        LDAPUrlExtension(extension)
        for extension in paramlist[4].strip().split(',')
      ]
      self.extensions = {}
      for e in extensions:
        self.extensions[e.extype] = e
    return


  def _urlEncoding(self,s,charset):
    """Returns URL encoding of string s"""
    if type(s)==UnicodeType:
      s = s.encode(charset)
    return quote(s).replace(',','%2C').replace('/','%2F')

  def initializeUrl(self):
    """
    Returns LDAP URL suitable to be passed to ldap.initialize()
    """
    if self.urlscheme=='ldapi':
      # hostport part might contain slashes when ldapi:// is used
      hostport = quote_plus(self.hostport)
    else:
      hostport = self.hostport
    return '%s://%s' % (self.urlscheme,self.hostport)

  def unparse(self,charset=None,urlEncode=0):
    """
    Returns LDAP URL depending on class attributes set.
    
    charset
        Character set used to encode the LDAP URL.
        If charset is None a Unicode object is returned.
    urlEncode
        Integer flag. If 1 the returned LDAP URL will be URL encoded.
    """
    if self.attrs is None:
      attrs_str = ''
    else:
      attrs_str = ','.join(self.attrs)
    scope_str = SEARCH_SCOPE_STR[self.scope]
    if urlEncode:
      dn = self._urlEncoding(self.dn,self.charset)
      filterstr = self._urlEncoding(self.filterstr,self.charset)
    else:
      dn = self.dn ; filterstr = self.filterstr
    if self.urlscheme=='ldapi':
      # hostport part might contain slashes when ldapi:// is used
      hostport = quote_plus(self.hostport)
    else:
      hostport = self.hostport
    ldap_url = u'%s://%s/%s?%s?%s?%s' % (
      self.urlscheme,
      hostport,
      dn,
      attrs_str,
      scope_str,
      filterstr
    )
    if self.extensions:
      ldap_url = ldap_url+'?'+','.join(
        [
          str(e)
          for e in self.extensions.values()
        ]
      )
    if charset is None:
      return ldap_url
    else:
      return ldap_url.encode(charset)
  
  def htmlHREF(self,urlPrefix='',hrefText=None,hrefTarget=None,httpCharset='utf-8'):
    """Complete """
    assert type(urlPrefix)==StringType, "urlPrefix must be StringType"
    if hrefText is None:
      hrefText = self.unparse(charset=httpCharset,urlEncode=0)
    assert type(hrefText)==StringType, "hrefText must be StringType"
    if hrefTarget is None:
      target = ''
    else:
      assert type(hrefTarget)==StringType, "hrefTarget must be StringType"
      target = ' target="%s"' % hrefTarget
    return '<a%s href="%s%s">%s</a>' % (
      target,urlPrefix,self.unparse('utf-8',urlEncode=1),hrefText
    )

  def __str__(self):
    return self.unparse('utf-8')


def test():
  """Test functions"""

  print '\nTesting function isLDAPUrl():'
  is_ldap_url_tests = {
    # Examples from RFC2255
    'ldap:///o=University%20of%20Michigan,c=US':1,
    'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,c=US':1,
    'ldap://ldap.itd.umich.edu/o=University%20of%20Michigan,':1,
    'ldap://host.com:6666/o=University%20of%20Michigan,':1,
    'ldap://ldap.itd.umich.edu/c=GB?objectClass?one':1,
    'ldap://ldap.question.com/o=Question%3f,c=US?mail':1,
    'ldap://ldap.netscape.com/o=Babsco,c=US??(int=%5c00%5c00%5c00%5c04)':1,
    'ldap:///??sub??bindname=cn=Manager%2co=Foo':1,
    'ldap:///??sub??!bindname=cn=Manager%2co=Foo':1,
    # More examples from various sources
    'ldap://ldap.nameflow.net:1389/c%3dDE':1,
    'ldap://root.openldap.org/dc=openldap,dc=org':1,
    'ldap://root.openldap.org/dc=openldap,dc=org':1,
    'ldap://x500.mh.se/o=Mitthogskolan,c=se????1.2.752.58.10.2=T.61':1,
    'ldp://root.openldap.org/dc=openldap,dc=org':0,
    'ldap://localhost:1389/ou%3DUnstructured%20testing%20tree%2Cdc%3Dstroeder%2Cdc%3Dcom??one':1,
  }
  for ldap_url in is_ldap_url_tests.keys():
    result_is_ldap_url = isLDAPUrl(ldap_url)
    if result_is_ldap_url !=is_ldap_url_tests[ldap_url]:
      print 'isLDAPUrl("%s") returns %d instead of %d.' % (
        repr(ldap_url),result_is_ldap_url,is_ldap_url_tests[ldap_url]
      )

  print '\nTesting class LDAPUrl:'
  parse_ldap_url_tests = {
    'ldap://root.openldap.org/dc=openldap,dc=org':(
      'ldap',
      u'root.openldap.org', u'dc=openldap,dc=org',None,LDAP_SCOPE_BASE,'(objectclass=*)',[]
    ),
    'ldap://localhost/dc=stroeder,dc=com??sub?':(
      'ldap',
      u'localhost', u'dc=stroeder,dc=com',None,LDAP_SCOPE_SUBTREE,'(objectclass=*)',[]
    ),
    'ldap://localhost??one?':(
      'ldap',
      u'localhost', u'',None,LDAP_SCOPE_ONELEVEL,'(objectclass=*)',[]
    ),
    'ldap://x500.mh.se/o=Mitthogskolan,c=se????1.2.752.58.10.2=T.61':(
      'ldap',
      u'x500.mh.se',
      u'o=Mitthogskolan,c=se',None,
      LDAP_SCOPE_BASE,
      u'(objectclass=*)',
      [u'1.2.752.58.10.2=T.61']
    ),
    'ldap://ldap.openldap.org/uid%3dkurt%2cdc%3dboolean%2cdc%3dnet??base?%28objectclass%3d%2a%29':(
      'ldap',
      'ldap.openldap.org',
      u'uid=kurt,dc=boolean,dc=net',
      None,
      LDAP_SCOPE_BASE,
      u'(objectclass=*)',
      []
    ),
    'ldap://localhost:12345/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
      'ldap',
      'localhost:12345',
      u'dc=stroeder,dc=com',
      None,
      LDAP_SCOPE_BASE,
      u'(objectclass=*)',
      [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
    ),
    'ldaps://localhost:12345/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
      'ldaps',
      'localhost:12345',
      u'dc=stroeder,dc=com',
      None,
      LDAP_SCOPE_BASE,
      u'(objectclass=*)',
      [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
    ),
    'ldapi://%2ftmp%2fopenldap2-1389/dc=stroeder,dc=com????bindname=cn=Michael%2Cdc=stroeder%2Cdc=com,X-BINDPW=secretpassword':(
      'ldapi',
      '/tmp/openldap2-1389',
      u'dc=stroeder,dc=com',
      None,
      LDAP_SCOPE_BASE,
      u'(objectclass=*)',
      [u'bindname=cn=Michael%2Cdc=stroeder%2Cdc=com',u'X-BINDPW=secretpassword']
    ),
  }
  for ldap_url in parse_ldap_url_tests.keys():
    print 72*'#','\nTesting LDAP URL:',ldap_url
    ldapUrl = LDAPUrl(ldapUrl=ldap_url)
    print 'Unparsed LDAP URL',ldapUrl.unparse()
    if (
         ldapUrl.urlscheme,ldapUrl.hostport,ldapUrl.dn,ldapUrl.attrs,
         ldapUrl.scope,ldapUrl.filterstr,map(str,ldapUrl.extensions.values())
       ) != \
       parse_ldap_url_tests[ldap_url]:
      print 'Attributes of LDAPUrl(%s) are:\n%s\ninstead of:\n%s\n' % (
        repr(ldap_url),
        (
         ldapUrl.urlscheme,ldapUrl.hostport,ldapUrl.dn,ldapUrl.attrs,
         ldapUrl.scope,ldapUrl.filterstr,map(str,ldapUrl.extensions.values())
        ),
        repr(parse_ldap_url_tests[ldap_url])
      )

if __name__ == '__main__':
  test()
