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

#include <sasl.h>


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

static char doc_unbind[] = "";

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

static char doc_abandon[] = "";

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
    	return LDAPerror( self->ldap, "ldap_add" );

    return PyInt_FromLong(msgid);
}

static char doc_add[] = "";

static char doc_bind[] = "";

static char doc_sasl_bind_s[] = "";

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


/* The following functions implement SASL binds. A new method
   sasl_bind_s(bind_dn, sasl_mechanism) has been introduced.

   * The bind_dn argument will be passed to the c library; however,
     normally it is not needed and should be an empty string.

   * The sasl_mechanism argument is an instance of a class that
     implements a callback interface. For convenience, it should be
     derived from the sasl class (which lives in the ldap.sasl module).
     See the module documentation for more information.

     Check your /usr/lib/sasl/ directory for locally installed SASL
     auth modules ("mechanisms"), or try

       ldapsearch   -b "" -s base -LLL -x  supportedSASLMechanisms
     
     (perhaps with an additional -h and -p argument for ldap host and
     port). The latter will show you which SASL mechanisms are known
     to the LDAP server. If you do not want to set up Kerberos, you
     can still use SASL binds. Your authentication data should then be
     stored in /etc/sasldb (see saslpasswd(8)). If the LDAP server
     does not find the sasldb, it wont allow for DIGEST-MD5 and
     CRAM-MD5. One important thing to get started with sasldb: you
     should first add a dummy user (saslpasswd -c dummy), and this
     will give you some strange error messages. Then delete the dummy
     user (saslpasswd -d dummy), and now you can start adding users to
     your sasldb (again, use the -c switch). Strange, eh?

   * The sasl_mechanism object must implement a method, which will be
     called by the sasl lib several times. The prototype of the
     callback looks like this: callback(id, challenge, prompt,
     defresult) has to return a string (or maybe None). The id
     argument specifies, which information should be passed back to
     the SASL lib (see SASL_CB_xxx in sasl.h)


   A nice "Howto get LDAPv3 up and running with Kerberos and SSL" can
   be found at http://www.bayour.com/LDAPv3-HOWTO.html.  Instead of
   MIT Kerberos, I used Heimdal for my tests (since it is included
   with SuSE Linux).

   Todo:
   
   * Find a better interface than the python callback. This is 
     really ugly. Perhaps one could make use of a sasl class, like
     in the perl ldap module.

   * Thread safety?

   * Memory Management?
   
   * Write more docs

   * ...

*/
static int interaction ( unsigned flags, 
			 sasl_interact_t *interact,
			 PyObject* SASLObject )
{
  const char *dflt = interact->defresult;
  PyObject *result;
  char *c_result;
  result = PyObject_CallMethod(SASLObject,
			       "callback",
			       "isss",
			       interact->id,  /* see sasl.h */
			       interact->challenge,
			       interact->prompt,   
			       interact->defresult);

  if (result == NULL) 
    /*searching for a better error code */
    return LDAP_OPERATIONS_ERROR; 
  c_result = PyString_AsString(result); /*xxx Error checking?? */
  
  /* according to the sasl docs, we should malloc() the returned
     string only for calls where interact->id == SASL_CB_PASS, so we
     probably leak a few bytes per ldap bind. However, if I restrict
     the strdup() to this case, I get segfaults. Should probably be
     fixed sometimes.
  */
  interact->result = strdup( c_result );
  if (interact->result == NULL)
    return LDAP_OPERATIONS_ERROR;
  interact->len = strlen(c_result);
  /* We _should_ overwrite the python string buffer for security
     reasons, however we may not (api/stringObjects.html). Any ideas?
  */
  
  Py_DECREF(result); /*not needed any longer */
  result = NULL;
  
  return LDAP_SUCCESS;
}


/* 
  This function will be called by ldap_sasl_interactive_bind(). The
  "*in" is an array of sasl_interact_t's (see sasl.h for a
  reference). The last interact in the array has an interact->id of
  SASL_CB_LIST_END.

*/

int py_ldap_sasl_interaction(   LDAP *ld, 
				unsigned flags, 
				void *defaults,
				void *in )
{
  /* These are just typecasts */
  sasl_interact_t *interact = in;
  PyObject *SASLObject = defaults;
  /* Loop over the array of sasl_interact_t structs */
  while( interact->id != SASL_CB_LIST_END ) {
    int rc = 0;
    rc = interaction( flags, interact, SASLObject );
    if( rc )  return rc;
    interact++;
  }
  return LDAP_SUCCESS;
}

