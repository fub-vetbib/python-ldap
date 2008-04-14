.. % $Id: ldap-dn.tex,v 1.8 2008/03/26 12:10:12 stroeder Exp 

Building and installing
=========================

Prerequisites
-------------

The following software packages are required to be installed
on the local system when building python-ldap:

- Python including its development files: http://www.python.org/
- OpenLDAP client libs version 2.3 or later: http://www.openldap.org/
- OpenSSL (optional): http://www.openssl.org/
- cyrus-sasl (optional): http://asg.web.cmu.edu/sasl/sasl-library.html
- Kerberos libs, MIT or heimdal (optional)

Section [_ldap] of setup.cfg
----------------------------

The file setup.cfg allows to set some build and installation
parameters for reflecting the local installation of required
software packages:

.. data:: library_dirs

   Specifies in which directories to search for required libraries.

.. data:: include_dirs

   Specifies in which directories to search for include files of required libraries.

.. data:: libs

   A space-separated list of library names to link to.

.. data:: extra_compile_args

   Compiler options.

.. data:: extra_objects

