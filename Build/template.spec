# $Id$
# This is a template file
Summary: Python module for LDAP clients
Name: python-ldap
Version: @version@
Release: @release@
Copyright: public domain
Group: Development/Libraries
Source: ftp://python-ldap.sourceforge.net/pub/python-ldap/python-ldap-@version@-src.tar.gz
URL: http://python-ldap.sourceforge.net/
Packager: python-ldap-dev@lists.sourceforge.net
Requires: python >= 1.5
Prefix: %{_usr}
BuildRoot: /var/tmp/%{name}-buildroot

%description
This Python library provides access to the LDAP (Lightweight Directory Access 
Protocol) RFC1823 C interface.
It includes OpenLDAP 1.2.11

%prep
%setup

%build
%{__rm} -rf /tmp/ldap-pfx; mkdir -p ./ldap-pfx; ln -s `pwd`/ldap-pfx /tmp/ldap-pfx
sh Misc/openldap.sh
sh configure
%{__make}
%{__make} filelist

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/usr
%{__make} install DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files -f filelist
%defattr(-,root,root)
%doc README

%changelog