static PyObject* 
l_ldap_sasl_bind_s( LDAPObject* self, PyObject* args )
{
    char *bind_dn, *c_mechanism;
    PyObject       *SASLObject = NULL;
    PyStringObject *mechanism = NULL;
    int msgid, version;

    void *defaults;
    static unsigned sasl_flags = LDAP_SASL_AUTOMATIC;

    /* first check if we are a LDAPv3 client */
    version = LDAP_VERSION3;
    if (ldap_set_option(self->ldap, 
			LDAP_OPT_PROTOCOL_VERSION, 
			&version) != LDAP_OPT_SUCCESS)
      return NULL;

    if (!PyArg_ParseTuple(args, 
			  "sO",
			  &bind_dn,
			  &SASLObject)) 
      return NULL;

    if (not_valid(self)) return NULL;

    /* now we extract the sasl mechanism from the SASL Object */
    mechanism = PyObject_GetAttrString(SASLObject, "mech");
    if (mechanism == NULL) return NULL;
    c_mechanism = PyString_AsString(mechanism);
    Py_DECREF(mechanism);
    mechanism = NULL;

    /* Don't know if it is the "intended use" of the defaults
       parameter of ldap_sasl_interactive_bind_s when we pass the
       Python object SASLObject, but passing it through some
       static variable would destroy thread safety, IMHO.
     */
    msgid = ldap_sasl_interactive_bind_s(self->ldap, 
					 bind_dn, 
					 c_mechanism, 
					 NULL, 
					 NULL,
					 sasl_flags, 
					 py_ldap_sasl_interaction, 
					 SASLObject);
    if (msgid != LDAP_SUCCESS)
    	return LDAPerror( self->ldap, "ldap_sasl_bind_s" );
    return PyInt_FromLong( msgid );
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

static char doc_set_rebind_proc[] = "";

#endif


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

static char doc_enable_cache[] = "";
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

static char doc_disable_cache[] = "";
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

static char doc_set_cache_options[] = "";
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

static char doc_destroy_cache[] = "";
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

static char doc_flush_cache[] = "";
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

static char doc_uncache_entry[] = "";
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

static char doc_uncache_request[] = "";
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

static char doc_compare[] = "";


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

static char doc_delete[] = "";

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

static char doc_modify[] = "";

/* ldap_rename */

static PyObject *
l_ldap_rename( LDAPObject* self, PyObject *args )
{
    char *dn, *newrdn;
    char *newSuperior = NULL;
    int delold = 1;
    int result, msgid;

    if (!PyArg_ParseTuple( args, "ss|z|i", &dn, &newrdn, &newSuperior, &delold ))
    	return NULL;
    if (not_valid(self)) return NULL;

    LDAP_BEGIN_ALLOW_THREADS( self );
    result = ldap_rename( self->ldap, dn, newrdn, newSuperior, delold, NULL, NULL, &msgid );
    LDAP_END_ALLOW_THREADS( self );
    if ( result != LDAP_SUCCESS )
    	return LDAPerror( self->ldap, "ldap_rename" );
    return PyInt_FromLong( msgid );
}

static char doc_rename[] = "";


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

static char doc_result[] = "";

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

static char doc_search[] = "";

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

static char doc_start_tls[] = "";
;
#endif

/* ldap_manage_dsa_it */

static PyObject*
l_ldap_manage_dsa_it( LDAPObject* self, PyObject* args )
{
    int result, manageDSAit, critical;
    LDAPControl c;
    LDAPControl *ctrls[2];
    ctrls[0] = &c;
    ctrls[1] = NULL;

    if (!PyArg_ParseTuple( args, "i|i", &manageDSAit, &critical )) return NULL;
    if (not_valid(self)) return NULL;

    if ( manageDSAit ) {
        c.ldctl_oid = LDAP_CONTROL_MANAGEDSAIT;
        c.ldctl_value.bv_val = NULL;
        c.ldctl_value.bv_len = 0;
        c.ldctl_iscritical = critical;
        result = ldap_set_option( self->ldap, LDAP_OPT_SERVER_CONTROLS, ctrls );
    } else {
        result = ldap_set_option( self->ldap, LDAP_OPT_SERVER_CONTROLS, NULL );
    }

    if ( result != LDAP_SUCCESS ){
	return LDAPerror( self->ldap, "ldap_manage_dsa_it" );
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static char doc_manage_dsa_it[] = "";
;

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
static char doc_fileno[] = "";
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

static char doc_set_option[] =  "";

/* ldap_get_option */

static PyObject*
l_ldap_get_option(PyObject* self, PyObject *args)
{
    int option;

    if (!PyArg_ParseTuple(args, "i:get_option", &option))
    	return NULL;
    return LDAP_get_option((LDAPObject *)self, option);
}

static char doc_get_option[] =  "";

/* methods */

static PyMethodDef methods[] = {
    {"unbind",		(PyCFunction)l_ldap_unbind,		METH_VARARGS,	doc_unbind},
    {"abandon",		(PyCFunction)l_ldap_abandon,		METH_VARARGS,	doc_abandon},
    {"add",		(PyCFunction)l_ldap_add,		METH_VARARGS,	doc_add},
    {"bind",		(PyCFunction)l_ldap_bind,		METH_VARARGS,	doc_bind},
    {"sasl_bind_s",	(PyCFunction)l_ldap_sasl_bind_s,	METH_VARARGS,	doc_sasl_bind_s},
#if 0    
    {"set_rebind_proc",	(PyCFunction)l_ldap_set_rebind_proc,	METH_VARARGS,	doc_set_rebind_proc},
#endif
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
    {"delete",		(PyCFunction)l_ldap_delete,		METH_VARARGS,	doc_delete},
    {"modify",		(PyCFunction)l_ldap_modify,		METH_VARARGS,	doc_modify},
    {"rename",		(PyCFunction)l_ldap_rename,		METH_VARARGS,	doc_rename},
    {"result",		(PyCFunction)l_ldap_result,		METH_VARARGS,	doc_result},
    {"search",		(PyCFunction)l_ldap_search,		METH_VARARGS,	doc_search},
#ifdef HAVE_LDAP_START_TLS_S
    {"start_tls_s",	(PyCFunction)l_ldap_start_tls_s,	METH_VARARGS,	doc_start_tls},
#endif
    {"manage_dsa_it",	(PyCFunction)l_ldap_manage_dsa_it,	METH_VARARGS,	doc_manage_dsa_it},
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
