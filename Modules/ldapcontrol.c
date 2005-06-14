/* Deepak Giridharagopal <deepak@arlut.utexas.edu>, 2004.
 * Applied Research Laboratories, University of Texas at Austin
 */

/*
 * ldapcontrol.c - wrapper around libldap LDAPControl structs.
 */

#include "common.h"
#include "LDAPObject.h"
#include "ldapcontrol.h"
#include "errors.h"

#include "lber.h"

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

PyObject*
LDAPControls_to_List(LDAPControl **ldcs)
{
    PyObject *res = 0, *pyctrl;
    LDAPControl **tmp = ldcs;
    unsigned num_ctrls = 0, i;

    if (tmp)
        while (*tmp++) num_ctrls++;

    if (!(res = PyList_New(num_ctrls)))
        goto endlbl;

    for (i = 0; i < num_ctrls; i++) {
        if (!(pyctrl = Py_BuildValue("sbs#", ldcs[i]->ldctl_oid,
                                     ldcs[i]->ldctl_iscritical,
                                     ldcs[i]->ldctl_value.bv_val,
                                     ldcs[i]->ldctl_value.bv_len))) {
            goto endlbl;
        }
        PyList_SET_ITEM(res, i, pyctrl);
    }
    Py_INCREF(res);

 endlbl:
    Py_XDECREF(res);
    return res;
}



/* --------------- en-/decoders ------------- */

PyDoc_STRVAR(encode_rfc2696__doc__,
             "encode_page_control(page_size, cookie) -> control_value\n"
             "\n"
             "The returned control_value is a string that contains the\n"
             " (BER-)encoded ASN.1 sequence 'realSearchControlValue'\n"
             " as defined by RFC 2696.");

static PyObject*
encode_rfc2696(PyObject *self, PyObject *args)
{
    PyObject *res = 0;
    BerElement *ber = 0;
    struct berval cookie, ctrl_val;
    unsigned long size;
    ber_tag_t tag;

    if (!PyArg_ParseTuple(args, "is#:encode_page_control", &size,
                          &cookie.bv_val, &cookie.bv_len)) {
        goto endlbl;
    }

    if (!(ber = ber_alloc_t(LBER_USE_DER))) {
        LDAPerr(LDAP_NO_MEMORY);
        goto endlbl;
    }

    tag = ber_printf(ber, "{i", size);
    if (tag == LBER_ERROR) {
        LDAPerr(LDAP_ENCODING_ERROR);
        goto endlbl;
    }

    if (!cookie.bv_len)
        tag = ber_printf(ber, "o", "", 0);
    else
        tag = ber_printf(ber, "O", &cookie);
    if (tag == LBER_ERROR) {
        LDAPerr(LDAP_ENCODING_ERROR);
        goto endlbl;
    }

    tag = ber_printf(ber, /*{ */ "N}");
    if (tag == LBER_ERROR) {
        LDAPerr(LDAP_ENCODING_ERROR);
        goto endlbl;
    }

    if (-1 == ber_flatten2(ber, &ctrl_val, 0)) {
        LDAPerr(LDAP_NO_MEMORY);
        goto endlbl;
    }

    res = Py_BuildValue("s#", ctrl_val.bv_val, ctrl_val.bv_len);

 endlbl:
    if (ber)
        ber_free(ber, 1);
    return res;
}


PyDoc_STRVAR(decode_rfc2696__doc__,
             "decode_page_control(control_value) -> (size, cookie)\n"
             "\n"
             "The parameter control_value is encoded as the result\n"
             " value of encode_page_control.");

static PyObject*
decode_rfc2696(PyObject *self, PyObject *args)
{
    PyObject *res = 0;
    BerElement *ber = 0;
    struct berval ldctl_value;
    ber_tag_t tag;
    struct berval *cookiep;
    unsigned long count;

    if (!PyArg_ParseTuple(args, "s#:decode_page_control",
                          &ldctl_value.bv_val, &ldctl_value.bv_len)) {
        goto endlbl;
    }

    if (!(ber = ber_init(&ldctl_value))) {
        LDAPerr(LDAP_NO_MEMORY);
        goto endlbl;
    }

    tag = ber_scanf(ber, "{iO", &count, &cookiep);
    if (tag == LBER_ERROR) {
        LDAPerr(LDAP_DECODING_ERROR);
        goto endlbl;
    }

    res = Py_BuildValue("(ls#)", count, cookiep->bv_val, cookiep->bv_len);

 endlbl:
    if (ber)
        ber_free(ber, 1);
    return res;
}


static PyMethodDef methods[] = {
    {"encode_page_control", encode_rfc2696, METH_VARARGS, encode_rfc2696__doc__},
    {"decode_page_control", decode_rfc2696, METH_VARARGS, decode_rfc2696__doc__},
    {0}
};

void
LDAPinit_control(PyObject *d)
{
    LDAPadd_methods(d, methods);
}


