#!/bin/sh

WRKDIST=`dirname $0`/..				# where the sources are now
VERSION=`sh $WRKDIST/Build/version.sh`		# version of src dist
DIST=python-ldap-$VERSION			# directory name to make
FLAGS="-rHEAD"					# flags to extract right vers

rm -rf $DIST

echo "Extracting release '$FLAGS' for $DIST"

if test "" = "$CVSROOT"; then
    CVSROOT=":pserver:anonymous@cvs.python-ldap.sourceforge.net:/cvsroot/python-ldap"
    export CVSROOT
fi

cvs -q -z3 export -d $DIST $FLAGS python-ldap

# create the configure script
(cd $DIST && autoreconf)

# prune out the build subdir..
rm -rf $DIST/Build

tar zfcv $DIST-src.tar.gz $DIST

TARGET=python-ldap.sourceforge.net:/home/groups/ftp/pub/python-ldap/$DIST-src.tar.gz
echo "Use this command to install"
echo "scp $DIST-src.tar.gz $TARGET"
