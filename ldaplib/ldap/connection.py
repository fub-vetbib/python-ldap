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
from schema.schema import LDAPSchema, build_v3_server_schema
from search import LDAPSearch


class LDAPConnection:
    """High level wrapper around the _ldap module functions.

       A new instance of this class binds to the LDAP server with the given
       dn and password. The estabilished connection can be used to retrieve
       information from the server by searching or browsing. LDAP objects
       are returned as instances of the LDAPEntry class."""

    def __init__(self, host, port=ldap.PORT,
                 binding_dn='', auth_token='', auth_type=ldap.AUTH_SIMPLE):
        """Open the connection and bind to the directory."""
        self.host = host
        self.port = port
        self.base = ''
        self.use_rdn = 0
        self.timeout = 60
        self.finder = LDAPSearch(self)
        self.__connection = ldap.open(host, port)
        self.__connection.bind_s(binding_dn, auth_token, auth_type)
        
    def __check_base(self, base_dn):
        """Check search base and raise exception if not set.
        """
        if (self.base == None) and base_dn == None:
            raise LDAPError('base not set')
        elif base_dn == None:
            base_dn = self.base
        elif self.use_rdn == 1:
            base_dn = canonical_dn(base_dn, self.base)
	return base_dn

    # some functions used internally by the LDAPEntry object
    def _modify(self, dn, modlist):
        """Modify dn using the given modlist."""
        if modlist and len(modlist) > 0:
            self.__connection.modify_s(self.__check_base(dn), modlist)

    def _add(self, dn, modlist):
        """Add to dn the given list of attributes."""
	if modlist and len(modlist) > 0:
            self.__connection.add_s(self.__check_base(dn), modlist)

    def _delete(self, dn):
        """Delete the given dn."""
        self.__connection.delete_s(self.__check_base(dn))

    def _search(self, filter, base_dn, scope, attrl):
        """Search the directory, return raw results.

        This method is used mainly by the LDAPEntry objects that want
        to initialize themselves from the connection. (Note that all the
        arguments are mandatory: the one who call this function should know
        what he's doing...)
        """
        return self.__connection.search_s(base_dn, scope, filter, attrl, 0,
                                          self.timeout)
        
    def set_base(self, base_dn, use_rdn=0):
        """Set base for future searches."""
        self.base = canonical_dn(base_dn)
        if use_rdn: self.use_rdn = 1        

    def get_schema(self, dn='cn=schema,cn=master', relax=1):
        """Get the schema from a v3 enabled LDAP server."""
        se = self.finder.find(dn)
        self.schema = build_v3_server_schema(se.get('objectclasses'),
                                             se.get('attributetypes'),
                                             se.get('ldapsyntaxes'),
                                             relax)
        return self.schema

            








