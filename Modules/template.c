/* David Leonard <david.leonard@csee.uq.edu.au>, 2000. Public domain. */

/* 
 * DispTmplObject - wrapper around an LDAP Display Template (disptmpl)
 * $Id$
 */

#include "common.h"

#if defined(HAVE_LDAP_INIT_TEMPLATES)
#include "lber.h"
#include "ldap.h"
#include "disptmpl.h"
#include "linkedlist.h"
#include "template.h"

PyObject *DispTmpl_Error;
PyObject *DispTmpl_VersionError;
PyObject *DispTmpl_SyntaxError;

LinkedListType DispTmplSeq_Type;
LinkedListType DispTmplRowSeq_Type;
LinkedListType DispTmplColSeq_Type;

static PyObject *DispTmplSeq_new(struct ldap_disptmpl *);
static PyObject *DispTmplRowSeq_new(DispTmplObject *);
static PyObject *DispTmplColSeq_new(DispTmplRowSeqObject *,
	struct ldap_tmplitem *);
static PyObject *DispTmplItem_new(DispTmplObject *, struct ldap_tmplitem *);
static PyObject *DispTmpl_new(struct ldap_disptmpl *, DispTmplSeqObject *);

static PyObject *
makestring(s)
	char *s;
{
	if (s != NULL)
		return PyString_FromString(s);
	Py_INCREF(Py_None);
	return Py_None;
}

/*------------------------------------------------------------
 * DispTmplSeq: a sequence of templates
 */

static PyObject *
DispTmplSeq_new(tmpllist)
	struct ldap_disptmpl *tmpllist;
{
	DispTmplSeqObject *seq;
	struct ldap_disptmpl *t;
	struct ldap_tmplitem *r, *c;

	seq = (DispTmplSeqObject *)LinkedList_new(&DispTmplSeq_Type);
	seq->tmpllist = tmpllist;

	/* clear all the application data fields */
	for (t = ldap_first_disptmpl(tmpllist);
	     t;
	     t = ldap_next_disptmpl(tmpllist, t))
	{
		LDAP_SET_DISPTMPL_APPDATA(t, NULL);
		for (r = ldap_first_tmplrow(t);
		     r;
		     r = ldap_next_tmplrow(t, r))
			for (c = ldap_first_tmplcol(t, r);
			     c;
			     c = ldap_next_tmplcol(t, r, c))
				LDAP_SET_TMPLITEM_APPDATA(c, NULL);
	}

	return (PyObject *)seq;
}

