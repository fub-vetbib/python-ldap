## ldap/connection.py - python bindings to LDAP
## Copyright (C) 2000  Federico Di Gregorio <fog@debian.org>
## Copyright (C) 2000  MIXAD LIVE [http://www.mixadlive.com]
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2 of the License, or
##   (at your option) any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public License
##   along with this program; if not, write to the Free Software
##   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
## -*- Mode: python -*-

import string, ldap, entry
from ldap import LDAPError, canonical_dn

class LDAPSearch:
    """High level wrapper around the _ldap search functions.

    An LDAPSearch object represents a single search and the results. It can
    also be used to walk the tree rooted ad the base dn used for the search.
    """
    def __init__(self, connection=None):
        """Open the connection and bind to the directory."""
        self.connection = connection
        if connection:
            self.base = connection.base
        else:
            self.base = ''
        self.use_rdn = 0
        self.results = []
        self.filter = 'objectclass=*'
        self.attrl = None
        
    def __check_base(self, base_dn):
        """Check search base and raise exception if not set."""
        if (self.base == None) and base_dn == None:
            raise LDAPError('base not set')
        elif base_dn == None:
            base_dn = self.base
        elif self.use_rdn == 1:
            base_dn = canonical_dn(base_dn, self.base)
	return base_dn

    def __check_connection(self):
        """Check if connection exists."""
        if not self.connection:
            raise LDAPError('missing connection')

    def _search(self, filter=None, base_dn=None,
                scope=ldap.SCOPE_SUBTREE, attrl=None):
        """Search the directory, return raw results."""
        base_dn = self.__check_base(base_dn)
        if filter == None: filter = self.filter
        if attrl == None: attrl = self.attrl
        return self.connection._search(filter, base_dn, scope, attrl)
        
    def set_base(self, base_dn, use_rdn=0):
        """Set base for future searches."""
        self.base = canonical_dn(base_dn)
        if use_rdn: self.use_rdn = 1        

    def search(self, filter=None, base_dn=None,
               scope=ldap.SCOPE_SUBTREE, attrl=None):
        """Search the directory, return an array of LDAPEntry instances."""
        try:
            data = self._search(filter, base_dn, scope, attrl)
        except ldap.NO_SUCH_OBJECT:
            data = None
        array = []
        if data == None: return array 
        for edata in data:
            e = entry.LDAPEntry(edata[0], None, edata[1], self.connection)
            array.append(e)
        self.results = array
        return array

    def find(self, base_dn=None, attrl=None):
        """Search for base_dn, return None if not found."""
        try:
            root = self.search('objectclass=*', base_dn,
                               ldap.SCOPE_BASE, attrl)
            self.results = root
            return root[0]
        except:
            self.results = []
            return None
                
    def root(self, base_dn=None, attrl=None):
        """Return the root object using base_dn as the base for the search."""
        root = self.find(base_dn, attrl)
        if not root:
            raise LDAPError('dn does not exists')
        else:
            return root
        
    def browse(self, filter=None, base_dn=None, attrl=None):
        """Return the objects one level under base_dn, sorted by filter."""
        return self.search(filter, base_dn, ldap.SCOPE_ONELEVEL, attrl)
