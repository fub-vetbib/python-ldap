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
	PyObject *zero, *author;

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

#if LDAP_API_VERSION >= 2000
	/* OpenLDAPv2 */
	add_int(d,VERSION3);
	add_int(d,VERSION_MIN);
	add_int(d,VERSION_MAX);
	add_int(d,TAG_LDAPDN);
	add_int(d,TAG_LDAPCRED);
	add_int(d,TAG_CONTROLS);
	add_int(d,TAG_REFERRAL);

	add_int(d,REQ_EXTENDED);
#endif
#if LDAP_API_VERSION >= 2004
	add_int(d,TAG_NEWSUPERIOR);
	add_int(d,TAG_EXOP_REQ_OID);
	add_int(d,TAG_EXOP_REQ_VALUE);
	add_int(d,TAG_EXOP_RES_OID);
	add_int(d,TAG_EXOP_RES_VALUE);
	add_int(d,TAG_SASL_RES_CREDS);
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

#if LDAP_API_VERSION >= 2000
	/* OpenLDAPv2 */
	add_int_r(d,RES_SEARCH_REFERENCE);
	add_int_r(d,RES_EXTENDED);
	add_int_r(d,RES_EXTENDED_PARTIAL);
	add_int_r(d,RES_UNSOLICITED);
#endif

	/* non-reversibles */

	add_int(d,AUTH_NONE);
	add_int(d,AUTH_SIMPLE);
	add_int(d,AUTH_KRBV4);
	add_int(d,AUTH_KRBV41);
	add_int(d,AUTH_KRBV42);
	add_int(d,FILTER_AND);
	add_int(d,FILTER_OR);
	add_int(d,FILTER_NOT);
	add_int(d,FILTER_EQUALITY);
	add_int(d,FILTER_SUBSTRINGS);
	add_int(d,FILTER_GE);
	add_int(d,FILTER_LE);
	add_int(d,FILTER_PRESENT);
	add_int(d,FILTER_APPROX);
	add_int(d,SUBSTRING_INITIAL);
	add_int(d,SUBSTRING_ANY);
	add_int(d,SUBSTRING_FINAL);
	add_int(d,SCOPE_BASE);
	add_int(d,SCOPE_ONELEVEL);
	add_int(d,SCOPE_SUBTREE);
	add_int(d,MOD_ADD);
	add_int(d,MOD_DELETE);
	add_int(d,MOD_REPLACE);
	add_int(d,MOD_BVALUES);

#if LDAP_API_VERSION >= 2000
	/* OpenLDAPv2 */
	add_int(d,FILTER_EXT);
	add_int(d,FILTER_EXT_OID);
	add_int(d,FILTER_EXT_TYPE);
	add_int(d,FILTER_EXT_VALUE);
	add_int(d,FILTER_EXT_DNATTRS);

	add_int(d,SCOPE_DEFAULT);

	add_int(d,MSG_ONE);
	add_int(d,MSG_ALL);
	add_int(d,MSG_RECEIVED);
#endif

	/* (errors.c contains the error constants) */

#ifdef LDAP_CACHE_BUCKETS
	add_int(d,CACHE_BUCKETS);
#endif
#ifdef LDAP_CACHE_OPT_CACHENOERRS
	add_int(d,CACHE_OPT_CACHENOERRS);
#endif
#ifdef LDAP_CACHE_OPT_CACHEALLERRS
	add_int(d,CACHE_OPT_CACHEALLERRS);
#endif
	add_int(d,FILT_MAXSIZ);
	add_int(d,DEREF_NEVER);
	add_int(d,DEREF_SEARCHING);
	add_int(d,DEREF_FINDING);
	add_int(d,DEREF_ALWAYS);
	add_int(d,NO_LIMIT);
#ifdef LDAP_OPT_DNS
	add_int(d,OPT_DNS);
#endif
#ifdef LDAP_OPT_REFERRALS
	add_int(d,OPT_REFERRALS);
#endif
	add_int(d,OPT_RESTART);

	/* XXX - these belong in errors.c */

	add_int(d,URL_ERR_BADSCOPE);
	add_int(d,URL_ERR_MEM);

	/* author */

	author = PyString_FromString("David Leonard <leonard@it.uq.edu.au>");
	PyDict_SetItemString(d, "__author__", author);
	Py_DECREF(author);

}