/* Deallocate */
static void
DispTmplSeq_dealloc(self)
	DispTmplSeqObject *self;
{
	struct ldap_disptmpl *t;
	struct ldap_tmplitem *r, *c;

	/* Deallocate any application data */
	for (t = ldap_first_disptmpl(self->tmpllist);
	     t;
	     t = ldap_next_disptmpl(self->tmpllist, t))
	{
		Py_XDECREF(LDAP_GET_DISPTMPL_APPDATA(t, PyObject *));
		for (r = ldap_first_tmplrow(t);
		     r;
		     r = ldap_next_tmplrow(t, r))
			for (c = ldap_first_tmplcol(t, r);
			     c;
			     c = ldap_next_tmplcol(t, r, c))
				Py_XDECREF(LDAP_GET_TMPLITEM_APPDATA(c,
				    PyObject *));
	}

	ldap_free_templates(self->tmpllist);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_disptmpl *
DispTmplSeq_first(self)
	DispTmplSeqObject *self;
{
	return ldap_first_disptmpl(self->tmpllist);
}

/* next in list */
static struct ldap_disptmpl *
DispTmplSeq_next(self, tmpl)
	DispTmplSeqObject *self;
	struct ldap_disptmpl *tmpl;
{
	return ldap_next_disptmpl(self->tmpllist, tmpl);
}

/* create object from pointer into list */
static PyObject *
DispTmplSeq_item(self, tmpl)
	DispTmplSeqObject *self;
	struct ldap_disptmpl *tmpl;
{
	return DispTmpl_new(tmpl, self);
}

/* retrieve a template by name */
static PyObject *
DispTmplSeq_name2template(self, args)
	DispTmplSeqObject *self;
	PyObject *args;
{
	struct ldap_disptmpl *t;
	char *s;

	if (!PyArg_ParseTuple(args, "s", &s))
		return NULL;
	t = ldap_name2template(s, self->tmpllist);
	if (t == NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	return DispTmpl_new(t, self);
}
static char DispTmplSeq_name2template_doc[] =
"name2template(name) -> template\n"
"Do stuff.";

/* retrieve a template by objectClass */
static PyObject *
DispTmplSeq_oc2template(self, args)
	DispTmplSeqObject *self;
	PyObject *args;
{
	struct ldap_disptmpl *t;
	PyObject *seq, *o;
	char **strs;
	int len, i;

	if (!PyArg_ParseTuple(args, "O", &seq))
		return NULL;
	if (!PySequence_Check(seq)) {
		PyErr_SetString(PyExc_TypeError, "expected list of strings");
		return NULL;
	}
	len = PySequence_Length(seq);
	strs = (char **)malloc(sizeof (char *) * (len + 1));
	if (strs == NULL)
		return PyErr_NoMemory();

	for (i = 0; i < len; i++) {
		o = PySequence_GetItem(seq, i);
		if (!PyString_Check(o)) {
			PyErr_SetString(PyExc_TypeError, 
			    "expected list of strings");
			free(strs);
			return NULL;
		}
		strs[i] = PyString_AsString(o);
	}
	strs[len] = NULL;

	t = ldap_oc2template(strs, self->tmpllist);
	free(strs);
	if (t == NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	return DispTmpl_new(t, self);
}
static char DispTmplSeq_oc2template_doc[] =
"oc2template(list of strings) -> template\n"
"Do stuff.";

static PyMethodDef DispTmplSeq_methods[] = {
	{ "name2template", (PyCFunction)DispTmplSeq_name2template, 
	  METH_VARARGS, DispTmplSeq_name2template_doc },
	{ "oc2template", (PyCFunction)DispTmplSeq_oc2template, 
	  METH_VARARGS, DispTmplSeq_oc2template_doc },
	{ NULL, NULL }
};

PyObject *
DispTmplSeq_getattr(self, name)
	LinkedListObject *self;
	char *name;
{
	return Py_FindMethod(DispTmplSeq_methods, (PyObject *)self, name);
}


/*------------------------------------------------------------
 * DispTmplRowSeq: a sequence of rows
 */

/* new row sequence */
static PyObject *
DispTmplRowSeq_new(template)
	DispTmplObject *template;
{
	DispTmplRowSeqObject *rowseq;
	rowseq = (DispTmplRowSeqObject *)LinkedList_new(
		&DispTmplRowSeq_Type);
	rowseq->tmplobj = template;
	Py_INCREF(template);
	return (PyObject *)rowseq;
}

/* deallocate */
static void
DispTmplRowSeq_dealloc(self)
	DispTmplRowSeqObject *self;
{
	Py_DECREF(self->tmplobj);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_tmplitem *
DispTmplRowSeq_first(self)
	DispTmplRowSeqObject *self;
{
	return ldap_first_tmplrow(self->tmplobj->disptmpl);
}

/* next in list */
static struct ldap_tmplitem *
DispTmplRowSeq_next(self, row)
	DispTmplRowSeqObject *self;
	struct ldap_tmplitem *row;
{
	return ldap_next_tmplrow(self->tmplobj->disptmpl, row);
}

/* return a row (sequence of columns) */
static PyObject *
DispTmplRowSeq_item(self, cols)
	DispTmplRowSeqObject *self;
	struct ldap_tmplitem *cols;
{
	return DispTmplColSeq_new(self, cols);
}

/*------------------------------------------------------------
 * DispTmplColSeq: a sequence of columns
 */

/* new columns */
static PyObject *
DispTmplColSeq_new(rowseq, row)
	DispTmplRowSeqObject *rowseq;
	struct ldap_tmplitem *row;
{
	DispTmplColSeqObject *colseq;

	colseq = (DispTmplColSeqObject *)LinkedList_new(
		&DispTmplColSeq_Type);
	colseq->tmplobj = rowseq->tmplobj;
	Py_INCREF(colseq->tmplobj);
	colseq->row = row;
	return (PyObject *)colseq;
}

/* Deallocate */
static void
DispTmplColSeq_dealloc(self)
	DispTmplColSeqObject *self;
{
	Py_DECREF(self->tmplobj);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_tmplitem *
DispTmplColSeq_first(self)
	DispTmplColSeqObject *self;
{
	return ldap_first_tmplcol(self->tmplobj->disptmpl,
		self->row);
}

/* next in list */
static struct ldap_tmplitem *
DispTmplColSeq_next(self, col)
	DispTmplColSeqObject *self;
	struct ldap_tmplitem *col;
{
	return ldap_next_tmplcol(self->tmplobj->disptmpl,
		self->row, col);
}

/* extract item from current column */
static PyObject *
DispTmplColSeq_item(self, item)
	DispTmplColSeqObject *self;
	struct ldap_tmplitem *item;
{
	return DispTmplItem_new(self->tmplobj, item);
}

/*------------------------------------------------------------
 * template item
 */

static struct { long attr; char *name; PyObject *intern; } anam[] = {
	{ LDAP_DITEM_OPT_READONLY, "readonly" },
	{ LDAP_DITEM_OPT_SORTVALUES, "sortvalues" },
	{ LDAP_DITEM_OPT_SINGLEVALUED, "singlevalued" },
	{ LDAP_DITEM_OPT_VALUEREQUIRED, "valuerequired" },
	{ LDAP_DITEM_OPT_HIDEIFEMPTY, "hideifempty" },
	{ LDAP_DITEM_OPT_HIDEIFFALSE, "hideiffalse" },
};
static int nanam = sizeof anam / sizeof anam[0];

/* deallocate item */
static PyObject *
DispTmplItem_repr(self)
	DispTmplItemObject *self;
{
	char *label;
	char buf[1024];

	label = self->item->ti_label;
fprintf(stderr, "label=%p\n", label);
	if (label == NULL) 
		return PyString_FromString("<TemplateItem>");
	snprintf(buf, sizeof buf, "<TemplateItem %s>", label);
fprintf(stderr, "buf='%s'\n", buf);
	return PyString_FromString(buf);
}

/* deallocate item */
static void
DispTmplItem_dealloc(self)
	DispTmplItemObject *self;
{
	/* Note: appdata is released later */
	Py_DECREF(self->tmplobj);
	PyMem_DEL((PyObject *)self);
}

/* read an attribute */
static PyObject *
DispTmplItem_getattr(self, attr)
	DispTmplItemObject *self;
	char *attr;
{
	if (streq(attr, "__members__"))
		return Py_BuildValue("[ssssss]",
			"appdata", "attrname", "label", 
			"args", "options", "syntaxid");

	if (streq(attr, "appdata")) {
		PyObject *data;
		data = LDAP_GET_TMPLITEM_APPDATA(self->item, PyObject *);
		if (data == NULL)
			data = Py_None;
		Py_INCREF(data);
		return data;
	}
	if (streq(attr, "attrname")) 
		return makestring(self->item->ti_attrname);
	if (streq(attr, "label")) 
		return makestring(self->item->ti_label);
	if (streq(attr, "args")) {
		int i;
		PyObject *tuple;

		for (i = 0; self->item->ti_args[i]; i++)
			;
		tuple = PyTuple_New(i);
		for (i = 0; self->item->ti_args[i]; i++)
			PyTuple_SetItem(tuple, i, PyString_FromString(
				self->item->ti_args[i]));
		return tuple;
	}
	if (streq(attr, "options")) {

		int i, len;
		PyObject *tuple;

		for (len = i = 0; i < nanam; i++) 
		    if (LDAP_IS_TMPLITEM_OPTION_SET(self->item, anam[i].attr))
			len++;
		tuple = PyTuple_New(len);
		for (len = i = 0; i < nanam; i++) 
		    if (LDAP_IS_TMPLITEM_OPTION_SET(self->item, anam[i].attr)) {
			PyTuple_SetItem(tuple, len, anam[i].intern);
			Py_INCREF(anam[i].intern);
			len++;
		    }
		return tuple;
	}
	if (streq(attr, "syntaxid")) 
		return PyInt_FromLong(self->item->ti_syntaxid);

	PyErr_SetString(PyExc_AttributeError, attr);
	return NULL;
}

/* set an attribute */
static int
DispTmplItem_setattr(self, attr, value)
	DispTmplItemObject *self;
	char *attr;
	PyObject *value;
{
	if (streq(attr, "appdata")) {
		Py_XDECREF(LDAP_GET_TMPLITEM_APPDATA(self->item, PyObject *));
		LDAP_SET_TMPLITEM_APPDATA(self->item, value);
		Py_INCREF(value);
		return 0;
	}
	PyErr_SetString(PyExc_AttributeError, attr);
	return -1;
}

static PyTypeObject DispTmplItem_Type = {
#ifdef WIN32
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	sizeof(DispTmplItemObject),/*ob_size*/
	"DispTmplItem",		/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)DispTmplItem_dealloc,/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)DispTmplItem_getattr,	/*tp_getattr*/
	(setattrfunc)DispTmplItem_setattr,	/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)DispTmplItem_repr,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};

static PyObject *
DispTmplItem_new(tmplobj, item)
	DispTmplObject *tmplobj;
	struct ldap_tmplitem *item;
{
	DispTmplItemObject *obj;

	obj = PyObject_NEW(DispTmplItemObject, &DispTmplItem_Type);
	obj->tmplobj = tmplobj;
	Py_INCREF(tmplobj);
	obj->item = item;
	return (PyObject *)obj;
}

/*------------------------------------------------------------
 * Template
 */

/* deallocate item */
static void
DispTmpl_dealloc(self)
	DispTmplObject *self;
{
	/* Note: appdata is released later */
	Py_DECREF(self->tmplseqobj);
	PyMem_DEL((PyObject *)self);
}

static PyObject *
DispTmpl_tmplattrs(self, args)
	PyObject *self, *args;
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}
static char DispTmpl_tmplattrs_doc[] =
"tmplattrs() -> \n"
"Do stuff.";

static PyMethodDef DispTmpl_methods[] = {
	{ "tmplattrs", (PyCFunction)DispTmpl_tmplattrs, 
	  METH_VARARGS, DispTmpl_tmplattrs_doc },
	{ NULL, NULL }
};

static struct { long attr; char *name; PyObject *intern; } tnam[] = {
	{ LDAP_DTMPL_OPT_ADDABLE, "addable" },
	{ LDAP_DTMPL_OPT_ALLOWMODRDN, "allowmodrdn" },
	{ LDAP_DTMPL_OPT_ALTVIEW, "altview" },
};
static int ntnam = sizeof tnam / sizeof tnam[0];

/* get an attribute */
static PyObject *
DispTmpl_getattr(self, attr)
	DispTmplObject *self;
	char *attr;
{
	if (streq(attr, "__members__"))
		return Py_BuildValue("[sssssssssss]",
			"items", "appdata", "options", 
			"name", "pluralname", "iconname", 
			"authattrname", "defrdnattrname", "defaddlocation",
			"oclist", "adddeflist");
	if (streq(attr, "items"))
		return DispTmplRowSeq_new(self);
	if (streq(attr, "appdata")) {
		PyObject *data;
		data = LDAP_GET_DISPTMPL_APPDATA(self->disptmpl, PyObject *);
		if (data == NULL)
			data = Py_None;
		Py_INCREF(data);
		return data;
	}
	if (streq(attr, "options")) {
		int i, len;
		PyObject *tuple;

		for (len = i = 0; i < ntnam; i++) 
		    if (LDAP_IS_DISPTMPL_OPTION_SET(self->disptmpl, 
				tnam[i].attr))
			len++;
		tuple = PyTuple_New(len);
		for (len = i = 0; i < ntnam; i++) 
		    if (LDAP_IS_DISPTMPL_OPTION_SET(self->disptmpl,
				tnam[i].attr)) {
			PyTuple_SetItem(tuple, len, tnam[i].intern);
			Py_INCREF(tnam[i].intern);
			len++;
		    }
		return tuple;
	}
	if (streq(attr, "name")) 
		return makestring(self->disptmpl->dt_name);
	if (streq(attr, "pluralname")) 
		return makestring(self->disptmpl->dt_pluralname);
	if (streq(attr, "iconname")) 
		return makestring(self->disptmpl->dt_iconname);
	if (streq(attr, "authattrname")) 
		return makestring(self->disptmpl->dt_authattrname);
	if (streq(attr, "defrdnattrname")) 
		return makestring(self->disptmpl->dt_defrdnattrname);
	if (streq(attr, "defaddlocation")) 
		return makestring(self->disptmpl->dt_defaddlocation);
	if (streq(attr, "oclist")) {
		struct ldap_oclist *ocl = self->disptmpl->dt_oclist; 
		struct ldap_oclist *o;
		int i;
		PyObject *tuple;

		for (i = 0, o = ocl; o; i++, o = o->oc_next)
			i++;
		tuple = PyTuple_New(i);
		for (i = 0, o = ocl; o; i++, o = o->oc_next) {
			PyObject *names;
			int j;
			for (j = 0; o->oc_objclasses[j]; j++)
				;
			names = PyTuple_New(j);
			for (j = 0; o->oc_objclasses[j]; j++)
				PyTuple_SetItem(names, j, 
				    PyString_FromString(o->oc_objclasses[j]));
			PyTuple_SetItem(tuple, i, names);
		}
		return tuple;
	}
	if (streq(attr, "adddeflist")) {
	}
	return Py_FindMethod(DispTmpl_methods, (PyObject *)self, attr);
}

/* set an attribute */
static int
DispTmpl_setattr(self, attr, value)
	DispTmplObject *self;
	char *attr;
	PyObject *value;
{
	if (streq(attr, "appdata")) {
		Py_XDECREF(LDAP_GET_DISPTMPL_APPDATA(self->disptmpl, 
			PyObject *));
		LDAP_SET_DISPTMPL_APPDATA(self->disptmpl, value);
		Py_INCREF(value);
		return 0;
	}
	PyErr_SetString(PyExc_AttributeError, attr);
	return -1;
}

static PyTypeObject DispTmpl_Type = {
#ifdef WIN32
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	sizeof(DispTmplObject),	/*ob_size*/
	"DispTmpl",		/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)DispTmpl_dealloc,/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)DispTmpl_getattr,	/*tp_getattr*/
	(setattrfunc)DispTmpl_setattr,	/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)0,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};

