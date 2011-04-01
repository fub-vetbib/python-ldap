#!/usr/bin/env python
"""
This sample script demonstrates the use of the pre-read control (see RFC 4527).

Originally contributed by Andreas Hasenack <ahasenack@terra.com.br>

Requires module pyasn1 (see http://pyasn1.sourceforge.net/)
"""

import ldap,ldap.sasl

from pyasn1.codec.ber import encoder,decoder
from ldap.controls import LDAPControl

from pyasn1_modules.rfc2251 import AttributeDescriptionList,SearchResultEntry


class ReadEntryControl(LDAPControl):
  """
  Base class for control described in RFC 4527
  """

  def __init__(self,criticality=False,attrList=None):
    self.criticality,self.attrList,self.entry = criticality,attrList or [],None

  def encodeControlValue(self):
    attributeSelection = AttributeDescriptionList()
    for i in range(len(self.attrList)):
      attributeSelection.setComponentByPosition(i,self.attrList[i])
    return encoder.encode(attributeSelection)

  def decodeControlValue(self,encodedControlValue):
    decodedEntry,_ = decoder.decode(encodedControlValue,asn1Spec=SearchResultEntry())
    decodedEntry.prettyPrint()
    self.entry = dict([])


class PreReadControl(ReadEntryControl):
  controlType = ldap.CONTROL_PRE_READ

class PostReadControl(ReadEntryControl):
  controlType = ldap.CONTROL_POST_READ

uri = "ldapi://%2Ftmp%2Fopenldap-socket"

l = ldap.initialize(uri,trace_level=2)
l.sasl_interactive_bind_s(
  "",
  ldap.sasl.sasl({},'EXTERNAL')
)

pr = PreReadControl(criticality=True,attrList=['uidNumber','gidNumber'])

msg_id = l.modify_ext(
  "cn=Samba Unix UID Pool,ou=Testing,dc=stroeder,dc=de",
  [(ldap.MOD_INCREMENT, "uidNumber", "1"),(ldap.MOD_INCREMENT, "gidNumber", "1")],
  serverctrls = [pr]
)
res = l.result3(
  msg_id,
  resp_ctrl_classes={PreReadControl.controlType:PreReadControl}
)
print "res:", res
