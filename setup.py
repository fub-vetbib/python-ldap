#! /usr/bin/env python
# $Id$

class OpenLDAP2:
	library_dirs =	[ "/usr/local/lib" ]
	include_dirs =	[ "/usr/local/include" ]
	libs =		['ldap', 'lber']
	defines =	[('USE_CIDICT', None),
			 #('WITH_KERBEROS', None),
			 #('HAVE_DES_SETKEY', None),
			 ('LDAP_TYPE_IS_OPAQUE', None),
			 ('HAVE_LDAP_DESTROY_CACHE', None),
			 ('HAVE_LDAP_DISABLE_CACHE', None),
			 ('HAVE_LDAP_ENABLE_CACHE', None),
			 ('HAVE_LDAP_FLUSH_CACHE', None),
			 ('HAVE_LDAP_INIT_TEMPLATES', None),
			 ('HAVE_LDAP_MODRDN2', None),
			 ('HAVE_LDAP_MODRDN2_S', None),
			 ('HAVE_LDAP_SET_CACHE_OPTIONS', None),
			 ('HAVE_LDAP_UNCACHE_ENTRY', None),
			 ('HAVE_LDAP_UNCACHE_REQUEST', None),
			 ('HAVE_DISPTMPL_H', None),
			]

version = '1.10'

from distutils.core import setup, Extension
from ConfigParser import ConfigParser

cfg = ConfigParser()
cfg.read('setup.cfg')
if cfg.has_section('_ldap') and cfg.has_option('_ldap', 'class'):
	LDAP_CLASS = eval(cfg.get('_ldap', 'class', raw=1))
else:
	LDAP_CLASS = OpenLDAP2

setup(
	name =		'Python-LDAP',
	version =	version,
	description =	'API for LDAP C library',
	author =	'David Leonard et al.', 
	author_email =	'python-ldap-dev@lists.sourceforge.net',
	url =		'http://python-ldap.sourceforge.net/',

	ext_modules = [
		Extension(
		    '_ldap',
		    [
			'Modules/CIDict.c',
			'Modules/LDAPObject.c',
			'Modules/common.c',
			'Modules/constants.c',
			'Modules/errors.c',
			'Modules/functions.c',
			'Modules/ldapmodule.c',
			'Modules/linkedlist.c',
			'Modules/message.c',
			'Modules/template.c',
			'Modules/version.c',
		    ],
		    libraries =		LDAP_CLASS.libs,
		    include_dirs =	['Modules'] + LDAP_CLASS.include_dirs,
		    library_dirs =	LDAP_CLASS.library_dirs,
		    runtime_library_dirs = LDAP_CLASS.library_dirs,
		    define_macros =	LDAP_CLASS.defines + [
						('LDAPMODULE_VERSION', version),
					],
		),
	],

	package_dir = { '': 'Lib' },
	py_modules = [
		'ldap',
		'ldif',
		#'perldap',
	],
)

