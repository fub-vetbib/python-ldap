## schema_test.py - test the schema support
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

import sys, ldap, ldap.connection
from ldap import LDAPError

if len(sys.argv) < 3:
    print "usage: %s host schema_dn" % sys.argv[0]
    sys.exit()

if len(sys.argv) == 5:
    user = sys.argv[3]
    passwd = sys.argv[4]
else:
    user = ''
    passwd = ''
    
# create a connection to the ldap directory
c = ldap.connection.LDAPConnection(sys.argv[1],
                                   binding_dn=user, auth_token=passwd)

# retrieve the schema and prints it
if sys.argv[2] != '*':
    s = c.get_schema(sys.argv[2])
else:
    s = c.get_schema()

# print some information about the schema
print "====> Errors"
for e in s.errors:
    print "      %s" % e
    






