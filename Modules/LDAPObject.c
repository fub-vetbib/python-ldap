/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */

/* 
 * LDAPObject - wrapper around an LDAP* context
 * $Id$
 */

#include <math.h>
#include <limits.h>
#include "common.h"
#include "errors.h"
#include "constants.h"
#include "LDAPObject.h"
#include "message.h"
#include "options.h"

static void free_attrs(char***);

/* constructor */

LDAPObject*
newLDAPObject( LDAP* l ) 
{
    LDAPObject* self = (LDAPObject*) PyObject_NEW(LDAPObject, &LDAP_Type);
    if (self == NULL) 
    	return NULL;
    self->ldap = l;
    self->_save = NULL;
    self->valid = 1;
    return self;
}

/* destructor */

static void
dealloc( LDAPObject* self )
{
    if (self->ldap) {
	if (self->valid) {
	    LDAP_BEGIN_ALLOW_THREADS( self );
	    ldap_unbind( self->ldap );
	    LDAP_END_ALLOW_THREADS( self );
	    self->valid = 0;
	}
	self->ldap = NULL;
    }
    PyMem_DEL(self);
}

/*------------------------------------------------------------
 * utility functions
 */

/* 
 * check to see if the LDAPObject is valid, 
 * ie has been opened, and not closed. An exception is set if not valid.
 */

static int
not_valid( LDAPObject* l ) {
    if (l->valid) {
    	return 0;
    } else {
    	PyErr_SetString( LDAPexception_class, "LDAP connection invalid" );
	return 1;
    }
}
  
/* free a LDAPMod (complete or partially) allocated in Tuple_to_LDAPMod() */

static void
LDAPMod_DEL( LDAPMod* lm )
{
    int i;

    if (lm->mod_type)
	PyMem_DEL(lm->mod_type);
    if (lm->mod_bvalues) {
	for (i = 0; lm->mod_bvalues[i]; i++) {
	    PyMem_DEL(lm->mod_bvalues[i]);
	}
	PyMem_DEL(lm->mod_bvalues);
    }
    PyMem_DEL(lm);
}

/* 
 * convert a tuple of the form (int,str,[str,...]) 
 * or (str, [str,...]) if no_op is true, into an LDAPMod structure.
 * See ldap_modify(3) for details.
 *
 * NOTE: the resulting LDAPMod structure has pointers directly into
 *       the Python string storage, so LDAPMod structures MUST have a
 *	 shorter lifetime than the tuple passed in.
 */

/* XXX - there is no way to pass complex-structured BER objects in here! */

static LDAPMod*
Tuple_to_LDAPMod( PyObject* tup, int no_op ) 
{
    int op;
    char *type;
    PyObject *list, *item;
    LDAPMod *lm = NULL;
    int i, len, nstrs;

    if (!PyTuple_Check(tup)) {
	PyErr_SetObject(PyExc_TypeError, Py_BuildValue("sO",
	   "expected a tuple", tup));
	return NULL;
    }

    if (no_op) {
	if (!PyArg_ParseTuple( tup, "sO", &type, &list ))
		return NULL;
	op = 0;
    } else {
	if (!PyArg_ParseTuple( tup, "isO", &op, &type, &list ))
		return NULL;
    }

    lm = PyMem_NEW(LDAPMod, 1);
    if (lm == NULL)
	goto nomem;

    lm->mod_op = op | LDAP_MOD_BVALUES;
    lm->mod_bvalues = NULL;

    len = strlen(type);
    lm->mod_type = PyMem_NEW(char, len + 1);
    if (lm->mod_type == NULL)
	goto nomem;
    memcpy(lm->mod_type, type, len + 1);

    if (list == Py_None) {
	/* None indicates a NULL mod_bvals */
    } else if (PyString_Check(list)) {
	/* Single string is a singleton list */
	lm->mod_bvalues = PyMem_NEW(struct berval *, 2);
	if (lm->mod_bvalues == NULL)
		goto nomem;
	lm->mod_bvalues[0] = PyMem_NEW(struct berval, 1);
	if (lm->mod_bvalues[0] == NULL)
		goto nomem;
	lm->mod_bvalues[1] = NULL;
	lm->mod_bvalues[0]->bv_len = PyString_Size(list);
	lm->mod_bvalues[0]->bv_val = PyString_AsString(list);
    } else if (PySequence_Check(list)) {
	nstrs = PySequence_Length(list);
	lm->mod_bvalues = PyMem_NEW(struct berval *, nstrs + 1);
	if (lm->mod_bvalues == NULL)
		goto nomem;
	for (i = 0; i < nstrs; i++) {
	   lm->mod_bvalues[i] = PyMem_NEW(struct berval, 1);
	   if (lm->mod_bvalues[i] == NULL)
		goto nomem;
	   lm->mod_bvalues[i+1] = NULL;
	   item = PySequence_GetItem(list, i);
	   if (item == NULL)
		goto error;
	   if (!PyString_Check(item)) {
		PyErr_SetObject( PyExc_TypeError, Py_BuildValue( "sO",
		   "expected a string in the list", item));
		Py_DECREF(item);
		goto error;
	   }
	   lm->mod_bvalues[i]->bv_len = PyString_Size(item);
	   lm->mod_bvalues[i]->bv_val = PyString_AsString(item);
	   Py_DECREF(item);
	}
	if (nstrs == 0)
	    lm->mod_bvalues[0] = NULL;
    }

    return lm;

nomem:
    PyErr_NoMemory();
error:
    if (lm) 
	LDAPMod_DEL(lm);

    return NULL;
}

/* free the structure allocated in List_to_LDAPMods() */

static void
LDAPMods_DEL( LDAPMod** lms ) {
    LDAPMod** lmp;
    for ( lmp = lms; *lmp; lmp++ )
    	LDAPMod_DEL( *lmp );
    PyMem_DEL(lms);
}

/* 
 * convert a list of tuples into a LDAPMod*[] array structure 
 * NOTE: list of tuples must live longer than the LDAPMods
 */

static LDAPMod**
List_to_LDAPMods( PyObject *list, int no_op ) {

    int i, len;
    LDAPMod** lms;
    PyObject *item;

    if (!PySequence_Check(list)) {
	PyErr_SetObject( PyExc_TypeError, Py_BuildValue("sO",
			"expected list of tuples", list ));
    	return NULL;
    }

    len = PySequence_Length(list);

    lms = PyMem_NEW(LDAPMod *, len + 1);
    if (lms == NULL) 
	goto nomem;

    for (i = 0; i < len; i++) {
        lms[i] = NULL;
        item = PySequence_GetItem(list, i);
        if (item == NULL) 
		goto error;
        lms[i] = Tuple_to_LDAPMod(item, no_op);
        Py_DECREF(item);
        if (lms[i] == NULL)
	    goto error;
    }
    lms[len] = NULL;
    return lms;

nomem:
    PyErr_NoMemory();
error:
    if (lms)
	LDAPMods_DEL(lms);
    return NULL;
}

/*
 * convert a python list of strings into an attr list (char*[]).
 * returns 1 if successful, 0 if not (with exception set)
 * XXX the strings should live longer than the resulting attrs pointer.
 */

