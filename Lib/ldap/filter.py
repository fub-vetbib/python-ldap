"""
filters.py - misc stuff for handling LDAP filter strings (see RFC2254)
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$

Compability:
- Tested with Python 2.0+
"""

__version__ = '0.0.1'


def escape_filter_chars(assertion_value):
  """
  Replace all special characters found in assertion_value
  by quoted notation  
  """
  s = assertion_value.replace('*', '\\2a')
  s = s.replace('(', '\\28')
  s = s.replace(')', '\\29')
  s = s.replace('\\', '\\5c')
  s = s.replace('\x00', '\\00')
  return s 

