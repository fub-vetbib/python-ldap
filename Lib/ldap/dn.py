"""
dn.py - misc stuff for handling distinguished names (see RFC2253)
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$

Compability:
- Tested with Python 2.0+
"""

__version__ = '0.0.1'


def escape_dn_chars(s):
  """
  Escape all DN special characters found in s
  with a back-slash
  """
  if s:
    s = s.replace('\\','\\\\')
    s = s.replace(',' ,'\\,')
    s = s.replace('+' ,'\\+')
    s = s.replace('"' ,'\\"')
    s = s.replace('<' ,'\\<')
    s = s.replace('>' ,'\\>')
    s = s.replace(';' ,'\\;')
    s = s.replace('=' ,'\\=')
    if s[0]=='#':
      s = ''.join(('\\',s))
    if s[-1]==' ':
      s = ''.join((s[:-1],'\\ '))
  return s
