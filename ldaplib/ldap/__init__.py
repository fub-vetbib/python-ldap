## ldap/__init__.py - python bindings to LDAP
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

import string
from _ldap import *

__all__ = ['connection', 'entry', 'widgets', 'parse', 'utils', 'session']

#### some short and usefull functions
def canonical_dn(*parts):
    """Return canonical dn from parts."""
    s = string.join(filter(None, parts), ',')
    s = string.replace(s, ' ', '')
    s = string.replace(s, ',,', ',')
    return s


    
