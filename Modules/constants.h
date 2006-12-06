/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_constants_
#define __h_constants_

/* $Id$ */

#include "common.h"
extern void LDAPinit_constants( PyObject* d );
extern PyObject* LDAPconstant( int );

#ifndef LDAP_CONTROL_PAGE_OID
#define LDAP_CONTROL_PAGE_OID "1.2.840.113556.1.4.319"
#endif /* !LDAP_CONTROL_PAGE_OID */

#endif /* __h_constants_ */