static PyObject *
DispTmpl_new(disptmpl, tmplseq)
	struct ldap_disptmpl *disptmpl;
	DispTmplSeqObject *tmplseq;
{
	DispTmplObject *obj;

	obj = PyObject_NEW(DispTmplObject, &DispTmpl_Type);
	obj->tmplseqobj = tmplseq;
	Py_INCREF(tmplseq);
	obj->disptmpl = disptmpl;
	return (PyObject *)obj;
}

/*------------------------------------------------------------
 * module-level methods
 */

/* create a sequence of templates */
PyObject *
l_init_templates(self, args)
	PyObject *self, *args;
{
	struct ldap_disptmpl *tmpllist;
	PyObject *bufobj;
	const void *buf;
	int buflen;
	int err;

	if (!PyArg_ParseTuple(args, "O", &bufobj))
		return NULL;
#if defined(PY_MAJOR_VERSION) && PY_VERSION_HEX >= 0x01060000
	if (PyObject_AsReadBuffer(bufobj, &buf, &buflen) == -1)
		return NULL;
#else
	if (!PyString_Check(bufobj)) {
		PyErr_SetObject(PyExc_TypeError, bufobj);
		return NULL;
	}
	buf = PyString_AS_STRING(bufobj);
	buflen = PyString_GET_SIZE(bufobj);
#endif
	err = ldap_init_templates_buf((char *)buf, buflen, &tmpllist);

	switch (err) {
	case LDAP_TMPL_ERR_MEM:
		return PyErr_NoMemory();
	case 0:
		return DispTmplSeq_new(tmpllist);
	case LDAP_TMPL_ERR_SYNTAX:
		PyErr_SetNone(DispTmpl_VersionError);
		return NULL;
	case LDAP_TMPL_ERR_VERSION:
		PyErr_SetNone(DispTmpl_VersionError);
		return NULL;
	default:
		PyErr_SetString(PyExc_SystemError, 
		    "unexpected return value from ldap_init_templates_buf");
		return NULL;
	}
}
char l_init_templates_doc[] =
"init_templates_buf(buffer) -> templates\n"
"Do stuff.";

