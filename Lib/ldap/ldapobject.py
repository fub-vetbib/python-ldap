"""
ldapobject.py - wraps class _ldap.LDAPObject
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
- LDAPObject class should be exactly the same like _ldap.LDAPObject

Usage:
Directly imported by ldap/__init__.py. The symbols of _ldap are
overridden.

Thread-lock:
Basically calls into the LDAP lib are serialized by the module-wide
lock self._ldap_object_lock.
"""

__version__ = '0.5.2'

__all__ = [
  'LDAPObject',
  'SimpleLDAPObject',
  'NonblockingLDAPObject',
  'ReconnectLDAPObject',
  'SmartLDAPObject'
]


if __debug__:
  # Tracing is only supported in debugging mode
  import traceback

import sys,time,_ldap,ldap

from ldap.schema import SCHEMA_ATTRS

from ldap import LDAPError

class SimpleLDAPObject:
  """
  Drop-in wrapper class around _ldap.LDAPObject
  """

  CLASSATTR_OPTION_MAPPING = {
    # taken from Modules/options.h
    "protocol_version":   ldap.OPT_PROTOCOL_VERSION,
    "deref":              ldap.OPT_DEREF,
    "referrals":          ldap.OPT_REFERRALS,
    "timelimit":          ldap.OPT_TIMELIMIT,
    "sizelimit":          ldap.OPT_SIZELIMIT,
    "network_timeout":    ldap.OPT_NETWORK_TIMEOUT,
  }

  def __init__(
    self,uri,
    trace_level=0,trace_file=None,trace_stack_limit=5
  ):
    self._trace_level = trace_level
    self._trace_file = trace_file or sys.stdout
    self._trace_stack_limit = trace_stack_limit
    self._uri = uri
    self._ldap_object_lock = self._ldap_lock()
    self._l = ldap._ldap_function_call(_ldap.initialize,uri)
    self.timeout = -1
    self.protocol_version = ldap.VERSION3

  def _ldap_lock(self):
    if ldap.LIBLDAP_R:
      return ldap.LDAPLock()
    else:
      return ldap._ldap_module_lock

  def _ldap_call(self,func,*args,**kwargs):
    """
    Wrapper method mainly for serializing calls into OpenLDAP libs
    and trace logs
    """
    if __debug__:
      if self._trace_level>=1:# and func.__name__!='result':
        self._trace_file.write('*** %s - %s (%s,%s)\n' % (
          self._uri,
          self.__class__.__name__+'.'+func.__name__,
          repr(args),repr(kwargs)
        ))
        if self._trace_level>=3:
          traceback.print_stack(limit=self._trace_stack_limit,file=self._trace_file)
    self._ldap_object_lock.acquire()
    try:
      try:
        result = func(*args,**kwargs)
      finally:
        self._ldap_object_lock.release()
    except LDAPError,e:
      if __debug__ and self._trace_level>=2:
        self._trace_file.write('=> LDAPError: %s\n' % (str(e)))
      raise
    if __debug__ and self._trace_level>=2:
      if result!=None and result!=(None,None):
        self._trace_file.write('=> result: %s\n' % (repr(result)))
    return result

  def __setattr__(self,name,value):
    if self.CLASSATTR_OPTION_MAPPING.has_key(name):
      self.set_option(self.CLASSATTR_OPTION_MAPPING[name],value)
    else:
      self.__dict__[name] = value

  def __getattr__(self,name):
    if self.CLASSATTR_OPTION_MAPPING.has_key(name):
      return self.get_option(self.CLASSATTR_OPTION_MAPPING[name])
    elif self.__dict__.has_key(name):
      return self.__dict__[name]
    else:
      raise AttributeError,'%s has no attribute %s' % (
        self.__class__.__name__,repr(name)
      )

  def abandon(self,msgid):
    """
    abandon(msgid) -> None    
        Abandons or cancels an LDAP operation in progress. The msgid should
        be the message id of an outstanding LDAP operation as returned
        by the asynchronous methods search(), modify() etc.  The caller
        can expect that the result of an abandoned operation will not be
        returned from a future call to result().
    """
    return self._ldap_call(self._l.abandon,msgid)

  def add(self,dn,modlist):
    """
    add(dn, modlist) -> int
        This function adds a new entry with a distinguished name
        specified by dn which means it must not already exist.
        The parameter modlist is similar to the one passed to modify(),
        except that no operation integer need be included in the tuples.
    """
    return self._ldap_call(self._l.add,dn,modlist)

  def add_s(self,dn,modlist):
    msgid = self.add(dn,modlist)
    self.result(msgid,all=1,timeout=self.timeout)

  def bind(self,who,cred,method):
    """
    bind(who, cred, method) -> int
    """
    return self._ldap_call(self._l.bind,who,cred,method)

  def bind_s(self,who,cred,method):
    """
    bind_s(who, cred, method) -> None
    """
    msgid = self.bind(who,cred,method)
    self.result(msgid,all=1,timeout=self.timeout)

  def sasl_bind_s(self,who,auth):
    """
    sasl_bind_s(who, auth) -> None
    """
    return self._ldap_call(self._l.sasl_bind_s,who,auth)

  def compare(self,dn,attr,value):
    """
    compare(dn, attr, value) -> int
    compare_s(dn, attr, value) -> int    
        Perform an LDAP comparison between the attribute named attr of
        entry dn, and the value value. The synchronous form returns 0
        for false, or 1 for true.  The asynchronous form returns the
        message id of the initiates request, and the result of the
        asynchronous compare can be obtained using result().

        Note that this latter technique yields the answer by raising
        the exception objects COMPARE_TRUE or COMPARE_FALSE.

        A design bug in the library prevents value from containing
        nul characters.
    """
    return self._ldap_call(self._l.compare,dn,attr,value)

  def compare_s(self,dn,attr,value):
    msgid = self.compare(dn,attr,value)
    try:
      self.result(msgid,all=1,timeout=self.timeout)
    except _ldap.COMPARE_TRUE:
      return 1
    except _ldap.COMPARE_FALSE:
      return 0
    return None

  def delete(self,dn):
    """
    delete(dn) -> int
    delete_s(dn) -> None    
        Performs an LDAP delete operation on dn. The asynchronous
        form returns the message id of the initiated request, and the
        result can be obtained from a subsequent call to result().
    """
    return self._ldap_call(self._l.delete,dn)

  def delete_s(self,dn):
    msgid = self.delete(dn)
    self.result(msgid,all=1,timeout=self.timeout)

  def manage_dsa_it(self,enable,critical=0):
    """
    manage_dsa_it() -> None
    Enable or disable manageDSAit mode (see draft-zeilenga-ldap-namedref)
    """
    self._ldap_call(self._l.manage_dsa_it,enable,critical)
  
  def modify(self,dn,modlist):
    """
    modify(dn, modlist) -> int
    modify_s(dn, modlist) -> None    
        Performs an LDAP modify operation on an entry's attributes.
        dn is the DN of the entry to modify, and modlist is the list
        of modifications to make to the entry.

        Each element of the list modlist should be a tuple of the form
        (mod_op,mod_type,mod_vals), where mod_op is the operation (one
        of MOD_ADD, MOD_DELETE, or MOD_REPLACE), mod_type is a string
        indicating the attribute type name, and mod_vals is either
        a string value or a list of string values to add, delete or
        replace respectively.  For the delete operation, mod_vals may
        be None indicating that all attributes are to be deleted.

        The asynchronous modify() returns the message id of the
        initiated request.
    """
    return self._ldap_call(self._l.modify,dn,modlist)

  def modify_s(self,dn,modlist):
    msgid = self.modify(dn,modlist)
    self.result(msgid,all=1,timeout=self.timeout)

  def modrdn(self,dn,newrdn,delold=1):
    """
    modrdn(dn, newrdn [,delold=1]) -> int
    modrdn_s(dn, newrdn [,delold=1]) -> None    
        Perform a modify RDN operation. These routines take dn, the
        DN of the entry whose RDN is to be changed, and newrdn, the
        new RDN to give to the entry. The optional parameter delold
        is used to specify whether the old RDN should be kept as
        an attribute of the entry or not.  The asynchronous version
        returns the initiated message id.

        This operation is emulated by rename() and rename_s() methods
        since the modrdn2* routines in the C library are deprecated.
    """
    return self.rename(dn,newrdn,None,delold)

  def modrdn_s(self,dn,newrdn,delold=1):
    self.rename_s(dn,newrdn,None,delold)

  def rename(self,dn,newrdn,newsuperior=None,delold=1):
    """
    rename(dn, newrdn [, newsuperior=None] [,delold=1]) -> int
    rename_s(dn, newrdn [, newsuperior=None] [,delold=1]) -> None
        Perform a rename entry operation. These routines take dn, the
        DN of the entry whose RDN is to be changed, newrdn, the
        new RDN, and newsuperior, the new parent DN, to give to the entry.
        If newsuperior is None then only the RDN is modified.
        The optional parameter delold is used to specify whether the
        old RDN should be kept as an attribute of the entry or not.
        The asynchronous version returns the initiated message id.

        This actually corresponds to the rename* routines in the
        LDAP-EXT C API library.
    """
    return self._ldap_call(self._l.rename,dn,newrdn,newsuperior,delold)

  def rename_s(self,dn,newrdn,newsuperior=None,delold=1):
    msgid = self.rename(dn,newrdn,newsuperior,delold)
    self.result(msgid,all=1,timeout=self.timeout)

  def result(self,msgid=_ldap.RES_ANY,all=1,timeout=None):
    """
    result([msgid=RES_ANY [,all=1 [,timeout=None]]]) -> (result_type, result_data)

        This method is used to wait for and return the result of an
        operation previously initiated by one of the LDAP asynchronous
        operation routines (eg search(), modify(), etc.) They all
        returned an invocation identifier (a message id) upon successful
        initiation of their operation. This id is guaranteed to be
        unique across an LDAP session, and can be used to request the
        result of a specific operation via the msgid parameter of the
        result() method.

        If the result of a specific operation is required, msgid should
        be set to the invocation message id returned when the operation
        was initiated; otherwise RES_ANY should be supplied.

        The all parameter only has meaning for search() responses
        and is used to select whether a single entry of the search
        response should be returned, or to wait for all the results
        of the search before returning.

        A search response is made up of zero or more search entries
        followed by a search result. If all is 0, search entries will
        be returned one at a time as they come in, via separate calls
        to result(). If all is 1, the search response will be returned
        in its entirety, i.e. after all entries and the final search
        result have been received.

        For all set to 0, result tuples
        trickle in (with the same message id), and with the result type
        RES_SEARCH_ENTRY, until the final result which has a result
        type of RES_SEARCH_RESULT and a (usually) empty data field.
        When all is set to 1, only one result is returned, with a
        result type of RES_SEARCH_RESULT, and all the result tuples
        listed in the data field.

        The method returns a tuple of the form (result_type,
        result_data).  The result_type is a string, being one of:
        'RES_BIND', 'RES_SEARCH_ENTRY', 'RES_SEARCH_RESULT',
        'RES_SEARCH_REFERENCE','RES_MODIFY', 'RES_ADD', 'RES_DELETE',
        'RES_MODRDN', or 'RES_COMPARE'.

        The constants RES_* are set to these strings, for convenience.

        See search() for a description of the search result's
        result_data, otherwise the result_data is normally meaningless.

        The result() method will block for timeout seconds, or
        indefinitely if timeout is negative.  A timeout of 0 will effect
        a poll. The timeout can be expressed as a floating-point value.
        If timeout is None the default in self.timeout is used.

        If a timeout occurs, a TIMEOUT exception is raised, unless
        polling (timeout = 0), in which case (None, None) is returned.
    """
    if timeout is None:
      timeout = self.timeout
    return self._ldap_call(self._l.result,msgid,all,timeout)
 
  def search_ext(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,serverctrls=None,clientctrls=None,timeout=-1,sizelimit=0):
    """
    search(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0]]]) -> int
    search_s(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0]]])
    search_st(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0 [,timeout=-1]]]])
    search_ext(base,scope,[,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0 [,serverctrls=None [,clientctrls=None [,timeout=-1 [,sizelimit=0]]]]]]])
    search_ext_s(base,scope,[,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0 [,serverctrls=None [,clientctrls=None [,timeout=-1 [,sizelimit=0]]]]]]])

        Perform an LDAP search operation, with base as the DN of
        the entry at which to start the search, scope being one of
        SCOPE_BASE (to search the object itself), SCOPE_ONELEVEL
        (to search the object's immediate children), or SCOPE_SUBTREE
        (to search the object and all its descendants).

        filter is a string representation of the filter to
        apply in the search (see RFC 2254).

        Each result tuple is of the form (dn,entry), where dn is a
        string containing the DN (distinguished name) of the entry, and
        entry is a dictionary containing the attributes.
        Attributes types are used as string dictionary keys and attribute
        values are stored in a list as dictionary value.

        The DN in dn is extracted using the underlying ldap_get_dn(),
        which may raise an exception of the DN is malformed.

        If attrsonly is non-zero, the values of attrs will be
        meaningless (they are not transmitted in the result).

        The retrieved attributes can be limited with the attrlist
        parameter.  If attrlist is None, all the attributes of each
        entry are returned.

        serverctrls=None

        clientctrls=None

        The synchronous form with timeout, search_st() or search_ext_s(),
        will block for at most timeout seconds (or indefinitely if
        timeout is negative). A TIMEOUT exception is raised if no result is
        received within the time.

        The amount of search results retrieved can be limited with the
        sizelimit parameter if non-zero.
    """
    return self._ldap_call(
      self._l.search_ext,
      base,scope,filterstr,
      attrlist,attrsonly,
      serverctrls,clientctrls,
      timeout,sizelimit
    )

  def search_ext_s(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,serverctrls=None,clientctrls=None,timeout=-1,sizelimit=0):
    msgid = self._ldap_call(self._l.search_ext,base,scope,filterstr,attrlist,attrsonly,serverctrls,clientctrls,timeout,sizelimit)
    return self.result(msgid,all=1,timeout=timeout)[1]

  def search(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0):
    return self.search_ext(base,scope,filterstr,attrlist,attrsonly)

  def search_s(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0):
    return self.search_ext_s(base,scope,filterstr,attrlist,attrsonly,timeout=self.timeout)

  def search_st(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,timeout=-1):
    return self.search_ext_s(base,scope,filterstr,attrlist,attrsonly,timeout)

  def set_cache_options(self,*args,**kwargs):
    """
    set_cache_options(option) -> None    
        Changes the caching behaviour. Currently supported options are
            CACHE_OPT_CACHENOERRS, which suppresses caching of requests
                that resulted in an error, and
            CACHE_OPT_CACHEALLERRS, which enables caching of all requests.
        The default behaviour is not to cache requests that result in
        errors, except those that result in a SIZELIMIT_EXCEEDED exception.
    """
    return self._ldap_call(self._l.set_cache_options,*args,**kwargs)

  def set_rebind_proc(self,func):
    """
    set_rebind_proc(func) -> None    
        If a referral is returned from the server, automatic re-binding
        can be achieved by providing a function that accepts as an
        argument the newly opened LDAP object and returns the tuple
        (who, cred, method).

        Passing a value of None for func will disable this facility.

        Because of restrictions in the implementation, only one
        rebinding function is supported at any one time. This method
        is only available if the module and library were compiled with
        support for it.
    """
    self._ldap_call(self._l.set_rebind_proc,func)

  def simple_bind(self,who='',cred=''):
    """
    simple_bind([who='' [,cred='']]) -> int
    """
    return self.bind(who,cred,_ldap.AUTH_SIMPLE)

  def simple_bind_s(self,who='',cred=''):
    """
    simple_bind_s([who='' [,cred='']]) -> None
    """
    self.bind_s(who,cred,_ldap.AUTH_SIMPLE)

  def start_tls_s(self,*args,**kwargs):
    """
    start_tls_s() -> None    
    Negotiate TLS with server. The `version' attribute must have been
    set to VERSION3 before calling start_tls_s.
    If TLS could not be started an exception will be raised.
    """
    self._ldap_call(self._l.start_tls_s,*args,**kwargs)
  
  def unbind(self):
    """
    unbind_s() -> None
    unbind() -> int    
        This call is used to unbind from the directory, terminate
        the current association, and free resources. Once called, the
        connection to the LDAP server is closed and the LDAP object
        is invalid. Further invocation of methods on the object will
        yield an exception.
    
        The unbind and unbind_s methods are identical, and are
        synchronous in nature
    """
    return self._ldap_call(self._l.unbind)

  def unbind_s(self):
    msgid = self.unbind()
    if msgid!=None:
      self.result(msgid,all=1,timeout=self.timeout)

  def uncache_entry(self,dn):
    """
    uncache_entry(dn) -> None    
        Removes all cached entries that make reference to dn. This should be
        used, for example, after doing a modify() involving dn.
    """
    self._ldap_call(self._l.uncache_entry,dn)

  def uncache_request(self,msgid):
    """
    uncache_request(msgid) -> None    
        Remove the request indicated by msgid from the cache.
    """
    self._ldap_call(self._l.uncache_request,msgid)

  def url_search(self,url,attrsonly=0):
    """
    url_search(url [,attrsonly=0])
    url_search_s(url [,attrsonly=0])
    url_search_st(url [,attrsonly=0 [,timeout=-1]])
        These routine works much like search_s*, except that many
        search parameters are pulled out of the URL url (see RFC 2255).
    """
    return self._ldap_call(self._l.url_search,url,attrsonly)

  def url_search_st(self,url,attrsonly=0,timeout=-1):
    msgid = self.url_search(url,attrsonly)
    return self.result(msgid,all=1,timeout=timeout)[1]

  def url_search_s(self,url,attrsonly=0):
    return self.url_search_st(url,attrsonly,timeout=self.timeout)

  def get_option(self,option):
    return self._ldap_call(self._l.get_option,option)

  def set_option(self,option,invalue):
    self._ldap_call(self._l.set_option,option,invalue)

  def search_subschemasubentry_s(self,dn=''):
    """
    Returns the distinguished name of the sub schema sub entry
    for a part of a DIT specified by dn.

    None as result indicates that the DN of the sub schema sub entry could
    not be determined.
    """
    try:
      r = self.search_s(
        dn,ldap.SCOPE_BASE,'(objectClass=*)',['subschemaSubentry']
      )
    except (ldap.NO_SUCH_OBJECT,ldap.NO_SUCH_ATTRIBUTE):
      r = []
    except ldap.UNDEFINED_TYPE:
      return None
    try:
      if r:
        e = ldap.cidict.cidict(r[0][1])
        search_subschemasubentry_dn = e.get('subschemaSubentry',[None])[0]
        if search_subschemasubentry_dn is None:
          if dn:
            # Try to find sub schema sub entry in root DSE
            return self.search_subschemasubentry_s(dn='')
          else:
            # If dn was already root DSE we can return here
            return None
        else:
          return search_subschemasubentry_dn
    except IndexError:
      return None

  def read_subschemasubentry_s(self,subschemasubentry_dn,attrs=None):
    """
    Returns the sub schema sub entry's data
    """
    attrs = attrs or SCHEMA_ATTRS
    try:
      r = self.search_s(
        subschemasubentry_dn,ldap.SCOPE_BASE,
        '(objectClass=subschema)',
        attrs
      )
    except ldap.NO_SUCH_OBJECT:
      return None
    else:
      if r:
        return r[0][1]
      else:
        return None


