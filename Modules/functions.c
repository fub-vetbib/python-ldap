/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * functions - functions available at the module level
 * $Id$
 */

#include "common.h"
#include "functions.h"
#include "LDAPObject.h"
#include "errors.h"
#include "template.h"
#include "CIDict.h"
#include "options.h"

static short default_ldap_port(void);

/* Return the port number for LDAP servers */
static short
default_ldap_port()
{
#ifndef WIN32
	struct servent *se;

	/* Prefer getting the LDAP port number from /etc/services */
	Py_BEGIN_ALLOW_THREADS
	se = getservbyname("ldap", "tcp");
	Py_END_ALLOW_THREADS
	if (se != NULL)
		return ntohs(se->s_port);
#endif
	return LDAP_PORT;
}


/* ldap_open */

static PyObject*
l_ldap_open(PyObject* unused, PyObject *args)
{
    char *host;
    int port = 0;
    LDAP *ld;

    if (!PyArg_ParseTuple(args, "s|i", &host, &port))
    	return NULL;

    /* Look up the ldap service from /etc/services if not port not given. */
    if (port == 0) 
	port = default_ldap_port();

    Py_BEGIN_ALLOW_THREADS
    ld = ldap_open(host, port);
    Py_END_ALLOW_THREADS
    if (ld == NULL)
    	return LDAPerror(ld, "ldap_open");
    return (PyObject*)newLDAPObject(ld);
}

static char doc_open[] = 
"open(host [,port=PORT]) -> LDAPObject\n\n"
"\tOpens a new connection with an LDAP server, and returns an LDAP object\n"
"\trepresentative of this.\n"
"\t(This function is depreciated: use init() or initialize() instead.)";


/* ldap_init */

static PyObject*
l_ldap_init(PyObject* unused, PyObject *args)
{
    char *host;
    int port = 0;
    LDAP *ld;

    if (!PyArg_ParseTuple(args, "s|i", &host, &port))
    	return NULL;

    /* Look up the ldap service from /etc/services if not port not given. */
    if (port == 0)
	port = default_ldap_port();

    Py_BEGIN_ALLOW_THREADS
    ld = ldap_init(host, port);
    Py_END_ALLOW_THREADS
    if (ld == NULL)
    	return LDAPerror(ld, "ldap_init");
    return (PyObject*)newLDAPObject(ld);
}

static char doc_init[] = 
"init(host [,port=PORT]) -> LDAPObject\n\n"
"\tReturns an LDAP object for new connection to LDAP server.\n"
"\tThe actual connection will be openend when the first operation\n"
"\tis attempted.\n";

/* ldap_initialize */

static PyObject*
l_ldap_initialize(PyObject* unused, PyObject *args)
{
    char *uri;
    LDAP *ld = NULL;
    int ret;

    if (!PyArg_ParseTuple(args, "s", &uri))
    	return NULL;

    Py_BEGIN_ALLOW_THREADS
    ret = ldap_initialize(&ld, uri);
    Py_END_ALLOW_THREADS
    if (ret != LDAP_SUCCESS)
    	return LDAPerror(ld, "ldap_initialize");
    return (PyObject*)newLDAPObject(ld);
}

static char doc_initialize[] = 
"initialize(uri) -> LDAPObject\n\n"
"\tReturns an LDAP object for new connection to LDAP server.\n"
"\tThe actual connection open will occur when the first operation\n"
"\tis attempted.\n";

/* ldap_dn2ufn */

static PyObject*
l_ldap_dn2ufn( PyObject* unused, PyObject *args )
{
    char *dn;
    char *ufn;
    PyObject *result;

    if (!PyArg_ParseTuple( args, "s", &dn )) return NULL;

    ufn = ldap_dn2ufn(dn);
    if (ufn == NULL)
    	return PyErr_SetFromErrno(LDAPexception_class);
    result = PyString_FromString( ufn );
    free(ufn);
    return result;
}

static char doc_dn2ufn[] =
"dn2ufn(dn) -> string\n\n"
"\tTurns the DN into a more user-friendly form, stripping off type names.\n"
"\tSee RFC 1781 ``Using the Directory to Achieve User Friendly Naming''\n"
"\tfor more details on the UFN format.";