void 
LDAPinit_template(dict) 
	PyObject *dict;
{
	int i;

	LinkedList_inittype(&DispTmplSeq_Type, "DispTmplSeq",
		sizeof (DispTmplSeqObject), 
		(firstfunc)DispTmplSeq_first, 
		(nextfunc)DispTmplSeq_next, 
		(itemfunc)DispTmplSeq_item);
	DispTmplSeq_Type.llt_type.tp_dealloc = DispTmplSeq_dealloc;
	DispTmplSeq_Type.llt_type.tp_getattr = DispTmplSeq_getattr;

	LinkedList_inittype(&DispTmplRowSeq_Type, "DispTmplRowSeq",
		sizeof (DispTmplRowSeqObject), 
		(firstfunc)DispTmplRowSeq_first,
		(nextfunc)DispTmplRowSeq_next, 
		(itemfunc)DispTmplRowSeq_item);
	DispTmplRowSeq_Type.llt_type.tp_dealloc = DispTmplRowSeq_dealloc;

	LinkedList_inittype(&DispTmplColSeq_Type, "DispTmplColSeq",
		sizeof (DispTmplColSeqObject), 
		(firstfunc)DispTmplColSeq_first,
		(nextfunc)DispTmplColSeq_next, 
		(itemfunc)DispTmplColSeq_item);
	DispTmplColSeq_Type.llt_type.tp_dealloc = DispTmplColSeq_dealloc;

	DispTmpl_Error = PyErr_NewException("ldap.TemplateError", 
		NULL, NULL);
	PyDict_SetItemString(dict, "TemplateError", DispTmpl_Error);

	DispTmpl_VersionError = PyErr_NewException(
		"ldap.TemplateVersionError", DispTmpl_Error, NULL);
	PyDict_SetItemString(dict, "TemplateVersionError", 
		DispTmpl_VersionError);

	DispTmpl_SyntaxError = PyErr_NewException(
		"ldap.TemplateSyntaxError", DispTmpl_Error, NULL);
	PyDict_SetItemString(dict, "TemplateSyntaxError", 
		DispTmpl_SyntaxError);

	for (i = 0; i < nanam; i++)
		anam[i].intern = PyString_FromString(anam[i].name);
	for (i = 0; i < ntnam; i++)
		tnam[i].intern = PyString_FromString(tnam[i].name);

#define setval(n) PyDict_SetItemString(dict, #n, PyInt_FromLong(LDAP_##n))
	setval(SYN_TYPE_TEXT);
	setval(SYN_TYPE_IMAGE);
	setval(SYN_TYPE_BOOLEAN);
	setval(SYN_TYPE_BUTTON);
	setval(SYN_TYPE_ACTION);
	setval(SYN_OPT_DEFER);
	setval(SYN_CASEIGNORESTR);
	setval(SYN_MULTILINESTR);
	setval(SYN_DN);
	setval(SYN_BOOLEAN);
	setval(SYN_JPEGIMAGE);
	setval(SYN_JPEGBUTTON);
	setval(SYN_FAXIMAGE);
	setval(SYN_FAXBUTTON);
	setval(SYN_AUDIOBUTTON);
	setval(SYN_TIME);
	setval(SYN_DATE);
	setval(SYN_LABELEDURL);
	setval(SYN_SEARCHACTION);
	setval(SYN_LINKACTION);
	setval(SYN_ADDDNACTION);
	setval(SYN_VERIFYDNACTION);
	setval(SYN_RFC822ADDR);
}

#endif /* ! HAVE_LDAP_INIT_TEMPLATES */

/*
 * To Do:
 *	implement comparison between objects. someone is bound to
 *	want to compare two row/cell/template objects.
 */
