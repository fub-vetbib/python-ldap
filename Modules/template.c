/* David Leonard <david.leonard@csee.uq.edu.au>, 2000. Public domain. */

/* 
 * TemplateObject - wrapper around an LDAP Display Template (Template)
 * $Id$
 */

/*
 *  init_templates_buf(buffer) -> Templates
 *
 *  <Templates>.name2template(string)       -> Template
 *	       .oc2template(seq of strings) -> Template
 *	       .__getitem__(int)            -> Template
 *	       .__len__()                   -> int
 *
 *  <Template>.items	        -> Rows
 *	      .tmplattrs([sequence of strings, int ,int]) -> seq of strings
 *	      .appdata         <-> object
 *	      .options	        -> string tuple ('addable', ...)
 *	      .name             -> string
 *	      .pluralname       -> string
 *	      .iconname         -> string
 *	      .authattrname     -> string
 *	      .defrdnattrname   -> string
 *	      .defaddlocation   -> string
 *	      .oclist           -> tuple of tuple of string
 *	      .adddeflist       -> tuple of Default
 *
 *  <Rows>.__getitem__(int) -> Items
 *	  .__len__()        -> int
 *
 *  <Items>.__getitem__(int) -> Item
 *	   .__len__()        -> int
 *
 *  <Item>.appdata <-> object
 *	  .attrname -> string
 *	  .label    -> string
 *	  .args     -> tuple of string
 *	  .options  -> string tuple ('readonly', 'sortvalues', ...)
 *	  .syntaxid -> int
 *
 *  <Default>.attrname -> string
 *	     .value    -> string
 *	     .source   -> 'constantvalue' or 'addersdn'
 *
 *
 *  SYN_TYPE_TEXT  -> int
 *  SYN_TYPE_IMAGE -> int
 *  SYN_TYPE...    -> int
 *
 *  TemplateError -> base exception class
 *  TemplateVersionError -> exception class
 *  TemplateSyntaxError -> exception class
 */

#include "common.h"

#if defined(HAVE_LDAP_INIT_TEMPLATES)
#include "lber.h"
#include "ldap.h"
#if defined(HAVE_DISPTMPL_H)
#include "disptmpl.h"
#endif
#include "linkedlist.h"
#include "template.h"

PyObject *Template_Error;
PyObject *Template_VersionError;
PyObject *Template_SyntaxError;

LinkedListType Templates_Type;
LinkedListType TemplateRows_Type;
LinkedListType TemplateItems_Type;
LinkedListType TemplateDefList_Type;

static PyObject *Templates_new(struct ldap_disptmpl *);
static PyObject *TemplateRows_new(TemplateObject *);
static PyObject *TemplateItems_new(TemplateRowsObject *,
	struct ldap_tmplitem *);
static PyObject *TemplateItem_new(TemplateObject *, struct ldap_tmplitem *);
static PyObject *Template_new(struct ldap_disptmpl *, TemplatesObject *);
static PyObject *TemplateDefList_new(struct ldap_adddeflist *,
	TemplateObject *);
static PyObject *TemplateDefault_new(struct ldap_adddeflist *,
	TemplateObject *);

/* make a string object, or "" if NULL */
static PyObject *emptystring;

static PyObject *
makestring(s)
	char *s;
{
fprintf(stderr, "(makestring(%s))", s ? s : "(null)");
	if (s == NULL) {
		Py_INCREF(emptystring);
		return emptystring;
	}
	return PyString_FromString(s);
}

/*------------------------------------------------------------
 * Templates: a sequence of templates
 */

static PyObject *
Templates_new(disptmpls)
	struct ldap_disptmpl *disptmpls;
{
	TemplatesObject *templates;
	struct ldap_disptmpl *t;
	struct ldap_tmplitem *r, *c;

	templates = (TemplatesObject *)LinkedList_new(&Templates_Type);
	templates->disptmpls = disptmpls;

	/*
	 * clear all the application appdata fields, because
	 * we will use them as a cache for previously created 
	 * items and templates.
	 */
	for (t = ldap_first_disptmpl(disptmpls);
	     t;
	     t = ldap_next_disptmpl(disptmpls, t))
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

fprintf(stderr, "new Templates obj %d\n", (int)templates);
	return (PyObject *)templates;
}

