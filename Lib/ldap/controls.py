"""
controls.py - support classes for LDAP controls

See http://python-ldap.sourceforge.net for details.

\$Id$

Description:
The ldap.controls module provides LDAPControl classes.
Each class provides support for a certain control.
"""

__version__ = '0.0.1'

__all__ = [
  'LDAPControl',
]


class LDAPControl:
  """
  Base class for all LDAP controls

  In this base class controlValue has to be passed in
  already BER-encoded!
  """

  def __init__(self,controlType,criticality,controlValue):
    self.controlType = controlType
    self.criticality = criticality
    self.controlValue = controlValue

  def encodeControlValue(self,value):
    return value

  def decodeControlValue(self,value):
    return value

  def __setattr__(self,name,value):
    if name=='controlValue':
      value = self.encodeControlValue(value)
    self.__dict__[name] = value

  def __getattr__(self,name):
    value = self.__dict__[name]
    if name=='controlValue':
      value = self.decodeControlValue(value)
    return value

  def getEncodedTuple(self):
    return (self.controlType,self.criticality,self.controlValue)


class BooleanControl(LDAPControl):
  """
  Base class for simple controls with booelan control value

  In this base class controlValue has to be passed as
  boolean type (True/False or 1/0).
  """
  boolean2ber = { 1:'\x01\x01\xFF', 0:'\x01\x01\x00' }
  ber2boolean = { '\x01\x01\xFF':1, '\x01\x01\x00':0 }

  def encodeControlValue(self,value):
    return int(boolean2ber[value])

  def decodeControlValue(self,value):
    return int(ber2boolean[value])


class SubentriesControl(BooleanControl):

  def __init__(self,criticality,controlValue):
    BooleanControl._init__('1.3.6.1.4.1.4203.1.10.1',criticality,controlValue)


class ManageDsaITControl(LDAPControl):

  def __init__(self,criticality):
    LDAPControl._init__('2.16.840.1.113730.3.4.2',criticality,None)


def EncodedControlTuples(ldapControls):
  """
  Return list of readily encoded 3-tuples which can be directly
  passed to C module _ldap
  """
  return [
    c.getEncodedTuple()
    for c in ldapControls
  ]
