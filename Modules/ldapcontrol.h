/* See http://python-ldap.sourceforge.net for details.
 * $Id$ */

#ifndef __h_ldapcontrol
#define __h_ldapcontrol

#include "common.h"
#include "ldap.h"

void LDAPinit_control(PyObject *d);
void LDAPControl_List_DEL( LDAPControl** );
LDAPControl** List_to_LDAPControls( PyObject* );
PyObject* LDAPControls_to_List(LDAPControl **ldcs);

#endif /* __h_ldapcontrol */
