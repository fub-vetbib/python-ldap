# $Id$
# This is a template file
Summary: Python module for LDAP clients
Name: python-ldap
Version: @version@
Release: @release@
Copyright: public domain
Group: Development/Libraries
Source: ftp://python-ldap.sourceforge.net/pub/python-ldap/python-ldap-@version@-src.tar.gz
BuildRoot: /var/tmp/%{name}-buildroot
URL: http://python-ldap.sourceforge.net/
Packager: python-ldap-dev@lists.sourceforge.net
Requires: python >= 1.5
Prefix: /usr

%description
This Python library provides access to the LDAP (Lightweight Directory Access 
Protocol) RFC1823 C interface.
It includes OpenLDAP 1.2.11

%prep
%setup

%build
rm -rf /tmp/ldap-pfx; mkdir -p ./ldap-pfx; ln -s `pwd`/ldap-pfx /tmp/ldap-pfx
sh Misc/openldap.sh
sh configure
make
make filelist

%install
make install

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist
%defattr(-,root,root)
%doc README

%changelog
