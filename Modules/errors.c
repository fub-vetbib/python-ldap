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

#if LDAP_API_VERSION >= 2000
	/* OpenLDAPv2 */
#define NUM_LDAP_ERRORS		LDAP_REFERRAL_LIMIT_EXCEEDED+1
#else
#define NUM_LDAP_ERRORS		LDAP_NO_MEMORY+1
#endif
static PyObject* 
errobjects[ NUM_LDAP_ERRORS ];

/* convert an LDAP error into a python exception */

PyObject*
LDAPerror( LDAP*l, char*msg ) 
{
	if (l == NULL) {
		PyErr_SetFromErrno( LDAPexception_class );
		return NULL;
	}
#if defined(LDAP_TYPE_IS_OPAQUE) && LDAP_API_VERSION < 2000
	else {
		PyErr_SetString(LDAPexception_class,
			"unknown error (C API does not expose error)");
		return NULL;
	}
#else /* defined(LDAP_TYPE_IS_OPAQUE) && LDAP_API_VERSION < 2000 */
	else {
		int errnum;
		PyObject *errobj;
		PyObject *info;
		PyObject *str;

#if LDAP_API_VERSION >= 2000
		char *matched, *error;
		if (ldap_get_option(l, LDAP_OPT_ERROR_NUMBER, &errnum) < 0)
#else
		errnum = l->ld_errno;
		if (errnum<0 || errnum>=NUM_LDAP_ERRORS)
#endif
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

#if LDAP_API_VERSION >= 2000
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
#else /* LDAP_API_VERSION >= 2000 */
		if (l->ld_matched != NULL && *l->ld_matched != '\0') 
		{
		   str = PyString_FromString(l->ld_matched);
		   if (str)
			   PyDict_SetItemString( info, "matched", str );
		   Py_XDECREF(str);
		}

		if (l->ld_error != NULL && *l->ld_error != '\0') 
		{
		   str = PyString_FromString(l->ld_error);
		   if (str)
			   PyDict_SetItemString( info, "info", str );
		   Py_XDECREF(str);
		}
#endif /* LDAP_API_VERSION >= 2000 */
		PyErr_SetObject( errobj, info );
		Py_DECREF(info);
		return NULL;
	}
#endif /* defined(LDAP_TYPE_IS_OPAQUE) && LDAP_API_VERSION < 2000 */
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

	seterrobj(SUCCESS);
	seterrobj(OPERATIONS_ERROR);
	seterrobj(PROTOCOL_ERROR);
	seterrobj(TIMELIMIT_EXCEEDED);
	seterrobj(SIZELIMIT_EXCEEDED);
	seterrobj(COMPARE_FALSE);
	seterrobj(COMPARE_TRUE);
#ifdef LDAP_STRONG_AUTH_NOT_SUPPORTED
	seterrobj(STRONG_AUTH_NOT_SUPPORTED);
#endif
	seterrobj(STRONG_AUTH_REQUIRED);
	seterrobj(PARTIAL_RESULTS);
	seterrobj(NO_SUCH_ATTRIBUTE);
	seterrobj(UNDEFINED_TYPE);
	seterrobj(INAPPROPRIATE_MATCHING);
	seterrobj(CONSTRAINT_VIOLATION);
	seterrobj(TYPE_OR_VALUE_EXISTS);
	seterrobj(INVALID_SYNTAX);
	seterrobj(NO_SUCH_OBJECT);
	seterrobj(ALIAS_PROBLEM);
	seterrobj(INVALID_DN_SYNTAX);
	seterrobj(IS_LEAF);
	seterrobj(ALIAS_DEREF_PROBLEM);
	seterrobj(INAPPROPRIATE_AUTH);
	seterrobj(INVALID_CREDENTIALS);
	seterrobj(INSUFFICIENT_ACCESS);
	seterrobj(BUSY);
	seterrobj(UNAVAILABLE);
	seterrobj(UNWILLING_TO_PERFORM);
	seterrobj(LOOP_DETECT);
	seterrobj(NAMING_VIOLATION);
	seterrobj(OBJECT_CLASS_VIOLATION);
	seterrobj(NOT_ALLOWED_ON_NONLEAF);
	seterrobj(NOT_ALLOWED_ON_RDN);
	seterrobj(ALREADY_EXISTS);
	seterrobj(NO_OBJECT_CLASS_MODS);
	seterrobj(RESULTS_TOO_LARGE);
	seterrobj(OTHER);
	seterrobj(SERVER_DOWN);
	seterrobj(LOCAL_ERROR);
	seterrobj(ENCODING_ERROR);
	seterrobj(DECODING_ERROR);
	seterrobj(TIMEOUT);
	seterrobj(AUTH_UNKNOWN);
	seterrobj(FILTER_ERROR);
	seterrobj(USER_CANCELLED);
	seterrobj(PARAM_ERROR);
	seterrobj(NO_MEMORY);
#if LDAP_API_VERSION >= 2000
	/* OpenLDAPv2 */
	seterrobj(REFERRAL);
	seterrobj(ADMINLIMIT_EXCEEDED);
	seterrobj(UNAVAILABLE_CRITICAL_EXTENSION);
	seterrobj(CONFIDENTIALITY_REQUIRED);
	seterrobj(SASL_BIND_IN_PROGRESS);
	seterrobj(AFFECTS_MULTIPLE_DSAS);
	seterrobj(CONNECT_ERROR);
	seterrobj(NOT_SUPPORTED);
	seterrobj(CONTROL_NOT_FOUND);
	seterrobj(NO_RESULTS_RETURNED);
	seterrobj(MORE_RESULTS_TO_RETURN);
	seterrobj(CLIENT_LOOP);
	seterrobj(REFERRAL_LIMIT_EXCEEDED);
#endif
}
