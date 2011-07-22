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


.. autoclass:: ldap.controls.RequestControl
   :members:

.. autoclass:: ldap.controls.ResponseControl
   :members:

.. autoclass:: ldap.controls.LDAPControl
   :members:


Functions
=========

This module defines the following functions:


.. autofunction:: ldap.controls.RequestControlTuples

.. autofunction:: ldap.controls.DecodeControlTuples


Sub-modules
===========

Various sub-modules implement specific LDAPv3 extended controls. The classes
therein are derived from the base-classes :py:class:`ldap.controls.RequestControl`
and :py:class:`ldap.controls.ResponseControl`.

Some of them need :py:mod:`pyasn1` and :py:mod:`pyasn1_modules` to be installed.


.. automodule:: ldap.controls.psearch
   :members:

.. automodule:: ldap.controls.simple
   :members:

.. automodule:: ldap.controls.libldap
   :members:

.. automodule:: ldap.controls.sessiontrack
   :members:

