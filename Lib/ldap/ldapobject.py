"""
ldapobject.py - wraps class _ldap.LDAPObject
written by Michael Stroeder <michael@stroeder.com>

\$Id$

License:
Public domain. Do anything you want with this module.

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
- LDAPObject class should be exactly the same like _ldap.LDAPObject

Usage:
Directly imported by ldap/__init__.py. The symbols of _ldap are
overridden.

Thread-lock:
Basically calls into the LDAP lib are serialized by the module-wide
lock ldap._ldap_lock. To avoid long-time blocking of other threads
synchronous methods like search_s() etc. and the result() method
were rewritten to do solely asynchronous LDAP lib calls with zero
timeout.
The timeout handling is done within the method result() which probably leads
to less exact timing.
"""

__version__ = '0.1.1'

__all__ = [
  'LDAPObject',
  'SimpleLDAPObject',
  'NonblockingLDAPObject',
  'SmartLDAPObject'
]


if __debug__:
  # Tracing is only supported in debugging mode
  import traceback

import sys,string,time,_ldap,ldap

class SimpleLDAPObject:
  """
  Drop-in wrapper class around _ldap.LDAPObject
  """

  def __init__(self,uri,trace_level=0,trace_file=sys.stdout):
    self._trace_level = trace_level
    self._trace_file = trace_file
    self._uri = uri
    self._l = self._ldap_call(_ldap.initialize,uri)

  def _ldap_call(self,func,*args,**kwargs):
    """Wrapper method mainly for trace logs"""
    if __debug__:
      if self._trace_level>=1 and func.__name__!='result':
        self._trace_file.write('*** %s.%s (%s,%s)\n' % (
          self.__module__,
          self.__class__.__name__+'.'+func.__name__,
          repr(args),repr(kwargs)
        ))
        if self._trace_level>=2:
          traceback.print_stack(file=self._trace_file)
    result = ldap._ldap_call(func,*args,**kwargs)
    if __debug__:
      if self._trace_level>=1 and result!=None and result!=(None,None):
        self._trace_file.write('=> result: %s\n' % (repr(result)))
    return result

  def __setattr__(self,name,value):
    if name in ['_l','_trace_level','_trace_file','_uri']:
      self.__dict__[name] = value
    else:
      if __debug__:
        if self._trace_level>=1:
          self._trace_file.write('*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__setattr__(%s,%s)' % (name,value)
          )
          if self._trace_level>=2:
            traceback.print_stack(file=self._trace_file)
      ldap._ldap_lock.acquire()
      try:
        setattr(self._l,name,value)
      finally:
        ldap._ldap_lock.release()

  def __getattr__(self,name):
    if name in ['_l','_trace_level','_trace_file','_uri']:
      return self.__dict__[name]
    else:
      ldap._ldap_lock.acquire()
      try:
        value = getattr(self._l,name)
      finally:
        ldap._ldap_lock.release()
      if __debug__:
        if self._trace_level>=1:
          self._trace_file.write('*** %s:' % (self.__module__),\
            self.__class__.__name__+'.__getattr__(%s)' % (name),'=>',value
          )
          if self._trace_level>=2:
            traceback.print_stack(file=sys.stdout)
    return value

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
        This function is similar to modify(), except that no operation
        integer need be included in the tuples.
    """
    return self._ldap_call(self._l.add,dn,modlist)

  def add_s(self,dn,modlist):
    msgid = self.add(dn,modlist)
    self.result(msgid)

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
    self.result(msgid)

  def compare(self,*args,**kwargs):
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
    return self._ldap_call(self._l.compare,*args,**kwargs)

  def compare_s(self,*args,**kwargs):
    msgid = self.compare(*args,**kwargs)
    try:
      self.result(msgid)
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
    self.result(msgid)

  def destroy_cache(self):
    """
    destroy_cache() -> None    
        Turns off caching and removed it from memory.
    """
    self._ldap_call(self._l.destroy_cache,)

  def disable_cache(self):
    """
    disable_cache() -> None    
        Temporarily disables use of the cache. New requests are
        not cached, and the cache is not checked when returning
        results. Cache contents are not deleted.
    """
    self._ldap_call(self._l.disable_cache,)

  def enable_cache(self,timeout=_ldap.NO_LIMIT,maxmem=_ldap.NO_LIMIT):
    """
    enable_cache([timeout=NO_LIMIT, [maxmem=NO_LIMIT]]) -> None    
        Using a cache often greatly improves performance. By default
        the cache is disabled. Specifying timeout in seconds is used
        to decide how long to keep cached requests. The maxmem value
        is in bytes, and is used to set an upper bound on how much
        memory the cache will use. A value of NO_LIMIT for either
        indicates unlimited.  Subsequent calls to enable_cache()
        can be used to adjust these parameters.

        This and other caching methods are not available if the library
        and the ldap module were compiled with support for it.
    """
    self._ldap_call(self._l.enable_cache,timeout,maxmem)

  def fileno(self):
    """
    fileno() -> int
        Return the file descriptor associated with this connection.
    """
    return self._ldap_call(self._l.fileno,)

  def flush_cache(self):
    """
    flush_cache() -> None    
        Deletes the cache's contents, but does not affect it in any other way.
    """
    self._ldap_call(self._l.flush_cache)

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
    self.result(msgid)

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
    self.result(msgid)

  def result(self,msgid=_ldap.RES_ANY,all=1,timeout=-1):
    """
    result([msgid=RES_ANY [,all=1 [,timeout=-1]]]) -> (result_type, result_data)

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

        The method returns a tuple of the form (result_type,
        result_data).  The result_type is a string, being one of:
        'RES_BIND', 'RES_SEARCH_ENTRY', 'RES_SEARCH_RESULT',
        'RES_MODIFY', 'RES_ADD', 'RES_DELETE', 'RES_MODRDN', or
        'RES_COMPARE'.

        The constants RES_* are set to these strings, for convenience.

        See search() for a description of the search result's
        result_data, otherwise the result_data is normally meaningless.

        The result() method will block for timeout seconds, or
        indefinitely if timeout is negative.  A timeout of 0 will effect
        a poll.  The timeout can be expressed as a floating-point value.

        If a timeout occurs, a TIMEOUT exception is raised, unless
        polling (timeout = 0), in which case (None, None) is returned.
    """
    return self._ldap_call(self._l.result,msgid,all,timeout)
 
  def search(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0):
    """
    search(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0]]) -> int
    search_s(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0]])
    search_st(base, scope [,filterstr='(objectClass=*)' [,attrlist=None [,attrsonly=0 [,timeout=-1]]])

        Perform an LDAP search operation, with base as the DN of
        the entry at which to start the search, scope being one of
        SCOPE_BASE (to search the object itself), SCOPE_ONELEVEL
        (to search the object's immediate children), or SCOPE_SUBTREE
        (to search the object and all its descendants).

        filter is a string representation of the filter to
        apply in the search (see RFC 2254).

        When using the asynchronous form and result(), the all parameter
        affects how results come in.  For all set to 0, result tuples
        trickle in (with the same message id), and with the result type
        RES_SEARCH_ENTRY, until the final result which has a result
        type of RES_SEARCH_RESULT and a (usually) empty data field.
        When all is set to 1, only one result is returned, with a
        result type of RES_SEARCH_RESULT, and all the result tuples
        listed in the data field.

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

        The synchronous form with timeout, search_st(), will block
        for at most timeout seconds (or indefinitely if timeout is
        negative). A TIMEOUT exception is raised if no result is
        received within the time.
    """
    return self._ldap_call(self._l.search,base,scope,filterstr,attrlist,attrsonly)

  def search_s(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0):
    return self.search_st(base,scope,filterstr,attrlist,attrsonly,timeout=-1)

  def search_st(self,base,scope,filterstr='(objectClass=*)',attrlist=None,attrsonly=0,timeout=-1):
    msgid = self.search(base,scope,filterstr,attrlist,attrsonly)
    return self.result(msgid,all=1,timeout=timeout)[1]

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

  def simple_bind(self,who,passwd):
    """
    simple_bind(who, passwd) -> int
    """
    return self.bind(who,passwd,_ldap.AUTH_SIMPLE)

  def simple_bind_s(self,who,passwd):
    """
    simple_bind_s(who, passwd) -> None
    """
    self.bind_s(who,passwd,_ldap.AUTH_SIMPLE)

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
      self.result(msgid)

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
    search_results = []
    for res_type,res_data in self.result(msgid,all=1,timeout=timeout):
      search_results.extend(res_data)
    return search_results

  def url_search_s(self,url,attrsonly=0):
    return self.url_search_st(url,attrsonly,timeout=-1)

  def get_option(self,option):
    return self._ldap_call(self._l.get_option,option)

  def set_option(self,option,invalue):
    self._ldap_call(self._l.set_option,option,invalue)


class NonblockingLDAPObject(SimpleLDAPObject):

  def __init__(self,uri,trace_level=0,trace_file=sys.stdout,result_timeout=0.05):
    self._result_timeout = result_timeout
    SimpleLDAPObject.__init__(self,uri,trace_level,trace_file)

  def result(self,msgid=_ldap.RES_ANY,all=1,timeout=-1):
    """
    result([msgid=RES_ANY [,all=1 [,timeout=-1]]]) -> (result_type, result_data)

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

        The method returns a tuple of the form (result_type,
        result_data).  The result_type is a string, being one of:
        'RES_BIND', 'RES_SEARCH_ENTRY', 'RES_SEARCH_RESULT',
        'RES_MODIFY', 'RES_ADD', 'RES_DELETE', 'RES_MODRDN', or
        'RES_COMPARE'.

        The constants RES_* are set to these strings, for convenience.

        See search() for a description of the search result's
        result_data, otherwise the result_data is normally meaningless.

        The result() method will block for timeout seconds, or
        indefinitely if timeout is negative.  A timeout of 0 will effect
        a poll.  The timeout can be expressed as a floating-point value.

        If a timeout occurs, a TIMEOUT exception is raised, unless
        polling (timeout = 0), in which case (None, None) is returned.
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
 

class SmartLDAPObject(SimpleLDAPObject):
  """
  Mainly the __init__() method does some smarter things.
  """

  def __init__(
    self,uri,
    trace_level=0,trace_file=sys.stdout,
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

    Because it has a more complex behaviour this function
    is not suitable for doing fast (re-)connects.

    Compability note:
    Since the module ldapurl is used this function only works
    with Python 2.0+.

    Parameters:
    uri
        LDAP URL containing at least connection scheme and hostport,
        e.g. ldap://localhost:389
    who
        The Bind-DN to use. If this is empty and the LDAP server
        supports LDAPv3 no extra BindRequest is done.
    cred
        The credential to use for simple bind. If this is empty
        and the LDAP server supports LDAPv3 no extra BindRequest
        is done.
    start_tls
        Determines if StartTLS extended operation is tried
        on a LDAPv3 server and if the LDAP URL scheme is ldap:.
        If LDAP URL scheme is not ldap: (e.g. ldaps: or ldapi:)
        this parameter is ignored.
        0       Don't use StartTLS ext op
        1       Try StartTLS ext op but proceed when unavailable
        2       Try StartTLS ext op and re-raise ldap.PROTOCOL_ERROR
                if it fails
    tls_cacertfile

    tls_clcertfile

    tls_clkeyfile

    trace_level
        If non-zero a trace output of LDAP calls is generated.
    trace_file
        File object where to write the trace output to.
        Default is to use stdout.
    """
    # Strip white-spaces from uri
    uri = string.strip(uri)
    # Initialize LDAP connection
    SimpleLDAPObject.__init__(self,uri,trace_level,trace_file)
    # Set protocol version to LDAPv3
    self.set_option(ldap.OPT_PROTOCOL_VERSION,ldap.VERSION3)
    try:
      self.search_s('',ldap.SCOPE_BASE,'(objectClass=*)',['objectClass'])
    except ldap.NO_SUCH_OBJECT,ldap.PROTOCOL_ERROR:
      # Drop connection completely
      self.unbind_s() ; del self._l
      self._l = self._ldap_call(_ldap.initialize,self._uri)
      self.set_option(ldap.OPT_PROTOCOL_VERSION,ldap.VERSION2)
      self.simple_bind_s(who,cred)
    protocol_version = self.get_option(ldap.OPT_PROTOCOL_VERSION)
    # Try to start TLS if requested
    if start_tls>0 and uri[:5]=='ldap:':
      if protocol_version>=ldap.VERSION3:
        try:
          self.start_tls_s()
        except ldap.PROTOCOL_ERROR:
          if start_tls>=2:
            # Application does not accept clear-text connection
            # => re-raise exception
            raise
      else:
        if start_tls>=2:
          raise ValueError,"StartTLS extended operation only possible on LDAPv3+ server!"
    if protocol_version==ldap.VERSION2 or (who and cred):
      self.simple_bind_s(who,cred)


# The class called LDAPObject will be used as default for
# ldap.open() and ldap.initialize()
LDAPObject = SimpleLDAPObject

