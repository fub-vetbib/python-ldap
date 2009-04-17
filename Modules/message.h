/* See http://www.python-ldap.org/ for details.
 * $Id$ */

#ifndef __h_message 
#define __h_message 

#include "common.h"
#include "lber.h"
#include "ldap.h"

extern PyObject* LDAPmessage_to_python( LDAP*ld, LDAPMessage*m );

#endif /* __h_message_ */

