/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* 
 * LDAP module
 * $Id$
 */

#include "common.h"
#include "version.h"
#include "constants.h"
#include "errors.h"
#include "functions.h"
/* #include "string_translators.h" */
#include "template.h"

#include "LDAPObject.h"

/* dummy module methods */

static PyMethodDef methods[]  = {
	{ NULL, NULL }
};

/* module initialisation */

void
init_ldap()
{
	PyObject *m, *d;

#ifdef WIN32
	/* See http://www.python.org/doc/FAQ.html#3.24 */
	LDAP_Type.ob_type = &PyType_Type;
#endif

	/* Create the module and add the functions */
	m = Py_InitModule("_ldap", methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);

	LDAPinit_version(d);
	LDAPinit_constants(d);
	LDAPinit_errors(d);
	LDAPinit_functions(d);
/*	LDAPinit_string_translators(d); */

#if defined(HAVE_LDAP_INIT_TEMPLATES)
	LDAPinit_template(d);
#endif

	/* Check for errors */
	if (PyErr_Occurred())
		Py_FatalError("can't initialize module _ldap");
}
