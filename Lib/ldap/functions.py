"""
functions.py - wraps functions of module _ldap
written by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
- functions should behave exactly the same like in _ldap

Usage:
Directly imported by ldap/__init__.py. The symbols of _ldap are
overridden.

Thread-lock:
Basically calls into the LDAP lib are serialized by the module-wide
lock _ldapmodule_lock.
"""

__version__ = '0.0.2'

__all__ = [
  'open','initialize','init',
  'explode_dn','explode_rdn',
  'get_option','set_option'
]

import sys,_ldap

from ldap import _ldap_function_call
from ldap.ldapobject import LDAPObject


def open(host,port=389,trace_level=0,trace_file=sys.stdout):
  """
  Return LDAPObject instance by opening LDAP connection to
  specified LDAP host
  
  Parameters:
  host
        LDAP host and port, e.g. localhost
  port
        integer specifying the port number to use, e.g. 389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  return LDAPObject('ldap://%s:%d' % (host,port),trace_level,trace_file)

init = open


def initialize(uri,trace_level=0,trace_file=sys.stdout):
  """
  Return LDAPObject instance by opening LDAP connection to
  LDAP host specified by LDAP URL
  
  Parameters:
  uri
        LDAP URL containing at least connection scheme and hostport,
        e.g. ldap://localhost:389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  if not is_ldap_url(uri):
    raise ValueError,"Parameter uri has to be a LDAP URL."
  return LDAPObject(uri,trace_level,trace_file)


def explode_dn(dn,notypes=0):
  """
  explode_dn(dn [, notypes=0]) -> list
  
  This function takes a DN and breaks it up into its component parts.
  The notypes parameter is used to specify that only the component's
  attribute values be returned and not the attribute types.
  """
  return _ldap_function_call(_ldap.explode_dn,dn,notypes)


def explode_rdn(rdn,notypes=0):
  """
  explode_rdn(rdn [, notypes=0]) -> list
  
  This function takes a RDN and breaks it up into its component parts
  if it is a multi-valued RDN.
  The notypes parameter is used to specify that only the component's
  attribute values be returned and not the attribute types.
  """
  return _ldap_function_call(_ldap.explode_rdn,rdn,notypes)


def get_option(option):
  return _ldap_function_call(_ldap.get_option,option)


def set_option(option,invalue):
  _ldap_function_call(_ldap.set_option,option,invalue)


def is_ldap_url(url):
  """
  is_ldap_url(url) -> int

  This function returns true if url `looks like' an LDAP URL
  (as opposed to some other kind of URL).
  """
  return _ldap_function_call(_ldap.is_ldap_url,url)
