"""
ldapthreadlock.py - mimics LDAPObject class in a thread-safe way
(c) 2001 by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.

Compability:
- The behaviour of the ldapthreadlock.LDAPObject class should be
  exactly the same like ldap.LDAPObject
- This module needs your Python installation to be built with
  thread support (module threading is imported).

Usage:
You can simply use function open() / intialize() of this module
instead of function open() / intialize() of module ldap to create
an instance of LDAPObject class.

Basically calls into the LDAP lib are serialized by the module-wide
lock _ldapmodule_lock. To avoid blocking of other threads synchronous
methods like search_s() etc. and the result() method were rewritten to do
solely asynchronous LDAP lib calls with zero timeout.

The timeout handling is done within the method result() which probably leads
to less exact timing.
"""

__version__ = '0.3.0'

__all__ = ['open','initialize','init','get_option','set_option']

import time,threading,ldap

if __debug__:
  import sys,traceback
  _module_debug_level = 0


# Global lock for serializing all calls into underlying LDAP lib
_ldapmodule_lock = threading.Lock()


def _ldap_call(self,func,*args,**kwargs):
  """Wrapper function which locks calls to func with via ldap_module_lock"""
  _ldapmodule_lock.acquire()
  try:
    result = apply(func,args,kwargs)
  finally:
    _ldapmodule_lock.release()
  return result


