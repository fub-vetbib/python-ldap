/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * constants defined for LDAP
 * $Id$
 */

#include "common.h"
#include "constants.h"
#include "lber.h"
#include "ldap.h"

static PyObject* reverse;
static PyObject* forward;

/* convert an result integer into a Python string */

PyObject*
LDAPconstant( int val ) {
    PyObject *i = PyInt_FromLong( val );
    PyObject *s = PyObject_GetItem( reverse, i );
    if (s == NULL) {
    	PyErr_Clear();
	return i;
    }
    Py_DECREF(i);
    return s;
}

/* initialise the module constants */

void
LDAPinit_constants( PyObject* d ) 
{
	PyObject *zero, *author,*obj;

	reverse = PyDict_New();
	forward = PyDict_New();
	
	PyDict_SetItemString( d, "_reverse", reverse );
	PyDict_SetItemString( d, "_forward", forward );

#define add_int_r(d, name)                                              \
	{                                                               \
	    long v = LDAP_##name;                                       \
	    PyObject *i = PyInt_FromLong( v );                          \
	    PyObject *s = PyString_FromString( #name );                 \
	    PyDict_SetItem( d, s, s );                                  \
	    PyDict_SetItem( reverse, i, s );                            \
	    PyDict_SetItem( forward, s, i );                            \
	    Py_DECREF(i);                                               \
	    Py_DECREF(s);                                               \
	    /* printf("%s -> %ld\n", #name, v );  */                    \
	}

#define add_int(d, name)                                                \
	{								\
		PyObject *i = PyInt_FromLong(LDAP_##name);		\
		PyDict_SetItemString( d, #name, i );			\
		Py_DECREF(i);						\
	}

	/* simple constants */

	add_int(d,API_VERSION);
	add_int(d,VENDOR_VERSION);

	add_int(d,PORT);
	add_int(d,VERSION1);
	add_int(d,VERSION2);
	add_int(d,VERSION);
	add_int(d,TAG_MESSAGE);
	add_int(d,TAG_MSGID);

	add_int(d,REQ_BIND);
	add_int(d,REQ_UNBIND);
	add_int(d,REQ_SEARCH);
	add_int(d,REQ_MODIFY);
	add_int(d,REQ_ADD);
	add_int(d,REQ_DELETE);
	add_int(d,REQ_MODRDN);
	add_int(d,REQ_COMPARE);
	add_int(d,REQ_ABANDON);

	add_int(d,VERSION3);
	add_int(d,VERSION_MIN);
	add_int(d,VERSION_MAX);
	add_int(d,TAG_LDAPDN);
	add_int(d,TAG_LDAPCRED);
	add_int(d,TAG_CONTROLS);
	add_int(d,TAG_REFERRAL);

	add_int(d,REQ_EXTENDED);
#if LDAP_API_VERSION >= 2004
	add_int(d,TAG_NEWSUPERIOR);
	add_int(d,TAG_EXOP_REQ_OID);
	add_int(d,TAG_EXOP_REQ_VALUE);
	add_int(d,TAG_EXOP_RES_OID);
	add_int(d,TAG_EXOP_RES_VALUE);
#ifdef HAVE_SASL
	add_int(d,TAG_SASL_RES_CREDS);
#endif
#endif

	/* reversibles */

	zero = PyInt_FromLong( 0 );
	PyDict_SetItem( reverse, zero, Py_None );
	Py_DECREF( zero );

	add_int_r(d,RES_BIND);
	add_int_r(d,RES_SEARCH_ENTRY);
	add_int_r(d,RES_SEARCH_RESULT);
	add_int_r(d,RES_MODIFY);
	add_int_r(d,RES_ADD);
	add_int_r(d,RES_DELETE);
	add_int_r(d,RES_MODRDN);
	add_int_r(d,RES_COMPARE);
	add_int(d,RES_ANY);

	add_int_r(d,RES_SEARCH_REFERENCE);
	add_int_r(d,RES_EXTENDED);
	add_int_r(d,RES_UNSOLICITED);

	/* non-reversibles */

	add_int(d,AUTH_NONE);
	add_int(d,AUTH_SIMPLE);
	add_int(d,AUTH_KRBV4);
	add_int(d,AUTH_KRBV41);
	add_int(d,AUTH_KRBV42);
	add_int(d,SCOPE_BASE);
	add_int(d,SCOPE_ONELEVEL);
	add_int(d,SCOPE_SUBTREE);
	add_int(d,MOD_ADD);
	add_int(d,MOD_DELETE);
	add_int(d,MOD_REPLACE);
	add_int(d,MOD_BVALUES);

	add_int(d,MSG_ONE);
	add_int(d,MSG_ALL);
	add_int(d,MSG_RECEIVED);

	/* (errors.c contains the error constants) */

	add_int(d,DEREF_NEVER);
	add_int(d,DEREF_SEARCHING);
	add_int(d,DEREF_FINDING);
	add_int(d,DEREF_ALWAYS);
	add_int(d,NO_LIMIT);

	add_int(d,OPT_API_INFO);
	add_int(d,OPT_DEREF);
	add_int(d,OPT_SIZELIMIT);
	add_int(d,OPT_TIMELIMIT);
#ifdef LDAP_OPT_REFERRALS
	add_int(d,OPT_REFERRALS);
#endif
	add_int(d,OPT_RESTART);
	add_int(d,OPT_PROTOCOL_VERSION);
	add_int(d,OPT_SERVER_CONTROLS);
	add_int(d,OPT_CLIENT_CONTROLS);
	add_int(d,OPT_API_FEATURE_INFO);
	add_int(d,OPT_HOST_NAME);
	add_int(d,OPT_ERROR_STRING);
	add_int(d,OPT_MATCHED_DN);
	add_int(d,OPT_PRIVATE_EXTENSION_BASE);
	add_int(d,OPT_DEBUG_LEVEL);
	add_int(d,OPT_TIMEOUT);
	add_int(d,OPT_REFHOPLIMIT);
	add_int(d,OPT_NETWORK_TIMEOUT);
	add_int(d,OPT_URI);
	add_int(d,OPT_X_TLS);
#if LDAP_VENDOR_VERSION>=20013
	add_int(d,OPT_X_TLS_CTX);
#endif
	add_int(d,OPT_X_TLS_CACERTFILE);
	add_int(d,OPT_X_TLS_CACERTDIR);
	add_int(d,OPT_X_TLS_CERTFILE);
	add_int(d,OPT_X_TLS_KEYFILE);
	add_int(d,OPT_X_TLS_REQUIRE_CERT);
	add_int(d,OPT_X_TLS_CIPHER_SUITE);
	add_int(d,OPT_X_TLS_RANDOM_FILE);
	add_int(d,OPT_X_TLS_NEVER);
	add_int(d,OPT_X_TLS_HARD);
	add_int(d,OPT_X_TLS_DEMAND);
	add_int(d,OPT_X_TLS_ALLOW);
	add_int(d,OPT_X_TLS_TRY);
	add_int(d,OPT_X_SASL_MECH);
	add_int(d,OPT_X_SASL_REALM);
	add_int(d,OPT_X_SASL_AUTHCID);
	add_int(d,OPT_X_SASL_AUTHZID);
	add_int(d,OPT_X_SASL_SSF);
	add_int(d,OPT_X_SASL_SSF_EXTERNAL);
	add_int(d,OPT_X_SASL_SECPROPS);
	add_int(d,OPT_X_SASL_SSF_MIN);
	add_int(d,OPT_X_SASL_SSF_MAX);
	
	/*add_int(d,OPT_ON);*/
	obj = PyInt_FromLong(1);
	PyDict_SetItemString( d, "LDAP_OPT_ON", obj );
	Py_DECREF(obj);
	/*add_int(d,OPT_OFF);*/
	obj = PyInt_FromLong(0);
	PyDict_SetItemString( d, "LDAP_OPT_OFF", obj );			
	Py_DECREF(obj);
	
	add_int(d,OPT_SUCCESS);

	/* XXX - these belong in errors.c */

	add_int(d,URL_ERR_BADSCOPE);
	add_int(d,URL_ERR_MEM);

	/* author */

	author = PyString_FromString("David Leonard <leonard@it.uq.edu.au>");
	PyDict_SetItemString(d, "__author__", author);
	Py_DECREF(author);

	/*add_int(d,LIBLDAP_R);*/
#ifdef HAVE_LIBLDAP_R
	obj = PyInt_FromLong(1);
#else
	obj = PyInt_FromLong(0);
#endif
	PyDict_SetItemString( d, "LIBLDAP_R", obj );
	Py_DECREF(obj);

}