int
attrs_from_List( PyObject *attrlist, char***attrsp ) {

    char **attrs = NULL;
    int i, len;
    PyObject *item;

    if (attrlist == Py_None) {
	/* None means a NULL attrlist */
    } else if (PyString_Check(attrlist)) {
	/* caught by John Benninghoff <johnb@netscape.com> */
	PyErr_SetObject( PyExc_TypeError, Py_BuildValue("sO",
		  "expected *list* of strings, not a string", attrlist ));
	goto error;
    } else if (PySequence_Check(attrlist)) {
	len = PySequence_Length(attrlist);
        attrs = PyMem_NEW(char *, len + 1);
	if (attrs == NULL)
	    goto nomem;

	for (i = 0; i < len; i++) {
	    attrs[i] = NULL;
	    item = PySequence_GetItem(attrlist, i);
	    if (item == NULL)
		goto error;
	    if (!PyString_Check(item)) {
		PyErr_SetObject(PyExc_TypeError, Py_BuildValue("sO",
			  "expected string in list", item));
		Py_DECREF(item);
		goto error;
	    }
	    attrs[i] = PyString_AsString(item);
	    Py_DECREF(item);
	}
	attrs[len] = NULL;
    } else {
    	PyErr_SetObject( PyExc_TypeError, Py_BuildValue("sO",
			  "expected list of strings or None", attrlist ));
	goto error;
    }

    *attrsp = attrs;
    return 1;

nomem:
    PyErr_NoMemory();
error:
    free_attrs(&attrs);
    return 0;
}

/* free memory allocated from above routine */

static void
free_attrs( char*** attrsp ) {
    char **attrs = *attrsp;

    if (attrs != NULL) {
   	PyMem_DEL(attrs);
	*attrsp = NULL;
    }
}

static void
set_timeval_from_double( struct timeval *tv, double d ) {
	tv->tv_usec = (long) ( fmod(d, 1.0) * 1000000.0 );
	tv->tv_sec = (long) floor(d);
}

/*------------------------------------------------------------
 * methods
 */

/* ldap_unbind */

static PyObject*
l_ldap_unbind( LDAPObject* self, PyObject* args )
{
    int ret;

    if (!PyArg_ParseTuple( args, "")) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    ret = ldap_unbind( self->ldap );
    LDAP_END_ALLOW_THREADS( self );
    if (ret == -1)
    	return LDAPerror( self->ldap, "ldap_unbind" );
    self->valid = 0;
    Py_INCREF(Py_None);
    return Py_None;
}

static char doc_unbind[] =
"unbind_s() -> None\n"
"unbind() -> int\n\n"
"\tThis call is used to unbind from the directory, terminate\n"
"\tthe current association, and free resources. Once called, the\n"
"\tconnection to the LDAP server is closed and the LDAP object\n"
"\tis invalid. Further invocation of methods on the object will\n"
"\tyield an exception.\n"
"\n"
"\tThe unbind and unbind_s methods are identical, and are\n"
"\tsynchronous in nature";

/* ldap_abandon */

static PyObject*
l_ldap_abandon( LDAPObject* self, PyObject* args )
{
    int msgid;
    int ret;

    if (!PyArg_ParseTuple( args, "i", &msgid)) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    ret = ldap_abandon( self->ldap, msgid );
    LDAP_END_ALLOW_THREADS( self );
    if (ret == -1)
    	return LDAPerror( self->ldap, "ldap_abandon" );
    Py_INCREF(Py_None);
    return Py_None;
}

static char doc_abandon[] =
"abandon(msgid) -> None\n\n"
"\tAbandons or cancels an LDAP operation in progress. The msgid should\n"
"\tbe the message id of an outstanding LDAP operation as returned\n"
"\tby the asynchronous methods search(), modify() etc.  The caller\n"
"\tcan expect that the result of an abandoned operation will not be\n"
"\treturned from a future call to result().";

/* ldap_add */

static PyObject *
l_ldap_add( LDAPObject* self, PyObject *args )
{
    char *dn;
    PyObject *modlist;
    int msgid;
    LDAPMod **mods;

    if (!PyArg_ParseTuple( args, "sO", &dn, &modlist )) return NULL;
    if (not_valid(self)) return NULL;

    mods = List_to_LDAPMods( modlist, 1 );
    if (mods == NULL)
	return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_add( self->ldap, dn, mods );
    LDAP_END_ALLOW_THREADS( self );
    LDAPMods_DEL( mods );

    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_add_s" );

    return PyInt_FromLong(msgid);
}

static char doc_add[] =
"add(dn, modlist) -> int\n\n"
"\tThis function is similar to modify(), except that no operation\n"
"\tinteger need be included in the tuples.";

/* ldap_add_s */

