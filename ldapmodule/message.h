/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_message 
#define __h_message 

/* $Id$ */

#include "lber.h"
#include "ldap.h"
#include "Python.h"

extern PyObject* LDAPmessage_to_python( LDAP*ld, LDAPMessage*m );

#endif /* __h_message_ */