class NonblockingLDAPObject(SimpleLDAPObject):

  def __init__(self,uri,trace_level=0,trace_file=None,result_timeout=-1):
    self._result_timeout = result_timeout
    SimpleLDAPObject.__init__(self,uri,trace_level,trace_file)

  def result(self,msgid=_ldap.RES_ANY,all=1,timeout=-1):
    """
    """
    ldap_result = self._ldap_call(self._l.result,msgid,0,self._result_timeout)
    if not all:
      return ldap_result
    start_time = time.time()
    all_results = []
    while all:
      while ldap_result[0] is None:
        if (timeout>=0) and (time.time()-start_time>timeout):
          self._ldap_call(self._l.abandon,msgid)
          raise _ldap.TIMEOUT(
            "LDAP time limit (%d secs) exceeded." % (timeout)
          )
        time.sleep(0.00001)
        ldap_result = self._ldap_call(self._l.result,msgid,0,self._result_timeout)
      if ldap_result[1] is None:
        break
      all_results.extend(ldap_result[1])
      ldap_result = None,None
    return all_results

  def search_st(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,timeout=-1):
    msgid = self.search(base,scope,filterstr,attrlist,attrsonly)
    return self.result(msgid,all=1,timeout=timeout)


class ReconnectLDAPObject(SimpleLDAPObject):
  """
  In case of server failure (ldap.SERVER_DOWN) the implementations
  of all synchronous operation methods (search_s() etc.) are doing
  an automatic reconnect and rebind and will retry the very same
  operation.
  
  This is very handy for broken LDAP server implementations
  (e.g. in Lotus Domino) which drop connections very often making
  it impossible to have a long-lasting control flow in the
  application.
  """

  __transient_attrs__ = {
    '_l':None,
    '_ldap_object_lock':None,
    '_trace_file':None,
  }

  def __init__(
    self,uri,
    trace_level=0,trace_file=None,trace_stack_limit=5,
    retry_max=1,retry_delay=60.0
  ):
    """
    Parameters like SimpleLDAPObject.__init__() with these
    additional arguments:

    retry_max
        Maximum count of reconnect trials
    retry_delay
        Time span to wait between two reconnect trials
    """
    self._uri = uri
    self._options = {}
    self._last_bind = None
    SimpleLDAPObject.__init__(
      self,uri,
      trace_level,
      trace_file,
      trace_stack_limit
    )
    self._retry_max = retry_max
    self._retry_delay = retry_delay
    self._start_tls = 0
    self._reconnects_done = 0L

  def __getstate__(self):
    """return data representation for pickled object"""
    d = {}
    for k,v in self.__dict__.items():
      if not self.__transient_attrs__.has_key(k):
        d[k] = v
    return d

  def __setstate__(self,d):
    """set up the object from pickled data"""
    self.__dict__.update(d)
    self._ldap_object_lock = self._ldap_lock()
    self._trace_file = sys.stdout
    self.reconnect(self._uri)

  def _apply_last_bind(self):
    if self._last_bind!=None:
      func,args,kwargs = self._last_bind
      func(*args,**kwargs)

  def _restore_options(self):
    """Restore all recorded options"""
    for k,v in self._options.items():
      SimpleLDAPObject.set_option(self,k,v)

  def reconnect(self,uri):
    # Drop and clean up old connection completely
    # Reconnect
    reconnect_counter = self._retry_max
    while reconnect_counter:
      if __debug__ and self._trace_level>=1:
        self._trace_file.write('*** Try %d. reconnect to %s...\n' % (
          self._retry_max-reconnect_counter+1,uri
        ))
      try:
        # Do the connect
        self._l = ldap._ldap_function_call(_ldap.initialize,uri)
        self._restore_options()
        # StartTLS extended operation in case this was called before
        if self._start_tls:
          self.start_tls_s()
        # Repeat last simple or SASL bind
        self._apply_last_bind()
      except:
        if __debug__ and self._trace_level>=1:
          self._trace_file.write('*** %d. reconnect to %s failed\n' % (
            self._retry_max-reconnect_counter+1,uri
          ))
        reconnect_counter = reconnect_counter-1
        if not reconnect_counter:
          raise
        if __debug__ and self._trace_level>=1:
          self._trace_file.write('=> delay %s...\n' % (self._retry_delay))
        time.sleep(self._retry_delay)
      else:
        if __debug__ and self._trace_level>=1:
          self._trace_file.write('*** %d. reconnect to %s successful, last operation will be repeated\n' % (
            self._retry_max-reconnect_counter+1,uri
          ))
        self._reconnects_done = self._reconnects_done + 1L
        break

  def _apply_method_s(self,func,*args,**kwargs):
    try:
      return func(self,*args,**kwargs)
    except ldap.SERVER_DOWN:
      # Reconnect
      self.reconnect(self._uri)
      # Re-try last operation
      return func(self,*args,**kwargs)

  def set_option(self,option,invalue):
    self._options[option] = invalue
    SimpleLDAPObject.set_option(self,option,invalue)

  def bind_s(self,*args,**kwargs):
    self._last_bind = (self.bind_s,args,kwargs)
    return SimpleLDAPObject.bind_s(self,*args,**kwargs)

  def start_tls_s(self,*args,**kwargs):
    res = SimpleLDAPObject.start_tls_s(self,*args,**kwargs)
    self._start_tls = 1
    return res

  def sasl_bind_s(self,who,auth):
    """
    sasl_bind_s(who, auth) -> None
    """
    self._last_bind = (self.sasl_bind_s,(who,auth),{})
    return self._ldap_call(self._l.sasl_bind_s,who,auth)

  def add_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.add_s,*args,**kwargs)

  def compare_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.compare_s,*args,**kwargs)

  def delete_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.delete_s,*args,**kwargs)

  def modify_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.modify_s,*args,**kwargs)

  def rename_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.rename_s,*args,**kwargs)

  def search_ext_s(self,*args,**kwargs):
    return self._apply_method_s(SimpleLDAPObject.search_ext_s,*args,**kwargs)


