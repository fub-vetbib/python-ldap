## ldap/entry.py - python bindings to LDAP
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

import string, re, ldap
from ldap import LDAPError


class LDAPEntry:
    """Wrapper around LDAP objects."""

    def __init__(self, dn, attrs={}):
        """Initialize from a dictionary of attributes."""
        self.dn = dn
        self.rdn = dn
        self.childrens= {}
        self.ancestor = None
        self.data = {}
        self._connection = None
        self.__list_type_cache = type([])
        for k in attrs.keys():
            LDAPEntry.__setitem__(self, k, attrs[k], 0)

    # some methods used to make the class work as a dictionary
    def __setitem__(self, key, value, changed=1):
        if key == 'dn':
            self.dn = dn
            if self.ancestor != None: self.set_ancestor(self.ancestor)
        else:
            if type(value) != self.__list_type_cache: value = [value]
            self.data[key] = (value, changed)
    def __getitem__(self, key):
        if key == 'dn': return self.dn
        elif self.data[key][1] != 2: return self.data[key][0]
    def __delitem__(self, key):
        if key == 'dn': raise LDAPError, ({'desc':'cannot delete dn'})
        else: self.data[key] = (self.data[key][0], 2)
    def __purge__(self):
        for k in self.data.keys():
            if self.data[k][1] == 2: del self.data[k]
    def __len__(self):
        return len(self.data)+1
    def keys(self):
        return self.data.keys()
    def has_key(self, key):
        return self.data.has_key(key)
    def values(self):
        l = []
        for k in self.data.keys():
            l.append(self.data[k][0])
        return l
    def items(self):
        l = []
        for k in self.data.keys():
            l.append((k, self.data[k][0]))
        return l

    # basic operations on *single* attribute values
    def get(self, key, default=None):
        return self.data.get(key, (default,))[0]
    def set(self, key, value):
        if self.data.has_key(key) and self.data[key][1] < 2:
            self.data[key] = (self.data[key][0]+[value], 1)
        else:
            self.data[key] = ([value], 1)
    def replace(self, key, oldvalue, newvalue):
        i = self.data[key][0].index(oldvalue)
        self.data[key][0][i:i+1] = [newvalue]
        self.data[key] = (self.data[key][0], 1)
    def delete(self, key, value):
        self.data[key][0].remove(value)
        self.data[key] = (self.data[key][0], 1)
            
    def __str__(self):
        """Return the ldif rapresentation of this object."""
        str = "dn: %s\n" % self.dn
        classes = self.get('objectClass', []) + self.get('objectclass', []) 
        for oc in classes:
            str = str + "objectClass: %s\n" % oc
        for k in self.data.keys():
            if re.match('object[cC]lass', k): continue
            for a in self.data[k][0]:
                str = str + "%s: %s\n" % (k, a)
        return str
    
    def __check_connection(self):
        """Raise an exception if the connection to the directory is missing."""
        if self._connection == None:
            raise LDAPError, ({'desc':'missing connection'})

    def set_connection(self, connection):
        """Set the connection this object should use for directory access."""
        self._connection = connection
        
    def set_ancestor(self, ancestor):
        """Set the ancestor and calculate rdn."""
        self.ancestor = ancestor
        parts = ldap.explode_dn(self.dn)
        aparts = ldap.explode_dn(ancestor.dn)
        rdnparts = []
        for p in parts:
            if len(aparts) > 0 and p == aparts[0]: del aparts[0]
            else: rdnparts.append(p)
        self.rdn = string.join(rdnparts, ldap.DNS)

    def init(self, dn, attrl=None):
        """Initialize itself from given dn."""
        self.__check_connection()
        c = self._connection
        new = c.search_s(self.dn, '(!(dn=*))', ldap.SCOPE_BASE, attrl)
        if len(new) == 0:
            raise LDAPError, ({'desc':'can not find dn'})
        items = {}
        for item in new[0].items():
            items[item[0]] = item[1]
        LDAPEntry.__init__(self, dn, items)
        self.set_connection(c)
        
    def browse(self, filter=None, attrl=None):
        """Retrieve childrens from the database.

           The directory level under the current object is browse and filtered
           by filter. Every object found is then added to the childrens hash
           using its rdn as the key. childrens is the returned for commodity.
        """
        self.__check_connection()
        childs = self._connection.browse_s(self.dn, filter, attrl)
        self.childrens = {}
        for child in childs:
            child.set_ancestor(self)
            self.childrens[child.rdn] = child
        return self.childrens

    def recurse_pre(self, func, *args):
        """Apply func() recursively to the whole children tree."""
        for ck in self.childrens.keys():
            apply(LDAPEntry.recurse_pre, (self.childrens[ck], func) + args)
        apply(func, (self,) + args)

    def recurse_post(self, func, *args):
        """Apply func() recursively to the whole children tree."""
        apply(func, (self,) + args)
        for ck in self.childrens.keys():
            apply(LDAPEntry.recurse_post, (self.childrens[ck], func) + args)

    def commit(self, new_dn=None, force=0):
        """Commit (save) the entry to the LDAP directory.

           First a query is done to obtain the attribute names, then do
           an ADD for every new attribute and a MODIFY for every modified
           one. Attributes not found in this object are deleted!
        """
        old = self._connection.find_s(self.dn)
            
        # now that we have the attributes, build the modify array
        mod = []
        if old == None:
            for k in self.keys():
                mod.append((k, self.data[k][0]))
            self._connection.add_s(self.dn, mod)
        else:
            for k in self.keys():
                if old.has_key(k):
                    if self.data[k][1] == 2:    # delete attribute from server
                        mod.append((ldap.MOD_DELETE, k, None))
                    elif self.data[k][1] == 1:  # modify existing attribute
                        mod.append((ldap.MOD_REPLACE, k, self.data[k][0]))
                    else:
                        if self.data[k][1] == 1:
                            mod.append((ldap.MOD_ADD, k, self.data[k][0]))
            self._connection.modify_s(self.dn, mod)
        self.__purge__()








