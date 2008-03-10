"""
ldap.schema -  LDAPv3 schema handling

See http://python-ldap.sourceforge.net for details.

\$Id$
"""

__version__ = '0.2.1'

from ldap.schema.subentry import SubSchema,SCHEMA_ATTRS,SCHEMA_CLASS_MAPPING,SCHEMA_ATTR_MAPPING,urlfetch
from ldap.schema.models import *
