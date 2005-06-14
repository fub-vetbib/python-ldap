/* Deepak Giridharagopal <deepak@arlut.utexas.edu>, 2004.
 * Applied Research Laboratories, University of Texas at Austin
 */

#ifndef __h_ldapcontrol
#define __h_ldapcontrol

#include "Python.h"
#include "ldap.h"

void LDAPinit_control(PyObject *d);
void LDAPControl_List_DEL( LDAPControl** );
LDAPControl** List_to_LDAPControls( PyObject* );
PyObject* LDAPControls_to_List(LDAPControl **ldcs);

#endif /* __h_ldapcontrol */
