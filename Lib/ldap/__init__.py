# $Id$

__version__ = '2.0.0pre05'

from _ldap import *

try:
  # Check if Python installation was build with thread support
  import threading
except ImportError:
  # Define dummy class with methods compatible to threading.Lock
  class LDAPLock:
    def __init__(self):
      pass
    def acquire(self):
      pass
    def release(self):
      pass
else:
  LDAPLock = threading.Lock

# Create module-wide lock for serializing all calls
# into underlying LDAP lib
_ldap_module_lock = LDAPLock()

def _ldap_call(func,*args,**kwargs):
  """
  Wrapper function which locks calls to func with via _ldap_lock
  """
  _ldap_module_lock.acquire()
  try:
    result = apply(func,args,kwargs)
  finally:
    pass
    _ldap_module_lock.release()
  return result


from functions import *