static PyObject *
l_ldap_add_s( LDAPObject* self, PyObject *args )
{
    char *dn;
    PyObject *modlist;
    int ret;
    LDAPMod **mods;

    if (!PyArg_ParseTuple( args, "sO", &dn, &modlist )) return NULL;
    if (not_valid(self)) return NULL;

    mods = List_to_LDAPMods( modlist, 1 );
    if (mods == NULL)
	return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    ret = ldap_add_s( self->ldap, dn, mods );
    LDAP_END_ALLOW_THREADS( self );

    LDAPMods_DEL( mods );

    if (ret != LDAP_SUCCESS) 
    	return LDAPerror( self->ldap, "ldap_add_s" );

    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_bind[] =
"bind(who, cred, method) -> int\n"
"bind_s(who, cred, method) -> None\n"
"simple_bind(who, passwd) -> int\n"
"simple_bind_s(who, passwd) -> None\n"
#ifdef WITH_KERBEROS
#ifdef HAVE_LDAP_KERBEROS_BIND_S
"kerberos_bind_s(who) -> None\n"
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND1
"kerberos_bind1(who) -> None\n"
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND1_S
"kerberos_bind1_s(who) -> None\n"
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND2
"kerberos_bind2(who) -> None\n"
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND2_S
"kerberos_bind2_s(who) -> None\n\n"
#endif
#endif
"\tAfter an LDAP object is created, and before any other operations\n"
"\tcan be attempted over the connection, a bind operation must\n"
"\tbe performed.\n"
"\n"
"\tThis method attempts to bind with the LDAP server using either\n"
"\tsimple authentication, or kerberos. The general method bind()\n"
"\ttakes a third parameter, method which can be one of AUTH_SIMPLE,\n"
"\tAUTH_KRBV41 or AUTH_KRBV42.  The cred parameter is ignored\n"
"\tfor Kerberos authentication.\n"
"\n"
"\tKerberos authentication is only available if the LDAP library\n"
"\tand the ldap module were both configured with --with-kerberos or\n"
"\tcompiled with -DWITH_KERBEROS.";

/* ldap_bind */

static PyObject*
l_ldap_bind( LDAPObject* self, PyObject* args )
{
    char *who, *cred;
    int method;
    int msgid;

    if (!PyArg_ParseTuple( args, "ssi", &who, &cred, &method)) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_bind( self->ldap, who, cred, method );
    LDAP_END_ALLOW_THREADS( self );
    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_bind" );
    return PyInt_FromLong( msgid );
}

/* ldap_bind_s */

static PyObject*
l_ldap_bind_s( LDAPObject* self, PyObject* args )
{
    char *who, *cred;
    int method;
    int result;

    if (!PyArg_ParseTuple( args, "ssi", &who, &cred, &method)) return NULL;
    if (not_valid(self)) return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    result =  ldap_bind_s( self->ldap, who, cred, method );
    LDAP_END_ALLOW_THREADS( self );

    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_bind_s" );
    Py_INCREF(Py_None);
    return Py_None;
}


#if 0 
/* removed until made OpenLDAP2 compatible */

/* ldap_set_rebind_proc */

/* XXX - this could be called when threads are allowed!!! */

  static PyObject* rebind_callback_func = NULL;
  static LDAPObject* rebind_callback_ld = NULL;

  static int rebind_callback( LDAP*ld, char**dnp, char**credp, 
  			      int*methp, int freeit
#ifdef LDAP_SET_REBIND_PROC_3ARGS
			      , void *unused			/* Ugh */
#endif
			      )
  {
      PyObject *result;
      PyObject *args;
      int was_saved;

      char *dn, *cred;
      int  meth;

      if (freeit)  {
      	if (*dnp) free(*dnp);
	if (*credp) free(*credp);
	return LDAP_SUCCESS;
      }

      /* paranoia? */
      if (rebind_callback_ld == NULL)
      	Py_FatalError("rebind_callback: rebind_callback_ld == NULL");
      if (rebind_callback_ld->ldap != ld) 
      	Py_FatalError("rebind_callback: rebind_callback_ld->ldap != ld");
      if (not_valid(rebind_callback_ld)) 
      	Py_FatalError("rebind_callback: ldap connection closed");

      was_saved = (rebind_callback_ld->_save != NULL);

      if (was_saved)
	  LDAP_END_ALLOW_THREADS( rebind_callback_ld );

      args = Py_BuildValue("(O)", rebind_callback_ld);
      result = PyEval_CallObject( rebind_callback_func, args );
      Py_DECREF(args);

      if (result != NULL && 
          !PyArg_ParseTuple( result, "ssi", &dn, &cred, &meth ) )
      {
	  Py_DECREF( result );
          result = NULL;
      }

      if (result == NULL) {
	PyErr_Print();
	if (was_saved) 
	    LDAP_BEGIN_ALLOW_THREADS( rebind_callback_ld );
      	return !LDAP_SUCCESS;
      }

      Py_DECREF(result);
      *dnp = strdup(dn);
      if (!*dnp) return LDAP_NO_MEMORY;
      *credp = strdup(cred);
      if (!*credp) return LDAP_NO_MEMORY;
      *methp = meth;

      if (was_saved) 
      	  LDAP_BEGIN_ALLOW_THREADS( rebind_callback_ld );

      return LDAP_SUCCESS;
  }

static PyObject*
l_ldap_set_rebind_proc( LDAPObject* self, PyObject* args )
{
    PyObject *func;

    if (!PyArg_ParseTuple( args, "O", &func)) return NULL;
    if (not_valid(self)) return NULL;


    if ( PyNone_Check(func) ) {
        Py_XDECREF(rebind_callback_func);
        Py_XDECREF(rebind_callback_ld);
        rebind_callback_func = NULL;
        rebind_callback_ld = NULL;
#ifdef LDAP_SET_REBIND_PROC_3ARGS
    	ldap_set_rebind_proc( self->ldap, NULL, 0);
#else
    	ldap_set_rebind_proc( self->ldap, NULL );
#endif
	Py_INCREF(Py_None);
	return Py_None;
    }

    if ( PyCallable_Check(func) ) {
        Py_XDECREF(rebind_callback_func);
        Py_XDECREF(rebind_callback_ld);
	rebind_callback_func = func;
	rebind_callback_ld = self;
	Py_INCREF(func);
	Py_INCREF(self);
#ifdef LDAP_SET_REBIND_PROC_3ARGS
        ldap_set_rebind_proc( self->ldap, rebind_callback, 0);
#else
        ldap_set_rebind_proc( self->ldap, rebind_callback);
#endif
	Py_INCREF(Py_None);
	return Py_None;
    }

    PyErr_SetString( PyExc_TypeError, "expected function or None" );
    return NULL;
}

static char doc_set_rebind_proc[] =
"set_rebind_proc(func) -> None\n\n"
"\tIf a referral is returned from the server, automatic re-binding\n"
"\tcan be achieved by providing a function that accepts as an\n"
"\targument the newly opened LDAP object and returns the tuple\n"
"\t(who, cred, method).\n"
"\n"
"\tPassing a value of None for func will disable this facility.\n"
"\n"
"\tBecause of restrictions in the implementation, only one\n"
"\trebinding function is supported at any one time. This method\n"
"\tis only available if the module and library were compiled with\n"
"\tsupport for it.";

#endif


/* ldap_simple_bind */

static PyObject*
l_ldap_simple_bind( LDAPObject *self, PyObject *args ) 
{
    char *who, *cred;
    int msgid;

    if (!PyArg_ParseTuple( args, "zz", &who, &cred )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_simple_bind( self->ldap, who, cred );
    LDAP_END_ALLOW_THREADS( self );
    if ( msgid == -1 )
    	return LDAPerror( self->ldap, "ldap_simple_bind" );
    return PyInt_FromLong( msgid );
}

/* ldap_simple_bind_s */

static PyObject*
l_ldap_simple_bind_s( LDAPObject *self, PyObject *args ) 
{
    char *who, *cred;
    int result;

    if (!PyArg_ParseTuple( args, "zz", &who, &cred )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_simple_bind_s( self->ldap, who, cred );
    LDAP_END_ALLOW_THREADS( self );
    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_simple_bind_s" );
    Py_INCREF(Py_None);
    return Py_None;
}

#ifdef WITH_KERBEROS

#ifdef HAVE_LDAP_KERBEROS_BIND_S	/* tsk. some libraries omit this.. */
/* ldap_kerberos_bind_s */

static PyObject*
l_ldap_kerberos_bind_s( LDAPObject *self, PyObject *args ) 
{
    char *who;
    int result;

    if (!PyArg_ParseTuple( args, "s", &who )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_kerberos_bind_s( self->ldap, who );
    LDAP_END_ALLOW_THREADS( self );
    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_kerberos_bind_s" );
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

#ifdef HAVE_LDAP_KERBEROS_BIND1
/* ldap_kerberos_bind1 */

static PyObject*
l_ldap_kerberos_bind1( LDAPObject *self, PyObject *args ) 
{
    char *who;
    int ret;

    if (!PyArg_ParseTuple( args, "s", &who )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    ret = ldap_kerberos_bind1( self->ldap, who );
    LDAP_END_ALLOW_THREADS( self );
    if (ret == -1)
    	return LDAPerror( self->ldap, "ldap_kerberos_bind1" );
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

#ifdef HAVE_LDAP_KERBEROS_BIND1_S
/* ldap_kerberos_bind1_s */

static PyObject*
l_ldap_kerberos_bind1_s( LDAPObject *self, PyObject *args ) 
{
    char *who;
    int result;

    if (!PyArg_ParseTuple( args, "s", &who )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_kerberos_bind1_s( self->ldap, who );
    LDAP_END_ALLOW_THREADS( self );
    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_kerberos_bind1_s" );
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

#ifdef HAVE_LDAP_KERBEROS_BIND2
/* ldap_kerberos_bind2 */

static PyObject*
l_ldap_kerberos_bind2( LDAPObject *self, PyObject *args ) 
{
    char *who;
    int ret;

    if (!PyArg_ParseTuple( args, "s", &who )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    ret = ldap_kerberos_bind2( self->ldap, who );
    LDAP_END_ALLOW_THREADS( self );
    if (ret == -1)
    	return LDAPerror( self->ldap, "ldap_kerberos_bind2" );
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

#ifdef HAVE_LDAP_KERBEROS_BIND2_S
/* ldap_kerberos_bind2_s */

static PyObject*
l_ldap_kerberos_bind2_s( LDAPObject *self, PyObject *args ) 
{
    char *who;
    int result;

    if (!PyArg_ParseTuple( args, "s", &who )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_kerberos_bind2_s( self->ldap, who );
    LDAP_END_ALLOW_THREADS( self );
    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_kerberos_bind2_s" );
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

#endif /* WITH_KERBEROS */

#ifndef NO_CACHE
#ifdef HAVE_LDAP_ENABLE_CACHE

/* ldap_enable_cache */

static PyObject*
l_ldap_enable_cache( LDAPObject* self, PyObject* args )
{
    long timeout = LDAP_NO_LIMIT;
    long maxmem  = LDAP_NO_LIMIT;

    if (!PyArg_ParseTuple( args, "|ll", &timeout, &maxmem )) return NULL;
    if (not_valid(self)) return NULL;
    if ( ldap_enable_cache( self->ldap, timeout, maxmem ) == -1 )
    	return LDAPerror( self->ldap, "ldap_enable_cache" );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_enable_cache[] =
"enable_cache([timeout=NO_LIMIT, [maxmem=NO_LIMIT]]) -> None\n\n"
"\tUsing a cache often greatly improves performance. By default\n"
"\tthe cache is disabled. Specifying timeout in seconds is used\n"
"\tto decide how long to keep cached requests. The maxmem value\n"
"\tis in bytes, and is used to set an upper bound on how much\n"
"\tmemory the cache will use. A value of NO_LIMIT for either\n"
"\tindicates unlimited.  Subsequent calls to enable_cache()\n"
"\tcan be used to adjust these parameters.\n"
"\n"
"\tThis and other caching methods are not available if the library\n"
"\tand the ldap module were compiled with support for it.";
#endif

#ifdef HAVE_LDAP_DISABLE_CACHE
/* ldap_disable_cache */

static PyObject *
l_ldap_disable_cache( LDAPObject* self, PyObject *args )
{
    if (!PyArg_ParseTuple( args, "" )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_disable_cache( self->ldap );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_disable_cache[] =
"disable_cache() -> None\n\n"
"\tTemporarily disables use of the cache. New requests are\n"
"\tnot cached, and the cache is not checked when returning\n"
"\tresults. Cache contents are not deleted.";
#endif

#ifdef HAVE_LDAP_SET_CACHE_OPTIONS
/* ldap_set_cache_options */

static PyObject *
l_ldap_set_cache_options( LDAPObject* self, PyObject *args )
{
    long opts;

    if (!PyArg_ParseTuple( args, "l", &opts )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_set_cache_options( self->ldap, opts );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_set_cache_options[] =
"set_cache_options(option) -> None\n\n"
"\tChanges the caching behaviour. Currently supported options are\n"
"\t    CACHE_OPT_CACHENOERRS, which suppresses caching of requests\n"
"\t        that resulted in an error, and\n"
"\t    CACHE_OPT_CACHEALLERRS, which enables caching of all requests.\n"
"\tThe default behaviour is not to cache requests that result in\n"
"\terrors, except those that result in a SIZELIMIT_EXCEEDED exception.";
#endif

#ifdef HAVE_LDAP_DESTROY_CACHE
/* ldap_destroy_cache */

static PyObject *
l_ldap_destroy_cache( LDAPObject* self, PyObject *args )
{
    if (!PyArg_ParseTuple( args, "" )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_destroy_cache( self->ldap );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_destroy_cache[] =
"destroy_cache() -> None\n\n"
"\tTurns off caching and removed it from memory.";
#endif

#ifdef HAVE_LDAP_FLUSH_CACHE
/* ldap_flush_cache */

static PyObject *
l_ldap_flush_cache( LDAPObject* self, PyObject *args )
{
    if (!PyArg_ParseTuple( args, "" )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_flush_cache( self->ldap );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_flush_cache[] =
"flush_cache() -> None\n\n"
"\tDeletes the cache's contents, but does not affect it in any other way.";
#endif


#ifdef HAVE_LDAP_UNCACHE_ENTRY
/* ldap_uncache_entry */

static PyObject *
l_ldap_uncache_entry( LDAPObject* self, PyObject *args )
{
    char *dn;

    if (!PyArg_ParseTuple( args, "s", &dn )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_uncache_entry( self->ldap, dn );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_uncache_entry[] =
"uncache_entry(dn) -> None\n\n"
"\tRemoves all cached entries that make reference to dn. This should be\n"
"\tused, for example, after doing a modify() involving dn.";
#endif

#ifdef HAVE_LDAP_UNCACHE_REQUEST
/* ldap_uncache_request */

static PyObject *
l_ldap_uncache_request( LDAPObject* self, PyObject *args )
{
    int msgid;

    if (!PyArg_ParseTuple( args, "i", &msgid )) return NULL;
    if (not_valid(self)) return NULL;
    ldap_uncache_request( self->ldap, msgid );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_uncache_request[] =
"uncache_request(msgid) -> None\n\n"
"\tRemove the request indicated by msgid from the cache.";
#endif

#endif /* !NO_CACHE */

/* ldap_compare */

static PyObject *
l_ldap_compare( LDAPObject* self, PyObject *args )
{
    char *dn, *attr, *value;
    int msgid;

    if (!PyArg_ParseTuple( args, "sss", &dn, &attr, &value )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_compare( self->ldap, dn, attr, value );
    LDAP_END_ALLOW_THREADS( self );
    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_compare" );
    return PyInt_FromLong( msgid );
}

/* ldap_compare_s */

static PyObject *
l_ldap_compare_s( LDAPObject* self, PyObject *args )
{
    char *dn, *attr, *value;
    int result;

    if (!PyArg_ParseTuple( args, "sss", &dn, &attr, &value )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_compare_s( self->ldap, dn, attr, value );
    LDAP_END_ALLOW_THREADS( self );
    if (result != LDAP_COMPARE_TRUE && 
        result != LDAP_COMPARE_FALSE )
    	return LDAPerror( self->ldap, "ldap_compare_s" );
    return PyInt_FromLong( result == LDAP_COMPARE_TRUE );
}

static char doc_compare[] =
"compare(dn, attr, value) -> int\n"
"compare_s(dn, attr, value) -> int\n\n"
"\tPerform an LDAP comparison between the attribute named attr of\n"
"\tentry dn, and the value value. The synchronous form returns 0\n"
"\tfor false, or 1 for true.  The asynchronous form returns the\n"
"\tmessage id of the initiates request, and the result of the\n"
"\tasynchronous compare can be obtained using result().\n"
"\n"
"\tNote that this latter technique yields the answer by raising\n"
"\tthe exception objects COMPARE_TRUE or COMPARE_FALSE.\n"
"\n"
"\tA design bug in the library prevents value from containing\n"
"\tnul characters.";


/* ldap_delete */

static PyObject *
l_ldap_delete( LDAPObject* self, PyObject *args )
{
    char *dn;
    int msgid;

    if (!PyArg_ParseTuple( args, "s", &dn )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_delete( self->ldap, dn );
    LDAP_END_ALLOW_THREADS( self );
    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_delete" );
    return PyInt_FromLong(msgid);
}

/* ldap_delete_s */

static PyObject *
l_ldap_delete_s( LDAPObject* self, PyObject *args )
{
    char *dn;
    int result;

    if (!PyArg_ParseTuple( args, "s", &dn )) return NULL;
    if (not_valid(self)) return NULL;
    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_delete_s( self->ldap, dn );
    LDAP_END_ALLOW_THREADS( self );
    if (result != LDAP_SUCCESS)
    	return LDAPerror( self->ldap, "ldap_delete_s" );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_delete[] =
"delete(dn) -> int\n"
"delete_s(dn) -> None\n\n"
"\tPerforms an LDAP delete operation on dn. The asynchronous\n"
"\tform returns the message id of the initiated request, and the\n"
"\tresult can be obtained from a subsequent call to result().";

/* ldap_modify */

static PyObject *
l_ldap_modify( LDAPObject* self, PyObject *args )
{
    char *dn;
    PyObject *modlist;
    int msgid;
    LDAPMod **mods;

    if (!PyArg_ParseTuple( args, "sO", &dn, &modlist )) return NULL;
    if (not_valid(self)) return NULL;

    mods = List_to_LDAPMods( modlist, 0 );
    if (mods == NULL)
	return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_modify( self->ldap, dn, mods );
    LDAP_END_ALLOW_THREADS( self );

    LDAPMods_DEL( mods );

    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_modify" );

    return PyInt_FromLong( msgid );
}

/* ldap_modify_s */

static PyObject *
l_ldap_modify_s( LDAPObject* self, PyObject *args )
{
    char *dn;
    PyObject *modlist;
    int result;
    LDAPMod **mods;

    if (!PyArg_ParseTuple( args, "sO", &dn, &modlist )) return NULL;
    if (not_valid(self)) return NULL;

    mods = List_to_LDAPMods( modlist, 0 );
    if (mods==NULL) return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_modify_s( self->ldap, dn, mods );
    LDAP_END_ALLOW_THREADS( self );

    LDAPMods_DEL( mods );

    if (result != LDAP_SUCCESS)
    	return LDAPerror( self->ldap, "ldap_modify_s" );

    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_modify[] =
"modify(dn, modlist) -> int\n"
"modify_s(dn, modlist) -> None\n\n"
"\tPerforms an LDAP modify operation on an entry's attributes.\n"
"\tdn is the DN of the entry to modify, and modlist is the list\n"
"\tof modifications to make to the entry.\n"
"\n"
"\tEach element of the list modlist should be a tuple of the form\n"
"\t(mod_op,mod_type,mod_vals), where mod_op is the operation (one\n"
"\tof MOD_ADD, MOD_DELETE, or MOD_REPLACE), mod_type is a string\n"
"\tindicating the attribute type name, and mod_vals is either\n"
"\ta string value or a list of string values to add, delete or\n"
"\treplace respectively.  For the delete operation, mod_vals may\n"
"\tbe None indicating that all attributes are to be deleted.\n"
"\n"
"\tThe asynchronous modify() returns the message id of the\n"
"\tinitiated request.";

/* ldap_modrdn */

static PyObject *
l_ldap_modrdn( LDAPObject* self, PyObject *args )
{
    char *dn, *newrdn;
    int delold = 1;
    int msgid;

    if (!PyArg_ParseTuple( args, "ss|i", &dn, &newrdn, &delold )) 
    	return NULL;
    if (not_valid(self)) return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
#if defined(HAVE_LDAP_MODRDN2)
    msgid = ldap_modrdn2( self->ldap, dn, newrdn, delold );
#else
#if    defined(LDAP_MODRDN_3ARGS)
    /* XXX the delold parameter is being ignored! should tell user */
    msgid = ldap_modrdn( self->ldap, dn, newrdn );
#else
    msgid = ldap_modrdn( self->ldap, dn, newrdn, delold );
#endif
#endif
    LDAP_END_ALLOW_THREADS( self );
    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_modrdn2" );
    return PyInt_FromLong(msgid);
}

/* ldap_modrdn_s */

static PyObject *
l_ldap_modrdn_s( LDAPObject* self, PyObject *args )
{
    char *dn, *newrdn;
    int delold = 1;
    int result;

    if (!PyArg_ParseTuple( args, "ss|i", &dn, &newrdn, &delold )) 
    	return NULL;
    if (not_valid(self)) return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
#if defined(HAVE_LDAP_MODRDN2_S)
    result = ldap_modrdn2_s( self->ldap, dn, newrdn, delold );
#else
#if    defined(LDAP_MODRDN_S_3ARGS)
    /* XXX the delold parameter is being ignored! should tell user */
    result = ldap_modrdn_s( self->ldap, dn, newrdn );
#else
    result = ldap_modrdn_s( self->ldap, dn, newrdn, delold );
#endif
#endif
    LDAP_END_ALLOW_THREADS( self );

    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_modrdn2_s" );
    Py_INCREF( Py_None );
    return Py_None;
}

static char doc_modrdn[] =
"modrdn(dn, newrdn [,delold=1]) -> int\n"
"modrdn_s(dn, newrdn [,delold=1]) -> None\n\n"
"\tPerform a modify RDN operation. These routines take dn, the\n"
"\tDN of the entry whose RDN is to be changed, and newrdn, the\n"
"\tnew RDN to give to the entry. The optional parameter delold\n"
"\tis used to specify whether the old RDN should be kept as\n"
"\tan attribute of the entry or not.  The asynchronous version\n"
"\treturns the initiated message id.\n"
"\n"
"\tThis actually corresponds to the modrdn2* routines in the\n"
"\tC library.";


/* ldap_result */

static PyObject *
l_ldap_result( LDAPObject* self, PyObject *args )
{
    int msgid = LDAP_RES_ANY;
    int all = 1;
    double timeout = -1.0;
    struct timeval tv;
    struct timeval* tvp;
    int res_type;
    LDAPMessage *msg = NULL;
    PyObject *result_str, *retval, *pmsg;

    if (!PyArg_ParseTuple( args, "|iid", &msgid, &all, &timeout ))
    	return NULL;
    if (not_valid(self)) return NULL;
    
    if (timeout >= 0) {
        tvp = &tv;
	set_timeval_from_double( tvp, timeout );
    } else {
    	tvp = NULL;
    }

    LDAP_BEGIN_ALLOW_THREADS( self );
    res_type = ldap_result( self->ldap, msgid, all, tvp, &msg );
    LDAP_END_ALLOW_THREADS( self );

    if (res_type < 0)	/* LDAP or system error */
    	return LDAPerror( self->ldap, "ldap_result" );

    if (res_type == 0) {
	/* Polls return (None, None); timeouts raise an exception */
	if (timeout == 0)
		return Py_BuildValue("(OO)", Py_None, Py_None);
	else
		return LDAPerr(LDAP_TIMEOUT);
    }

    if (res_type == LDAP_RES_SEARCH_ENTRY
	    || res_type == LDAP_RES_SEARCH_REFERENCE
	)
	pmsg = LDAPmessage_to_python( self->ldap, msg );
    else {
	int result;
	char **refs = NULL;
	LDAP_BEGIN_ALLOW_THREADS( self );
	ldap_parse_result( self->ldap, msg, &result, NULL, NULL, &refs, NULL, 0 );
	LDAP_END_ALLOW_THREADS( self );

	if (result != LDAP_SUCCESS) {		/* result error */
	    char *e, err[1024];
	    if (result == LDAP_REFERRAL && refs && refs[0]) {
		snprintf(err, sizeof(err), "Referral:\n%s", refs[0]);
		e = err;
	    } else
		e = "ldap_parse_result";
	    return LDAPerror( self->ldap, e );
	}
	pmsg = Py_None;
    }

    result_str = LDAPconstant( res_type );

    if (pmsg == NULL) {
	    retval = NULL;
    } else {
	    retval = Py_BuildValue("(OO)", result_str, pmsg);
	if (pmsg != Py_None) {
        Py_DECREF(pmsg);
    }
    }
    Py_DECREF(result_str);
    return retval;
}

static char doc_result[] =
"result([msgid=RES_ANY [,all=1 [,timeout=-1]]]) -> (result_type, result_data)\n"
"\n"
"\tThis method is used to wait for and return the result of an\n"
"\toperation previously initiated by one of the LDAP asynchronous\n"
"\toperation routines (eg search(), modify(), etc.) They all\n"
"\treturned an invocation identifier (a message id) upon successful\n"
"\tinitiation of their operation. This id is guaranteed to be\n"
"\tunique across an LDAP session, and can be used to request the\n"
"\tresult of a specific operation via the msgid parameter of the\n"
"\tresult() method.\n"
"\n"
"\tIf the result of a specific operation is required, msgid should\n"
"\tbe set to the invocation message id returned when the operation\n"
"\twas initiated; otherwise RES_ANY should be supplied.\n"
"\n"
"\tThe all parameter only has meaning for search() responses\n"
"\tand is used to select whether a single entry of the search\n"
"\tresponse should be returned, or to wait for all the results\n"
"\tof the search before returning.\n"
"\n"
"\tA search response is made up of zero or more search entries\n"
"\tfollowed by a search result. If all is 0, search entries will\n"
"\tbe returned one at a time as they come in, via separate calls\n"
"\tto result(). If all is 1, the search response will be returned\n"
"\tin its entirety, i.e. after all entries and the final search\n"
"\tresult have been received.\n"
"\n"
"\tThe method returns a tuple of the form (result_type,\n"
"\tresult_data).  The result_type is a string, being one of:\n"
"\t'RES_BIND', 'RES_SEARCH_ENTRY', 'RES_SEARCH_RESULT',\n"
"\t'RES_MODIFY', 'RES_ADD', 'RES_DELETE', 'RES_MODRDN', or\n"
"\t'RES_COMPARE'.\n"
"\n"
"\tThe constants RES_* are set to these strings, for convenience.\n"
"\n"
"\tSee search() for a description of the search result's\n"
"\tresult_data, otherwise the result_data is normally meaningless.\n"
"\n"
"\tThe result() method will block for timeout seconds, or\n"
"\tindefinitely if timeout is negative.  A timeout of 0 will effect\n"
"\ta poll.  The timeout can be expressed as a floating-point value.\n"
"\n"
"\tIf a timeout occurs, a TIMEOUT exception is raised, unless\n"
"\tpolling (timeout = 0), in which case (None, None) is returned.";

/* ldap_search */

static PyObject*
l_ldap_search( LDAPObject* self, PyObject* args )
{
    char *base;
    int scope;
    char *filter;
    PyObject *attrlist = Py_None;
    char **attrs;
    int attrsonly = 0;

    int msgid;

    if (!PyArg_ParseTuple( args, "sis|Oi", 
    	&base, &scope, &filter, &attrlist, &attrsonly)) return NULL;
    if (not_valid(self)) return NULL;

    if (!attrs_from_List( attrlist, &attrs )) 
   	 return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    msgid = ldap_search( self->ldap, base, scope, filter, 
                             attrs, attrsonly );
    LDAP_END_ALLOW_THREADS( self );

    free_attrs( &attrs );

    if (msgid == -1)
    	return LDAPerror( self->ldap, "ldap_search" );

    return PyInt_FromLong( msgid );
}	

/* ldap_search_st */

static PyObject*
l_ldap_search_st( LDAPObject* self, PyObject* args )
{
    char *base;
    int scope;
    char *filter;
    PyObject *attrlist = Py_None;
    char **attrs;
    int attrsonly = 0;
    double timeout = -1.0;
    struct timeval tv, *tvp;
    LDAPMessage *resmsg = NULL;
    int result;

    if (!PyArg_ParseTuple( args, "sis|Oid", 
    	&base, &scope, &filter, &attrlist, &attrsonly, &timeout )) return NULL;
    if (not_valid(self)) return NULL;

    if (timeout >= 0) {
    	tvp = &tv;
	set_timeval_from_double( tvp, timeout );
    } else {
    	tvp = NULL;
    }

    if (!attrs_from_List( attrlist, &attrs )) 
   	 return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_search_st( self->ldap, base, scope, filter, 
                             attrs, attrsonly, tvp, &resmsg );
    LDAP_END_ALLOW_THREADS( self );

    free_attrs( &attrs );

    if (result != LDAP_SUCCESS)
    	return LDAPerror( self->ldap, "ldap_search_st" );

    if (resmsg == NULL) {
    	Py_INCREF( Py_None );
	return Py_None;
    } else {
    	return LDAPmessage_to_python( self->ldap, resmsg );
    }
}	

static char doc_search[] =
"search(base, scope, filter [,attrlist=None [,attrsonly=0]]) -> int\n"
"search_s(base, scope, filter [,attrlist=None [,attrsonly=0]])\n"
"search_st(base, scope, filter [,attrlist=None [,attrsonly=0 [,timeout=-1]]])\n"
"\n"
"\tPerform an LDAP search operation, with base as the DN of\n"
"\tthe entry at which to start the search, scope being one of\n"
"\tSCOPE_BASE (to search the object itself), SCOPE_ONELEVEL\n"
"\t(to search the object's immediate children), or SCOPE_SUBTREE\n"
"\t(to search the object and all its descendants).\n"
"\n"
"\tfilter is a string representation of the filter to\n"
"\tapply in the search. Simple filters can be specified as\n"
"\t'attribute_type=attribute_value'.  More complex filters are\n"
"\tspecified using a prefix notation according to the following\n"
"\tBNF:\n"
"\n"
"\t    filter     ::=  '(' filtercomp ')'\n"
"\t    filtercomp ::=  and | or | not | simple\n"
"\t    and        ::=  '&' filterlist\n"
"\t    or         ::=  '|' filterlist\n"
"\t    not        ::=  '!' filter\n"
"\t    filterlist ::=  filter | filter filterlist\n"
"\t    simple     ::=  attributetype filtertype attributevalue\n"
"\t    filtertype ::=  '=' | '~=' | '<=' | '>='\n"
"\n"
"\tWhen using the asynchronous form and result(), the all parameter\n"
"\taffects how results come in.  For all set to 0, result tuples\n"
"\ttrickle in (with the same message id), and with the result type\n"
"\tRES_SEARCH_ENTRY, until the final result which has a result\n"
"\ttype of RES_SEARCH_RESULT and a (usually) empty data field.\n"
"\tWhen all is set to 1, only one result is returned, with a\n"
"\tresult type of RES_SEARCH_RESULT, and all the result tuples\n"
"\tlisted in the data field.\n"
"\n"
"\tEach result tuple is of the form (dn,attrs), where dn is a\n"
"\tstring containing the DN (distinguished name) of the entry, and\n"
"\tattrs is a dictionary containing the attributes associated with\n"
"\tthe entry.  The keys of attrs are strings, and the associated\n"
"\tvalues are lists of strings.\n"
"\n"
"\tThe DN in dn is extracted using the underlying ldap_get_dn(),\n"
"\twhich may raise an exception of the DN is malformed.\n"
"\n"
"\tIf attrsonly is non-zero, the values of attrs will be\n"
"\tmeaningless (they are not transmitted in the result).\n"
"\n"
"\tThe retrieved attributes can be limited with the attrlist\n"
"\tparameter.  If attrlist is None, all the attributes of each\n"
"\tentry are returned.\n"
"\n"
"\tThe synchronous form with timeout, search_st(), will block\n"
"\tfor at most timeout seconds (or indefinitely if timeout is\n"
"\tnegative). A TIMEOUT exception is raised if no result is\n"
"\treceived within the time.";

/* ldap_search_s == ldap_search_st */

/* ldap_sort_entries */

#ifdef HAVE_LDAP_START_TLS_S
/* ldap_start_tls_s */

static PyObject*
l_ldap_start_tls_s( LDAPObject* self, PyObject* args )
{
    int result;

    if (!PyArg_ParseTuple( args, "" )) return NULL;
    if (not_valid(self)) return NULL;

    result = ldap_start_tls_s( self->ldap, NULL, NULL );
    if ( result != LDAP_SUCCESS ){
	ldap_set_option(self->ldap, LDAP_OPT_ERROR_NUMBER, &result);
	return LDAPerror( self->ldap, "ldap_start_tls_s" );
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static char doc_start_tls[] =
"start_tls_s() -> None\n\n"
"\tNegotiate TLS with server. The `version' attribute must have been\n"
"\tset to VERSION3 before calling start_tls_s.\n"
"\tIf TLS could not be started an exception will be raised.\n"
;
#endif

/* ldap_url_search */

/* ldap_url_search_s */

/* ldap_url_search_st */

static PyObject*
l_ldap_url_search_st( LDAPObject* self, PyObject* args )
{
    char *url;
    int attrsonly = 0;
    LDAPMessage *resmsg;
    int result;
    double timeout = -1.0;
    struct timeval tv, *tvp;

    if (!PyArg_ParseTuple( args, "s|id", &url, &attrsonly, &timeout )) 
    	return NULL;
    if (not_valid(self)) return NULL;

    if (timeout>=0) {
        tvp = &tv;
	set_timeval_from_double( tvp, timeout );
    } else {
    	tvp = NULL;
    }

    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_url_search_st( self->ldap, url, attrsonly, tvp, &resmsg );
    LDAP_END_ALLOW_THREADS( self );

    if (result != LDAP_SUCCESS)
    	return LDAPerror( self->ldap, "ldap_ufn_search_st" );
    
    if (resmsg == NULL) {
    	Py_INCREF( Py_None );
	return Py_None;
    } else {
    	return LDAPmessage_to_python( self->ldap, resmsg );
    }
}

static char doc_url_search[] =
"url_search_s(url [,attrsonly=0])\n"
"url_search_s(url [,attrsonly=0 [,timeout=-1]])\n\n"
"\tThese routine works much like search_s*, except that many\n"
"\tsearch parameters are pulled out of the URL url.\n"
"\n"
"\tLDAP URLs look like this:\n"
"\t    ldap://host[:port]/dn[?attributes[?scope[?filter]]]\n"
"\n"
"\twhere scope is one of 'base' (default), 'one' or 'sub',\n"
"\tand attributes is a comma-separated list of attributes to\n"
"\tbe retrieved.\n"
"\n"
"\tURLs wrapped in angle-brackets and/or preceded by 'URL:'\n"
"\tare tolerated.";

#if defined(HAVE_FILENO_LD_SB_SB_SD) /* || defined(...) */
#define FILENO_SUPPORTED
#endif

#if defined(FILENO_SUPPORTED)
static PyObject*
l_ldap_fileno(LDAPObject* self, PyObject* args)
{
    int fileno;

    if (PyArg_ParseTuple(args, "") == NULL)
	return NULL;
    if (!self->valid)
	fileno = -1;
    else {
#if defined(HAVE_FILENO_LD_SB_SB_SD)
	fileno = self->ldap->ld_sb.sb_sd;
/* #else ... other techniques */
#endif
    }
    return PyInt_FromLong(fileno);
}
static char doc_fileno[] =
"fileno() -> int\n"
"\tReturn the file descriptor associated with this connection.";
#endif /* FILENO_SUPPORTED */

/* ldap_set_option */

static PyObject*
l_ldap_set_option(PyObject* self, PyObject *args)
{
    PyObject *value;
    int option;

    if (!PyArg_ParseTuple(args, "iO:set_option", &option, &value))
    	return NULL;
    if (LDAP_set_option((LDAPObject *)self, option, value) == -1)
	return NULL;
    Py_INCREF(Py_None);
    return Py_None;
}

static char doc_set_option[] = 
"set_option(option, value)\n\n"
"\tSet an LDAP option to the given value.\n";

/* ldap_get_option */

static PyObject*
l_ldap_get_option(PyObject* self, PyObject *args)
{
    int option;

    if (!PyArg_ParseTuple(args, "i:get_option", &option))
    	return NULL;
    return LDAP_get_option((LDAPObject *)self, option);
}

static char doc_get_option[] = 
"get_option(option) -> object\n\n"
"\tGet the value of an LDAP option.\n";

/* methods */

static PyMethodDef methods[] = {
    {"unbind",		(PyCFunction)l_ldap_unbind,		METH_VARARGS,	doc_unbind},	
    {"unbind_s",	(PyCFunction)l_ldap_unbind,		METH_VARARGS,	doc_unbind},	
    {"abandon",		(PyCFunction)l_ldap_abandon,		METH_VARARGS,	doc_abandon},	
    {"add",		(PyCFunction)l_ldap_add,		METH_VARARGS,	doc_add},	
    {"add_s",		(PyCFunction)l_ldap_add_s,		METH_VARARGS,	doc_add},	
    {"bind",		(PyCFunction)l_ldap_bind,		METH_VARARGS,	doc_bind},	
    {"bind_s",		(PyCFunction)l_ldap_bind_s,		METH_VARARGS,	doc_bind},	
#if 0    
    {"set_rebind_proc",	(PyCFunction)l_ldap_set_rebind_proc,	METH_VARARGS,	doc_set_rebind_proc},	
#endif
    {"simple_bind",	(PyCFunction)l_ldap_simple_bind,	METH_VARARGS,	doc_bind},	
    {"simple_bind_s",	(PyCFunction)l_ldap_simple_bind_s,	METH_VARARGS,	doc_bind},	
#ifdef WITH_KERBEROS
#ifdef HAVE_LDAP_KERBEROS_BIND_S
    {"kerberos_bind_s",	(PyCFunction)l_ldap_kerberos_bind_s,	METH_VARARGS,	doc_bind},	
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND1
    {"kerberos_bind1",	(PyCFunction)l_ldap_kerberos_bind1,	METH_VARARGS,	doc_bind},	
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND1_S
    {"kerberos_bind1_s",(PyCFunction)l_ldap_kerberos_bind1_s,	METH_VARARGS,	doc_bind},	
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND2
    {"kerberos_bind2",	(PyCFunction)l_ldap_kerberos_bind2,	METH_VARARGS,	doc_bind},	
#endif
#ifdef HAVE_LDAP_KERBEROS_BIND2_S
    {"kerberos_bind2_s",(PyCFunction)l_ldap_kerberos_bind2_s,	METH_VARARGS,	doc_bind},	
#endif
#endif /* WITH_KERBEROS */
#ifndef NO_CACHE
#ifdef HAVE_LDAP_ENABLE_CACHE
    {"enable_cache",	(PyCFunction)l_ldap_enable_cache,	METH_VARARGS,	doc_enable_cache},	
#endif
#ifdef HAVE_LDAP_DISABLE_CACHE
    {"disable_cache",	(PyCFunction)l_ldap_disable_cache,	METH_VARARGS,	doc_disable_cache},	
#endif
#ifdef HAVE_LDAP_SET_CACHE_OPTIONS
    {"set_cache_options",(PyCFunction)l_ldap_set_cache_options,	METH_VARARGS,	doc_set_cache_options},	
#endif
#ifdef HAVE_LDAP_DESTROY_CACHE
    {"destroy_cache",	(PyCFunction)l_ldap_destroy_cache,	METH_VARARGS,	doc_destroy_cache},	
#endif
#ifdef HAVE_LDAP_FLUSH_CACHE
    {"flush_cache",	(PyCFunction)l_ldap_flush_cache,	METH_VARARGS,	doc_flush_cache},	
#endif
#ifdef HAVE_LDAP_UNCACHE_ENTRY
    {"uncache_entry",	(PyCFunction)l_ldap_uncache_entry,	METH_VARARGS,	doc_uncache_entry},	
#endif
#ifdef HAVE_LDAP_UNCACHE_REQUEST
    {"uncache_request",	(PyCFunction)l_ldap_uncache_request,	METH_VARARGS,	doc_uncache_request},	
#endif
#endif /* !NO_CACHE */
    {"compare",		(PyCFunction)l_ldap_compare,		METH_VARARGS,	doc_compare},	
    {"compare_s",	(PyCFunction)l_ldap_compare_s,		METH_VARARGS,	doc_compare},	
    {"delete",		(PyCFunction)l_ldap_delete,		METH_VARARGS,	doc_delete},	
    {"delete_s",	(PyCFunction)l_ldap_delete_s,		METH_VARARGS,	doc_delete},	
    {"modify",		(PyCFunction)l_ldap_modify,		METH_VARARGS,	doc_modify},	
    {"modify_s",	(PyCFunction)l_ldap_modify_s,		METH_VARARGS,	doc_modify},	
    {"modrdn",		(PyCFunction)l_ldap_modrdn,		METH_VARARGS,	doc_modrdn},	
    {"modrdn_s",	(PyCFunction)l_ldap_modrdn_s,		METH_VARARGS,	doc_modrdn},
    {"result",		(PyCFunction)l_ldap_result,		METH_VARARGS,	doc_result},	
    {"search",		(PyCFunction)l_ldap_search,		METH_VARARGS,	doc_search},	
    {"search_s",	(PyCFunction)l_ldap_search_st,		METH_VARARGS,	doc_search},	
    {"search_st",	(PyCFunction)l_ldap_search_st,		METH_VARARGS,	doc_search},	
#ifdef HAVE_LDAP_START_TLS_S
    {"start_tls_s",	(PyCFunction)l_ldap_start_tls_s,	METH_VARARGS,	doc_start_tls},
#endif
    {"url_search_s",	(PyCFunction)l_ldap_url_search_st,	METH_VARARGS,	doc_url_search},	
    {"url_search_st",	(PyCFunction)l_ldap_url_search_st,	METH_VARARGS,	doc_url_search},	
    {"set_option",	(PyCFunction)l_ldap_set_option,		METH_VARARGS,	doc_set_option},	
    {"get_option",	(PyCFunction)l_ldap_get_option,		METH_VARARGS,	doc_get_option},	
#if defined(FILENO_SUPPORTED)
    {"fileno",		(PyCFunction)l_ldap_fileno,		METH_VARARGS,	doc_fileno},	
#endif
    { NULL, NULL }
};

/* representation */

static PyObject*
repr( LDAPObject* self )
{
    static char buf[4096];

#   define STRFMT	"%s%s%s"
#   define STRFMTP(s)							\
    		(s)==NULL?"":"'",					\
		(s)==NULL?"None":(s),					\
		(s)==NULL?"":"'"

#   define LIMITFMT	"%d%s"
#   define LIMITFMTP(v)							\
    		(v),							\
		(v)==LDAP_NO_LIMIT?" (NO_LIMIT)":""
    		

    sprintf(buf,
#ifndef LDAP_TYPE_IS_OPAQUE
    	"<LDAP {lberoptions:%d, deref:%s, "
	"timelimit:" LIMITFMT ", "
	"sizelimit:" LIMITFMT ", "
	"errno:%d, error:" STRFMT ", "
	"matched:" STRFMT ", refhoplimit:%d, options:< %s%s%s>}>",
	    self->ldap->ld_lberoptions,
	    (
		self->ldap->ld_deref==LDAP_DEREF_NEVER ? "DEREF_NEVER" :
		self->ldap->ld_deref==LDAP_DEREF_SEARCHING ? "DEREF_SEARCHING" :
		self->ldap->ld_deref==LDAP_DEREF_FINDING ? "DEREF_FINDING" :
		self->ldap->ld_deref==LDAP_DEREF_ALWAYS ? "DEREF_ALWAYS" :
							  "*illegal*" 
	    ),
	    LIMITFMTP(self->ldap->ld_timelimit),
	    LIMITFMTP(self->ldap->ld_sizelimit),
	    self->ldap->ld_errno,
	    STRFMTP(self->ldap->ld_error),
	    STRFMTP(self->ldap->ld_matched),
	    self->ldap->ld_refhoplimit,

#ifdef LDAP_DNS
	   (self->ldap->ld_options & LDAP_OPT_DNS ? "OPT_DNS ":""),
#else
	      "",
#endif /* LDAP_DNS */

#ifdef LDAP_REFERRALS
	   (self->ldap->ld_options & LDAP_OPT_REFERRALS ? "OPT_REFERRALS ":""),
#else
	      "",
#endif /* LDAP_REFERRALS */

	   (self->ldap->ld_options & LDAP_OPT_RESTART   ? "OPT_RESTART ":"")
#else	/* LDAP_TYPE_IS_OPAQUE */
	"<LDAP>"
#endif
    );
    return PyString_FromString( buf );
}

/* get attribute */

static PyObject*
getattr(LDAPObject* self, char* name) 
{
	int option;

	option = LDAP_optionval_by_name(name);
	if (option != -1)
		return LDAP_get_option(self, option);

	return Py_FindMethod(methods, (PyObject*)self, name);
}

/* set attribute */

static int
setattr(LDAPObject* self, char* name, PyObject* value) 
{
	int option;

	option = LDAP_optionval_by_name(name);
	if (option != -1)
		return LDAP_set_option(self, option, value);

	PyErr_SetString(PyExc_AttributeError, name);
	return -1;
}

/* type entry */

PyTypeObject LDAP_Type = {
#if defined(WIN32) || defined(__CYGWIN__)
	/* see http://www.python.org/doc/FAQ.html#3.24 */
	PyObject_HEAD_INIT(NULL)
#else /* ! WIN32 */
	PyObject_HEAD_INIT(&PyType_Type)
#endif /* ! WIN32 */
	0,                      /*ob_size*/
	"LDAP",                 /*tp_name*/
	sizeof(LDAPObject),     /*tp_basicsize*/
	0,                      /*tp_itemsize*/
	/* methods */
	(destructor)dealloc,	/*tp_dealloc*/
	0,                      /*tp_print*/
	(getattrfunc)getattr,	/*tp_getattr*/
	(setattrfunc)setattr,	/*tp_setattr*/
	0,                      /*tp_compare*/
	(reprfunc)repr,         /*tp_repr*/
	0,                      /*tp_as_number*/
	0,                      /*tp_as_sequence*/
	0,                      /*tp_as_mapping*/
	0,                      /*tp_hash*/
};
