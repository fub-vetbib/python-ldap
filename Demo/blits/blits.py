#!/usr/bin/python

"""
##########################################################################
# blits.py - Implementation of
# Basic LDAPv3 Interoperability Test Suite (BLITS)
# for testing compability between python-ldap and a arbitrary
# LDAPv3 server loaded with a specific test data set.
########################################################################
# (C) 2000, Michael Stroeder <michael@stroeder.com>
#
# This software is distributed under the terms of the
# GPL (GNU GENERAL PUBLIC LICENSE) Version 2
# (see http://www.gnu.org/copyleft/gpl.html)
########################################################################

Credits go to Chris Apple, Chris Harding and Ludovic Poitou for defining
the test suite BLITS.

See http://www.opennc.org/directory/mats/blits24/index.htm for details.

Invoke this script for running all tests or import version module
(e.g. blits24) for calling specific test functions.

Each test function is defined as follows:

def test_section(
  l,			# LDAP connection object created with ldap.open()
  x500=1,		# Do X.500 names testing
  dc=1,			# Do dc names testing
  vendor_id=1,		# Vendor ID given by directory manager
  client_id=1		# Client ID given by directory manager
):

##########################################################################
# Coding guide lines for test functions
##########################################################################

Results of test functions:

The test function returns result TEST_FAILED if the result
of the test is not as expected.

The test function MAY return result TEST_ACCEPTABLE
in some rare circumstances if the result of the test is not
as expected by the test definition but the caller could work
around the problem VERY easily. If unsure TEST_FAILED should
be returned. TEST_ACCEPTABLE still means that the test function
did not work conform to LDAPv3 standard.

The test function MUST return result TEST_APPROVED if the test
passed exactly like expected.

##########################################################################

Error/Exception handling:

The test function has to catch all possible LDAP-related
exceptions and has to return a test result like defined above.

For easily finding implementation errors the test function MUST NOT
catch all exceptions with except:.

"""

from blits24 import *

# To avoid too many method calls
blits_sections = blits_desc.keys()
blits_sections.sort()

import sys, string

def test():

  l = None

  all_globals = globals()
  all_globals_keys = all_globals.keys()

  for test in blits_sections:

    if not l or not l.valid:
      l = ldap.open('localhost')

    print test,blits_desc[test]
    fname = 'blits_test_' + string.replace(test,'.','_')
    if not fname in all_globals_keys:
      print 'Test function %s not defined' % fname
    else:
      print 'Executing %s...' % fname
      test_func = all_globals[fname]
      test_func_result = test_func(l)
      if test_func_result is None:
        print 'Test not done.\n'
      else:
        test_result, description = test_func_result
        print 'Test %s: "%s"\n' % (
	  {
	    TEST_FAILED:"failed",
	    TEST_ACCEPTABLE:"acceptable",
	    TEST_APPROVED:"approved"
	  }[test_result],
	  description
	)

  if l and l.valid:
    l.unbind_s()
    

if __name__ == '__main__':
  test()