class LDAPObject:
  """
  Thread-safe drop-in wrapper class around ldap.LDAPObject.
  """

  def _ldap_call(self,func,*args,**kwargs):
    """Wrapper method mainly for trace logs"""
    if __debug__:
      if _module_debug_level>=1 and func.__name__!='result':
        print '*** %s:' % (self.__module__),\
          self.__class__.__name__+'.'+func.__name__,\
          repr(args),repr(kwargs)
        if _module_debug_level>=2:
          traceback.print_stack(file=sys.stdout)
    result = _ldap_call(self,func,*args,**kwargs)
    if __debug__:
      if _module_debug_level>=1 and result!=None:
        print '=> result:',result
    return result

  def __init__(self,host=None,uri=None):
    if uri!=None:
      self._l = self._ldap_call(ldap.intialize,uri)
    elif host!=None:
      self._l = self._ldap_call(ldap.open,host)
    else:
      raise ValueError,"Either host or uri must be set."

  def __setattr__(self,name,value):
    if name!='_l':
      if __debug__:
        if _module_debug_level>=1:
          print '*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__setattr__(%s,%s)' % (name,value)
          if _module_debug_level>=2:
            traceback.print_stack(file=sys.stdout)
      _ldapmodule_lock.acquire()
      try:
        setattr(self._l,name,value)
      finally:
        _ldapmodule_lock.release()
    else:
      self.__dict__[name] = value

  def __getattr__(self,name):
    if name!='_l':
      _ldapmodule_lock.acquire()
      try:
        value = getattr(self._l,name)
      finally:
        _ldapmodule_lock.release()
      if __debug__:
        if _module_debug_level>=1:
          print '*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__getattr__(%s)' % (name),'=>',value
          if _module_debug_level>=2:
            traceback.print_stack(file=sys.stdout)
    else:
      value = self.__dict__[name]
    return value

  def abandon(self,msgid):
    return self._ldap_call(self._l.abandon,msgid)

  def add(self,dn,modlist):
    return self._ldap_call(self._l.add,dn,modlist)

  def add_s(self,dn,modlist):
    msgid = self.add(dn,modlist)
    return self.result(msgid)

  def bind(self,who,cred,method):
    return self._ldap_call(self._l.bind,who,cred,method)

  def bind_s(self,who,cred,method):
    msgid = self.bind(who,cred,method)
    return self.result(msgid)

  def compare(self,*args,**kwargs):
    return self._ldap_call(self._l.compare,*args,**kwargs)

  def compare_s(self,*args,**kwargs):
    msgid = self.compare(*args,**kwargs)
    return self.result(msgid)

  def delete(self,dn):
    return self._ldap_call(self._l.delete,dn)

  def delete_s(self,dn):
    msgid = self.delete(dn)
    return self.result(msgid)

  def destroy_cache(self):
    return self._ldap_call(self._l.destroy_cache,)

  def disable_cache(self):
    return self._ldap_call(self._l.disable_cache,)

  def enable_cache(self,timeout=ldap.NO_LIMIT,maxmem=ldap.NO_LIMIT):
    return self._ldap_call(self._l.enable_cache,timeout,maxmem)

  def fileno(self):
    return self._ldap_call(self._l.fileno,)

  def flush_cache(self):
    return self._ldap_call(self._l.flush_cache)

  def modify(self,dn,modlist):
    return self._ldap_call(self._l.modify,dn,modlist)

  def modify_s(self,dn,modlist):
    return self._ldap_call(self._l.modify_s,dn,modlist)

  def modrdn(self,dn,newrdn,delold=1):
    return self._ldap_call(self._l.modrdn,dn,newrdn,delold)

  def modrdn_s(self,dn,newrdn,delold=1):
    msgid = self.modrdn(dn,newrdn,delold)
    return self.result(msgid)

  def result(self,msgid=ldap.RES_ANY,all=1,timeout=-1):
    if timeout==0:
      return self._ldap_call(self._l.result,msgid,all,0)
    else:
      result_ldap = None
      start_time = time.time()
      while (result_ldap is None) or (result_ldap==(None,None)):
        if (timeout>0) and (time.time()-start_time>timeout):
          self._ldap_call(self._l.abandon,msgid)
          raise ldap.TIMELIMIT_EXCEEDED(
            "LDAP time limit (%d secs) exceeded." % (timeout)
          )
        result_ldap = self._ldap_call(self._l.result,msgid,all,0)
      return result_ldap

  def search(self,base,scope,filterstr,attrlist=None,attrsonly=0):
    return self._ldap_call(self._l.search,base,scope,filterstr,attrlist,attrsonly)

  def search_s(self,base,scope,filterstr,attrlist=None,attrsonly=0):
    return self.search_st(base,scope,filterstr,attrlist,attrsonly,timeout=-1)

  def search_st(self,base,scope,filterstr,attrlist=None,attrsonly=0,timeout=-1):
    msgid = self.search(base,scope,filterstr,attrlist,attrsonly)
    result = []
    result_type,result_data = self.result(msgid,0,timeout)
    while result_data:
      result.extend(result_data)
      result_type,result_data = self.result(msgid,0,timeout)
    return result

  def set_cache_options(self,*args,**kwargs):
    return self._ldap_call(self._l.set_cache_options,*args,**kwargs)

  def set_rebind_proc(self,func):
    return self._ldap_call(self._l.set_rebind_proc,func)

  def simple_bind(self,who,passwd):
    return self.bind(who,passwd,ldap.AUTH_SIMPLE)

  def simple_bind_s(self,who,passwd):
    return self.bind_s(who,passwd,ldap.AUTH_SIMPLE)

  def start_tls_s(self,*args,**kwargs):
    return self._ldap_call(self._l.start_tls_s,*args,**kwargs)
  
  def ufn_search_s(self,*args,**kwargs):
    return self._ldap_call(self._l.ufn_search_s,*args,**kwargs)

  def ufn_setfilter(self,*args,**kwargs):
    return self._ldap_call(self._l.ufn_setfilter,*args,**kwargs)

  def ufn_setprefix(self,*args,**kwargs):
    return self._ldap_call(self._l.ufn_setprefix,*args,**kwargs)

  def unbind(self):
    return self._ldap_call(self._l.unbind,)

  def unbind_s(self):
    return self._ldap_call(self._l.unbind_s,)

  def uncache_entry(self,dn):
    return self._ldap_call(self._l.uncache_entry,dn)

  def uncache_request(self,msgid):
    return self._ldap_call(self._l.uncache_request,msgid)

  def url_search_s(self,*args,**kwargs):
    return self._ldap_call(self._l.url_search_s,*args,**kwargs)

  def url_search_st(self,*args,**kwargs):
    return self._ldap_call(self._l.url_search_st,*args,**kwargs)

  def get_option(self,*args,**kwargs):
    return self._ldap_call(self._l.get_option,*args,**kwargs)

  def set_option(self,*args,**kwargs):
    return self._ldap_call(self._l.set_option,*args,**kwargs)

def open(host):
  """Return ldapthreadlock.LDAPObject instance"""
  return LDAPObject(host=host)

def initialize(uri):
  """Return ldapthreadlock.LDAPObject instance"""
  return LDAPObject(uri=uri)
# init() is just an alias for initialize()
init = initialize

def get_option(self,*args,**kwargs):
  return _ldap_call(ldap.get_option,*args,**kwargs)

def set_option(self,*args,**kwargs):
  return _ldap_call(ldap.get_option,*args,**kwargs)

