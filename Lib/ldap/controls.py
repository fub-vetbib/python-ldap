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

  def __repr__(self):
    return '%s(%s,%s,%s)' % (self.__class__.__name__,self.controlType,self.criticality,self.controlValue)

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
    return self.boolean2ber[int(value)]

  def decodeControlValue(self,value):
    return self.ber2boolean[value]


def EncodeControlTuples(ldapControls):
  """
  Return list of readily encoded 3-tuples which can be directly
  passed to C module _ldap
  """
  if ldapControls is None:
    return None
  else:
    result = [
      c.getEncodedTuple()
      for c in ldapControls
    ]
    return result


def DecodeControlTuples(ldapControlTuples):
  """
  Return list of readily encoded 3-tuples which can be directly
  passed to C module _ldap
  """
  return [
    LDAPControl(t[0],t[1],t[2])
    for t in ldapControlTuples or []
  ]
