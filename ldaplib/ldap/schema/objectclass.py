## ldap/schema/objectclass.py - schema parsing classes for python-ldap
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

class LDAPSchemaObjectClass(LDAPSchemaObject):
    """Encapsulates a single objectClass entry in the LDAP schema."""

    """Allowed flags, attributes and lists."""
    ALLOWED_FLAGS = ['abstract', 'auxiliary']
    ALLOWED_ATTRS = ['oid', 'sup']
    ALLOWED_QUOTES = ['name', 'desc']
    ALLOWED_LISTS = ['may', 'must']
    
    """Tags used in parsing single entries."""
    PARSE_TAGS = (

        ('start', Is, '('),
        
        # oid and name
        _whiteskip_tag,
        ('oid', AllInSet, _oid_set),
        _whiteskip_tag,
        (None, Word, 'NAME'),
        _whiteskip_tag,
        (None, Is, '\''),
        ('name', Table, _quote_tags),

        # flags
        _whiteskip_tag,
        ('abstract', Word, 'ABSTRACT', +2),
        (None, Jump, To, -2),
        ('auxiliary', Word, 'AUXILIARY', +2),
        (None, Jump, To, -4),

        # then the SUP keyword and argument
        (None, Word, 'SUP', +4),
        _whiteskip_tag,
        ('sup', AllInSet, _name_set),
        (None, Jump, To, -8),

        # the MUST and MAY keywords and the list argument
        (None, Word, 'MUST', +5),
        _whiteskip_tag,
        (None, Is, '('),
        ('must', Table, _list_tags),
        (None, Jump, To, -13),

        (None, Word, 'MAY', +5),
        _whiteskip_tag,
        (None, Is, '('),
        ('may', Table, _list_tags),
        (None, Jump, To, -18),

        (None, Word, 'DESC', +5),
        _whiteskip_tag,
        (None, Is, '\''),
        ('desc', Table, _quote_tags),
        (None, Jump, To, -23),

        _whiteskip_tag,
        ('end', Is, ')'))
    
    def __init__(self, str=None):
        """Initialize the entry.

        First all the mandatory fields are initialized to empty values, then
        the parse() method is called on the initialization string, if present.
        """
        self.flags = ()
        self.oid = ''
        self.name = ''
        self.desc = None
        self.sup = None
        self.may = ()
        self.must = ()
        if str:
            self.parse(str)

    def validate(self, schema=None):
        """Validate an object against `schema'.

        If `schema' is not given, simply check the object for
        mandatory attributes.
        """
        if not self.oid or not self.name:
            return 0
        if schema:
            return schema.check_oids(self.may+self.must)
        
