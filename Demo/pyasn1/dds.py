# -*- coding: utf-8 -*-
"""
Helper classes for Dynamic Entries (see RFC 2589)

This needs the following software:
Python
pyasn1
pyasn1-modules
python-ldap 2.4+
"""

from ldap.extop import ExtendedRequest,ExtendedResponse

# Imports from pyasn1
from pyasn1.type import namedtype,univ,tag
from pyasn1.codec.der import encoder,decoder
from pyasn1_modules.rfc2251 import LDAPDN


class RefreshRequest(ExtendedRequest):

  requestName = '1.3.6.1.4.1.1466.101.119.1'
  defaultRequestTtl = 86400

  class RefreshRequestValue(univ.Sequence):
    componentType = namedtype.NamedTypes(
      namedtype.NamedType(
        'entryName',
        LDAPDN().subtype(
          implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0)
        )
      ),
      namedtype.NamedType(
        'requestTtl',
        univ.Integer().subtype(
          implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1)
        )
      ),
    )

  def __init__(self,requestName=None,entryName=None,requestTtl=None):
    self.entryName = entryName
    self.requestTtl = requestTtl or self.defaultRequestTtl

  def encodedRequestValue(self):
    p = self.RefreshRequestValue()
    p.setComponentByName(
      'entryName',
      LDAPDN(self.entryName).subtype(
        implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple,0)
      )
    )
    p.setComponentByName(
      'requestTtl',
      univ.Integer(self.requestTtl).subtype(
        implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,1)
      )
    )
    return encoder.encode(p)


class RefreshResponse(ExtendedResponse):
  
  responseName = '1.3.6.1.4.1.1466.101.119.1'

  class RefreshResponseValue(univ.Sequence):
    componentType = namedtype.NamedTypes(
      namedtype.NamedType(
        'responseTtl',
        univ.Integer().subtype(
          # let use assume tag [0] here to make it work with OpenLDAP
          implicitTag=tag.Tag(tag.tagClassContext,tag.tagFormatSimple,0)
        )
      )
    )

  def decodeResponseValue(self,value):
    respValue,_ = decoder.decode(value,asn1Spec=self.RefreshResponseValue())
    self.responseTtl = int(respValue.getComponentByName('responseTtl'))
    return self.responseTtl


if __name__ == '__main__':

  import sys,ldap,ldapurl,getpass

  try:
    ldap_url = ldapurl.LDAPUrl(sys.argv[1])
    request_ttl = int(sys.argv[2])
  except IndexError,ValueError:
    print 'Usage: dds.py <LDAP URL> <TTL>'
    sys.exit(1)

  # Set debugging level
  #ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)
  ldapmodule_trace_level = 2
  ldapmodule_trace_file = sys.stderr

  ldap_conn = ldap.ldapobject.LDAPObject(
    ldap_url.initializeUrl(),
    trace_level=ldapmodule_trace_level,
    trace_file=ldapmodule_trace_file
  )

  if ldap_url.cred is None:
    print 'Password for %s:' % (repr(ldap_url.who))
    ldap_url.cred = getpass.getpass()

  try:
    ldap_conn.simple_bind_s(ldap_url.who,ldap_url.cred)

  except ldap.INVALID_CREDENTIALS,e:
    print 'Simple bind failed:',str(e)
    sys.exit(1)

  else:
    extreq = RefreshRequest(entryName=ldap_url.dn,requestTtl=request_ttl)
    try:
      extop_resp_obj = ldap_conn.extop_s(extreq,extop_resp_class=RefreshResponse)
    except ldap.LDAPError,e:
      print str(e)
    else:
      if extop_resp_obj.responseTtl!=request_ttl:
        print 'Different response TTL:',extop_resp_obj.responseTtl
      else:
        print 'Response TTL:',extop_resp_obj.responseTtl
