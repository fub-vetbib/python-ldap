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
from ldap import LDAPError


class LDAPConnection:
    """High level wrapper around the _ldapmodule functions.

       A new instance of this class binds to the LDAP server with the given
       dn and password. The estabilished connection can be used to retrieve
       information from the server by searching or browsing. LDAP objects
       are returned as instances of the LDAPEntry class."""

    def __init__(self, host, port=ldap.PORT,
                 binding_dn='', auth_token='', auth_type=ldap.AUTH_SIMPLE):
        """Open the connection and bind to the directory."""
        self.host = host
        self.port = port
        self.base = binding_dn
        self.use_rdn = 0
        self.timeout = 60
        self.filter = 'cn=*'
        self.attrl = None
        self.__connection = ldap.open(host, port)
        self.__connection.bind_s(binding_dn, auth_token, auth_type)

    def __check_base(self, base_dn):
        """Check search base and raise exception if not set.
        """
        if (self.base == None or self.base == '') and base_dn == None:
            raise LDAPError, ({'desc':'base not set'})
        elif base_dn == None:
            base_dn = self.base
        elif self.use_rdn == 1:
            base_dn = string.join([base_dn, self.base], ',')
        return string.replace(base_dn, ' ', '')
    
    def search_s(self, base_dn=None, filter=None,
                 scope=ldap.SCOPE_SUBTREE, attrl=None):
        """Search the directory, return an array of LDAPEntry instances."""
        base_dn = self.__check_base(base_dn)
        if filter == None: filter = self.filter
        if attrl == None: attrl = self.attrl
        data = self.__connection.search_s(base_dn, scope, filter, attrl, 0,
                                          self.timeout)
        array = []
        if data == None: return array 
        for edata in data:
            e = entry.LDAPEntry(edata[0], edata[1])
            e.set_connection(self)
            array.append(e)
        return array

    def find_s(self, base_dn=None, attrl=None):
        """Search for base_dn, return None if not found."""
        try:
            root = self.search_s(base_dn, 'objectclass=*',
                                 ldap.SCOPE_BASE, attrl)   
        except LDAPError:
            root = []
        if len(root) == 1: return root[0]
        else: return None
        
    def root_s(self, base_dn=None, attrl=None):
        """Return the root object using base_dn as the base for the search."""
        root = self.search_s(base_dn, 'objectclass=*', ldap.SCOPE_BASE, attrl)
        if len(root) == 0:
            raise LDAPError, ({'desc':'dn does not exists'},)
        elif len(root) > 1:
            raise LDAPError, ({'desc':'more than one root objects found'},)
        return root[0]

    def browse_s(self, base_dn=None, filter=None, attrl=None):
        """Return the objects one level under base_dn, sorted by filter."""
        return self.search_s(base_dn, filter, ldap.SCOPE_ONELEVEL, attrl)
        
    def modify_s(self, dn, modlist):
        """Modify dn using the given modlist."""
        self.__connection.modify_s(self.__check_base(dn), modlist)

    def add_s(self, dn, modlist):
        """Add to dn the given list of attributes."""
        self.__connection.add_s(self.__check_base(dn), modlist)

    def delete_s(self, dn):
        """Delete the given dn."""
        self.__connection.delete_s(self.__check_base(dn))

    def rebind(binding_dn='', auth_token='', auth_type=ldap.AUTH_SIMPLE):
        """Rebind to the directory changing authorization info."""
        self.__connection.unbind_s()
        self.__connection.bind_s(binding_dn, auth_token, auth_type)