/* Deallocate */
static void
Templates_dealloc(self)
	TemplatesObject *self;
{
fprintf(stderr, "dealloc Templates obj %d\n", (int)self);
	ldap_free_templates(self->disptmpls);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_disptmpl *
Templates_first(self)
	TemplatesObject *self;
{
	struct ldap_disptmpl *ret;

fprintf(stderr, "Templates_first(%p) -> ", self->disptmpls);
	ret = ldap_first_disptmpl(self->disptmpls);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* next in list */
static struct ldap_disptmpl *
Templates_next(self, tmpl)
	TemplatesObject *self;
	struct ldap_disptmpl *tmpl;
{
	struct ldap_disptmpl *ret;

fprintf(stderr, "Templates_next(%p, %p) -> ", self->disptmpls, tmpl);
	ret = ldap_next_disptmpl(self->disptmpls, tmpl);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* create object from pointer into list */
static PyObject *
Templates_item(self, tmpl)
	TemplatesObject *self;
	struct ldap_disptmpl *tmpl;
{
	PyObject *ret;

fprintf(stderr, "Templates_item(%p, obj %d) -> ", tmpl, (int)self);
	ret = Template_new(tmpl, self);
fprintf(stderr, "obj %d\n", (int)ret);
	return ret;
}

/* retrieve a template by name */
static PyObject *
Templates_name2template(self, args)
	TemplatesObject *self;
	PyObject *args;
{
	struct ldap_disptmpl *t;
	char *s;

	if (!PyArg_ParseTuple(args, "s:name2template", &s))
		return NULL;
	t = ldap_name2template(s, self->disptmpls);
	if (t == NULL) {
		/* XXX - should raise an exception? */
		Py_INCREF(Py_None);
		return Py_None;
	}
	return Template_new(t, self);
}
static char Templates_name2template_doc[] =
"name2template(name) -> template\n"
"Do stuff.";

/* retrieve a template by objectClass */
static PyObject *
Templates_oc2template(self, args)
	TemplatesObject *self;
	PyObject *args;
{
	struct ldap_disptmpl *t;
	PyObject *seq, *o;
	char **strs;
	int len, i;

	if (!PyArg_ParseTuple(args, "O:oc2template", &seq))
		return NULL;
	if (!PySequence_Check(seq)) {
		PyErr_SetString(PyExc_TypeError, "expected list of strings");
		return NULL;
	}
	len = PySequence_Length(seq);
	strs = PyMem_NEW(char *, len + 1);
	if (strs == NULL)
		return PyErr_NoMemory();

	for (i = 0; i < len; i++) {
		o = PySequence_GetItem(seq, i);
		if (!PyString_Check(o)) {
			PyErr_SetString(PyExc_TypeError, 
			    "expected list of strings");
			Py_DECREF(o);
			PyMem_DEL(strs);
			return NULL;
		}
		strs[i] = PyString_AsString(o);
		Py_DECREF(o);
	}
	strs[len] = NULL;

	t = ldap_oc2template(strs, self->disptmpls);
	PyMem_DEL(strs);
	if (t == NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	return Template_new(t, self);
}
static char Templates_oc2template_doc[] =
"oc2template(list of strings) -> template\n"
"Do stuff.";

static PyMethodDef Templates_methods[] = {
	{ "name2template", (PyCFunction)Templates_name2template, 
	  METH_VARARGS, Templates_name2template_doc },
	{ "oc2template", (PyCFunction)Templates_oc2template, 
	  METH_VARARGS, Templates_oc2template_doc },
	{ NULL, NULL }
};

PyObject *
Templates_getattr(self, name)
	LinkedListObject *self;
	char *name;
{
	return Py_FindMethod(Templates_methods, (PyObject *)self, name);
}


/*------------------------------------------------------------
 * TemplateRows: a sequence of rows
 */

/* new row sequence */
static PyObject *
TemplateRows_new(template)
	TemplateObject *template;
{
	TemplateRowsObject *rows;
	rows = (TemplateRowsObject *)LinkedList_new(&TemplateRows_Type);
	Py_INCREF(template);
	rows->template = template;
fprintf(stderr, "new Rows obj %d\n", (int)rows);
	return (PyObject *)rows;
}

/* deallocate */
static void
TemplateRows_dealloc(self)
	TemplateRowsObject *self;
{
fprintf(stderr, "dealloc Rows obj %d\n", (int)self);
	Py_DECREF(self->template);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_tmplitem *
TemplateRows_first(self)
	TemplateRowsObject *self;
{
	struct ldap_tmplitem *ret;

fprintf(stderr, "TemplateRows_first(%p) -> ", self->template->disptmpl);
	ret = ldap_first_tmplrow(self->template->disptmpl);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* next in list */
static struct ldap_tmplitem *
TemplateRows_next(self, row)
	TemplateRowsObject *self;
	struct ldap_tmplitem *row;
{
	struct ldap_tmplitem *ret;

fprintf(stderr, "TemplateRows_next(%p, %p) -> ", self->template->disptmpl, row);
	ret = ldap_next_tmplrow(self->template->disptmpl, row);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* return a row (sequence of columns) */
static PyObject *
TemplateRows_item(self, cols)
	TemplateRowsObject *self;
	struct ldap_tmplitem *cols;
{
	PyObject *ret;

fprintf(stderr, "TemplateRows_item(obj %d, %p) -> ", (int)self, cols);
	ret = TemplateItems_new(self, cols);
fprintf(stderr, "obj %d\n", (int)ret);
	return ret;
}

/*------------------------------------------------------------
 * TemplateItems: a sequence of columns
 */

/* new columns */
static PyObject *
TemplateItems_new(rows, row)
	TemplateRowsObject *rows;
	struct ldap_tmplitem *row;
{
	TemplateObject *template;
	TemplateItemsObject *items;

	items = (TemplateItemsObject *)LinkedList_new(
		&TemplateItems_Type);
	template = rows->template;
	Py_INCREF(template);
	items->template = template;
	items->row = row;
fprintf(stderr, "new Items obj %d\n", (int)items);
	return (PyObject *)items;
}

/* Deallocate */
static void
TemplateItems_dealloc(self)
	TemplateItemsObject *self;
{
fprintf(stderr, "dealloc Items obj %d\n", (int)self);
	Py_DECREF(self->template);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_tmplitem *
TemplateItems_first(self)
	TemplateItemsObject *self;
{
	struct ldap_tmplitem *ret;
fprintf(stderr, "TemplateItems_first(%p, %p) -> ", self->template->disptmpl,
						self->row);
	ret = ldap_first_tmplcol(self->template->disptmpl,
		self->row);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* next in list */
static struct ldap_tmplitem *
TemplateItems_next(self, col)
	TemplateItemsObject *self;
	struct ldap_tmplitem *col;
{
	struct ldap_tmplitem *ret;
fprintf(stderr, "TemplateItems_next(%p, %p, %p) -> ",
	self->template->disptmpl, self->row, col);
	ret = ldap_next_tmplcol(self->template->disptmpl,
		self->row, col);
fprintf(stderr, "%p\n", ret);
	return ret;
}

/* extract item from current column */
static PyObject *
TemplateItems_item(self, item)
	TemplateItemsObject *self;
	struct ldap_tmplitem *item;
{
	PyObject *ret;
fprintf(stderr, "TemplateItems_item(obj %d, %p) -> ", 
					(int)self->template, item);
	ret = TemplateItem_new(self->template, item);
fprintf(stderr, "obj %d\n", (int)ret);
	return ret;
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
TemplateItem_repr(self)
	TemplateItemObject *self;
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
TemplateItem_dealloc(self)
	TemplateItemObject *self;
{
fprintf(stderr, "dealloc Item obj %d", (int)self);
	LDAP_SET_TMPLITEM_APPDATA(self->item, NULL);
fprintf(stderr, ".");
	Py_DECREF(self->template);
fprintf(stderr, "[appdata=%p]", self->appdata);
	Py_XDECREF(self->appdata);
fprintf(stderr, ".");
	PyMem_DEL((PyObject *)self);
fprintf(stderr, "!\n");
}

/* read an attribute */
static PyObject *
TemplateItem_getattr(self, attr)
	TemplateItemObject *self;
	char *attr;
{
	if (streq(attr, "__members__"))
		return Py_BuildValue("[ssssss]",
			"appdata", "attrname", "label", 
			"args", "options", "syntaxid");

	if (streq(attr, "appdata")) {
		PyObject *data;
		data = self->appdata;
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
		int i, len;
		PyObject *tuple;

		for (len = 0; self->item->ti_args[len]; len++)
			;
		tuple = PyTuple_New(len);
		if (tuple == NULL)
			return NULL;
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
		if (tuple == NULL)
			return NULL;
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
TemplateItem_setattr(self, attr, value)
	TemplateItemObject *self;
	char *attr;
	PyObject *value;
{
	if (streq(attr, "appdata")) {
		Py_INCREF(value);
		Py_XDECREF(self->appdata);
		self->appdata = value;
		return 0;
	}
	PyErr_SetString(PyExc_AttributeError, attr);
	return -1;
}

static PyTypeObject TemplateItem_Type = {
#ifdef WIN32
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	sizeof(TemplateItemObject),/*ob_size*/
	"TemplateItem",		/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)TemplateItem_dealloc,/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)TemplateItem_getattr,	/*tp_getattr*/
	(setattrfunc)TemplateItem_setattr,	/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)TemplateItem_repr,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};

static PyObject *
TemplateItem_new(template, item)
	TemplateObject *template;
	struct ldap_tmplitem *item;
{
	TemplateItemObject *obj;

	obj = LDAP_GET_TMPLITEM_APPDATA(item, TemplateItemObject *);
	if (obj != NULL) {
		Py_INCREF(obj);
fprintf(stderr, "REUSE Item obj %d\n", (int)obj);
	} else {
		obj = PyObject_NEW(TemplateItemObject, &TemplateItem_Type);
		Py_INCREF(template);
		obj->template = template;
		obj->item = item;
		obj->appdata = NULL;
		LDAP_SET_TMPLITEM_APPDATA(item, obj);
fprintf(stderr, "new Item obj %d\n", (int)obj);
	}
fprintf(stderr, "[Item.appdata = %p (@%p)]\n", obj->appdata, &obj->appdata);
	return (PyObject *)obj;
}

/*------------------------------------------------------------
 * List of defaults
 */

/* new columns */
static PyObject *
TemplateDefList_new(adddeflist, template)
	struct ldap_adddeflist *adddeflist;
	TemplateObject *template;
{
	TemplateDefListObject *deflist;

	deflist = (TemplateDefListObject *)LinkedList_new(
		&TemplateDefList_Type);
	Py_INCREF(template);
	deflist->template = template;
	deflist->def = adddeflist;
fprintf(stderr, "new DefList obj %d\n", (int)deflist);
	return (PyObject *)deflist;
}

/* Deallocate */
static void
TemplateDefList_dealloc(self)
	TemplateDefListObject *self;
{
fprintf(stderr, "dealloc DefList obj %d\n", (int)self);
	Py_DECREF(self->template);
	PyMem_DEL((PyObject *)self);
}

/* first in list */
static struct ldap_adddeflist *
TemplateDefList_first(self)
	TemplateDefListObject *self;
{
	return self->def;
}

/* next in list */
static struct ldap_adddeflist *
TemplateDefList_next(self, pos)
	TemplateDefListObject *self;
	struct ldap_adddeflist *pos;
{
	return pos->ad_next;
}

/* extract item from current position */
static PyObject *
TemplateDefList_item(self, pos)
	TemplateDefListObject *self;
	struct ldap_adddeflist *pos;
{
	return TemplateDefault_new(pos, self->template);
}

/*------------------------------------------------------------
 * Default element
 */

static struct { char *name; int val; PyObject *intern; } dnam[] = {
	{ "constantvalue",	LDAP_ADSRC_CONSTANTVALUE },
	{ "addersdn",		LDAP_ADSRC_ADDERSDN },
};
static int ndnam = sizeof dnam / sizeof dnam[0];

static void
TemplateDefault_dealloc(self)
	TemplateDefaultObject *self;
{
	Py_DECREF(self->template);
	PyMem_DEL(self);
}

/* read an attribute */
static PyObject *
TemplateDefault_getattr(self, attr)
	TemplateDefaultObject *self;
	char *attr;
{
	int i;

fprintf(stderr, "TemplateDefault_getattr(obj %d, %s) def=%p\n", 
				(int)self, attr, self->def);
	if (streq(attr, "__members__"))
		return Py_BuildValue("[sss]", "source", "attrname", "value");
	if (streq(attr, "source")) {
		for (i = 0; i < ndnam; i++)
			if (dnam[i].val == self->def->ad_source) {
				Py_INCREF(dnam[i].intern);
				return dnam[i].intern;
			}
		/* unknown source? */
		/* XXX should raise exception */
		return PyString_FromString("?");
		/* return PyInt_FromLong(self->def->ad_source); */
	}
	if (streq(attr, "attrname"))
		return makestring(self->def->ad_attrname);
	if (streq(attr, "value"))
		return makestring(self->def->ad_value);
	PyErr_SetString(PyExc_AttributeError, attr);
	return NULL;
}

static PyObject *
TemplateDefault_repr(self)
	PyObject *self;
{
	PyObject *s;

fprintf(stderr, "TemplateDefault_repr obj %d", (int)self);
	s = PyString_FromString("<Default attrname=");
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyObject_GetAttrString(self, "attrname"));
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyString_FromString(" value="));
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyObject_GetAttrString(self, "value"));
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyString_FromString(" source="));
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyObject_GetAttrString(self, "source"));
fprintf(stderr, ".");
	PyString_ConcatAndDel(&s, PyString_FromString(">"));
fprintf(stderr, "TemplateDefault_repr RETURN obj %d\n", (int)s);
	return s;
}

static PyTypeObject TemplateDefault_Type = {
#ifdef WIN32
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	sizeof(TemplateDefaultObject),	/*ob_size*/
	"TemplateDefault",	/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)TemplateDefault_dealloc,/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)TemplateDefault_getattr,	/*tp_getattr*/
	(setattrfunc)0,		/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)TemplateDefault_repr,	/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};

static PyObject *
TemplateDefault_new(deflist, template)
	struct ldap_adddeflist *deflist;
	TemplateObject *template;
{
	TemplateDefaultObject *obj;

	obj = PyObject_NEW(TemplateDefaultObject, &TemplateDefault_Type);
	Py_INCREF(template);
	obj->template = template;
	obj->def = deflist;
	return (PyObject *)obj;
}

/*------------------------------------------------------------
 * Template
 */

/* deallocate item */
static void
Template_dealloc(self)
	TemplateObject *self;
{
fprintf(stderr, "dealloc Template obj %d\n", (int)self);
	LDAP_SET_DISPTMPL_APPDATA(self->disptmpl, NULL);
	Py_XDECREF(self->appdata);
	Py_DECREF(self->templates);
	PyMem_DEL((PyObject *)self);
}

static PyObject *
Template_tmplattrs(self, args)
	PyObject *self, *args;
{
	PyErr_SetNone(PyExc_NotImplementedError);
	return NULL;
}
static char Template_tmplattrs_doc[] =
"tmplattrs() -> \n"
"Do stuff.";

static PyMethodDef Template_methods[] = {
	{ "tmplattrs", (PyCFunction)Template_tmplattrs, 
	  METH_VARARGS, Template_tmplattrs_doc },
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
Template_getattr(self, attr)
	TemplateObject *self;
	char *attr;
{
	if (streq(attr, "__members__"))
		return Py_BuildValue("[sssssssssss]",
			"items", "appdata", "options", 
			"name", "pluralname", "iconname", 
			"authattrname", "defrdnattrname", "defaddlocation",
			"oclist", "adddeflist");
	if (streq(attr, "items"))
		return TemplateRows_new(self);
	if (streq(attr, "appdata")) {
		PyObject *data;
		data = self->appdata;
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
		if (tuple == NULL)
			return NULL;
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
		int i, len;
		PyObject *tuple;

		len = 0;
		for (o = ocl; o != NULL; o = o->oc_next)
			len++;
		tuple = PyTuple_New(len);
		if (tuple == NULL)
			return NULL;
		for (i = 0, o = ocl; o != NULL; i++, o = o->oc_next) {
			PyObject *names;
			int j;
			for (j = 0; o->oc_objclasses[j]; j++)
				;
			names = PyTuple_New(j);
			if (names == NULL) {
				Py_DECREF(tuple);
				return NULL;
			}
			for (j = 0; o->oc_objclasses[j]; j++)
				PyTuple_SetItem(names, j, 
				    PyString_FromString(o->oc_objclasses[j]));
			PyTuple_SetItem(tuple, i, names);
		}
		return tuple;
	}
	if (streq(attr, "adddeflist"))
		return TemplateDefList_new(self->disptmpl->dt_adddeflist,
			self);
	return Py_FindMethod(Template_methods, (PyObject *)self, attr);
}

/* set an attribute */
static int
Template_setattr(self, attr, value)
	TemplateObject *self;
	char *attr;
	PyObject *value;
{
	if (streq(attr, "appdata")) {
		Py_XDECREF(self->appdata);
		Py_INCREF(value);
		self->appdata = value;
		return 0;
	}
	PyErr_SetString(PyExc_AttributeError, attr);
	return -1;
}

static PyTypeObject Template_Type = {
#ifdef WIN32
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	sizeof(TemplateObject),	/*ob_size*/
	"Template",		/*tp_name*/
	0,			/*tp_basicsize*/
	0,			/*tp_itemsize*/
	/* methods */
	(destructor)Template_dealloc,/*tp_dealloc*/
	0,			/*tp_print*/
	(getattrfunc)Template_getattr,	/*tp_getattr*/
	(setattrfunc)Template_setattr,	/*tp_setattr*/
	0,			/*tp_compare*/
	(reprfunc)0,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,			/*tp_as_sequence*/
	0,			/*tp_as_mapping*/
	0,			/*tp_hash*/
};

static PyObject *
Template_new(disptmpl, templates)
	struct ldap_disptmpl *disptmpl;
	TemplatesObject *templates;
{
	TemplateObject *obj;

	obj = LDAP_GET_DISPTMPL_APPDATA(disptmpl, TemplateObject *);
	if (obj != NULL) {
		Py_INCREF(obj);
fprintf(stderr, "REUSE Template obj %d\n", (int)obj);
	} else {
		obj = PyObject_NEW(TemplateObject, &Template_Type);
		Py_INCREF(templates);
		obj->templates = templates;
		obj->disptmpl = disptmpl;
		obj->appdata = NULL;
		LDAP_SET_DISPTMPL_APPDATA(disptmpl, obj);
fprintf(stderr, "new Template obj %d\n", (int)obj);
	}
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
	struct ldap_disptmpl *disptmpls;
	PyObject *bufobj;
	const void *buf;
	int buflen;
	int err;

	if (!PyArg_ParseTuple(args, "O:init_templates", &bufobj))
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

	err = ldap_init_templates_buf((char *)buf, buflen, &disptmpls);

	switch (err) {
	case LDAP_TMPL_ERR_MEM:
		return PyErr_NoMemory();
	case 0:
		return Templates_new(disptmpls);
	case LDAP_TMPL_ERR_SYNTAX:
		PyErr_SetNone(Template_VersionError);
		return NULL;
	case LDAP_TMPL_ERR_VERSION:
		PyErr_SetNone(Template_VersionError);
		return NULL;
	default:
		PyErr_SetString(PyExc_SystemError, 
		    "unexpected return value from ldap_init_tmpllist_buf");
		return NULL;
	}
}
char l_init_templates_doc[] =
"init_templates_buf(buffer) -> templates\n"
"\n"
"Reads a sequence of templates from the given string/buffer.\n"
"See ldaptemplates.conf(5).\n";

void 
LDAPinit_template(dict) 
	PyObject *dict;
{
	int i;

	LinkedList_inittype(&Templates_Type, "Templates",
		sizeof (TemplatesObject), 
		(firstfunc)Templates_first, 
		(nextfunc)Templates_next, 
		(itemfunc)Templates_item,
		(destructor)Templates_dealloc);
	Templates_Type.llt_type.tp_getattr = Templates_getattr;

	LinkedList_inittype(&TemplateRows_Type, "TemplateRows",
		sizeof (TemplateRowsObject), 
		(firstfunc)TemplateRows_first,
		(nextfunc)TemplateRows_next, 
		(itemfunc)TemplateRows_item,
		(destructor)TemplateRows_dealloc);

	LinkedList_inittype(&TemplateItems_Type, "TemplateItems",
		sizeof (TemplateItemsObject), 
		(firstfunc)TemplateItems_first,
		(nextfunc)TemplateItems_next, 
		(itemfunc)TemplateItems_item,
		(destructor)TemplateItems_dealloc);

	LinkedList_inittype(&TemplateDefList_Type, "TemplateDefList",
		sizeof (TemplateDefListObject), 
		(firstfunc)TemplateDefList_first,
		(nextfunc)TemplateDefList_next, 
		(itemfunc)TemplateDefList_item,
		(destructor)TemplateDefList_dealloc);

	Template_Error = PyErr_NewException("ldap.TemplateError", 
		NULL, NULL);
	PyDict_SetItemString(dict, "TemplateError", Template_Error);

	Template_VersionError = PyErr_NewException(
		"ldap.TemplateVersionError", Template_Error, NULL);
	PyDict_SetItemString(dict, "TemplateVersionError", 
		Template_VersionError);

	Template_SyntaxError = PyErr_NewException(
		"ldap.TemplateSyntaxError", Template_Error, NULL);
	PyDict_SetItemString(dict, "TemplateSyntaxError", 
		Template_SyntaxError);

	emptystring = PyString_InternFromString("");
	for (i = 0; i < nanam; i++)
		anam[i].intern = PyString_InternFromString(anam[i].name);
	for (i = 0; i < ntnam; i++)
		tnam[i].intern = PyString_InternFromString(tnam[i].name);
	for (i = 0; i < ndnam; i++)
		dnam[i].intern = PyString_InternFromString(dnam[i].name);

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
