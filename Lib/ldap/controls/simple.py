# -*- coding: utf-8 -*-
"""
ldap.controls.simple - classes for some very simple LDAP controls

See http://www.python-ldap.org/ for details.

$Id$
"""

import ldap
from ldap.controls import RequestControl,ResponseControl,LDAPControl,KNOWN_RESPONSE_CONTROLS


class ValueLessRequestControl(RequestControl):

  def __init__(self,controlType=None,criticality=False):
    self.controlType = controlType
    self.criticality = criticality

  def encodeControlValue(self):
    return None


class ManageDSAITControl(ValueLessRequestControl):

  def __init__(self,criticality=False):
    ValueLessRequestControl.__init__(self,ldap.CONTROL_MANAGEDSAIT,criticality=False)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_MANAGEDSAIT] = ManageDSAITControl


class RelaxRulesControl(ValueLessRequestControl):

  def __init__(self,criticality=False):
    ValueLessRequestControl.__init__(self,ldap.CONTROL_RELAX,criticality=False)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_RELAX] = RelaxRulesControl


class BooleanControl(LDAPControl):
  """
  Base class for simple request controls with booelan control value

  In this base class controlValue has to be passed as
  boolean type (True/False or 1/0).
  """
  boolean2ber = { 1:'\x01\x01\xFF', 0:'\x01\x01\x00' }
  ber2boolean = { '\x01\x01\xFF':1, '\x01\x01\x00':0 }

  def __init__(self,controlType=None,criticality=False,booleanValue=False):
    self.controlType = controlType
    self.criticality = criticality
    self.booleanValue = booleanValue

  def encodeControlValue(self):
    return self.boolean2ber[int(self.booleanValue)]

  def decodeControlValue(self,encodedControlValue):
    self.booleanValue = self.ber2boolean[encodedControlValue]


class ProxyAuthzControl(RequestControl):
  """
  Proxy Authorization Control (see RFC 4370)
  """

  def __init__(self,criticality,authzId):
    RequestControl.__init__(self,ldap.CONTROL_PROXY_AUTHZ,criticality,authzId)


class AuthorizationIdentityControl(ValueLessRequestControl,ResponseControl):
  """
  Authorization Identity Request and Response Controls (RFC 3829)
  """
  controlType = '2.16.840.1.113730.3.4.16'

  def __init__(self,criticality):
    ValueLessRequestControl.__init__(self,self.controlType,criticality)

  def decodeControlValue(self,encodedControlValue):
    self.authzId = encodedControlValue

KNOWN_RESPONSE_CONTROLS[AuthorizationIdentityControl.controlType] = AuthorizationIdentityControl
