/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * version info
 * $Id$
 */

#include "version.h"

static char version_str[] =
#	include "version_str.h"
;

void
LDAPinit_version( PyObject* d ) 
{
	PyDict_SetItemString( d, "__version__", 
				PyString_FromString(version_str) );
}
