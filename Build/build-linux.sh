#! /bin/sh

# Locate the top of the distribution
srcdir=`dirname $0`/..
version=`sh ${srcdir}/Build/version.sh`
release=1
specfile=SPECS/python-ldap-$version-$release.spec

if test  -f $HOME/.rpmmacros; then
	: hope it works
else
	mkdir -p BUILD RPMS SPECS SOURCES
	echo "%_topdir		"`pwd` > $HOME/.rpmmacros
fi

rm -f ${specfile}
sed -e "s/@version@/$version/g" \
    -e "s/@release@/$release/g" \
    < ${srcdir}/Build/template.spec \
    > ${specfile}

rpm -bb $specfile

