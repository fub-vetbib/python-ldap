/* David Leonard <david.leonard@csee.uq.edu.au>, 1999. Public domain. */
/*
 * LDAPMessageObject - wrapper around an LDAPMessage*
 * $Id$
 */

#include "common.h"
#include "message.h"
#include "errors.h"
#include "CIDict.h"

PyObject*
LDAPmessage_to_python( LDAP*ld, LDAPMessage*m )
{
    /* we convert an LDAP message into a python structure.
     * It is always a list of dictionaries.
     * We always free m.
     */

     PyObject* result;
     LDAPMessage* entry;

     result = PyList_New(0);
     if (result == NULL) {
        ldap_msgfree( m );
	return NULL;
     }

     for(entry = ldap_first_entry(ld,m);
         entry != NULL;
	 entry = ldap_next_entry(ld,entry))
     {
	 char *dn;
	 char *attr;
	 BerElement *ber = NULL;
	 PyObject* entrytuple; 
	 PyObject* attrdict; 

	 dn = ldap_get_dn( ld, entry );
	 if (dn == NULL)  {
	     Py_DECREF(result);
             ldap_msgfree( m );
	     return LDAPerror( ld, "ldap_get_dn" );
	 }

#ifdef USE_CIDICT
	 attrdict = CIDict_New();
#else /* use standard python dictionary */
	 attrdict = PyDict_New();
#endif /* !CIDICT */
	 if (attrdict == NULL) {
		Py_DECREF(result);
		ldap_msgfree( m );
		free(dn);
		return NULL;
	 }

	 /* Fill attrdict with lists */
	 for( attr = ldap_first_attribute( ld, entry, &ber );
	      attr != NULL;
	      attr = ldap_next_attribute( ld, entry, ber )
	 ) {
	     PyObject* valuelist;
	     struct berval ** bvals =
	     	ldap_get_values_len( ld, entry, attr );

	     /* Find which list to append to */
	     if ( PyMapping_HasKeyString( attrdict, attr ) ) {
		 valuelist = PyMapping_GetItemString( attrdict, attr );
	     } else {
		 valuelist = PyList_New(0);
		 if (valuelist != NULL && PyMapping_SetItemString(attrdict, 
		     attr, valuelist) == -1) {
			Py_DECREF(valuelist);
			valuelist = NULL;	/* catch error later */
		 }
	     }

	     if (valuelist == NULL) {
		Py_DECREF(attrdict);
		Py_DECREF(result);
		ldap_msgfree( m );
		free(dn);
		return NULL;
	     }

	     if (bvals != NULL) {
	        int i;
		for (i=0; bvals[i]; i++) {
		    PyObject *valuestr;

		    valuestr = PyString_FromStringAndSize( 
			    bvals[i]->bv_val, bvals[i]->bv_len 
			);
		    if (PyList_Append( valuelist, valuestr ) == -1) {
			Py_DECREF(attrdict);
			Py_DECREF(result);
			Py_DECREF(valuestr);
			Py_DECREF(valuelist);
			ldap_msgfree( m );
			free(dn);
			return NULL;
		    }
		    Py_DECREF(valuestr);
	    	}
		ldap_value_free_len(bvals);
	     }
	     Py_DECREF( valuelist );
	 }

	 entrytuple = Py_BuildValue("(sO)", dn, attrdict);
         free(dn);
	 Py_DECREF(attrdict);
	 PyList_Append(result, entrytuple);
	 Py_DECREF(entrytuple);
     }
     ldap_msgfree( m );
     return result;
}
