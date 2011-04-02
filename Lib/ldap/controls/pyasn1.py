# -*- coding: utf-8 -*-
"""
ldap.controls.psearch - classes for simple controls implemented with the help
of pyasn1 and pyasn1_modules

See http://www.python-ldap.org/ for project details.

This needs the following software:
Python
pyasn1
pyasn1-modules
python-ldap 2.4+
"""

__all__ = [
  'AuthorizationIdentityControl',
  'LDAPStringRequestControl',
  'LDAPStringResponseControl',
  'ProxyAuthzControl',
]

# Imports from python-ldap 2.4+
import ldap.controls
from ldap.controls import RequestControl,ResponseControl,KNOWN_RESPONSE_CONTROLS
from ldap.controls.simple import ValueLessRequestControl

# Imports from pyasn1
from pyasn1.codec.ber import encoder,decoder
from pyasn1_modules.rfc2251 import LDAPString


class LDAPStringRequestControl(RequestControl):
  """
  Base class for controls where the controlValue is a simple LDAPString
  """

  def __init__(self,controlType,criticality,controlValue):
    self.controlType,self.criticality,self.controlValue = controlType,criticality,controlValue

  def encodeControlValue(self):
    return encoder.encode(LDAPString(self.authzId))


class LDAPStringResponseControl(ResponseControl):
  """
  Base class for controls where the controlValue is a simple LDAPString
  """

  def __init__(self,controlType,criticality,controlValue):
    self.controlType,self.criticality,self.controlValue = controlType,criticality,controlValue

  def decodeControlValue(self,encodedControlValue):
    self.controlValue = decoder.decode(LDAPString(encodedControlValue))


class ProxyAuthzControl(RequestControl):
  """
  Proxy Authorization Control (see RFC 4370)
  """

  def __init__(self,criticality,authzId):
    LDAPStringRequestControl.__init__(self,ldap.CONTROL_PROXY_AUTHZ,criticality,authzId)


class AuthorizationIdentityControl(ValueLessRequestControl,LDAPStringResponseControl):
  """
  Authorization Identity Request and Response Controls (RFC 3829)
  """
  controlType = '2.16.840.1.113730.3.4.16'

  def __init__(self,criticality):
    ValueLessRequestControl.__init__(self,self.controlType,criticality)

  def decodeControlValue(self,encodedControlValue):
    LDAPStringResponseControl.decodeControlValue(self,encodedControlValue)
    self.authzId = self.controlValue

KNOWN_RESPONSE_CONTROLS[AuthorizationIdentityControl.controlType] = AuthorizationIdentityControl
