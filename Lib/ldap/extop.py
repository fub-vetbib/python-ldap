"""
controls.py - support classes for LDAPv3 extended operations

See http://www.python-ldap.org/ for details.

\$Id$

Description:
The ldap.extop module provides base classes for LDAPv3 extended operations.
Each class provides support for a certain extended operation request and
response.
"""

from ldap import __version__

__all__ = [
  'ExtendedRequest',
  'ExtendedResponse',
]


class ExtendedRequest:
  """
  Generic base class for a LDAP extended operation request
  """

  def __init__(self,requestName,requestValue):
    self.requestName = requestName
    self.requestValue = requestValue

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.requestName,self.requestValue)

  def encodedRequestValue(self,value):
    return self.requestValue

  def decodeRequestValue(self,encodedValue):
    return encodedValue


class ExtendedResponse:
  """
  Generic base class for a LDAP extended operation response
  """

  def __init__(self,responseName,responseValue):
    self.responseName = responseName
    self.responseValue = responseValue

  def __repr__(self):
    return '%s(%s,%s)' % (self.__class__.__name__,self.responseName,self.responseValue)

  def encodeResponseValue(self,value):
    return value

  def decodedResponseValue(self):
    return self.responseValue
