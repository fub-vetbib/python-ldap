/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/*	$Id$	*/

#include "common.h"
#ifdef USE_CIDICT
#include "CIDict.h"

/*
 * Case Insensitive dictionary
 *
 * e.g:
 *	>>> foo['Bar'] = 123
 *	>>> print foo['baR']
 *	123
 *
 * This dictionary can be used to hold the replies returned by
 * case-insensitive X.500 directory services, without the
 * caller having to know what case it has converted everything to.
 *
 * XXX I forget whose idea this originally was, but its a good one. - d
 */

typedef struct {
	PyObject_HEAD
	PyObject *dict;
} CIDictObject;

/*
 * Return a new object representing a lowercased version of the argument.
 * Typically this is a string -> string conversion.
 * Returns: New Reference
 */
static PyObject *
lowercase(PyObject *o)
{
	char *str, *cp;
	int len, i;
	PyObject *s;

	if (o == NULL)
		return NULL;

	if (!PyString_Check(o)) {
		Py_INCREF(o);
		return o;
	}

	str = PyString_AS_STRING(o);
	len = PyString_GET_SIZE(o);
	cp = PyMem_NEW(char, len);
	if (cp == NULL)
		return PyErr_NoMemory();
	for (i = 0; i < len; i++)
		cp[i] = tolower(str[i]);
	s = PyString_FromString(cp);
	PyMem_DEL(cp);
	return s;
}

/* Access an element of the dictionary by key */
static PyObject *
subscript(CIDictObject *self, PyObject *k)
{
	PyObject *ret;
	PyObject *cik;

	cik = lowercase(k);
	if (cik == NULL)
		return NULL;
	ret = PyObject_GetItem(self->dict, cik);
	Py_DECREF(cik);
	return ret;
}

/* Return the length of the dictionary */
static int
length(CIDictObject *self)
{
	return PyMapping_Length(self->dict);
}

/* Assign to an element of the dictionary by key */
static int
ass_subscript(CIDictObject *self, PyObject *k, PyObject *v)
{
	int ret;
	PyObject *cik;

	cik = lowercase(k);
	if (cik == NULL)
		return -1;
	ret = PyObject_SetItem(self->dict, cik, v);
	Py_DECREF(cik);
	return ret;
}

/* Release storage associated with the dictionary */
static void
dealloc(CIDictObject *self)
{
	Py_DECREF(self->dict);
	PyMem_DEL(self);
}

/* Print the dictionary */
static int
print(CIDictObject *self, FILE *fp, int flags)
{
	return PyObject_Print(self->dict, fp, flags);
}

/* Retreive attributes from the dictionary */
PyObject *
getattr(CIDictObject *self, char *attr_name)
{
	return PyObject_GetAttr(self->dict, attr_name);
}

/* Compare two dictionaries for (in)equality */
static int
compare(CIDictObject *self, PyObject *o)
{
	PyObject *lo = NULL;
	PyObject *oitems = NULL;
	PyObject *key = NULL;
	PyObject *item = NULL;
	int len, i, ret = -1;

	if (!PyMapping_Check(o))
		return PyObject_Compare(self->dict, o);

	/* Create equivalent dictionary with lowercased keys */
	if ((lo = PyDict_New()) == NULL)
		goto done;
	if ((oitems = PyMapping_Items(o)) == NULL)
		goto done;
	len = PyObject_Length(oitems);
	for (i = 0; i < len; i++) {
		Py_XDECREF(item);
		if ((item = PySequence_GetItem(oitems, i)) == NULL)
			goto done;
		Py_XDECREF(key);
		if ((key = lowercase(PyTuple_GET_ITEM(item, 0))) == NULL)
			goto done;
		PyMapping_SetItem(key, PyTuple_GET_ITEM(item, 1));
	}
	ret = PyObject_Compare(self->dict, lo);
    done:
	Py_XDECREF(key);
	Py_XDECREF(item);
	Py_XDECREF(oitems);
	Py_XDECREF(lo);
	return ret;
}

/* Return a string representation of the dictionary */
static PyObject *
repr(CIDictObject *self)
{
	return PyObject_Repr(self->dict);
}

/* Mapping interface */
static PyMappingMethods as_mapping = { 
	length, 			/* mp_length */
	subscript, 			/* mp_subscript */
	ass_subscript			/* mp_ass_subscript */
};

/* Python object interface */
PyTypeObject CIDict_Type = {
#if defined(WIN32) || defined(__CYGWIN__)
	/* see http://www.python.org/doc/FAQ.html#3.24 */
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	"cidictionary",			/* tp_name */
	sizeof (CIDictObject),		/* tp_basicsize */
	0,				/* tp_itemsize */
	(destructor)dealloc,		/* tp_dealloc */
	(printfunc)print,		/* tp_print */
	(getattrfunc)getattr,		/* tp_getattr */
	NULL,				/* tp_setattr */
	(cmpfunc)compare,		/* tp_compare */
	(reprfunc)repr,			/* tp_repr */
	NULL,				/* tp_as_number */
	NULL,				/* tp_as_sequence */
	&as_mapping,			/* tp_as_mapping */
};

/* Create a new case-insensitive dictionary, based on PyDict */
PyObject *
CIDict_New()
{
	CIDictObject *o;
	PyObject *dict;

	dict = PyDict_New();
	if (dict == NULL)
		return NULL;
#if defined(WIN32) || defined(__CYGWIN__)
	CIDict_Type.ob_type = &PyType_Type
#endif
	o = PyObject_NEW(CIDictObject, &CIDict_Type);
	if (o == NULL) 
		Py_DECREF(dict);
	else
		o->dict = dict;
	return o;
}

#endif /* USE_CIDICT */