class SmartLDAPObject(ReconnectLDAPObject):
  """
  Mainly the __init__() method does some smarter things
  like negotiating the LDAP protocol version and calling
  LDAPObject.start_tls_s().
  """

  def __init__(
    self,uri,
    trace_level=0,trace_file=None,trace_stack_limit=5,
    retry_max=1,retry_delay=60.0,
    who='',cred='',
    start_tls=1,
    tls_cacertfile=None,tls_cacertdir=None,
    tls_clcertfile=None,tls_clkeyfile=None,
  ):
    """
    Return LDAPObject instance by opening LDAP connection to
    LDAP host specified by LDAP URL.

    Unlike ldap.initialize() this function also trys to bind
    explicitly with the bind DN and credential given as parameter,
    probe the supported LDAP version and trys to use
    StartTLS extended operation if this was specified.

    Parameters like ReconnectLDAPObject.__init__() with these
    additional arguments:
    who,cred
        The Bind-DN and credential to use for simple bind
        right after connecting.
    start_tls
        Determines if StartTLS extended operation is tried
        on a LDAPv3 server and if the LDAP URL scheme is ldap:.
        If LDAP URL scheme is not ldap: (e.g. ldaps: or ldapi:)
        this parameter is ignored.
        0       Don't use StartTLS ext op
        1       Try StartTLS ext op but proceed when unavailable
        2       Try StartTLS ext op and re-raise exception if it fails
    tls_cacertfile

    tls_clcertfile

    tls_clkeyfile

    """
    # Initialize LDAP connection
    ReconnectLDAPObject.__init__(
      self,uri,
      trace_level=trace_level,
      trace_file=trace_file,
      trace_stack_limit=trace_stack_limit,
      retry_max=retry_max,
      retry_delay=retry_delay
    )
    # Set protocol version to LDAPv3
    self.protocol_version = ldap.VERSION3
    self.started_tls = 0
    try:
      self.simple_bind_s(who,cred)
    except ldap.PROTOCOL_ERROR:
      # Drop connection completely
      self.unbind_s() ; del self._l
      self._l = self._ldap_call(_ldap.initialize,self._uri)
      self.protocol_version = ldap.VERSION2
      self.simple_bind_s(who,cred)
    # Try to start TLS if requested
    if start_tls>0 and uri[:5]=='ldap:':
      if self.protocol_version>=ldap.VERSION3:
        try:
          self.start_tls_s()
        except (ldap.PROTOCOL_ERROR,ldap.CONNECT_ERROR):
          if start_tls>=2:
            # Application does not accept clear-text connection
            # => re-raise exception
            raise
        else:
          self.started_tls = 1
      else:
        if start_tls>=2:
          raise ValueError,"StartTLS extended operation only possible on LDAPv3+ server!"
    if self.protocol_version==ldap.VERSION2 or (who and cred):
      self.simple_bind_s(who,cred)


# The class called LDAPObject will be used as default for
# ldap.open() and ldap.initialize()
LDAPObject = SimpleLDAPObject
