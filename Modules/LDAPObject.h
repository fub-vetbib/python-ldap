/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
#ifndef __h_LDAPObject 
#define __h_LDAPObject 

/* $Id$ */

#include "lber.h"
#include "ldap.h"
#if LDAP_API_VERSION < 2000
#error Current python-ldap requires OpenLDAP 2.x
#endif
#include "Python.h"

#if PYTHON_API_VERSION < 1007
typedef PyObject*	_threadstate;
#else
typedef PyThreadState*	_threadstate;
#endif

typedef struct {
        PyObject_HEAD
	LDAP* ldap;
	_threadstate	_save; /* for thread saving on referrals */
	int valid;
} LDAPObject;

extern PyTypeObject LDAP_Type;
#define LDAPObject_Check(v)     ((v)->ob_type == &LDAP_Type)

extern LDAPObject *newLDAPObject( LDAP* );

/* macros to allow thread saving in the context of an LDAP connection */

#define LDAP_BEGIN_ALLOW_THREADS( l )                                   \
	{                                                               \
	  LDAPObject *lo = (l);                                         \
	  if (lo->_save != NULL)                                        \
	  	Py_FatalError( "saving thread twice?" );                \
	  lo->_save = PyEval_SaveThread();                              \
	}

#define LDAP_END_ALLOW_THREADS( l )                                     \
	{                                                               \
	  LDAPObject *lo = (l);                                         \
	  _threadstate _save = lo->_save;                               \
	  lo->_save = NULL;                                             \
	  PyEval_RestoreThread( _save );                                \
	}

PyObject* l_ldap_get_option(PyObject* self, PyObject *args);
PyObject* l_ldap_set_option(PyObject* self, PyObject *args);

#endif /* __h_LDAPObject */

