## ldap/schema/attributetype.py - schema parsing classes for python-ldap
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
from object import _name_set, _quote_set, _oid_set, _white_set
from object import _whiteskip_tag, _quote_tags, _list_tags
from object import LDAPSchemaObject, LDAPSchemaError


######## the high-level classes ###############################################

class LDAPSchemaAttributeType(LDAPSchemaObject):
    """Encapsulates a single objectClass entry in the LDAP schema."""

    """Allowed flags, attributes and lists."""
    ALLOWED_FLAGS = ['single-value', 'no-user-modification']
    ALLOWED_ATTRS = ['oid', 'syntax', 'equality', 'usage']
    ALLOWED_QUOTES = ['name', 'desc']
    ALLOWED_LISTS = []
    
    """Tags used in parsing single entries."""
    PARSE_TAGS = (

        # this part is mandatory in an objectclasses attribute
        ('start', Is, '('),
        _whiteskip_tag,
        ('oid', AllInSet, _oid_set),
        _whiteskip_tag,
        (None, Word, 'NAME'),
        _whiteskip_tag,
        (None, Is, '\''),
        ('name', Table, _quote_tags),

        # here begins the real parsing (first some flags)
        _whiteskip_tag,
        ('single-value', Word, 'SINGLE-VALUE', +2),
        (None, Jump, To, -2),
        ('no-user-modification', Word, 'NO-USER-MODIFICATION', +2),
        (None, Jump, To, -4),

        # then the SYNTAX, USAGE and EQUALITY keywords and argument
        (None, Word, 'SYNTAX', +4),
        _whiteskip_tag,
        ('syntax', AllInSet, _oid_set),
        (None, Jump, To, -8),

        (None, Word, 'USAGE', +4),
        _whiteskip_tag,
        ('usage', AllInSet, _name_set),
        (None, Jump, To, -12),

        (None, Word, 'EQUALITY', +4),
        _whiteskip_tag,
        ('equality', AllInSet, _name_set),
        (None, Jump, To, -16),

        (None, Word, 'DESC', +5),
        _whiteskip_tag,
        (None, Is, '\''),
        ('desc', Table, _quote_tags),
        (None, Jump, To, -21),

        _whiteskip_tag,
        ('end', Is, ')'))
    
    def __init__(self, str=None):
        """Initialize the entry.

        First all the mandatory fields are initialized to empty values, then
        the parse() method is called on the initialization string, if present.
        """
        self.flags = ()
        self.oid = ''
        self.syntax = ''
        self.name = ''
        self.desc = None
        self.usage = None
        self.equality= None
        if str:
            self.parse(str)

    def validate(self, schema=None):
        """Validate this object against `schema'.

        If `schema' is not given, simply check the object for
        mandatory attributes.
        """
        if not self.oid or not self.name or not self.syntax:
            return 0
        if schema:
            return schema.check_oids((self.syntax,))
        
