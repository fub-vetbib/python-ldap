## ldap/schema/misc.py - schema parsing classes for python-ldap
##
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

from TextTools import *


######## parsing stuff from TextTools #########################################

_name_set = set(alpha+'-_'+number)
_quote_set = set(alpha+number+'-_ ;')
_list_set = set(alpha+'-_;'+number)
_oid_set = set('.'+number)
_white_set = set(' \n\r\t')


_whiteskip_tag = (None, AllInSet, set(' \n\r\t'), +1)

_quote_tags = (
    ('quote_chunk', AllInSet, _quote_set),
    (None, Is, "'"))

_list_tags = (
    _whiteskip_tag,
    ('list_chunk', AllInSet, _list_set),
    _whiteskip_tag,
    (None, Is, '$', +1, -3),
    (None, Is, ')'))


def _list_extract(str, tag):
    """Extract a list of text chunks from a string, using the given tag."""
    l = []
    for c in tag[3]:
        l.append(str[c[1]:c[2]])
    return tuple(l)


######## schema exception #####################################################

class LDAPSchemaError(StandardError):
    """Default error for schema exceptions."""
    pass


######## basic class ##########################################################

class LDAPSchemaObject:
    """Generic schema object."""

    """Dummy flags, attributes and lists."""
    ALLOWED_FLAGS = []
    ALLOWED_ATTRS = []
    ALLOWED_LISTS = []
    ALLOWED_QUOTES = []
    
    def parse(self, str):
        """Parse a string into class attributes."""
        tags = tag(str, self.__class__.PARSE_TAGS)[1]
            
         # check for parse errors
        if len(tags) < 2 or tags[0][0] != 'start' or tags[-1][0] != 'end':
            raise LDAPSchemaError('parse error: %s' % str)

        # cache class-level parsing stuff
        attrs = self.__class__.ALLOWED_ATTRS
        flags = self.__class__.ALLOWED_FLAGS
        lists = self.__class__.ALLOWED_LISTS
        quotes = self.__class__.ALLOWED_QUOTES
        self.flags = []
        
        # loop on all the tags (order does not matter) 
        for t in tags[1:-1]:
            id = t[0]
            if id in flags:
                self.flags.append(id)
            elif id in attrs:
                setattr(self, id, str[t[1]:t[2]])
            elif id in quotes:
                setattr(self, id, str[t[3][0][1]:t[3][0][2]])
            elif id in lists:
                setattr(self, id, _list_extract(str, t))
            else:
                raise LDAPSchemaError('parse error: %s' % id)

        # makes lists read-only
        self.flags = tuple(self.flags)
        
    def validate(self, schema=None):
        """Validate an object against `schema'.

        By default an object is *not* valid (subclasses should implement a real
        validate method.)
        """
        return 0
    
