/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * version info
 * $Id$
 */

#include "common.h"

#define _STR(x)	#x
#define STR(x)	_STR(x)

static char version_str[] = STR(LDAPMODULE_VERSION);

void
LDAPinit_version( PyObject* d ) 
{
	PyObject *version;

	version = PyString_FromString(version_str);
	PyDict_SetItemString( d, "__version__", version );
	Py_DECREF(version);
}
