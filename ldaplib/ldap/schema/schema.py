## ldap/schema/schema.py - schema parsing classes for python-ldap
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
from object import LDAPSchemaError
from objectclass import *
from attributetype import *
from syntax import *


######## parsing functions ####################################################

def _parse_schema_openldap_config(lines, klass):
    """Parse an openldap-style (comments) config file and extract the schema.

    Note that the input should be formatted as a list (tuple) of lines, just
    like file.readlines() does. That is for uniformity with the other parsing
    functions.

    Parsing this kind of configuration file poses some problems, because each
    file is formatted in a slightly different way. This code tries to cope with
    the problem by sopposing that a keyword like `OID' or `NAME' after a blank
    line begins a new block.

    `klass' should be the class to be used to build the objects.
    """
    ## TODO: eheh. write me!


def _parse_v3_server_schema(lines,  klass, relax):
    """Parse a set of lines coming from a v3 enabled LDAP server."""
    objects = [] ; errors = []
    for l in lines:
        try:
            o = klass(l)
            objects.append(o)
        except LDAPSchemaError, err:
            if not relax:
                raise LDAPSchemaError(err)
            errors.append(str(err))
    return (objects, errors)


######## the schema class #####################################################

class LDAPSchema:
    """The whole schema."""

    """Some flags."""
    STATUS_CLOSED = 1
    STATUS_RELAXED = 2

    def __init__(self):
        """Initialize the schema."""
        self.flags = 0 
        self.objectclasses = {}
        self.oc_names = {}
        self.attributetypes = {}
        self.at_names = {}
        self.syntaxes = {}
        
    def add_object(self, o, oid_dict, name_dict=None, relax=0):
        """Add an object to this schema."""
        if not o.oid:
            if not relax:
                raise LDAPSchemaError('missing oid')
            else:
                self.flags = STATUS_RELAXED
        else:
            oid_dict[o.oid] = o

        if name_dict:
            if not o.name:
                if not relax:
                    raise LDAPSchemaError('missing name')
                else:
                    self.flags = STATUS_RELAXED
            else:
                name_dict[o.name] = o            
        
    def add_objectclass(self, oc, relax=0):
        """Add an objectClass definition to the schema."""
        self.add_object(oc, self.objectclasses, self.oc_names, relax)

    def add_attributetype(self, at, relax=0):
        """Add an attributeType definition to the schema."""
        self.add_object(at, self.attributetypes, self.at_names, relax)

    def add_syntax(self, syn, relax=0):
        """Add a syntax definition to the schema."""
        self.add_object(syn, self.syntaxes, None, relax)
        
    def validate(self):
        """Validates the entire schema by cross-checking oids."""
        ## TODO: fixme
        pass


######## schema building functions ############################################
    
def build_v3_server_schema(classes, attrs, syntaxes, relax=1):
    """Build a full schema from a set of attributes."""

    schema = LDAPSchema()

    oc = _parse_v3_server_schema(classes, LDAPSchemaObjectClass, relax)
    at = _parse_v3_server_schema(attrs, LDAPSchemaAttributeType, relax)
    syn = _parse_v3_server_schema(syntaxes, LDAPSchemaSyntax, relax)

    for o in oc[0]:
        schema.add_objectclass(o, relax)
    for o in at[0]:
        schema.add_objectclass(o, relax)
    for o in syn[0]:
        schema.add_objectclass(o, relax)

    schema.errors = oc[1]+at[1]+syn[1]
    return schema
