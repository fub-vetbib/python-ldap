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

import ldap, re
from string import lower
from ldap import LDAPError, canonical_dn
from types import *


class LDAPEntry:
    """Wrapper around LDAP objects."""

    STATUS_REAL = 1
    STATUS_NEW = 2
    STATUS_GHOST = 4
    STATUS_ZOMBIE = 8
    STATUS_MODIFIED = 256
    
    def __init__(self, dn, connection=None, attrs=None, internal=None):
        """Initialize the entry.

           If the connection argument is given, the object tries to initialize
           itself by looking for the given dn via the connection. If it exists,
           its status is set to REAL else to NEW. attrs is used to filter the
           attributes.

           If the connection is None, the entry status is set to GHOST and the
           entry is initialized using the optional attrs dictionary.
        """
        self.dn = dn
        self.rdn = dn
        self.classes = []
        self.ancestor = None
        self.childrens= {}
        self.data = {}
        self.attrl = None
        self.connection = connection
        self.schema = None
        
        if connection:
            LDAPEntry.reload(self, dn, attrs)
        elif attrs:
            if internal:
                self.status = LDAPEntry.STATUS_REAL
                self.connection = internal
            else:
                self.status = LDAPEntry.STATUS_GHOST
            for k in attrs.keys():
                LDAPEntry.__setitem__(self, k, attrs[k], 0)

    # some methods used to make the class work as a dictionary, with multiple
    # entries for every key (some high level functions for single-value
    # addition and deletion are provided below)
    
    def __setitem__(self, key, value, changed=1):
        key = lower(key)
        if key == 'dn':
            self.dn = dn
            if self.ancestor != None:
                self.set_ancestor(self.ancestor)
        else:
            if type(value) != ListType: value = [value]
            if key == 'objectclass': self.classes = value
            else: self.data[key] = (value, changed)
        self.status = self.status | LDAPEntry.STATUS_MODIFIED
            
    def __getitem__(self, key):
        key = lower(key)
        if key == 'dn': return self.dn
        elif key == 'objectclass': return self.classes
        elif self.data[key][1] != 2: return self.data[key][0]
        
    def __delitem__(self, key):
        key = lower(key)
        if key == 'dn': raise LDAPError('cannot delete dn')
        elif key == 'objectclass': self.classes = []
        else: self.data[key] = (self.data[key][0], 2)
        self.status = self.status | LDAPEntry.STATUS_MODIFIED
        
    def __purge__(self):
        for k in self.data.keys():
            if self.data[k][1] == 2: del self.data[k]
        self.status = self.status | LDAPEntry.STATUS_MODIFIED
            
    def __len__(self):
        return len(self.data)+2
    
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

    # basic operations on *single* attribute values (note that get *never*
    # return a single value, it always return a list!)
    def get(self, key, default=[]):
        if self.data.has_key(key) and self.data[key][1] < 2:
            return self.data[key][0]
        else:
            return default
    
    def set(self, key, *values):
        if self.data.has_key(key) and self.data[key][1] < 2:
            self.data[key] = (self.data[key][0]+values, 1)
        else:
            self.data[key] = (values, 1)
        self.status = self.status | LDAPEntry.STATUS_MODIFIED

    def replace(self, key, oldvalue, newvalue):
        i = self.data[key][0].index(oldvalue)
        self.data[key][0][i:i+1] = [newvalue]
        self.data[key] = (self.data[key][0], 1)
        self.status = self.status | LDAPEntry.STATUS_MODIFIED

    def delete(self, key, *values):
        for v in values:
            self.data[key][0].remove(v)
        self.data[key] = (self.data[key][0], 1)
        self.status = self.status | LDAPEntry.STATUS_MODIFIED
            
    def __str__(self):
        """Return the ldif rapresentation of this object."""
        str = "dn: %s\n" % self.dn
        classes = self.classes
        for oc in classes:
            str = str + "objectClass: %s\n" % oc
        for k in self.data.keys():
            if re.match('object[cC]lass', k): continue
            for a in self.data[k][0]:
                str = str + "%s: %s\n" % (k, a)
        return str
    
    def __check_connection(self):
        """Raise an exception if the connection to the directory is missing."""
        if self.connection == None:
            raise LDAPError('missing connection')

    def set_connection(self, connection):
        """Set the connection this object should use for directory access."""
        self.connection = connection
        self.reload(self.dn, self.attrl)
        
    def set_ancestor(self, ancestor):
        """Set the ancestor and calculate rdn."""
        self.ancestor = ancestor
        parts = ldap.explode_dn(self.dn)
        aparts = ldap.explode_dn(ancestor.dn)
        rdnparts = []
        for p in parts:
            if len(aparts) > 0 and p == aparts[0]: del aparts[0]
            else: rdnparts.append(p)
        self.rdn = apply(canonical_dn, rdnparts)

    def reload(self, dn, attrl=None):
        """Initialize itself from given dn.

        If the given dn is not available on the current connection,
        this entry is marked as NEW.
        """
        self.__check_connection()
        self.attrl = attrl
        try:
	    data = self.connection._search('objectclass=*',
                                           dn, ldap.SCOPE_BASE, attrl)
            data = data[0][1]
            for k in data.keys():
                LDAPEntry.__setitem__(self, k, data[k], 0)
            self.status = LDAPEntry.STATUS_REAL
	except ldap.NO_SUCH_OBJECT:
	    self.status = LDAPEntry.STATUS_NEW
	    
    def browse(self, filter=None, attrl=None):
        """Retrieve childrens from the database.

           The directory level under the current object is browse and filtered
           by filter. Every object found is then added to the childrens hash
           using its rdn as the key. childrens is the returned for commodity.
        """
        self.__check_connection()
        childs = self.connection.finder.browse(filter, self.dn, attrl)
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
        """Commit changes to the LDAP directory.

           First a query is done to obtain the attribute names, then do
           an ADD for every new attribute and a MODIFY for every modified
           one. Attributes not found in this object are deleted!
        """
	mod = []

        if self.status & LDAPEntry.STATUS_GHOST:
            raise LDAPError('cannot commit a ghost entry')

        elif self.status & LDAPEntry.STATUS_REAL:
            if self.status & LDAPEntry.STATUS_MODIFIED:
                old = self.connection.finder.find(self.dn)
                for k in self.keys():
                    if old.has_key(k):
                        if self.data[k][1] == 2:
                            # delete attribute from server
                            mod.append((ldap.MOD_DELETE, k, None))
                        elif self.data[k][1] == 1:
                            # modify existing attribute
                            mod.append((ldap.MOD_REPLACE, k, self.data[k][0]))
                        else:
                            if self.data[k][1] == 1:
                                mod.append((ldap.MOD_ADD, k, self.data[k][0]))
                self.connection._modify(self.dn, mod)
                self.__purge__()
                self.status = LDAPEntry.STATUS_REAL

        elif self.status & LDAPEntry.STATUS_NEW:
            for k in self.keys():
                mod.append((k, self.data[k][0]))
            self.connection._add(self.dn, mod)
            self.status = LDAPEntry.STATUS_REAL

        elif self.status & LDAPEntry.STATUS_ZOMBIE:
            self.connection._delete(self.dn)
            self.status = LDAPEntry.STATUS_NEW

    def die(self):
        """Remove this entry from the directory on next commit()."""
        self.status = LDAPEntry.STATUS_ZOMBIE





