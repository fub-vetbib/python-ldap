/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * functions - functions available at the module level
 * $Id$
 #*/

#include "common.h"
#include "functions.h"
#include "LDAPObject.h"
#include "errors.h"
#include "options.h"

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

/* ldap_explode_rdn */

static PyObject*
l_ldap_explode_rdn( PyObject* unused, PyObject *args )
{
    char *rdn;
    int notypes = 0;
    char **exploded;
    PyObject *result;
    int i;

    if (!PyArg_ParseTuple( args, "s|i", &rdn, &notypes )) return NULL;

    exploded = ldap_explode_rdn(rdn, notypes);

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

/* ldap_get_option (global options) */

static PyObject*
l_ldap_get_option(PyObject* self, PyObject *args)
{
    int option;

    if (!PyArg_ParseTuple(args, "i:get_option", &option))
	return NULL;
    return LDAP_get_option(NULL, option);
}


/* methods */

static PyMethodDef methods[] = {
    { "initialize",	(PyCFunction)l_ldap_initialize,		METH_VARARGS },
    { "explode_dn",	(PyCFunction)l_ldap_explode_dn,		METH_VARARGS },
    { "explode_rdn",	(PyCFunction)l_ldap_explode_rdn,	METH_VARARGS },
    { "set_option", (PyCFunction)l_ldap_set_option,		METH_VARARGS },
    { "get_option", (PyCFunction)l_ldap_get_option,		METH_VARARGS },
    { NULL, NULL }
};

/* initialisation */

void
LDAPinit_functions( PyObject* d ) {
    LDAPadd_methods( d, methods );
}
