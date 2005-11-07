"""
ldap.resiter - processing LDAP results with iterators
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$

Python compability note:
Requires Python 2.3+
"""

import ldap

__version__ = '0.0.1'


class ResultProcessor:
  """
  Mix-in class for ldap.ldapopbject.LDAPObject which adds method allresults().
  """

  def allresults(self,msgid,timeout=-1):
    """
    Generator function which returns an iterator for processing all LDAP operation
    results of the given msgid.
    """
    result_type,result_list,result_msgid,result_serverctrls = self.result3(msgid,0,timeout)
    while result_type and result_list:
      # Loop over list of search results
      for result_item in result_list:
        yield (result_type,result_list,result_msgid,result_serverctrls)
      result_type,result_list,result_msgid,result_serverctrls = self.result3(msgid,0,timeout)
    return # allresults()
