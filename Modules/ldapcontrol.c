/* Deepak Giridharagopal <deepak@arlut.utexas.edu>, 2004.
 * Applied Research Laboratories, University of Texas at Austin
 */

/*
 * ldapcontrol.c - wrapper around libldap LDAPControl structs.
 */

#include "ldapcontrol.h"
#include "common.h"

/* Prints to stdout the contents of an array of LDAPControl objects */

/* XXX: This is a debugging tool, and the printf generates some warnings
 * about pointer types. I left it here in case something breaks and we
 * need to inspect an LDAPControl structure.

static void
LDAPControl_DumpList( LDAPControl** lcs ) {
    LDAPControl** lcp;
    LDAPControl* lc;
    
    for ( lcp = lcs; *lcp; lcp++ ) {
        lc = *lcp;
        printf("OID: %s\nCriticality: %d\nBER length: %d\nBER value: %x\n",
            lc->ldctl_oid, lc->ldctl_iscritical, lc->ldctl_value.bv_len,
            lc->ldctl_value.bv_val);
    }
} */

/* Free a single LDAPControl object created by Tuple_to_LDAPControl */
  
static void
LDAPControl_DEL( LDAPControl* lc )
{
    if (lc == NULL)
        return;
  
    if (lc->ldctl_oid)
        PyMem_DEL(lc->ldctl_oid);
    PyMem_DEL(lc);
}

/* Free an array of LDAPControl objects created by List_to_LDAPControls */

void
LDAPControl_List_DEL( LDAPControl** lcs )
{
    LDAPControl** lcp;
    if (lcs == NULL)
        return;

    for ( lcp = lcs; *lcp; lcp++ )
        LDAPControl_DEL( *lcp );

    PyMem_DEL( lcs );
}

/* Takes a tuple of the form:
 * (OID: string, Criticality: int/boolean, Value: string/None)
 * and converts it into an LDAPControl structure.
 *
 * The Value string should represent an ASN.1 encoded structure.
 */

static LDAPControl*
Tuple_to_LDAPControl( PyObject* tup )
{
    char *oid;
    char iscritical;
    struct berval berbytes;
    PyObject *bytes;
    LDAPControl *lc = NULL;
    int len;

    if (!PyTuple_Check(tup)) {
	PyErr_SetObject(PyExc_TypeError, Py_BuildValue("sO",
	   "expected a tuple", tup));
	return NULL;
    }

    if (!PyArg_ParseTuple( tup, "sbO", &oid, &iscritical, &bytes ))
        return NULL;
  
    lc = PyMem_NEW(LDAPControl, 1);
    if (lc == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    lc->ldctl_iscritical = iscritical;

    len = strlen(oid);
    lc->ldctl_oid = PyMem_NEW(char, len + 1);
    if (lc->ldctl_oid == NULL) {
        PyErr_NoMemory();
        LDAPControl_DEL(lc);
        return NULL;
    }
    memcpy(lc->ldctl_oid, oid, len + 1);

    /* The berval can either be None or a String */
    if (PyNone_Check(bytes)) {
        berbytes.bv_len = 0;
        berbytes.bv_val = NULL;
    }
    else if (PyString_Check(bytes)) {
        berbytes.bv_len = PyString_Size(bytes);
        berbytes.bv_val = PyString_AsString(bytes);
    }
    else {
	PyErr_SetObject(PyExc_TypeError, Py_BuildValue("sO",
            "expected a string", bytes));
        LDAPControl_DEL(lc);
        return NULL;
    }
    
    lc->ldctl_value = berbytes;

    return lc;
}

/* Convert a list of tuples (of a format acceptable to the Tuple_to_LDAPControl
 * function) into an array of LDAPControl objects. */

LDAPControl**
List_to_LDAPControls( PyObject* list )
{
    int len, i;
    LDAPControl** ldcs;
    LDAPControl* ldc;
    PyObject* item;
  
    if (!PySequence_Check(list)) {
	PyErr_SetObject(PyExc_TypeError, Py_BuildValue("sO",
	   "expected a list", list));
	return NULL;
    }

    len = PySequence_Length(list);
    ldcs = PyMem_NEW(LDAPControl*, len + 1);
    if (ldcs == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    for (i = 0; i < len; i++) {
      item = PySequence_GetItem(list, i);
      if (item == NULL) {
          PyMem_DEL(ldcs);
          return NULL;
      }

      ldc = Tuple_to_LDAPControl(item);
      if (ldc == NULL) {
          PyMem_DEL(ldcs);
          return NULL;
      }

      ldcs[i] = ldc;
    }

    ldcs[len] = NULL;
    return ldcs;
}


