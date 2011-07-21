.. % $Id$


*********************************************************************
:py:mod:`ldap.controls` High-level access to LDAPv3 extended controls
*********************************************************************

.. py:module:: ldap.controls
   :synopsis: High-level access to LDAPv3 extended controls.
.. moduleauthor:: python-ldap project (see http://www.python-ldap.org/)


Classes
=======

This module defines the following classes:

.. py:class:: LDAPControl(controlType, criticality [, controlValue=:const:`None` [, encodedControlValue=:const:`None`]])

   Base class for all LDAP controls. This class should not be used directly,
   instead one of the following subclasses should be used as appropriate.


   .. py:method:: LDAPControl.encodeControlValue(value)

      Dummy method to be overridden by subclasses.


   .. py:method:: LDAPControl.decodeControlValue(value)

      Dummy method to be overridden by subclasses.


   .. py:method:: LDAPControl.getEncodedTuple()

      Return a readily encoded 3-tuple which can be directly  passed to C module
      :py:mod:_ldap. This method is called by  function :py:func:`ldap.EncodeControlTuples`.


.. py:class:: BooleanControl(controlType, criticality [, controlValue=:const:`None` [, encodedControlValue=:const:`None`]])

   Base class for simple controls with booelan control value.    In this base class
   *controlValue* has to be passed as  boolean type (:const:`True`/:const:`False`
   or :const:`1`/:const:`0`).



.. py:class:: SimplePagedResultsControl(controlType, criticality [, controlValue=:const:`None` [, encodedControlValue=:const:`None`]])

   The class provides the LDAP Control Extension for Simple Paged Results
   Manipulation. *controlType* is ignored  in favor of
   :const:`ldap.LDAP_CONTROL_PAGE_OID`.


   .. seealso::

      :rfc:`2696` - LDAP Control Extension for Simple Paged Results Manipulation


.. py:class:: MatchedValuesControl(criticality [, controlValue=:const:`None`])

   This class provides the LDAP Matched Values control. *controlValue* is an LDAP
   filter.

   .. seealso::

      :rfc:`3876` - Returning Matched Values with the Lightweight Directory Access Protocol version 3 (LDAPv3)


Functions
=========

This module defines the following functions:

.. py:function:: EncodeControlTuples(ldapControls) -> list

   Returns list of readily encoded 3-tuples which can be directly  passed to C
   module _ldap.


.. py:function:: DecodeControlTuples(ldapControlTuples) -> list

   Decodes a list of readily encoded 3-tuples as returned by the C module _ldap.

