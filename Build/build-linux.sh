#! /bin/sh

# Locate the top of the distribution
srcdir=`dirname $0`/..

#re-sync
#(cd $srcdir && cvs up -PAd && autoreconf)

# clean up a bit
rm -rf Makefile Modules config.cache config.log config.status

# build openldap as required
rm -rf /tmp/ldap-pfx
mkdir -p ldap-pfx
ln -s `pwd`/ldap-pfx /tmp/ldap-pfx
sh $srcdir/Misc/openldap.sh

# perform an independent build
sh $srcdir/configure
make

# install under a different root
rm -rf destdir; mkdir destdir
mkdir -p destdir/usr
DESTDIR=`pwd`/destdir make install

