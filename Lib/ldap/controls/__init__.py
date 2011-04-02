"""
controls.py - support classes for LDAP controls

See http://www.python-ldap.org/ for details.

$Id$

Description:
The ldap.controls module provides LDAPControl classes.
Each class provides support for a certain control.
"""

from ldap import __version__

__all__ = [
  # control OID to class registy
  'KNOWN_CONTROLS',
  # Classes
  'AssertionControl',
  'BooleanControl',
  'LDAPControl',
  'ManageDSAITControl',
  'MatchedValuesControl',
  'RelaxRulesControl',
  'RequestControl',
  'ResponseControl',
  'SimplePagedResultsControl',
  'ValueLessRequestControl',
  # Functions
  'RequestControlTuples',
  'DecodeControlTuples',
]

KNOWN_RESPONSE_CONTROLS = {}

from types import ClassType

import _ldap,ldap


class RequestControl:
  """
  Base class for all request controls
  """

  def __init__(self,controlType=None,criticality=False,encodedControlValue=None):
    self.controlType = controlType
    self.criticality = criticality
    self.encodedControlValue = encodedControlValue

  def encodeControlValue(self):
    return self.encodedControlValue


class ResponseControl:
  """
  Base class for all response controls
  """

  def __init__(self,controlType=None,criticality=False):
    self.controlType = controlType
    self.criticality = criticality

  def decodeControlValue(self,encodedControlValue):
    self.encodedControlValue = encodedControlValue


class LDAPControl(RequestControl,ResponseControl):

  def __init__(self,controlType=None,criticality=False,controlValue=None,encodedControlValue=None):
    self.controlType = controlType
    self.criticality = criticality
    self.controlValue = controlValue
    self.encodedControlValue = encodedControlValue


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


class SimplePagedResultsControl(LDAPControl):
  """
  LDAP Control Extension for Simple Paged Results Manipulation

  see RFC 2696
  """
  controlType = ldap.CONTROL_PAGEDRESULTS

  def __init__(self,criticality=False,size=None,cookie=None):
    self.criticality = criticality
    self.size,self.cookie = size,cookie

  def encodeControlValue(self):
    return _ldap.encode_page_control(self.size,self.cookie)

  def decodeControlValue(self,encodedControlValue):
    self.size,self.cookie = _ldap.decode_page_control(encodedControlValue)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_PAGEDRESULTS] = SimplePagedResultsControl


class MatchedValuesControl(RequestControl):
  """
  LDAP Matched Values control, as defined in RFC 3876
  """
  
  controlType = ldap.CONTROL_VALUESRETURNFILTER
  
  def __init__(self,criticality=False,filterstr='(objectClass=*)'):
    self.criticality = criticality
    self.filterstr = filterstr

  def encodeControlValue(self):
    return _ldap.encode_valuesreturnfilter_control(self.filterstr)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_VALUESRETURNFILTER] = MatchedValuesControl


class AssertionControl(LDAPControl):
  """
  LDAP Assertion control, as defined in RFC 4528
  """
  
  controlType = ldap.CONTROL_ASSERT    
  def __init__(self,criticality=True,filterstr='(objectClass=*)'):
    self.criticality = criticality
    self.filterstr = filterstr

  def encodeControlValue(self):
    return _ldap.encode_assertion_control(self.filterstr)

KNOWN_RESPONSE_CONTROLS[ldap.CONTROL_ASSERT] = AssertionControl


def RequestControlTuples(ldapControls):
  """
  Return list of readily encoded 3-tuples which can be directly
  passed to C module _ldap
  """
  if ldapControls is None:
    return None
  else:
    result = [
      (c.controlType,c.criticality,c.encodeControlValue())
      for c in ldapControls
    ]
    return result


def DecodeControlTuples(ldapControlTuples,knownLDAPControls):
  """
  Return list of readily decoded ResponseControl objects
  """
  knownLDAPControls = knownLDAPControls or {}
  result = []
  for controlType,criticality,encodedControlValue in ldapControlTuples or []:
    control = knownLDAPControls.get(controlType,ResponseControl)()
    control.controlType,control.criticality = controlType,criticality
    control.decodeControlValue(encodedControlValue)
    result.append(control)  
  return result
