"""
ldap - base module
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

$Id$
"""

__version__ = '2.0.0pre06'

import sys

if __debug__:
  # Tracing is only supported in debugging mode
  import traceback
  _trace_level = 0
  _trace_file = sys.stderr
  _trace_stack_limit = None

from _ldap import *

class DummyLock:
  """Define dummy class with methods compatible to threading.Lock"""
  def __init__(self):
    pass
  def acquire(self):
    pass
  def release(self):
    pass


try:
  # Check if Python installation was build with thread support
  import threading
except ImportError:
  _ldap_module_lock = DummyLock()
  LDAPLock = DummyLock
else:
  LDAPLock = threading.Lock

# Create module-wide lock for serializing all calls
# into underlying LDAP lib
_ldap_module_lock = LDAPLock()

def _ldap_function_call(func,*args,**kwargs):
  """
  Wrapper function which locks calls to func with via
  module-wide ldap_lock
  """
  if __debug__:
    if _trace_level>=1:
      _trace_file.write('*** %s.%s (%s,%s)\n' % (
        '_ldap',repr(func),
        repr(args),repr(kwargs)
      ))
      if _trace_level>=3:
        traceback.print_stack(limit=_trace_stack_limit,file=_trace_file)
  _ldap_module_lock.acquire()
  try:
    try:
      result = apply(func,args,kwargs)
    finally:
      _ldap_module_lock.release()
  except LDAPError,e:
    if __debug__ and _trace_level>=2:
      _trace_file.write('=> LDAPError: %s\n' % (str(e)))
    raise
  if __debug__ and _trace_level>=2:
    if result!=None and result!=(None,None):
      _trace_file.write('=> result: %s\n' % (repr(result)))
  return result


from functions import *
