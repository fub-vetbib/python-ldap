#! /bin/sh
# $Id$

#
# Extract the current version number from configure.in
#

CONFIGURE_IN=`dirname $0`/../configure.in
sed -n -e 's/^AC_DEFINE(LDAPMODULE_VERSION, \(.*\)).*/\1/p' \
		< $CONFIGURE_IN

