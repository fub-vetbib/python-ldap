/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* $Id$ */

/*
 * read-only linked list type template.
 * These utility functions construct python object types that provide
 * a sequence interface to a linked list in C. Three C functions are
 * provided to the template: first, next, and item. The first two manipulate
 * pointers, while the third generate a python object from a C pointer.
 * All pointers are void *.
 */

#include "common.h"
#include "linkedlist.h"

#define LINKCLASS(obj)		\
	((LinkedListType *)((obj)->ob_type))
#define FIRST(obj)		\
	(*LINKCLASS(obj)->llt_firstfn)((obj))
#define NEXT(obj, pos)		\
	(*LINKCLASS(obj)->llt_nextfn)((obj), pos)
#define ITEM(obj, pos)		\
	(*LINKCLASS(obj)->llt_itemfn)((obj), pos)

/*
 * Create a new instance of the linked list. The caller should keep
 * the head pointer somewhere for when FIRST() is called later.
 */
PyObject *
LinkedList_new(type)
	LinkedListType *type;
{
	return (PyObject *)PyObject_NEW(LinkedListObject, &type->llt_type);
}

/* Dodgy representation: much of this from listobject.c */
static PyObject *
repr(obj)
	PyObject *obj;
{
	LinkedListObject *self = (LinkedListObject *)obj;
	PyObject *s, *comma, *itm;
	void *pos;
	int i;

	i = Py_ReprEnter((PyObject *)self);
	if (i != 0) {
		if (i > 0)
			return PyString_FromString("<...>");
		return NULL;
	}
	s = PyString_FromString("<");
	comma = PyString_FromString(", ");
	for (i = 0, pos = FIRST(self); pos; pos = NEXT(self, pos), i++) {
		if (i > 0)
			PyString_Concat(&s, comma);
		itm = ITEM(self, pos);
		PyString_ConcatAndDel(&s, PyObject_Repr(itm));
	}
	Py_XDECREF(comma);
	PyString_ConcatAndDel(&s, PyString_FromString(">"));
	Py_ReprLeave((PyObject *)self);
	return s;
}

/* Inefficiently find the length of the list */
static PyObject *
length(obj)
	PyObject *obj;
{
	LinkedListObject *self = (LinkedListObject *)obj;
	int len;
	void *pos;

	len = 0;
	for (pos = FIRST(self); pos != NULL; pos = NEXT(self, pos))
		len++;
	return PyInt_FromLong(len);
}

/* Inefficiently access an item in the list */
static PyObject *
item(obj, index)
	PyObject *obj;
	int index;
{
	LinkedListObject *self = (LinkedListObject *)obj;
	void *pos;

	pos = FIRST(self);
	while (pos && index) {
		pos = NEXT(self, pos);
		index--;
	}
	if (pos && index == 0)
		return ITEM(self, pos);

	PyErr_SetObject(PyExc_IndexError, PyInt_FromLong(index));
	return NULL;
}


static PySequenceMethods default_methods = {
        (inquiry)length,	/* sq_length */
        (binaryfunc)0,		/* sq_concat */
        (intargfunc)0,		/* sq_repeat */
        (intargfunc)item,	/* sq_item */
        (intintargfunc)0,	/* sq_slice */
        (intobjargproc)0,	/* sq_ass_item */
        (intintobjargproc)0,	/* sq_ass_slice */
};

static PyTypeObject default_type = {
#if defined(WIN32) || defined(__CYGWIN__)
	/* see http://www.python.org/doc/FAQ.html#3.24 */
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	0,			/*ob_size*/
	0,			/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)0,		/*tp_dealloc*/
	0,			/*tp_print*/
	0,			/*tp_getattr*/
	0,			/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)repr,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};	

/*
 * Create a new linked-list object type.
 * Caller must set tp_dealloc.
 */
void
LinkedList_inittype(type, name, size, firstfn, nextfn, itemfn, dealloc)
	LinkedListType *type;
	char *name;
	size_t size;
	firstfunc firstfn;
	nextfunc nextfn;
	itemfunc itemfn;
	destructor dealloc;
{
	memcpy(&type->llt_type, &default_type, sizeof type->llt_type);
	memcpy(&type->llt_sequence, &default_methods, 
	    sizeof type->llt_sequence);
	type->llt_firstfn = firstfn;
	type->llt_nextfn = nextfn;
	type->llt_itemfn = itemfn;
	type->llt_type.tp_as_sequence = &type->llt_sequence;
	type->llt_type.ob_size = size;
	type->llt_type.tp_dealloc = dealloc;
}
