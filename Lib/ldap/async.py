"""
ldap.async - handle async LDAP operations
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$

Python compability note:
Tested on Python 2.0+ but should run on Python 1.5.x.
"""

__version__ = '0.0.2'


_searchResultTypes={
  'RES_SEARCH_ENTRY':None,
  'RES_SEARCH_RESULT':None,
  'RES_SEARCH_REFERENCE':None
}

_entryResultTypes={
  'RES_SEARCH_ENTRY':None,
  'RES_SEARCH_RESULT':None,
}


class WrongResultType(Exception):

  def __init__(self,receivedResultType,expectedResultTypes):
    self.receivedResultType = receivedResultType
    self.expectedResultTypes = expectedResultTypes

  def __str__(self):
    return 'Received wrong result type %s (expected one of %s).' % (
      self.receivedResultType,
      ', '.join(self.expectedResultTypes),
    )
      

class AsyncSearchHandler:
  """
  Class for stream-processsing LDAP search results
  """

  def __init__(self,l):
    """
    Initialize a StreamResultHandler
    
    Parameters:
    l
        LDAPObject instance
    """
    self._l = l
    self._msgId = None

  def startSearch(
    self,
    searchRoot,
    searchScope,
    filterStr,
    attrList=None,
    attrsOnly=0,
    timeout=-1,
    sizelimit=0
  ):
    """
    searchRoot
        See parameter base of method LDAPObject.search()
    searchScope
        See parameter scope of method LDAPObject.search()
    filterStr
        See parameter filter of method LDAPObject.search()
    attrList=None
        See parameter attrlist of method LDAPObject.search()
    attrsOnly
        See parameter attrsonly of method LDAPObject.search()
    timeout
        Maximum time the server shall use for search operation
    sizeLimit
        Maximum number of entries a server should return
        (request client-side limit)
    """
    self._msgId = self._l.search_ext(
      searchRoot,searchScope,filterStr,
      attrList,attrsOnly,None,None,timeout,sizelimit
    )
    return # startSearch()

  def preProcessing(self):
    """
    Do anything you want after starting search but
    before receiving and processing results
    """

  def postProcessing(self):
    """
    Do anything you want after receiving and processing results
    """

  def processResults(self,ignoreResultsNumber=0,processResultsCount=0,timeout=-1):
    """
    ignoreResultsNumber
        Don't process the first ignoreResultsNumber results.
    processResultsCount
        If non-zero this parameters indicates the number of results
        processed is limited to processResultsCount.
    timeout
        See parameter timeout of ldap.LDAPObject.result()
    """
    self.preProcessing()
    result_counter = 0
    end_result_counter = ignoreResultsNumber+processResultsCount
    go_ahead = 1
    partial = 0
    self.beginResultsDropped = 0
    self.endResultBreak = result_counter
    try:
      result_type,result_list = None,None
      while go_ahead:
        while result_type is None and not result_list:
          result_type,result_list = self._l.result(self._msgId,0,timeout)
        if not result_list:
          break
        if not _searchResultTypes.has_key(result_type):
          raise WrongResultType(result_type,_searchResultTypes.keys())
        # Loop over list of search results
        for result_item in result_list:
          if result_counter<ignoreResultsNumber:
            self.beginResultsDropped = self.beginResultsDropped+1
          elif processResultsCount==0 or result_counter<end_result_counter:
            self._processSingleResult(result_type,result_item)
          else:
            go_ahead = 0 # break-out from while go_ahead
            partial = 1
            break # break-out from this for-loop
          result_counter = result_counter+1
        result_type,result_list = None,None
        self.endResultBreak = result_counter
    finally:
      if self._msgId!=None:
        self._l.abandon(self._msgId)
    self.postProcessing()
    return partial # processResults()

  def _processSingleResult(self,resultType,resultItem):
    """
    Process single entry

    resultType
        result type
    resultItem
        Single item of a result list
    """
    pass


class List(AsyncSearchHandler):
  """
  Class for collecting all search results.
  
  This does not seem to make sense in the first place but think
  of retrieving exactly a certain portion of the available search
  results.
  """

  def __init__(self,l):
    AsyncSearchHandler.__init__(self,l)
    self.allResults = []

  def _processSingleResult(self,resultType,resultItem):
    self.allResults.append((resultType,resultItem))


class FileWriter(AsyncSearchHandler):
  """
  Class for writing a stream of LDAP search results to a file object
  """

  def __init__(self,l,f,headerStr='',footerStr=''):
    """
    Initialize a StreamResultHandler
    
    Parameters:
    l
        LDAPObject instance
    f
        File object instance where the LDIF data is written to
    """
    AsyncSearchHandler.__init__(self,l)
    self._f = f
    self.headerStr = headerStr
    self.footerStr = footerStr

  def preProcessing(self):
    """
    The headerStr is written to output after starting search but
    before receiving and processing results.
    """
    self._f.write(self.headerStr)

  def postProcessing(self):
    """
    The footerStr is written to output after receiving and
    processing results.
    """
    self._f.write(self.footerStr)


class LDIFWriter(FileWriter):
  """
  Class for writing a stream LDAP search results to a LDIF file
  """

  def __init__(self,l,writer_obj,headerStr='',footerStr=''):
    """
    Initialize a StreamResultHandler
    
    Parameters:
    l
        LDAPObject instance
    writer_obj
        Either a file-like object or a ldif.LDIFWriter instance
        used for output
    """
    if isinstance(writer_obj,file):
      import ldif
      self._ldif_writer = ldif.LDIFWriter(writer_obj)
    else:
      self._ldif_writer = writer_obj
    FileWriter.__init__(self,l,self._ldif_writer._output_file,headerStr,footerStr)

  def _processSingleResult(self,resultType,resultItem):
    if _entryResultTypes.has_key(resultType):
      # Search continuations are ignored
      dn,entry = resultItem
      self._ldif_writer.unparse(dn,entry)

