#! /bin/sh

# Locate the top of the distribution
srcdir=`dirname $0`/..
version=`sh ${srcdir}/Build/version.sh`
release=1
specfile=python-ldap-$version-$release.spec

rm -f ${specfile}
sed -e "s/@version@/$version/g" \
    -e "s/@release@/$release/g" \
    < ${srcdir}/Build/template.spec \
    > ${specfile}

rpm -b --buildroot `pwd`/root --test $specfile