/* ldap_explode_dn */

static PyObject*
l_ldap_explode_dn( PyObject* unused, PyObject *args )
{
    char *dn;
    int notypes = 0;
    char **exploded;
    PyObject *result;
    int i;

    if (!PyArg_ParseTuple( args, "s|i", &dn, &notypes )) return NULL;

    exploded = ldap_explode_dn(dn, notypes);

    if (exploded == NULL) 
    	return PyErr_SetFromErrno(LDAPexception_class);

    result = PyList_New(0);
    for(i = 0; exploded[i]; i++) {
	PyObject *s = PyString_FromString(exploded[i]);
    	PyList_Append(result, s);
	Py_DECREF(s);
    }

    ldap_value_free(exploded);
    return result;
}

static char doc_explode_dn[] =
"explode_dn(dn [, notypes=0]) -> list\n\n"
"\tThis function takes the DN and breaks it up into its component parts.\n"
"\tEach part is known as an RDN (Relative Distinguished Name). The notypes\n"
"\tparameter is used to specify that only the RDN values be returned\n"
"\tand not their types. For example, the DN \"cn=Bob, c=US\" would be\n"
"\treturned as either [\"cn=Bob\", \"c=US\"] or [\"Bob\",\"US\"]\n"
"\tdepending on whether notypes was 0 or 1, respectively.";

/* ldap_is_ldap_url */

static PyObject*
l_ldap_is_ldap_url( PyObject* unused, PyObject *args )
{
    char *url;

    if (!PyArg_ParseTuple( args, "s", &url )) return NULL;
    return PyInt_FromLong( ldap_is_ldap_url( url ));
}

static char doc_is_ldap_url[] = 
"is_ldap_url(url) -> int\n\n"
"\tThis function returns true if url `looks like' an LDAP URL\n"
"\t(as opposed to some other kind of URL).";

/* ldap_set_option (global options) */

static PyObject*
l_ldap_set_option(PyObject* self, PyObject *args)
{
    PyObject *value;
    int option;

    if (!PyArg_ParseTuple(args, "iO:set_option", &option, &value))
	return NULL;
    if (LDAP_set_option(NULL, option, value) == -1)
	return NULL;
    Py_INCREF(Py_None);
	return Py_None;
}

static char doc_set_option[] = 
"set_option(name, value)\n\n"
"\tSet the value of an LDAP global option.\n";

/* ldap_get_option (global options) */

static PyObject*
l_ldap_get_option(PyObject* self, PyObject *args)
{
    int option;

    if (!PyArg_ParseTuple(args, "i:get_option", &option))
	return NULL;
    return LDAP_get_option(NULL, option);
}

static char doc_get_option[] = 
"get_option(name) -> value\n\n"
"\tGet the value of an LDAP global option.\n";

/* methods */

static PyMethodDef methods[] = {
    { "open",		(PyCFunction)l_ldap_open,		METH_VARARGS,
    	doc_open },
    { "init",		(PyCFunction)l_ldap_init,		METH_VARARGS,
    	doc_init },
    { "initialize",	(PyCFunction)l_ldap_initialize,		METH_VARARGS,
    	doc_initialize },
    { "dn2ufn",		(PyCFunction)l_ldap_dn2ufn,		METH_VARARGS,
    	doc_dn2ufn },
    { "explode_dn",	(PyCFunction)l_ldap_explode_dn,		METH_VARARGS,
    	doc_explode_dn },
    { "is_ldap_url",	(PyCFunction)l_ldap_is_ldap_url,	METH_VARARGS,
    	doc_is_ldap_url },
#if defined(HAVE_LDAP_INIT_TEMPLATES)
    { "init_templates", (PyCFunction)l_init_templates,		METH_VARARGS,
    	l_init_templates_doc },
#endif
    { "set_option", (PyCFunction)l_ldap_set_option,		METH_VARARGS,
    	doc_set_option },
    { "get_option", (PyCFunction)l_ldap_get_option,		METH_VARARGS,
    	doc_get_option },
    { NULL, NULL }
};

/* initialisation */

void
LDAPinit_functions( PyObject* d ) {
    LDAPadd_methods( d, methods );
}
