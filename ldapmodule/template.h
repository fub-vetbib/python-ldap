/* David Leonard <david.leonard@csee.uq.edu.au>, 2000. Public domain. */
#ifndef __h_TemplateObject 
#define __h_TemplateObject 

/* $Id$ */

#if defined(HAVE_LDAP_INIT_TEMPLATES)

typedef struct {
	PyObject_HEAD
	struct ldap_disptmpl	*tmpllist;
} DispTmplSeqObject;

typedef struct {
	PyObject_HEAD
	DispTmplSeqObject	*tmplseqobj;
	struct ldap_disptmpl	*disptmpl;
} DispTmplObject;

typedef struct {
	PyObject_HEAD
	DispTmplObject		*tmplobj;
} DispTmplRowSeqObject;

typedef struct {
	PyObject_HEAD
	DispTmplObject		*tmplobj;
	struct ldap_tmplitem	*row;
} DispTmplColSeqObject;

typedef struct {
	PyObject_HEAD
	DispTmplObject *tmplobj;
	struct ldap_tmplitem *item;
} DispTmplItemObject;

void LDAPinit_template(PyObject *);
PyObject *l_init_templates(PyObject *, PyObject *);
extern char l_init_templates_doc[];

#endif /* HAVE_LDAP_INIT_TEMPLATES */

#endif /* __h_TemplateObject */

