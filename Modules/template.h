/* David Leonard <david.leonard@csee.uq.edu.au>, 2000. Public domain. */
#ifndef __h_TemplateObject 
#define __h_TemplateObject 

/* $Id$ */

#if defined(HAVE_LDAP_INIT_TEMPLATES)

typedef struct {
	PyObject_HEAD
	struct ldap_disptmpl	*disptmpls;
} TemplatesObject;

typedef struct {
	PyObject_HEAD
	TemplatesObject		*templates;
	struct ldap_disptmpl	*disptmpl;
	PyObject		*appdata;
} TemplateObject;

typedef struct {
	PyObject_HEAD
	TemplateObject		*template;
} TemplateRowsObject;

typedef struct {
	PyObject_HEAD
	TemplateObject		*template;
	struct ldap_tmplitem	*row;
} TemplateItemsObject;

typedef struct {
	PyObject_HEAD
	TemplateObject 		*template;
	PyObject 		*appdata;
	struct ldap_tmplitem 	*item;
} TemplateItemObject;

typedef struct {
	PyObject_HEAD
	TemplateObject		*template;
	struct ldap_adddeflist	*def;
} TemplateDefListObject;

typedef struct {
	PyObject_HEAD
	TemplateObject		*template;
	struct ldap_adddeflist	*def;
} TemplateDefaultObject;

void LDAPinit_template(PyObject *);
PyObject *l_init_templates(PyObject *, PyObject *);
extern char l_init_templates_doc[];

#endif /* HAVE_LDAP_INIT_TEMPLATES */

#endif /* __h_TemplateObject */

