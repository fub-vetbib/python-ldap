/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/* $Id$ */

/* read-only linked list type template. */

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

PyObject *
LinkedList_new(type)
	LinkedListType *type;
{
	return (PyObject *)PyObject_NEW(LinkedListObject, &type->llt_type);
}

static void
dealloc(self)
	PyObject *self;
{
	PyMem_DEL(self);
}

/* Much of this from listobject.c */
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
			return PyString_FromString("[...]");
		return NULL;
	}
	s = PyString_FromString("[");
	comma = PyString_FromString(", ");
	for (i = 0, pos = FIRST(self); pos; pos = NEXT(self, pos), i++) {
		if (i > 0)
			PyString_Concat(&s, comma);
		itm = ITEM(self, pos);
		PyString_ConcatAndDel(&s, PyObject_Repr(itm));
	}
	Py_XDECREF(comma);
	PyString_ConcatAndDel(&s, PyString_FromString("]"));
	Py_ReprLeave((PyObject *)self);
	return s;
}

static PyObject *
length(obj)
	PyObject *obj;
{
	LinkedListObject *self = (LinkedListObject *)obj;
	int len;
	void *pos;

	for (len = 0, pos = FIRST(self); pos; pos = NEXT(self, pos), len++)
		;

	return PyInt_FromLong(len);
}

static PyObject *
item(obj, index)
	PyObject *obj;
	int index;
{
	LinkedListObject *self = (LinkedListObject *)obj;
	int len;
	void *pos;

	for (len = 0, pos = FIRST(self);
	    pos && len < index; 
	    pos = NEXT(self, pos), len++)
		;

	if (len == index)
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
        (objobjproc)0		/* sq_contains */
};

static PyTypeObject default_type = {
#ifdef WIN32
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
	(destructor)dealloc,	/*tp_dealloc*/
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

void
LinkedList_inittype(type, name, size, firstfn, nextfn, itemfn)
	LinkedListType *type;
	char *name;
	size_t size;
	firstfunc firstfn;
	nextfunc nextfn;
	itemfunc itemfn;
{

	memcpy(&type->llt_type, &default_type, sizeof type->llt_type);
	memcpy(&type->llt_sequence, &default_methods, 
	    sizeof type->llt_sequence);
	type->llt_firstfn = firstfn;
	type->llt_nextfn = nextfn;
	type->llt_itemfn = itemfn;
	type->llt_type.tp_as_sequence = &type->llt_sequence;
	type->llt_type.ob_size = size;
}
