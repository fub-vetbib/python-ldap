# $Id$

WRKDIST=		${.CURDIR}/../..
VERSION!=		sh ${WRKDIST}/Build/version.sh

PKGNAME=		python-ldap-${VERSION}
RUN_DEPENDS=		python:lang/python
CATEGORIES=		misc
MAINATINER=		leonard@users.sourceforge.net
HOMEPAGE=		http://python-ldap.sourceforge.net/

FAKE=			Yes
CONFIGURE_STYLE=	gnu
SEPARATE_BUILD=		Yes
EXTRACT_ONLY=	

CONFIGURE_ARGS+=	--with-ldap=${LOCALBASE}

do-fetch:;

#-- put package on sourceforge ftp server
export-ftp: ${PKGFILE}
	scp ${PKGFILE} python-ldap.sourceforge.net:/home/groups/ftp/pub/python-ldap/${PKGNAME}-${OPSYS}-${ARCH}${PKG_SUFX}

.include <bsd.port.mk>
