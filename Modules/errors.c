/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/*
 * errors that arise from ldap use
 * $Id$
 *
 * Most errors become their own exception
 */

#include "common.h"
#include "errors.h"

/* the base exception class */

PyObject*
LDAPexception_class;

/* list of error objects */

#define NUM_LDAP_ERRORS		LDAP_REFERRAL_LIMIT_EXCEEDED+1
static PyObject* errobjects[ NUM_LDAP_ERRORS ];


/* Convert a bare LDAP error number into an exception */
PyObject*
LDAPerr(int errnum)
{
	if (errnum > 0 && errnum < NUM_LDAP_ERRORS)
		PyErr_SetNone(errobjects[errnum]);
	else
		PyErr_SetObject(LDAPexception_class, 
		    Py_BuildValue("{s:i}", "errnum", errnum));
	return NULL;
}

/* Convert an LDAP error into an informative python exception */
PyObject*
LDAPerror( LDAP*l, char*msg ) 
{
	if (l == NULL) {
		PyErr_SetFromErrno( LDAPexception_class );
		return NULL;
	}
	else {
		int errnum;
		PyObject *errobj;
		PyObject *info;
		PyObject *str;

		char *matched, *error;
		if (ldap_get_option(l, LDAP_OPT_ERROR_NUMBER, &errnum) < 0)
			errobj = LDAPexception_class;	/* unknown error XXX */
		else
			errobj = errobjects[errnum];
		
		if (errnum == LDAP_NO_MEMORY)
			return PyErr_NoMemory();

		info = PyDict_New();
		if (info == NULL)
			return NULL;

		str = PyString_FromString(ldap_err2string(errnum));
		if (str)
			PyDict_SetItemString( info, "desc", str );
		Py_XDECREF(str);

		if (ldap_get_option(l, LDAP_OPT_MATCHED_DN, &matched) >= 0
			&& matched != NULL) {
		    if (*matched != '\0') {
			str = PyString_FromString(matched);
			if (str)
			    PyDict_SetItemString( info, "matched", str );
			Py_XDECREF(str);
		    }
		    ldap_memfree(matched);
		}
		
		if (errnum == LDAP_REFERRAL) {
		    str = PyString_FromString(msg);
		    if (str)
			PyDict_SetItemString( info, "info", str );
		    Py_XDECREF(str);
		} else if (ldap_get_option(l, LDAP_OPT_ERROR_STRING, &error) >= 0
			&& error != NULL) {
		    if (error != '\0') {
			str = PyString_FromString(error);
			if (str)
			    PyDict_SetItemString( info, "info", str );
			Py_XDECREF(str);
		    }
		    ldap_memfree(error);
		}
		PyErr_SetObject( errobj, info );
		Py_DECREF(info);
		return NULL;
	}
}


/* initialisation */

void
LDAPinit_errors( PyObject*d ) {
        
        /* create the base exception class */
        LDAPexception_class = PyErr_NewException("ldap.LDAPError",
                                                  NULL,
                                                  NULL);
        PyDict_SetItemString( d, "LDAPError", LDAPexception_class );

	/* XXX - backward compatibility with pre-1.8 */
        PyDict_SetItemString( d, "error", LDAPexception_class );
	Py_DECREF( LDAPexception_class );

	/* create each LDAP error object */

#	define seterrobj2(n,o) \
		PyDict_SetItemString( d, #n, (errobjects[LDAP_##n] = o) )


#	define seterrobj(n) { \
		PyObject *e = PyErr_NewException("ldap." #n,		\
				  LDAPexception_class, NULL);		\
		seterrobj2(n, e);					\
		Py_DECREF(e);						\
	}

#	define seterrobjas(n,existing) \
		seterrobj2( n, existing )

	seterrobj(ADMINLIMIT_EXCEEDED);
	seterrobj(AFFECTS_MULTIPLE_DSAS);
	seterrobj(ALIAS_DEREF_PROBLEM);
	seterrobj(ALIAS_PROBLEM);
	seterrobj(ALREADY_EXISTS);
	seterrobj(AUTH_UNKNOWN);
	seterrobj(BUSY);
	seterrobj(CLIENT_LOOP);
	seterrobj(COMPARE_FALSE);
	seterrobj(COMPARE_TRUE);
	seterrobj(CONFIDENTIALITY_REQUIRED);
	seterrobj(CONNECT_ERROR);
	seterrobj(CONSTRAINT_VIOLATION);
	seterrobj(CONTROL_NOT_FOUND);
	seterrobj(DECODING_ERROR);
	seterrobj(ENCODING_ERROR);
	seterrobj(FILTER_ERROR);
	seterrobj(INAPPROPRIATE_AUTH);
	seterrobj(INAPPROPRIATE_MATCHING);
	seterrobj(INSUFFICIENT_ACCESS);
	seterrobj(INVALID_CREDENTIALS);
	seterrobj(INVALID_DN_SYNTAX);
	seterrobj(INVALID_SYNTAX);
	seterrobj(IS_LEAF);
	seterrobj(LOCAL_ERROR);
	seterrobj(LOOP_DETECT);
	seterrobj(MORE_RESULTS_TO_RETURN);
	seterrobj(NAMING_VIOLATION);
	seterrobj(NO_OBJECT_CLASS_MODS);
	seterrobj(NOT_ALLOWED_ON_NONLEAF);
	seterrobj(NOT_ALLOWED_ON_RDN);
	seterrobj(NOT_SUPPORTED);
	seterrobj(NO_MEMORY);
	seterrobj(NO_OBJECT_CLASS_MODS);
	seterrobj(NO_RESULTS_RETURNED);
	seterrobj(NO_SUCH_ATTRIBUTE);
	seterrobj(NO_SUCH_OBJECT);
	seterrobj(OBJECT_CLASS_VIOLATION);
	seterrobj(OPERATIONS_ERROR);
	seterrobj(OTHER);
	seterrobj(PARAM_ERROR);
	seterrobj(PARTIAL_RESULTS);
	seterrobj(PROTOCOL_ERROR);
	seterrobj(REFERRAL);
	seterrobj(REFERRAL_LIMIT_EXCEEDED);
	seterrobj(RESULTS_TOO_LARGE);
#ifdef HAVE_SASL
	seterrobj(SASL_BIND_IN_PROGRESS);
#endif
	seterrobj(SERVER_DOWN);
	seterrobj(SIZELIMIT_EXCEEDED);
#ifdef LDAP_STRONG_AUTH_NOT_SUPPORTED
	seterrobj(STRONG_AUTH_NOT_SUPPORTED);
#endif
	seterrobj(STRONG_AUTH_REQUIRED);
	seterrobj(SUCCESS);
	seterrobj(TIMELIMIT_EXCEEDED);
	seterrobj(TIMEOUT);
	seterrobj(TYPE_OR_VALUE_EXISTS);
	seterrobj(UNAVAILABLE);
	seterrobj(UNAVAILABLE_CRITICAL_EXTENSION);
	seterrobj(UNDEFINED_TYPE);
	seterrobj(UNWILLING_TO_PERFORM);
	seterrobj(USER_CANCELLED);
}
