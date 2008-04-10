.. % $Id: ldap-dn.tex,v 1.8 2008/03/26 12:10:12 stroeder Exp 

Building and installing
=========================

Prerequisites
-------------

The following software packages are required to be installed
on the local system when building python-ldap:

- Python including its development files: http://www.python.org/
- OpenLDAP client libs: http://www.openldap.org/
- OpenSSL (optional): http://www.openssl.org/
- cyrus-sasl (optional): http://asg.web.cmu.edu/sasl/sasl-library.html
- Kerberos libs, MIT or heimdal (optional)

Definitions in setup.cfg
------------------------

The file setup.cfg allows to set some build and installation
parameters for reflecting the local installation of required
software packages.

