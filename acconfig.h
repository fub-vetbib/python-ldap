/* $Id$ */
@TOP@

/*
 * Module version
 */
#define LDAPMODULE_VERSION	major.minor

/*
 * Case-insensitive dictionary used for evil LDAP server responses
 */
#undef USE_CIDICT

/*
 * Use Kerberos authentication
 */
#undef WITH_KERBEROS

/*
 * ldap_set_rebind_proc() with three arguments (Solaris, not OpenLDAP)
 */
#undef LDAP_SET_REBIND_PROC_3ARGS

/*
 * ldap_modrdn_s is documented in the RFC as having 4 args, but OpenLDAP
 * and I think some other libraries don't have the 4th arg - instead
 * they supply a separate function (ldap_modrdn2_s). This is just in case
 * they are broken and don't supply the 2nd form.
 */
#undef LDAP_MODRDN_3ARGS
#undef LDAP_MODRDN_S_3ARGS

/*
 * 'LDAP' is an opaque data type, struct ldap, in ldap.h (iSolaris, Netscape)
 */
#undef LDAP_TYPE_IS_OPAQUE

/*
 * Variant forms of ldap_modrdn2
 */
#undef HAVE_LDAP_MODRDN2_S
#undef HAVE_LDAP_MODRDN2

/*
 * Are templates available?
 */
#undef HAVE_LDAP_INIT_TEMPLATES 
