## ldap/parse.py - parsing of LDAP objectClasses and attribute maps 
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


import string, re
from ldap import LDAPError


class FileReader:
    """Attach to an open file and provide iteration functions."""
    def __init__(self, file):
        self.__file = file
        self.line = ''
    def readline(self):
        self.line = self.__file.readline()
        if self.line == '': return 0
        else: return 1
        
        
class LDAPObjectClass:
    """Wrapper around LDAP objectClass definitions.

       Every instance of this class describe a single objectClass antry and
       can be used to validate LDAPEntry objects. Note that the file parameter
       is *not* file name, but an open and ready to read file object.
    """
    def __init__(self, file=None):
        self.name = ''
        self.must = []
        self.may = []
        if file:
            self.load(file, 0)
            if self.name == '':
                raise LDAPError, "not enought data"
        
    def load(self, file, init=1):
        """Scan objectClass definition file and init.

           Return 0 if EOF is encountered while scanning the file for data.
        """
        if not init: self.__init__()
        n = None; d = None
        i = FileReader(file)
        while i.readline():
            ll = len(i.line)
            l = string.strip(i.line[0:-1])
            moc = re.match('object[cC]lass\s+(.+)', l)
            if n == None:
                if moc == None: continue
                else:
                    n = moc.group(1)
                    self.name = n
                    moc = None
            else:
                if moc != None:
                    # rewind the file to let it ready for the next one
                    file.seek(-ll, 1)
                    return 1
                else:
                    if len(l) <= 1: continue
                    elif re.match('requires', l):
                        d = self.must
                    elif re.match('allows', l):
                        d = self.may
                    elif d != None:
                        val = string.replace(l, ',', '')
                        d.append(val)
            if l == '': return 0
            else: return 1

    def save(self, file):
        """Save a human-readable version of the objectClass."""
        file.write('objectClass %s\n' % self.name)
        file.write('    requires\n')
        for i in range(len(self.must)):
            if i != 0: file.write(',\n')
            file.write('        '+self.must[i])
        file.write('\n    allows\n')
        for i in range(len(self.may)):
            if i != 0: file.write(',\n')
            file.write('        '+self.may[i])
        file.write('\n\n')


def load_objectclasses(*file_names):
    """Load all the objectClasses from file_names and return them in array."""
    all = []
    for fn in file_names:
        f = open(fn)
        try:
            oc = LDAPObjectClass(f)
            while oc:
                all.append(oc)
                oc = LDAPObjectClass(f)
        except LDAPError:
            f.close()
    return all


def load_objectclasses_d(*file_names):
    """Load all the objectClasses from file_names and return a dictionary."""
    dict = {}
    for fn in file_names:
        ar = load_objectclasses(fn)
        for i in range(len(ar)):
            dict[ar[i].name] = ar[i]
    return dict


# TODO: implement me!
def sort_attrs_by_oc(attrs, *ocs):
    return attrs


def __load_attributes(file_name):
    f = open(file_name, 'r')
    i = FileReader(f)
    attrs = []
    while i.readline():
        parts = string.split(i.line)
        if parts == None or len(parts) < 2 or parts[0][0] == '#':
            continue
        else:
            if len(parts) > 2: aliases = parts[1:-1]
            else: aliases = []
            attrs.append((parts[0], parts[-1], aliases))
    close(f)
    return attrs

def load_attributes(*file_names):
    """Load all the attributes from file_names and return them in tuples.

       The format of every tuple (attribute) is as follows:
       (attribute_name, attribute_type, attribute_aliases)
    """
    all = []
    for fn in file_names:
        all = all + __load_attributes(fn)
    return all


def canonical_dn(*parts):
    """Return canonical dn from parts."""
    return string.strip(string.replace(string.join(parts, ','), ', ', ','))
