#! /usr/bin/env python
"""
setup.py - Setup package with the help Python's DistUtils

See http://python-ldap.sourceforge.net for details.

$Id$
"""

from distutils.core import setup, Extension
from ConfigParser import ConfigParser
import sys,string,time

#-- Release version of Python-ldap
version = '2.0.0pre09' # -%s' % (time.strftime('%Y%m%d',time.gmtime(time.time())))

#-- A class describing the features and requirements of OpenLDAP 2.0
class OpenLDAP2:
	library_dirs =	[]
	include_dirs =	[]
        extra_compile_args = []
        extra_objects = []

	libs =		['ldap', 'lber']
	defines =	[ ]

LDAP_CLASS = OpenLDAP2

#-- Read the [_ldap] section of setup.cfg
cfg = ConfigParser()
cfg.read('setup.cfg')
if cfg.has_section('_ldap'):
    for name in LDAP_CLASS.__dict__.keys():
	if cfg.has_option('_ldap', name):
	    setattr(LDAP_CLASS, name, string.split(cfg.get('_ldap', name)))

#-- Let distutils do the rest
setup(
	#-- Package description
	name =		'python-ldap',
	version =	version,
	description =	'Various LDAP-related Python modules',
	author =	'David Leonard et al.', 
	author_email =	'python-ldap-dev@lists.sourceforge.net',
	url =		'http://python-ldap.sourceforge.net/',
	#-- C extension modules
	ext_modules = [
		Extension(
		    '_ldap',
		    [
			'Modules/LDAPObject.c',
			'Modules/common.c',
			'Modules/constants.c',
			'Modules/errors.c',
			'Modules/functions.c',
			'Modules/schema.c',
			'Modules/ldapmodule.c',
			'Modules/linkedlist.c',
			'Modules/message.c',
			'Modules/version.c',
			'Modules/options.c',
		    ],
		    libraries =	LDAP_CLASS.libs,
		    include_dirs = ['Modules'] + LDAP_CLASS.include_dirs,
		    library_dirs = LDAP_CLASS.library_dirs,
                    extra_compile_args = LDAP_CLASS.extra_compile_args,
                    extra_objects = LDAP_CLASS.extra_objects,
		    runtime_library_dirs = LDAP_CLASS.library_dirs,                    
		    define_macros =	LDAP_CLASS.defines + \
              ('ldap_r' in LDAP_CLASS.libs)*[('HAVE_LIBLDAP_R',None)] + \
              ('sasl' in LDAP_CLASS.libs or 'sasl2' in LDAP_CLASS.libs)*[('HAVE_SASL',None)] + \
              ('ssl' in LDAP_CLASS.libs and 'crypto' in LDAP_CLASS.libs)*[('HAVE_TLS',None)] + \
              [('LDAPMODULE_VERSION', version)]
		),
	],
	#-- Python modules
	py_modules = [
                'ldap',
                'ldap.async',
                'ldap.cidict',
                'ldap.functions',
		'ldap.sasl',
		'ldap.schema',
		'ldap.schema.tokenizer',
		'ldap.schema.models',
		'ldap.schema.subentry',
                'ldap.ldapobject',
                'ldap.modlist',
                'ldapurl',
		'ldif',
	],
	#-- where to find the python modules
	package_dir = { '': 'Lib' },
)

