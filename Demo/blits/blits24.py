########################################################################
# Basic LDAPv3 Interoperability Test Suite (BLITS) Issue 2.4 Draft 1
########################################################################

# Result types
TEST_FAILED            = -1
TEST_ACCEPTABLE        = 0
TEST_APPROVED          = 1

blits_desc = {

  '3.3.1':'Bind/Unbind Tests',
  '3.3.1.1':'Anonymous Bind',
  '3.3.1.2':'Unbind',
  '3.3.1.3':'Bind With Correct Credentials',
  '3.3.1.3.1':'Bind With Simple Password',
  '3.3.1.3.2':'Bind With DIGEST-MD5 Password Exchange',
  '3.3.1.4':'Bind Errors',
  '3.3.1.4.1':'Bind with Incorrect Credentials',
  '3.3.1.4.2':'Bind With Missing Password',
  '3.3.1.4.3':'BIND with Invalid DN Syntax',
  '3.3.1.4.4':'BIND with Inappropriate Authentication',
  '3.3.1.4.5':'BIND with Unsupported Protocol Version',
  '3.3.1.4.6':'Bind with Incorrect Credentials using DIGEST-MD5',
  '3.3.2':'Search Tests',
  '3.3.2.1':'Simple Search Filters',
  '3.3.2.1.1':'Equality Matching',
  '3.3.2.1.2':'Substring Matching',
  '3.3.2.1.3':'Approximate Matching',
  '3.3.2.1.4':'Less-Than-Or-Equal-To Matching',
  '3.3.2.1.5':'Greater-Than-Or-Equal-To Matching',
  '3.3.2.1.6':'Presence Matching',
  '3.3.2.1.7':'Extensible Matching',
  '3.3.2.2':'Complex Search Filters',
  '3.3.2.2.1':'Unnested Boolean AVA Combinations',
  '3.3.2.2.1.1':'Equality AND Presence',
  '3.3.2.2.1.3':'Substring OR Substring',
  '3.3.2.2.1.4':'Substring OR Approximate',
  '3.3.2.2.2':'Negation of AVAs',
  '3.3.2.2.2.1':'NOT Presence (for person objects)',
  '3.3.2.2.2.2':'NOT Substring (for person objects)',
  '3.3.2.2.3':'Nested Boolean AVA Combinations',
  '3.3.2.2.3.1':'(Substring OR Substring) AND (Presence AND Presence)',
  '3.3.2.2.3.2':' (Approximate AND Substring) OR (Approximate AND Substring)',
  '3.3.2.2.3.3':'NOT (Presence OR Presence) (for person objects)',
  '3.3.2.3':'Search for Entry with Multi-Valued RDN',
  '3.3.2.4':'Three-Valued Logic Search Filter Evaluation',
  '3.3.2.4.1':'Filter of "AND" Choice with an Undefined Attribute Type (Evaluates to UNDEFINED)',
  '3.3.2.4.2':'Filter of "OR" Choice with an Undefined Attribute Type (Evaluates to TRUE)',
  '3.3.2.4.3':'Filter of "NOT" Choice with an Undefined Attribute Type (Evaluates to UNDEFINED)',
  '3.3.2.5':'Unrecognized Option in Attribute Description List',
  '3.3.2.6':'Retrieve Operational Attributes for an Entry',
  '3.3.2.7':'Alias Dereferencing',
  '3.3.2.7.1':'Never Dereference Aliases - Aliased Base Object',
  '3.3.2.7.2':'Never Dereference Aliases - Aliased Leaf Object',
  '3.3.2.7.3':'Dereference Aliases in Searching - Aliased Base Object',
  '3.3.2.7.4':'Dereference Aliases in Searching - Aliased Leaf Object',
  '3.3.2.7.5':'Dereference Finding Base Object - Aliased Base Object',
  '3.3.2.7.6':'Dereference Finding Base Object - Aliased Leaf Object',
  '3.3.2.7.7':'Always Dereference - Aliased Base Object',
  '3.3.2.7.8':'Always Dereference - Aliased Leaf Object',
  '3.3.2.8':'Miscellaneous Searching Feature Tests',
  '3.3.2.8.1':'Search Result Size Limit',
  '3.3.2.8.2':'Search Time Limit',
  '3.3.2.8.3':'Return Attribute Types Only',
  '3.3.2.9':'Search Operation Errors',
  '3.3.2.9.1':'Invalid Search Filter Syntax',
  '3.3.2.9.2':'noSuchObject Error for Subtree Search',
  '3.3.2.9.3':'noSuchObject for Single-Level Search',
  '3.3.2.9.4':'noSuchObject for Base-Level Search',
  '3.3.2.9.5':'invalidDNSyntax for Subtree Search',
  '3.3.2.9.6':'invalidDNSyntax for Single-Level Search',
  '3.3.2.9.7':'invalidDNSyntax for Base-Level Search',
  '3.3.3':'Modify Operation Tests',
  '3.3.3.1':'Modify-Add Tests',
  '3.3.3.1.1':'Add Value - Create Attribute',
  '3.3.3.1.2':'Add Value to Existing Attribute',
  '3.3.3.1.3':'Modify-Add Errors',
  '3.3.3.1.3.1':'attributeOrValueExists',
  '3.3.3.1.3.2':'invalidAttributeSyntax',
  '3.3.3.1.3.3':'invalidDNSyntax',
  '3.3.3.2':'Modify-Delete Tests',
  '3.3.3.2.1':'Delete One Value of a Multi-valued Attribute',
  '3.3.3.2.2':'Delete Single-Valued Attribute',
  '3.3.3.2.3':'Delete Multi-Valued Attribute',
  '3.3.3.2.4':'Modify-Delete Errors',
  '3.3.3.2.4.1':'noSuchAttribute with Attribute Type Only',
  '3.3.3.2.4.2':'noSuchAttribute with Attribute Type-Value Pair',
  '3.3.3.2.4.3':'noSuchAttribute with Incorrect Attribute Value',
  '3.3.3.2.4.4':'objectClassViolation',
  '3.3.3.3':'Modify-Replace Tests',
  '3.3.3.3.1':'Replace Multi-Valued Attribute with Single Value',
  '3.3.3.3.2':'Replace Single-Valued Attribute',
  '3.3.3.3.3':'Delete Attribute Using Modify-Replace',
  '3.3.3.3.4':'Modify-Replace Errors',
  '3.3.3.3.4.1':'noSuchObject',
  '3.3.3.3.4.2':'notAllowedOnRDN',
  '3.3.4':'Add Operation Tests',
  '3.3.4.1':'Add New Entry',
  '3.3.4.2':'Add Errors',
  '3.3.4.2.1':'noSuchObject',
  '3.3.4.2.2':'invalidDNSyntax',
  '3.3.4.2.3':'entryAlreadyExists',
  '3.3.4.2.4':'objectClassViolation',
  '3.3.5':'Delete Operation Tests',
  '3.3.5.1':'Delete Existing Object',
  '3.3.5.2':'Delete Errors',
  '3.3.5.2.1':'noSuchObject',
  '3.3.5.2.2':'invalidDNSyntax',
  '3.3.5.2.3':'notAllowedOnNonLeaf',
  '3.3.6':'ModifyDN Operation Tests',
  '3.3.6.1':'Rename a Leaf Entry',
  '3.3.6.2':'Move a Leaf Entry to A New Parent',
  '3.3.6.3':'Move a Renamed Leaf Entry to A New Parent',
  '3.3.6.4':'Rename Subtree of Entries',
  '3.3.6.5':'Move Subtree of Entries',
  '3.3.6.6':'Move a Renamed Subtree of Entries to a New Parent',
  '3.3.6.7':'ModifyDN Errors',
  '3.3.6.7.1':'entryAlreadyExists',
  '3.3.6.7.2':'noSuchObject',
  '3.3.6.7.3':'invalidDNSyntax with Bad DN',
  '3.3.6.7.4':'invalidDNSyntax with Bad RDN',
  '3.3.7':'Compare Operation Tests',
  '3.3.7.1':'Comparison with FALSE Return Code',
  '3.3.7.2':'Comparison with TRUE Return Code',
  '3.3.7.3':'Compare Errors',
  '3.3.7.3.1':'noSuchAttribute',
  '3.3.7.3.2':'noSuchObject',
  '3.3.7.3.3':'invalidDNSyntax',
  '3.3.8':'Extended Operations Tests',
  '3.3.9':'Charset-Related Tests',
  '3.3.10':'DN Quoting Form Tests',
  '3.3.11':'Certificate Storage, Retrieval, and Comparison',
  '3.3.11.1':'Search',
  '3.3.11.1.1':'Search for Entry Containing a User Certificate',
  '3.3.11.1.2':'Search for Entry Not Containing a User Certificate',
  '3.3.11.1.3':'Search for Entry Containing a CA Certificate',
  '3.3.11.1.4':'Search for Entry Not Containing a CA Certificate',
  '3.3.11.1.5':'Search for Entry Containing a CRL',
  '3.3.11.2':'Compare',
  '3.3.11.3':'Add and Modify Entries',
  '3.3.11.3.1':'Add Entry with Certificate',
  '3.3.11.3.2':'Modify-Add Tests',
  '3.3.11.3.2.1':'Create userCertificate Attribute',
  '3.3.11.3.2.2':'Add userCertificate Value to Existing Attribute',
  '3.3.11.3.2.3':'Create cACertificate Attribute',
  '3.3.11.3.2.4':'Create certificateRevocationList Attribute',
  '3.3.11.3.3':'Modify-Delete Tests',
  '3.3.11.3.3.1':'Delete One Value of a Multi-valued userCertificate Attribute',
  '3.3.11.3.3.2':'Delete Single-Valued userCertificate Attribute',
  '3.3.11.3.4':'Replace userCertificate Attribute',
  '3.3.12':'LDAP Extension Tests',
  '3.3.12.1':'Paged Results',
  '3.3.12.1.1':'Page completely through a set.',
  '3.3.12.1.2':'Abort paging part-way through a set.',
  '3.3.12.2':'Server-Side Sorting',
  '3.3.12.2.1':'Sort on Single Numeric Attribute',
  '3.3.12.2.2':'Sort on Single Alphabetic Attribute',
  '3.3.12.2.3':'Sort on Multiple Attributes',
  '3.3.12.2.4':'Sort in reverse order',
  '3.3.12.3':'Feature Interactions with Paged and Sorted Results',
  '3.3.12.3.1':'Page a Sorted Set.',
  '3.3.12.4':'Scrolling View Browsing of Search Results',
  '3.3.12.4.1':'Scroll Completely Through Large Set of Results',
  '3.3.12.4.2':'Scroll Incrementally through Set of Results',
  '3.3.12.4.3':'Scroll Part Way Through Large Set of Results',
  '3.3.12.4.4':'Go to Arbitrary Place in Large Set of Results',
  '3.3.12.5':'Language Tags',
  '3.3.12.5.1':'Search for Language Tagged Attributes.',
  '3.3.12.5.2':'Check Attribute Subtype Matching.',
  '3.3.12.5.3':'Search Without Specifying Language Tags.',
  '3.3.12.5.4':'Comparison with TRUE Return Code',
  '3.3.12.5.5':'Comparison with noSuchAttribute Return Code',
  '3.3.12.5.6':'Search for Tagged Attribute Types',
  '3.3.12.5.7':'Add and Modify Entries',
  '3.3.12.5.7.1':'Add Entry with Language Tags',
  '3.3.12.5.7.2':'Modify Entry with Language Tags',
  '3.3.13':'Schema-Related Tests',
  '3.3.13.1':'Schema Access tests.',
  '3.3.13.1.1':'subSchemaSubEntry attribute in root DSE.',
  '3.3.13.1.2':'subSchemaSubEntry attribute in any entry.',
  '3.3.13.1.3':'Schema publication.',
  '3.3.13.2':'Schema Modification tests.',
  '3.3.13.2.1':'Adding an Object class.',
  '3.3.13.2.2':'Removing an Object class.',
  '3.3.13.2.3':'Adding an Attribute definition in the schema.',
  '3.3.13.2.4':'Removing an Attribute definition from the schema.',
  '3.3.14':'Referral Tests',
  '3.3.14.1':'Superior Reference',
  '3.3.14.2':'Subordinate Reference',
  '3.3.14.3':'Named Referral',
  '3.3.14.3.1':'Base Contains Ref Attribute',
  '3.3.14.3.2':'Target Contains Ref Attribute',
  '3.3.14.3.3':'Base Subordinate to Entry that Contains Ref Attribute',
  '3.3.14.3.4':'Target Subordinate to Entry that Contains Ref Attribute',
  '3.3.14.3.5':'Single-Level Search',
  '3.3.14.3.6':'Subtree Search',
  '3.3.15':'Transport Security',
  '3.3.15.1':'START TLS',
  '3.3.15.1.1':'Anonymous Bind over TLS',
  '3.3.15.1.2':'Bind With Password Exchange over TLS',
  '3.3.15.1.3':'TLS with Certificates',
  '3.3.15.1.3.1':'TLS Bind with Valid Certificate',
  '3.3.15.1.3.2':'TLS Bind with Expired Certificate',
  '3.3.15.1.3.3':'TLS Bind with Certificate Validated via Non-Trivial Path',
  '3.3.15.1.3.4':'TLS Bind with Revoked Certificate in Validation Path',
  '3.3.15.1.4':'Bind with Incorrect Credentials over TLS',
  '3.3.15.1.5':'Bind With Insufficiently Strong Authentication',
  '3.3.15.1.6':'Abort TLS Session',
  '3.3.15.2':'Port 636',
  '3.3.15.2.1':'Anonymous Bind over TLS',
  '3.3.15.2.2':'Bind With Password Exchange over TLS',
  '3.3.15.2.3':'TLS with Certificates',
  '3.3.15.2.3.1':'TLS Bind with Valid Certificate',
  '3.3.15.2.3.2':'TLS Bind with Expired Certificate',
  '3.3.15.2.3.3':'TLS Bind with Certificate Validated via Non-Trivial Path',
  '3.3.15.2.3.4':'TLS Bind with Revoked Certificate in Validation Path',
  '3.3.15.2.4':'Bind with Incorrect Credentials over TLS',
  '3.3.15.2.5':'Bind With Insufficiently Strong Authentication',
  '3.3.15.2.6':'Abort TLS Session',
  '3.3.16':'Server Location',
  '3.3.16.1':'Locate Server',

}

import ldap


# Bind/Unbind Tests
def blits_test_3_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """


# Anonymous Bind
def blits_test_3_3_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Bind Anonymously to an LDAP server.                            |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.2, pp. 20-23)                          |
+---------+---------------------------------------------------------------+
|Procedure|Issues  a  Bind request to an LDAP server with null credentials|
|         |(anonymous bind)                                               |
+---------+---------------------------------------------------------------+
|Expected |The   test   is  successful  if  the  LDAP  connection  can  be|
|Results  |established  without  errors.  Search  requests  should  now be|
|         |accepted and processed by the server.                          |
+---------+---------------------------------------------------------------+
  """

  try:
    l.bind_s('','',ldap.AUTH_SIMPLE)
  except ldap.LDAPError,e:
    return (TEST_FAILED, str(e))
  else:
    return (TEST_APPROVED, '')


# Unbind
def blits_test_3_3_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+--------------+----------------------------------------------------------+
|Purpose       |Unbind from an LDAP server.                               |
+--------------+----------------------------------------------------------+
|Reference     |[RFC 2251] (paragraph 4.3, pp. 19-20 )                    |
+--------------+----------------------------------------------------------+
|Procedure     |An UNBIND operation must be issued to the responding LDAP |
|              |server.                                                   |
+--------------+----------------------------------------------------------+
|Expected      |The  test  is  successful  if  the association is released|
|Results       |gracefully.                                               |
+--------------+----------------------------------------------------------+
  """

  try:
    l.unbind_s()
  except ldap.LDAPError,e:
    return (TEST_FAILED, str(e))
  else:
    return (TEST_APPROVED, '')


# Bind With Correct Credentials
def blits_test_3_3_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Bind With Simple Password
def blits_test_3_3_1_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  authenticated  unprotected  simple  bind  with  correct|
|           |credentials.                                                 |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.2)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Test  simple  authenticated  Bind  as  'Paul  Cezanne' with a|
|           |correct password ('Paul0005').                               |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, ou=Americas, ou=Search, o=IMC, c=US         |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, dc=Americas, dc=Search, dc=Relative,  dc=   |
|(dc-naming)|IMC, dc=ORG                                                  |
+-----------+-------------------------------------------------------------+
|Password   |Paul0005                                                     |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is  successful  if  the Bind is successful. Search|
|results    |requests should now be accepted and processed by the server. |
+-----------+-------------------------------------------------------------+
  """

  try:
    if x500:
      l.bind_s(
        'cn=Paul Cezanne, ou=Americas, ou=Search, o=IMC, c=US',
	'Paul0005',
	ldap.AUTH_SIMPLE
      )
    if dc:
      l.bind_s(
        'cn=Paul Cezanne, dc=Americas, dc=Search, dc=Relative,  dc=IMC, dc=ORG',
	'Paul0005',
	ldap.AUTH_SIMPLE
      )
  except ldap.LDAPError,e:
    return (TEST_FAILED, str(e))
  else:
    return (TEST_APPROVED, '')


# Bind With DIGEST-MD5 Password Exchange
def blits_test_3_3_1_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test authenticated DIGEST-MD5 bind with correct credentials. |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2829] (paragraph 6.1), [RFC 2251] (paragraph 4.2)       |
+-----------+-------------------------------------------------------------+
|Procedure  |Configure  client  to  use  DIGEST-MD5  authentication.  Test|
|           |authenticated Bind as 'Marc Chagall' with a correct password |
|           |('Marc0001').                                                |
+-----------+-------------------------------------------------------------+
|DN         |cn= Marc Chagall, ou=Security, o=IMC, c=US                   |
+-----------+-------------------------------------------------------------+
|DN         |cn= Marc Chagall, dc=Security, dc=Relative,  dc=IMC, dc=ORG  |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Password   |Marc0001                                                     |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is  successful  if  the Bind is successful. Search|
|results    |requests should now be accepted and processed by the server. |
+-----------+-------------------------------------------------------------+
  """

  try:
    if x500:
      l.bind_s(
        'cn=Marc Chagall, ou=Security, o=IMC, c=US',
	'Marc0001',
	ldap.AUTH_SIMPLE
      )
    if dc:
      l.bind_s(
        'cn=Marc Chagall, dc=Security, dc=Relative, dc=IMC, dc=ORG',
	'Marc0001',
	ldap.AUTH_SIMPLE
      )
  except ldap.LDAPError,e:
    return (TEST_FAILED, str(e))
  else:
    return (TEST_APPROVED, '')


# Bind Errors
def blits_test_3_3_1_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Bind with Incorrect Credentials
def blits_test_3_3_1_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  authenticated  unprotected  simple  bind with incorrect|
|           |credentials.                                                 |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraphs 4.1.10, 4.2)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Attempt  to  Bind as a DN which has a userPassword attribute,|
|           |but specify the wrong password.                              |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, ou=Americas, ou=Search, o=IMC, c=US         |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, dc=Americas, dc=Search, dc=Relative,  dc=   |
|(dc-naming)|IMC, dc=ORG                                                  |
+-----------+-------------------------------------------------------------+
|Password   |Wrong (The correct password is Paul0005)                     |
+-----------+-------------------------------------------------------------+
|Expected   |Result  code  49 (invalidCredentials) should be returned. The|
|results    |Bind  should  fail.  The  server  may  not accept and process|
|           |requests;  if  they  are  accepted, they should be treated as|
|           |anonymous requests.                                          |
+-----------+-------------------------------------------------------------+
  """

# Bind With Missing Password
def blits_test_3_3_1_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  authenticated  unprotected  simple  Bind  with  missing|
|           |password.                                                    |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraphs 4.1.10, 4.2)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Test authenticated unprotected simple Bind as 'Paul Cezanne' |
|           |with a null password.                                        |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, ou=Americas, ou=Search, o=IMC, c=US         |
+-----------+-------------------------------------------------------------+
|DN         |cn=Paul Cezanne, dc=Americas, dc=Search, dc=Relative,  dc=   |
|(dc-naming)|IMC, dc=ORG                                                  |
+-----------+-------------------------------------------------------------+
|Password   |<unspecified>                                                |
+-----------+-------------------------------------------------------------+
|Expected   |The test is successful if the connection attempt is accepted,|
|results    |but established as an anonymous bind. Search requests should |
|           |now be accepted and processed by the server.                 |
+-----------+-------------------------------------------------------------+
  """

# BIND with Invalid DN Syntax
def blits_test_3_3_1_4_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  correct  behavior  when  a  DN  of  invalid syntax is|
|           |included in a Bind attempt.                                  |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraphs 4.1.10, 4.2)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Bind  supplying  a DN with an invalid syntax and an arbitrary|
|           |value for the userPassword attribute.                        |
+-----------+-------------------------------------------------------------+
|DN         |cn, ou=Americas, ou=Search, o=IMC, c=US                      |
+-----------+-------------------------------------------------------------+
|DN         |cn, dc=Americas, dc=Search,  dc=Relative, dc=IMC, dc=ORG     |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Password   |AnythingYouWant                                              |
+-----------+-------------------------------------------------------------+
|Expected   |The  Bind  should  fail.  Requests  may  not  be accepted and|
|results    |processed by the server; if they are accepted, they should be|
|           |treated as anonymous requests.                               |
+-----------+-------------------------------------------------------------+
  """

# BIND with Inappropriate Authentication
def blits_test_3_3_1_4_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify correct behavior when inappropriate authentication is |
|           |used on a Bind attempt.                                      |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraphs 4.1.10, 4.2)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Test  authenticated  unprotected  simple  Bind  as 'Directory|
|           |Manager' with a null password.                               |
+-----------+-------------------------------------------------------------+
|DN         |cn=Directory Manager, o=IMC, c=US                            |
+-----------+-------------------------------------------------------------+
|DN         |cn=Directory Manager,  dc=Relative, dc=IMC, dc=ORG           |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Password   |(None)                                                       |
+-----------+-------------------------------------------------------------+
|Expected   |Result   code   48  (inappropriateAuthentication)  should  be|
|results    |returned. The Bind should fail. Requests may not be accepted |
|           |and processed by the server.                                 |
+-----------+-------------------------------------------------------------+
  """

# BIND with Unsupported Protocol Version
def blits_test_3_3_1_4_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  correct  behavior  when an unsupported protocol version|
|         |parameter value is supplied on a Bind attempt.                 |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraphs 4.1.10, 4.2)                            |
+---------+---------------------------------------------------------------+
|Procedure|Bind, anonymously with a null DN, supplying a version number of|
|         |4.                                                             |
+---------+---------------------------------------------------------------+
|DN       |null                                                           |
+---------+---------------------------------------------------------------+
|Password |null                                                           |
+---------+---------------------------------------------------------------+
|Expected |Result  code  2  (protocolError)  should  be returned. The Bind|
|results  |should fail. Requests may not be accepted and processed by the |
|         |server;  if  they  are  accepted,  they  should  be  treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# Bind with Incorrect Credentials using DIGEST-MD5
def blits_test_3_3_1_4_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test    authenticated    DIGEST-MD5   bind   with   incorrect|
|           |credentials.                                                 |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2829] (paragraph 6.1), [RFC 2251] (paragraphs 4.1.10,   |
|           |4.2)                                                         |
+-----------+-------------------------------------------------------------+
|Procedure  |Configure  client  to  use  DIGEST-MD5  authentication.  Test|
|           |authenticated Bind as 'Marc Chagall' with incorrect password |
|           |('Marc1110').                                                |
+-----------+-------------------------------------------------------------+
|DN         |cn=Marc Chagall, ou=Security, o=IMC, c=US                    |
+-----------+-------------------------------------------------------------+
|DN         |cn=Marc Chagall, dc=Security,  dc=Relative, dc=IMC, dc=ORG   |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Password   |Marc1110                                                     |
+-----------+-------------------------------------------------------------+
|Expected   |Result  code  49 (invalidCredentials) should be returned. The|
|results    |Bind  should  fail.  The  server  may  not accept and process|
|           |requests;  if  they  are  accepted, they should be treated as|
|           |anonymous requests.                                          |
+-----------+-------------------------------------------------------------+
  """

# Search Tests
def blits_test_3_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Simple Search Filters
def blits_test_3_3_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Equality Matching
def blits_test_3_3_2_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Test equality matching in simple search filter.            |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                    |
+-------------+-----------------------------------------------------------+
|Procedure    |Submit  a  Search request with a filter, base, and scope as|
|             |indicated below.                                           |
+-------------+-----------------------------------------------------------+
|Base         |ou=Search, o=IMC, c=US                                     |
+-------------+-----------------------------------------------------------+
|Base         |dc=Search, dc=Relative, dc=IMC, dc=org                     |
|(dc-naming)  |                                                           |
+-------------+-----------------------------------------------------------+
|Scope        |subtree                                                    |
+-------------+-----------------------------------------------------------+
|Filter       |cn=Pat Bakers                                              |
+-------------+-----------------------------------------------------------+
|Expected     |The following entry should be returned: Pat Bakers         |
|results      |                                                           |
+-------------+-----------------------------------------------------------+
  """

# Substring Matching
def blits_test_3_3_2_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Test substring matching in simple search filter.           |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                    |
+-------------+-----------------------------------------------------------+
|Procedure    |Submit  a  Search request with a filter, base, and scope as|
|             |indicated below.                                           |
+-------------+-----------------------------------------------------------+
|Base         |ou=Search, o=IMC, c=US                                     |
+-------------+-----------------------------------------------------------+
|Base         |dc=Search, dc=Relative, dc=IMC, dc=org                     |
|(dc-naming)  |                                                           |
+-------------+-----------------------------------------------------------+
|Scope        |subtree                                                    |
+-------------+-----------------------------------------------------------+
|Filter       |cn=p*smith                                                 |
+-------------+-----------------------------------------------------------+
|Expected     |The  following  entries  should  be  returned:  Peter Smith|
|results      |Paulette Smith                                             |
+-------------+-----------------------------------------------------------+
  """

# Approximate Matching
def blits_test_3_3_2_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test approximate matching in simple search filter.           |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit  a  Search  request  with a filter, base, and scope as|
|           |indicated below.                                             |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |cn~=clint                                                    |
+-----------+-------------------------------------------------------------+
|Expected   |The following entries should be returned: Clint Eastwood Bill|
|results    |Clinton Hillory Clinton                                      |
+-----------+-------------------------------------------------------------+
  """

# Less-Than-Or-Equal-To Matching
def blits_test_3_3_2_1_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test less-than-or-equal-to matching in simple search filter. |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit  a  Search  request  with a filter, base, and scope as|
|           |indicated below.                                             |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber<=1100008                                      |
+-----------+-------------------------------------------------------------+
|Expected   |The  5  following  entries  should be returned: Paul Cezanne,|
|results    |Johan  Jongkind,  Johan  Jongkind  (No  Title), Milton Berle,|
|           |Clint Eastwood                                               |
+-----------+-------------------------------------------------------------+
  """

# Greater-Than-Or-Equal-To Matching
def blits_test_3_3_2_1_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test   greater-than-or-equal-to  matching  in  simple  search|
|           |filter.                                                      |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber>=2200500                                      |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entries should be returned: Kip Barker, Larry|
|results    |Barker, Leslie Barker, Lincoln Barker, Linda Barker          |
+-----------+-------------------------------------------------------------+
  """

# Presence Matching
def blits_test_3_3_2_1_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test presence matching in simple search filter.             |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Fin-Accounting, ou=Americas, ou=Search, o=IMC, c=US      |
+------------+------------------------------------------------------------+
|Base        |dc=Fin-Accounting, dc=Americas, dc=Search, dc=Relative, dc= |
|(dc-naming) |IMC, dc=org                                                 |
+------------+------------------------------------------------------------+
|Scope       |single-level                                                |
+------------+------------------------------------------------------------+
|Filter      |title=*                                                     |
+------------+------------------------------------------------------------+
|Expected    |The  following  entry  should  be  returned:  Johan Jongkind|
|results     |(title VP)                                                  |
+------------+------------------------------------------------------------+
  """

# Extensible Matching
def blits_test_3_3_2_1_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
TBD, but to be based on extensible matching rules listed in [RFC 2252] and
the description of extensible matching in searchRequest [RFC 2251].
  """

# Complex Search Filters
def blits_test_3_3_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Unnested Boolean AVA Combinations
def blits_test_3_3_2_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Equality AND Presence
def blits_test_3_3_2_2_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test  equality  and presence matching combination in complex|
|            |search filter.                                              |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Search, o=IMC, c=US                                      |
+------------+------------------------------------------------------------+
|Base        |dc=Search, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |(&(sn=thatcher)(title=*))                                   |
+------------+------------------------------------------------------------+
|Expected    |The  following  entry  should be returned: Margaret Thatcher|
|results     |(title: Director)                                           |
+------------+------------------------------------------------------------+
  """

# Substring AND Presence
def blits_test_3_3_2_2_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test substring and presence matching combination in complex |
|            |search filter.                                              |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Search, o=IMC, c=US                                      |
+------------+------------------------------------------------------------+
|Base        |dc=Search, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |(&(cn=cl*ews)(title=*))                                     |
+------------+------------------------------------------------------------+
|Expected    |The  following  entry  should  be  returned:  Cliff  Andrews|
|results     |(title: Associate)                                          |
+------------+------------------------------------------------------------+
  """

# Substring OR Substring
def blits_test_3_3_2_2_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  multiple  substring  matching  combination  in  complex|
|           |search filter.                                               |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(|(cn=*od)(cn=*ad))                                          |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entries  should  be returned: Clint Eastwood,|
|results    |Charlie Abood, Henry Atwood, Alice Frostad                   |
+-----------+-------------------------------------------------------------+
  """

# Substring OR Approximate
def blits_test_3_3_2_2_1_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test  substring  and  approximate  matching  combination  in|
|            |complex search filter.                                      |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Search, o=IMC, c=US                                      |
+------------+------------------------------------------------------------+
|Base        |dc=Search, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |(|(cn=*homer*)(cn~=body))                                   |
+------------+------------------------------------------------------------+
|Expected    |The  following  entries  should  be returned: Homer Winslow,|
|results     |Bette Davis, Buddy Holly                                    |
+------------+------------------------------------------------------------+
  """

# Negation of AVAs
def blits_test_3_3_2_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# NOT Presence (for person objects)
def blits_test_3_3_2_2_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test presence (for person objects) matching in search filter|
|            |that includes negation.                                     |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Europe, ou=Search, o=IMC, c=US                           |
+------------+------------------------------------------------------------+
|Base        |dc=Europe, dc=Search, dc=Relative, dc=IMC, dc=org           |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |single-level                                                |
+------------+------------------------------------------------------------+
|Filter      |(&(!(description=*))(objectclass=person))                   |
+------------+------------------------------------------------------------+
|Expected    |The following entry should be returned: Jonathan Adams      |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# NOT Substring (for person objects)
def blits_test_3_3_2_2_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test presence (for person objects) matching in search filter|
|            |that includes negation.                                     |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Sales, ou=Europe,ou=Search, o=IMC, c=US                  |
+------------+------------------------------------------------------------+
|Base        |dc=Sales, dc=Europe,dc=Search, dc=Relative, dc=IMC, dc=org  |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |single-level                                                |
+------------+------------------------------------------------------------+
|Filter      |(&(!(sn=wa*))(objectclass=person))                          |
+------------+------------------------------------------------------------+
|Expected    |The following entry should be returned: Paulette Smith      |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Nested Boolean AVA Combinations
def blits_test_3_3_2_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# (Substring OR Substring) AND (Presence AND Presence)
def blits_test_3_3_2_2_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test   a   search  filter  with  AVAs  having  the  following|
|           |combination of match type operators (Substring OR Substring) |
|           |AND (Presence AND Presence)                                  |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(& (|(sn=*ood*)(sn=*woo*)) (&(telephonenumber=*)(title=*)) ) |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entries  should  be returned: Clint Eastwood,|
|results    |Merry  Aboods,  Charlie  Abood, Brian Atwoods, Henry Atwoods,|
|           |Henry Atwood                                                 |
+-----------+-------------------------------------------------------------+
  """

# (Approximate AND Substring) OR (Approximate AND Substring)
def blits_test_3_3_2_2_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |(Approximate AND Sub-string) OR (Approximate AND Sub-string) |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(| (&(cn~=body)(telephonenumber=*825*)) (&(cn~=smythe)       |
|           |(telephonenumber=*720*)) )                                   |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entries  should  be  returned:  Peter  Smith,|
|results    |Paulette Smith, Bette Davis, Buddy Holly                     |
+-----------+-------------------------------------------------------------+
  """

# NOT (Presence OR Presence) (for person objects)
def blits_test_3_3_2_2_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |NOT (Presence OR Presence) (for person objects)             |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Americas, ou=Search, o=IMC, c=US                         |
+------------+------------------------------------------------------------+
|Base        |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org         |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |single-level                                                |
+------------+------------------------------------------------------------+
|Filter      |(&(!(|(internationaliSDNNumber=*)(description=*)))          |
|            |(objectclass=person))                                       |
+------------+------------------------------------------------------------+
|Expected    |The following entry should be returned: Paul Cezanne        |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Search for Entry with Multi-Valued RDN
def blits_test_3_3_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Read the entry with the common name of 'cn=Pablo Picasso' and|
|           |the  user  identifier  of 'uid=00123456789', to check that an|
|           |entry with a multi-valued RDN can be retrieved correctly     |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28), [RFC 2253]          |
+-----------+-------------------------------------------------------------+
|Procedure  |Instruct  the  LDAP  user agent to locate and display all the|
|           |attributes for the entry with the common name 'Pablo Picasso'|
|           |and the user identifier of '00123456789'.                    |
+-----------+-------------------------------------------------------------+
|Base       |cn=Pablo Picasso + uid=00123456789, ou=Search, o=IMC, c=US   |
+-----------+-------------------------------------------------------------+
|Base       |cn=Pablo  Picasso  + uid=00123456789, dc=Search, dc=Relative,|
|(dc-naming)|dc=IMC, dc=org                                               |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(objectclass=*)                                              |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is successful if the entry is returned and all the|
|Results    |attributes are displayed.                                    |
+-----------+-------------------------------------------------------------+
  """

# Three-Valued Logic Search Filter Evaluation
def blits_test_3_3_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Filter of "AND" Choice with an Undefined Attribute Type
def blits_test_3_3_2_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
(Evaluates to UNDEFINED)

+-----------+-------------------------------------------------------------+
|Purpose    |Search  for  entries  with  a  common name value of "Margaret|
|           |Thatcher"  and  include an unrecognized attribute type in the|
|           |search filter.                                               |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 27-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Instruct  the  LDAP  user agent to search for and display all|
|           |entries matching the search filter below.                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(&(cn=Margaret Thatcher)(foo=bar))                           |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is  successful if no entries are displayed because|
|Results    |the search filter evaluates to UNDEFINED.                    |
+-----------+-------------------------------------------------------------+
  """

# Filter of "OR" Choice with an Undefined Attribute Type (Evaluates to TRUE)
def blits_test_3_3_2_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search  for  entries  with  a  common name value of "Margaret|
|           |Thatcher"  and  include an unrecognized attribute type in the|
|           |search filter.                                               |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 27-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Instruct  the  LDAP  user agent to search for and display all|
|           |entries matching the search filter below.                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(|(cn=Margaret Thatcher)(foo=bar))                           |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is successful if an entry for Margaret Thatcher is|
|Results    |displayed because the search filter evaluates to TRUE.       |
+-----------+-------------------------------------------------------------+
  """

# Filter of "NOT" Choice with an Undefined Attribute Type (Evaluates to UNDEFINED)
def blits_test_3_3_2_4_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entries and only include an unrecognized attribute|
|           |type in the search filter.                                   |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 27-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Instruct  the  LDAP  user agent to search for and display all|
|           |entries matching the search filter below.                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(!(foo=bar))                                                 |
+-----------+-------------------------------------------------------------+
|Expected   |The  test  is  successful if no entries are displayed because|
|Results    |the search filter evaluates to UNDEFINED.                    |
+-----------+-------------------------------------------------------------+
  """

# Unrecognized Option in Attribute Description List
def blits_test_3_3_2_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify appropriate behavior when the list of attributes to be|
|           |retrieved  for  an  entry  includes an unrecognized option as|
|           |part of an attribute description.                            |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.1.5, pg. 13), [RFC 2251] (paragraph  |
|           |4.5.1, pp. 25-28)                                            |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit  a  Search  request with a search filter, base, scope,|
|           |and attributes list as indicated below.                      |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Attributes |cn, telephonenumber;foo, mail                                |
+-----------+-------------------------------------------------------------+
|Filter     |cn=*Margaret*                                                |
+-----------+-------------------------------------------------------------+
|Expected   |Unrecognized option should be ignored. The entry for Margaret|
|results    |Thatcher   should   be   returned.  (note:  telephone  number|
|           |attribute  should  not  be  included  in attributes returned,|
|           |because  an  unknown  option requires that a server treat the|
|           |attribute affected by that option as an unknown attribute)   |
+-----------+-------------------------------------------------------------+
  """

# Retrieve Operational Attributes for an Entry
def blits_test_3_3_2_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  correct  behavior  when all attributes, plus specific|
|           |operational ones, are requested.                             |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-29)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit  a  Search  request as specified below, making sure to|
|           |use  a  '*' character and also specific operational attribute|
|           |names as the list of attributes to return for each entry.    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |base-level                                                   |
+-----------+-------------------------------------------------------------+
|Attributes |*,     creatorsname,     creatorstimestamp,     modifersname,|
|           |modifytimestamp                                              |
+-----------+-------------------------------------------------------------+
|Filter     |objectclass=organizationalunit                               |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entry  should be returned with all attributes|
|results    |present,  including  requested  operational  attributes:  ou=|
|           |Americas, ou=Search, o=IMC, c=US                             |
+-----------+-------------------------------------------------------------+
  """

# Alias Dereferencing
def blits_test_3_3_2_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Never Dereference Aliases - Aliased Base Object
def blits_test_3_3_2_7_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  an  aliased  base  object  supplied on a Search|
|           |request is not deferenced.                                   |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search for a subordinate of a base object which is an alias, |
|           |requesting neverDerefAliases.                                |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, ou=Search, o=IMC, c=US                            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, dc=Search, dc=Relative, dc=IMC, dc=org            |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=Thatcher)                                                |
+-----------+-------------------------------------------------------------+
|Expected   |Search  base  alias  will  not  be  dereferenced,  entry  for|
|results    |Margaret  Thatcher  will  not be returned. No entries will be|
|           |returned.                                                    |
+-----------+-------------------------------------------------------------+
  """

# Never Dereference Aliases - Aliased Leaf Object
def blits_test_3_3_2_7_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  an aliased leaf object will not be dereferenced|
|           |as a part of the Search response.                            |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search  for  a  leaf  entry  which  is  an  alias, requesting|
|           |neverDerefAliases.                                           |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, ou=Europe, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, dc=Europe, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(telephonenumber=*)                                          |
+-----------+-------------------------------------------------------------+
|Expected   |Alias for Jonathan Adams will not be dereferenced. No entries|
|results    |will be returned.                                            |
+-----------+-------------------------------------------------------------+
  """

# Dereference Aliases in Searching - Aliased Base Object
def blits_test_3_3_2_7_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  an aliased base object will not be dereferenced|
|           |when alias dereferencing during searching is enabled.        |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search for a subordinate of a base object which is an alias, |
|           |requesting derefInSearching                                  |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, ou=Search, o=IMC, c=US                            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, dc=Search, dc=Relative, dc=IMC, dc=org            |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=Thatcher)                                                |
+-----------+-------------------------------------------------------------+
|Expected   |Search  base  alias will not be dereferenced. No entries will|
|results    |be returned.                                                 |
+-----------+-------------------------------------------------------------+
  """

# Dereference Aliases in Searching - Aliased Leaf Object
def blits_test_3_3_2_7_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that an aliased leaf object will be dereferenced as a |
|           |part  of  the  SEARCH results when alias dereferencing during|
|           |searching is enabled.                                        |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search  for  a  leaf  entry  which  is  an  alias, requesting|
|           |derefInSearching.                                            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, ou=Europe, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, dc=Europe, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(telephonenumber=*)                                          |
+-----------+-------------------------------------------------------------+
|Expected   |Alias for DN "cn=Jonathan Adams, ou=Europe, ou=Search, o=IMC,|
|results    |c=US"  will  be dereferenced and will be returned as a match,|
|           |with telephone number +1 408 720 0000.                       |
+-----------+-------------------------------------------------------------+
  """

# Dereference Finding Base Object - Aliased Base Object
def blits_test_3_3_2_7_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that an aliased base object will be dereferenced when |
|           |alias dereferencing while finding base objects is enabled.   |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search for a subordinate of a base object which is an alias, |
|           |requesting derefFindingBaseObj.                              |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, ou=Search, o=IMC, c=US                            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, dc=Search, dc=Relative, dc=IMC, dc=org            |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=Thatcher)                                                |
+-----------+-------------------------------------------------------------+
|Expected   |Search  base  alias  will be dereferenced, the entries for DN|
|results    |"cn=Margaret Thatcher, ou=Help Desk, ou=IT, ou=Americas, ou= |
|           |Search, o=IMC, c=US" and "cn=Margaret Thatcher (No Title), ou|
|           |=Help Desk, ou=IT, ou=Americas, ou=Search, o=IMC, c=US" will |
|           |be returned.                                                 |
+-----------+-------------------------------------------------------------+
  """

# Dereference Finding Base Object - Aliased Leaf Object
def blits_test_3_3_2_7_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  an aliased leaf object will not be dereferenced|
|           |when  alias  dereferencing  while  finding  base  objects  is|
|           |enabled.                                                     |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search    for    a    leaf   entry   which   is   an   alias,|
|           |derefFindingBaseObj.                                         |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, ou=Europe, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, dc=Europe, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(telephonenumber=*)                                          |
+-----------+-------------------------------------------------------------+
|Expected   |Alias for Jonathan Adams will not be dereferenced. No entries|
|results    |will be returned.                                            |
+-----------+-------------------------------------------------------------+
  """

# Always Dereference - Aliased Base Object
def blits_test_3_3_2_7_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that an aliased base object is dereferenced when full |
|           |alias dereferencing is enabled.                              |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search for a subordinate of a base object which is an alias, |
|           |requesting derefAlways.                                      |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, ou=Search, o=IMC, c=US                            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Canada, dc=Search, dc=Relative, dc=IMC, dc=org            |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=Thatcher)                                                |
+-----------+-------------------------------------------------------------+
|Expected   |Search  base  alias  will be dereferenced, the entries for DN|
|results    |"cn=Margaret Thatcher, ou=Help Desk, ou=IT, ou=Americas, ou= |
|           |Search, o=IMC, c=US" and "cn=Margaret Thatcher (No Title), ou|
|           |=Help Desk, ou=IT, ou=Americas, ou=Search, o=IMC, c=US" will |
|           |be returned.                                                 |
+-----------+-------------------------------------------------------------+
  """

# Always Dereference - Aliased Leaf Object
def blits_test_3_3_2_7_8(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that an aliased base object is dereferenced when full |
|           |alias dereferencing is enabled.                              |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search  for  a  leaf  entry  which  is  an  alias, requesting|
|           |derefAlways.                                                 |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, ou=Europe, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, dc=Europe, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(telephonenumber=*)                                          |
+-----------+-------------------------------------------------------------+
|Expected   |Alias for DN "cn=Jonathan Adams, ou=Europe, ou=Search, o=IMC,|
|results    |c=US"  will  be dereferenced and will be returned as a match,|
|           |with telephone number +1 408 720 0000.                       |
+-----------+-------------------------------------------------------------+
"""

# Always Dereference - Aliased Leaf Object
def blits_test_3_3_2_7_8(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that an aliased base object is dereferenced when full |
|           |alias   dereferencing   is   enabled,  and  that  matches  in|
|           |non-dereferenced search paths are not returned..             |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Search  for  a  leaf  entry  which  is  an  alias, requesting|
|           |derefAlways.                                                 |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, ou=Europe, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |cn=Jonny Adams, dc=Europe, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=Adams)                                                   |
+-----------+-------------------------------------------------------------+
|Expected   |Alias for DN "cn=Jonathan Adams, ou=Europe, ou=Search, o=IMC,|
|results    |c=US"  will  be dereferenced and will be returned as a match,|
|           |with telephone number +1 408 720 0000. The "Jonny Adams"     |
|           |alias entry is not returned.                                 |
+-----------+-------------------------------------------------------------+
  """

# Miscellaneous Searching Feature Tests
def blits_test_3_3_2_8(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Search Result Size Limit
def blits_test_3_3_2_8_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that size limit feature works appropriately.          |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Set  sizelimit  parameter  to  1.  Perform a search that will|
|           |return more than 1 entry.                                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(cn=*)                                                       |
+-----------+-------------------------------------------------------------+
|Expected   |One  entry  should  be  returned,  followed  by return code 4|
|results    |(sizeLimitExceeded).  Reset  the  size  limit to its original|
|           |value.                                                       |
+-----------+-------------------------------------------------------------+
  """

# Search Time Limit
def blits_test_3_3_2_8_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that time limit feature works appropriately.          |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.5.1, pp. 25-28)                      |
+-----------+-------------------------------------------------------------+
|Procedure  |Set timelimit parameter to 1. Perform search that should take|
|           |longer than 1 second.                                        |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(objectclass=*)                                              |
+-----------+-------------------------------------------------------------+
|Expected   |Some  entries  should  be returned, followed by return code 3|
|results    |(timeLimitExceeded).  Reset  the  timelimit  parameter to its|
|           |original value.                                              |
+-----------+-------------------------------------------------------------+
  """

# Return Attribute Types Only
def blits_test_3_3_2_8_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  the  feature  designed  to  allow for returning|
|           |attribute   names   instead   of   name-value   pairs   works|
|           |appropriately.                                               |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]         |
|           |(paragraph 4.5.1, pp. 25-28)                                 |
+-----------+-------------------------------------------------------------+
|Procedure  |Set  typesonly  parameter to TRUE. Perform a search that will|
|           |return matching results.                                     |
+-----------+-------------------------------------------------------------+
|Base       |ou=Search, o=IMC, c=US                                       |
+-----------+-------------------------------------------------------------+
|Base       |dc=Search, dc=Relative, dc=IMC, dc=org                       |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(cn=*)                                                       |
+-----------+-------------------------------------------------------------+
|Expected   |Only attribute names should be returned.                     |
|results    |                                                             |
+-----------+-------------------------------------------------------------+
  """

# Search Operation Errors
def blits_test_3_3_2_9(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Invalid Search Filter Syntax
def blits_test_3_3_2_9_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  appropriate  behavior when a search filter of invalid|
|           |syntax is included as a search request parameter.            |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph TBD , pp. TBD)                         |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a bad filter syntax.            |
+-----------+-------------------------------------------------------------+
|Base       |ou=Americas, ou=Search, o=IMC, c=US                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |(&(!(|internationaliSDNNumber=*(description=*                |
+-----------+-------------------------------------------------------------+
|Expected   |Return  code  TBD  (codeTBD)  should be returned. No matching|
|results    |entries should be returned. (note: there was a response code |
|           |for  this  in LDAPv2, but I can't seem to find the equivalent|
|           |requirement in LDAPv3)                                       |
|           |The  error  is should be an API error since the filter string|
|           |is parsed to be encoded.                                     |
+-----------+-------------------------------------------------------------+
  """

# noSuchObject Error for Subtree Search
def blits_test_3_3_2_9_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that the server will generate a noSuchObject error for|
|           |a subtree search.                                            |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]         |
|           |(paragraph 4.5.1, pp. 25-28)                                 |
+-----------+-------------------------------------------------------------+
|Procedure  |Perform a subtree search with a base that does not exist.    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Staff, ou=Americas, ou=Search, o=IMC, c=US                |
+-----------+-------------------------------------------------------------+
|Base       |dc=Staff, dc=Americas, dc=Search, dc=Relative, dc=IMC, dc=org|
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=person)                                                  |
+-----------+-------------------------------------------------------------+
|Expected   |Return code 32 (noSuchObject) should be returned as an error.|
|results    |No entries will be returned.                                 |
+-----------+-------------------------------------------------------------+
  """

# noSuchObject for Single-Level Search
def blits_test_3_3_2_9_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  the  server will generate a noSuchObject error|
|            |for a single-level search.                                  |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]        |
|            |(paragraph 4.5.1, pp. 25-28)                                |
+------------+------------------------------------------------------------+
|Procedure   |Perform  a  single-level  search  with  a base that does not|
|            |exist.                                                      |
+------------+------------------------------------------------------------+
|Base        |ou=People, ou=Search, o=IMC, c=US                           |
+------------+------------------------------------------------------------+
|Base        |dc=People, dc=Search, dc=Relative, dc=IMC, dc=org           |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |single-level                                                |
+------------+------------------------------------------------------------+
|Filter      |(objectclass=person)                                        |
+------------+------------------------------------------------------------+
|Expected    |Return code 32 (noSuchObject) should be returned. No entries|
|results     |will be returned.                                           |
+------------+------------------------------------------------------------+
  """

# noSuchObject for Base-Level Search
def blits_test_3_3_2_9_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  the  server will generate a noSuchObject error|
|            |for a base-level search.                                    |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]        |
|            |(paragraph 4.5.1, pp. 25-28)                                |
+------------+------------------------------------------------------------+
|Procedure   |Perform a base-scope search with a base that does not exist.|
+------------+------------------------------------------------------------+
|Base        |cn=Madonna, ou=Search, o=IMC, c=US                          |
+------------+------------------------------------------------------------+
|Base        |cn=Madonna, dc=Search, dc=Relative, dc=IMC, dc=org          |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |base                                                        |
+------------+------------------------------------------------------------+
|Filter      |(objectclass=*)                                             |
+------------+------------------------------------------------------------+
|Expected    |Return code 32 (noSuchObject) should be returned. No entries|
|results     |will be returned.                                           |
+------------+------------------------------------------------------------+
  """

# invalidDNSyntax for Subtree Search
def blits_test_3_3_2_9_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  the  server  will  generate an invalidDNSyntax|
|            |error for a subtree search.                                 |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]        |
|            |(paragraph 4.5.1, pp. 25-28)                                |
+------------+------------------------------------------------------------+
|Procedure   |Specify a DN with bad syntax for a subtree search.          |
+------------+------------------------------------------------------------+
|Base        |cn=Tom Jones,ou, ou=Search, o=IMC, c=US                     |
+------------+------------------------------------------------------------+
|Base        |cn=Tom Jones,ou, dc=Search, dc=Relative, dc=IMC, dc=org     |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |(sn=jones)                                                  |
+------------+------------------------------------------------------------+
|Expected    |Return  code  34  (invalidDNSyntax)  should  be returned. No|
|results     |entries will be returned.                                   |
+------------+------------------------------------------------------------+
  """

# invalidDNSyntax for Single-Level Search
def blits_test_3_3_2_9_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that the server will generate an invalidDNSyntax error|
|           |for a single-level search.                                   |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]         |
|           |(paragraph 4.5.1, pp. 25-28)                                 |
+-----------+-------------------------------------------------------------+
|Procedure  |Specify a DN with bad syntax for a single-level search.      |
+-----------+-------------------------------------------------------------+
|Base       |cn=Tom Jones,ou, ou=Search, o=IMC, c=US                      |
+-----------+-------------------------------------------------------------+
|Base       |cn=Tom Jones,ou, dc=Search, dc=Relative, dc=IMC, dc=org      |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=jones)                                                   |
+-----------+-------------------------------------------------------------+
|Expected   |Return  code  34  (invalidDNSyntax)  should  be  returned. No|
|results    |entries will be returned.                                    |
+-----------+-------------------------------------------------------------+
  """

# invalidDNSyntax for Base-Level Search
def blits_test_3_3_2_9_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that the server will generate an invalidDNSyntax error|
|           |for a base-level search.                                     |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]         |
|           |(paragraph 4.5.1, pp. 25-28)                                 |
+-----------+-------------------------------------------------------------+
|Procedure  |Specify a DN with bad syntax for a base-level search.        |
+-----------+-------------------------------------------------------------+
|Base       |ou="Any Unit, ou=Americas, ou=Search, o=IMC, c=US            |
+-----------+-------------------------------------------------------------+
|Base       |dc="Any Unit, dc=Americas, dc=Search, dc=Relative, dc=IMC, dc|
|(dc-naming)|=org                                                         |
+-----------+-------------------------------------------------------------+
|Scope      |base-level                                                   |
+-----------+-------------------------------------------------------------+
|Filter     |(sn=jones)                                                   |
+-----------+-------------------------------------------------------------+
|Expected   |Return  code  34  (invalidDNSyntax)  should  be  returned. No|
|results    |entries will be returned.                                    |
+-----------+-------------------------------------------------------------+
  """

# Modify Operation Tests
def blits_test_3_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.3, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two  parameters  in  all  of  the DNs found in paragraph 3.3.3;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10"; if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make appropriate modifications to the LDIF file intended for use during
    the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Modify-Add Tests
def blits_test_3_3_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Add Value - Create Attribute
def blits_test_3_3_3_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  an  attribute  type is created when a request for|
|         |adding  an  attribute value for an attribute type that does not|
|         |currently exist for an entry.                                  |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.6, pp. 32-33)                          |
+---------+---------------------------------------------------------------+
|Procedure|Add the first value of an attribute type.                      |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=Modify, o= |
|         |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Attribute|facsimileTelephoneNumber                                       |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|+1 908 555 1212                                                |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Entry should now have +1 908 555 1212 as a fax number.         |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Add Value to Existing Attribute
def blits_test_3_3_3_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Verify that an additional value can be added to an existing|
|             |attribute.                                                 |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2251] (paragraph 4.6, pp. 32-33)                      |
+-------------+-----------------------------------------------------------+
|Procedure    |Add a second attribute value of an attribute type.         |
+-------------+-----------------------------------------------------------+
|DN           |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=Modify,|
|             |o=IMC, c=US                                                |
+-------------+-----------------------------------------------------------+
|Attribute    |title                                                      |
|type         |                                                           |
+-------------+-----------------------------------------------------------+
|Attribute    |CEO                                                        |
|value        |                                                           |
+-------------+-----------------------------------------------------------+
|Expected     |Entry should now have both "President" and "CEO" as titles.|
|results      |                                                           |
+-------------+-----------------------------------------------------------+
  """

# Modify-Add Errors
def blits_test_3_3_3_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# attributeOrValueExists
def blits_test_3_3_3_1_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  an attributeOrValueExists error message can be|
|            |generated.                                                  |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251]        |
|            |(paragraph 4.6, pp. 32-33)                                  |
+------------+------------------------------------------------------------+
|Procedure   |Attempt  to  add a surname attribute value already contained|
|            |within an entry.                                            |
+------------+------------------------------------------------------------+
|DN          |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=Modify, |
|            |o=IMC, c=US                                                 |
+------------+------------------------------------------------------------+
|Attribute   |sn                                                          |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Cezanne                                                     |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Return code 20 (attributeOrValueExists) should be returned. |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# invalidAttributeSyntax
def blits_test_3_3_3_1_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  an  invalid attribute syntax causes the server to|
|         |generate an invalidAttributeSyntax error.                      |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Do  not  supply  a  value for the attribute being added using a|
|         |modify-add request.                                            |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=Modify, o= |
|         |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Attribute|mail                                                           |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|<unspecified>                                                  |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 21 (invalidAttributeSyntax) should be returned. The|
|results  |attribute should not have been added to the entry.             |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax
def blits_test_3_3_3_1_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that an invalid DN syntax causes the server to generate |
|         |an invalidDNSyntax error for a modify-add request.             |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a DN with bad syntax for a modify-add.                 |
+---------+---------------------------------------------------------------+
|DN       |cn, ou, ou=<vendor-ID>, ou=Modify, o=IMC, c=US                 |
+---------+---------------------------------------------------------------+
|Attribute|cn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Missing Person                                                 |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return  code  34  (invalidDNSytnax)  should  be  returned.  The|
|results  |attribute should not have been added to the entry.             |
+---------+---------------------------------------------------------------+
  """

# Modify-Delete Tests
def blits_test_3_3_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Delete One Value of a Multi-valued Attribute
def blits_test_3_3_3_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Verify  deletion  of  a  single  value  for  a multi-valued|
|             |attribute.                                                 |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2251] (paragraph 4.6, pp. 32-33)                      |
+-------------+-----------------------------------------------------------+
|Procedure    |Delete one of three attribute values for an attribute type.|
+-------------+-----------------------------------------------------------+
|DN           |cn=Paul Newman, ou=<client-ID>, ou=<vendor-ID>, ou=Modify, |
|             |o=IMC, c=US                                                |
+-------------+-----------------------------------------------------------+
|Attribute    |title                                                      |
|type         |                                                           |
+-------------+-----------------------------------------------------------+
|Attribute    |Head Honcho                                                |
|value        |                                                           |
+-------------+-----------------------------------------------------------+
|Expected     |Entry should now have "President" and "CEO" as titles.     |
|results      |                                                           |
+-------------+-----------------------------------------------------------+
  """

# Delete Single-Valued Attribute
def blits_test_3_3_3_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  a single-valued attribute can be deleted using|
|            |the MODIFY operation.                                       |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.6, pp. 32-33)                       |
+------------+------------------------------------------------------------+
|Procedure   |Delete the only attribute for an attribute type.            |
+------------+------------------------------------------------------------+
|DN          |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=   |
|            |Modify, o=IMC, c=US                                         |
+------------+------------------------------------------------------------+
|Attribute   |title                                                       |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Director                                                    |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Entry should now have no title attributes.                  |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Delete Multi-Valued Attribute
def blits_test_3_3_3_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  a  multi-valued attribute can be deleted using|
|            |the MODIFY operation.                                       |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.6, pp. 32-33)                       |
+------------+------------------------------------------------------------+
|Procedure   |Delete a multi-valued attribute.                            |
+------------+------------------------------------------------------------+
|DN          |cn=Emeril Lagosse, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|            |Modify, o=IMC, c=US                                         |
+------------+------------------------------------------------------------+
|Attribute   |title                                                       |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |<unspecified>                                               |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Entry should now have no title attributes.                  |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Modify-Delete Errors
def blits_test_3_3_3_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# noSuchAttribute with Attribute Type Only
def blits_test_3_3_3_2_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  server  will  generate  a  noSuchAttribute  error|
|         |message  when  instructed via a modify-delete request to delete|
|         |an attribute not contained within an entry.                    |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Based on a specification of an attribute type only, attempt to |
|         |delete  an  attribute  from an entry that does not contain that|
|         |attribute.                                                     |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |Modify, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|facsimileTelephoneNumber                                       |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 16 (noSuchAttribute) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# noSuchAttribute with Attribute Type-Value Pair
def blits_test_3_3_3_2_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  server  will  generate  a  noSuchAttribute  error|
|         |message  when  instructed via a modify-delete request to delete|
|         |an attribute not contained within an entry.                    |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Based  on  a  specification  of  an  attribute type-value pair,|
|         |attempt  to  delete  an attribute type-value pair from an entry|
|         |that does not contain that attribute.                          |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |Modify, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|internationaliSDNNumber                                        |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|1 313 555 1234                                                 |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 16 (noSuchAttribute) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# noSuchAttribute with Incorrect Attribute Value
def blits_test_3_3_3_2_4_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  server  will  generate  a  noSuchAttribute  error|
|         |message  when  instructed via a modify-delete request to delete|
|         |an attribute type-value pair not contained within an entry.    |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Based  on  a specification of an attribute type-value pair with|
|         |an  incorrect  value, attempt to delete an attribute value from|
|         |an entry that does not contain that attribute.                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |Modify, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|telephoneNumber                                                |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|313 555-8300                                                   |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Notes    |Actual existing value is 825-0008                              |
+---------+---------------------------------------------------------------+
|Expected |Return code 16 (noSuchAttribute) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# objectClassViolation
def blits_test_3_3_3_2_4_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that server will generate an objectClassViolation error |
|         |message when instructed via a modify-delete request to delete a|
|         |mandatory attribute.                                           |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Attempt to remove a required attribute from an entry.          |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |Modify, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|objectclass                                                    |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 65 (objectClassViolation) should be returned.      |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Modify-Replace Tests
def blits_test_3_3_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Replace Multi-Valued Attribute with Single Value
def blits_test_3_3_3_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  that  a  multi-valued attribute can be replaced by a|
|            |single-valued attribute.                                    |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.6, pp. 32-33)                       |
+------------+------------------------------------------------------------+
|Procedure   |Replace an attribute type which has multiple values using a |
|            |Modify request.                                             |
+------------+------------------------------------------------------------+
|DN          |cn=David Rosengarten, ou=<client-ID>, ou=<vendor-ID>, ou=   |
|            |Modify, o=IMC, c=US                                         |
+------------+------------------------------------------------------------+
|Attribute   |title                                                       |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Chief Taster                                                |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Entry should now have only "Chief Taster" as a title.       |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Replace Single-Valued Attribute
def blits_test_3_3_3_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify that a single-valued attribute can be replaced.      |
+------------+------------------------------------------------------------+
|Procedure   |Replace  an  attribute  value  for an attribute type using a|
|            |Modify request.                                             |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.6, pp. 32-33)                       |
+------------+------------------------------------------------------------+
|DN          |cn=David Rosengarten, ou=<client-ID>, ou=<vendor-ID>, ou=   |
|            |Modify, o=IMC, c=US                                         |
+------------+------------------------------------------------------------+
|Attribute   |mail                                                        |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |David.Rosengarten@tvfood.com                                |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Entry should now have only "David.Rosengarten@tvfood.com" as|
|results     |an e-mail address.                                          |
+------------+------------------------------------------------------------+
  """

# Delete Attribute Using Modify-Replace
def blits_test_3_3_3_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify that a server will remove attributes to be replaced if|
|           |specified with no value.                                     |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.6, pp. 32-33)                        |
+-----------+-------------------------------------------------------------+
|Procedure  |Do  not  supply a value for the attribute type being replaced|
|           |using a Modify request.                                      |
+-----------+-------------------------------------------------------------+
|DN         |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=    |
|           |Modify, o=IMC, c=US                                          |
+-----------+-------------------------------------------------------------+
|Attribute  |givenname                                                    |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |<unspecified>                                                |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Expected   |The givenname attribute should no longer be contained within |
|results    |the entry.                                                   |
+-----------+-------------------------------------------------------------+
  """

# Modify-Replace Errors
def blits_test_3_3_3_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# noSuchObject
def blits_test_3_3_3_3_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  a modify-replace request involving a non-existent|
|         |object will generate a noSuchObject error message.             |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify  an  entry  that  does  not  exist for a modify-replace|
|         |request.                                                       |
+---------+---------------------------------------------------------------+
|DN       |cn=Invisible Person, ou=<client-ID>, ou=<vendor-ID>, ou=Modify,|
|         |o=IMC, c=US                                                    |
+---------+---------------------------------------------------------------+
|Attribute|sn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Person                                                         |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 32 (noSuchObject) should be returned. The operation|
|results  |should not succeed.                                            |
+---------+---------------------------------------------------------------+
  """

# notAllowedOnRDN
def blits_test_3_3_3_3_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  a  modify-replace request specified to change the|
|         |naming attribute generates a notAllowedOnRDN error message.    |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.6, pp. 32-33)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Attempt  to  rename  the  naming  attribute of an entry using a|
|         |modify-replace request.                                        |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |Modify, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|cn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Maggy Thatcher                                                 |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return  code  67  (notAllowedOnRDN)  should  be  returned.  The|
|results  |operation should not succeed.                                  |
+---------+---------------------------------------------------------------+
  """

# Add Operation Tests
def blits_test_3_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.4, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two  parameters  in  all  of  the DNs found in paragraph 3.4.4;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10" if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make  appropriate  modifications  to  the  LDIF  file that will be used
    during the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Add New Entry
def blits_test_3_3_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify capability to add a new entry to the directory using |
|            |the ADD operation.                                          |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.7 , pg. 34)                         |
+------------+------------------------------------------------------------+
|Procedure   |Add  an  entire  new  directory  entry using the information|
|            |below.                                                      |
+------------+------------------------------------------------------------+
|DN          |cn=Austin Powers, ou=<client-ID>, ou=<vendor-ID>, ou=Add, o=|
|            |IMC, c=US                                                   |
+------------+------------------------------------------------------------+
|Attribute   |objectclass                                                 |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |top person organizationalPerson inetOrgPerson               |
|values      |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |sn                                                          |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Powers                                                      |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |cn                                                          |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Austin \"Danger\" Powers                                    |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |telephoneNumber                                             |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |+ 44 582 10101                                              |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |mail                                                        |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |secret_agent_man@imc.org                                    |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |description                                                 |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Yea Baby!!                                                  |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |uid                                                         |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |secret_agent_man                                            |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |description                                                 |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Behave!                                                     |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |A new entry should now be present in the directory with the |
|results     |above attributes.                                           |
+------------+------------------------------------------------------------+
  """

# Add Errors
def blits_test_3_3_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# noSuchObject
def blits_test_3_3_4_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that servers will return a noSuchObject error message in|
|         |response  to  an Add request that includes a specification of a|
|         |non-existent superior object.                                  |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.7, pp. 34-35)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a non-existent organizationalUnit value in the path of |
|         |the name of a new entry for an add operation.                  |
+---------+---------------------------------------------------------------+
|DN       |cn=Dweezle Zappa, ou=Zappaland, ou=<client-ID>, ou=<vendor-ID>,|
|         |ou=Add, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|objectclass                                                    |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|top person                                                     |
|values   |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|sn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Person                                                         |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|cn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Not A Person                                                   |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return  code  32  (noSuchObject)  should be returned. The entry|
|results  |should not be created.                                         |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax
def blits_test_3_3_4_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for an Add request including an improperly-formed DN.          |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.7, pp. 34-35)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a DN with bad syntax for an add operation.             |
+---------+---------------------------------------------------------------+
|DN       |cn=New Person, ou=<client-ID>, ou=<vendor-ID>, =IMC, c=US      |
+---------+---------------------------------------------------------------+
|Attribute|objectclass                                                    |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|top person                                                     |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|sn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Person                                                         |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|cn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|New Person                                                     |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 34 (invalidDNSyntax) should be returned. The entry |
|results  |should not have been added to the directory.                   |
+---------+---------------------------------------------------------------+
  """

# entryAlreadyExists
def blits_test_3_3_4_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the  server  will  generate an entryAlreadyExists|
|         |error for an Add request including specification of an existing|
|         |entry.                                                         |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.7, pp. 34-35)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Attempt  to  add  a new entry with the same name as an existing|
|         |entry.                                                         |
+---------+---------------------------------------------------------------+
|DN       |ou=<client-ID>, ou=<vendor-ID>, ou=Add, o=IMC, c=US            |
+---------+---------------------------------------------------------------+
|Attribute|objectclass                                                    |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|top organizationalUnit                                         |
|values   |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|ou                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|<client-ID>                                                    |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return  code  68  (entryAlreadyExists)  should be returned. The|
|results  |existing entry should remain in the directory, unmodified.     |
+---------+---------------------------------------------------------------+
  """

# objectClassViolation
def blits_test_3_3_4_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the  server will generate an objectClassViolation|
|         |error for an Add request that is missing the specification of a|
|         |mandatory attribute.                                           |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.7, pp. 34-35)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Attempt  to  add an alias entry without specifying the required|
|         |aliasedObjectName attribute.                                   |
+---------+---------------------------------------------------------------+
|DN       |cn=Alias Entry, ou=<client-ID>, ou=<vendor-ID>, ou=Add, o=IMC, |
|         |c=US                                                           |
+---------+---------------------------------------------------------------+
|Attribute|objectclass                                                    |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|top alias                                                      |
|values   |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return  code  65 (objectClassViolation) should be returned. The|
|results  |entry should not be present in the directory.                  |
+---------+---------------------------------------------------------------+
  """

# Delete Operation Tests
def blits_test_3_3_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.5, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two  parameters  in  all  of  the DNs found in paragraph 3.4.4;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10" if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make  appropriate  modifications  to  the  LDIF  file that will be used
    during the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Delete Existing Object
def blits_test_3_3_5_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Verify that an entry can be deleted.                       |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2251] (paragraph 4.8, pg. 35)                         |
+-------------+-----------------------------------------------------------+
|Procedure    |Delete the entry with the DN specified below.              |
+-------------+-----------------------------------------------------------+
|DN           |cn=Mary-Sue Milliken, ou=<client-ID>, ou=<vendor-ID>, ou=  |
|             |Delete, o=IMC, c=US                                        |
+-------------+-----------------------------------------------------------+
|Expected     |The entry should no longer exist.                          |
|results      |                                                           |
+-------------+-----------------------------------------------------------+
  """

# Delete Errors
def blits_test_3_3_5_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# noSuchObject
def blits_test_3_3_5_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that the server will generate a noSuchObject error for a|
|         |Delete request that includes a specification of a non-existent |
|         |object.                                                        |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.8, pg. 35)                                                   |
+---------+---------------------------------------------------------------+
|Procedure|Specify an entry that does not exist for a delete operation.   |
+---------+---------------------------------------------------------------+
|DN       |cn=Susan Feniger, ou=<client-ID>, ou=<vendor-ID>, ou=Delete, o=|
|         |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Expected |Return  code  32  (noSuchObject) should be returned. No changes|
|results  |should have been made to the directory.                        |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax
def blits_test_3_3_5_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for a Delete request including an improperly-formed DN.        |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.8, pg. 35)                                                   |
+---------+---------------------------------------------------------------+
|Procedure|Specify a DN with bad syntax for a delete operation.           |
+---------+---------------------------------------------------------------+
|DN       |Sarah Thorton,<client-ID>,<vendor-ID>,Modify, IMC, US          |
+---------+---------------------------------------------------------------+
|Expected |Return code 34 (invalidDNSyntax) should be returned. The entry |
|results  |should not have been deleted from the directory.               |
+---------+---------------------------------------------------------------+
  """

# notAllowedOnNonLeaf
def blits_test_3_3_5_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for  a  Delete request specifying the removal of an object that|
|         |has children.                                                  |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.8, pg. 35)                                                   |
+---------+---------------------------------------------------------------+
|Procedure|Attempt  to  remove  an entry which has entries below it in the|
|         |tree.                                                          |
+---------+---------------------------------------------------------------+
|DN       |ou=<vendor-ID>, ou=Delete, o=IMC, c=US                         |
+---------+---------------------------------------------------------------+
|Expected |Return  code  66  (notAllowedOnNonLeaf)  should  be return. The|
|results  |object should not have been removed from the directory.        |
+---------+---------------------------------------------------------------+
  """

# ModifyDN Operation Tests
def blits_test_3_3_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.6, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two  parameters  in  all  of  the DNs found in paragraph 3.3.3;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10"; if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make appropriate modifications to the LDIF file intended for use during
    the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Rename a Leaf Entry
def blits_test_3_3_6_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that RDNs can be modified.                              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Change the RDN of the entry specified below.                   |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o|
|         |=IMC, c=US                                                     |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Paul Newman                                                 |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished  name  of  this entry should be cn=Paul|
|results  |Newman, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o=IMC, c= |
|         |US                                                             |
+---------+---------------------------------------------------------------+
  """

# Move a Leaf Entry to A New Parent
def blits_test_3_3_6_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that RDNs can be modified.                              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Change the RDN of the entry specified below.                   |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Hoffman, ou=Current Parent, ou=<client-ID>, ou=<       |
|         |vendor-ID>, ou=ModifyDN, o=IMC, c=US                           |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Paul Hoffman                                                |
+---------+---------------------------------------------------------------+
|New      |ou=New Parent, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o= |
|Superior |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished  name  of  this entry should be cn=Paul|
|results  |Hoffman, ou=New Parent, ou=<client-ID>, ou=<vendor-ID>, ou=    |
|         |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
  """

# Move a Renamed Leaf Entry to A New Parent
def blits_test_3_3_6_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that RDNs can be modified.                              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Change the RDN of the entry specified below.                   |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Revere, ou=Current Parent, ou=<client-ID>, ou=<        |
|         |vendor-ID>, ou=ModifyDN, o=IMC, c=US                           |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Paul McCartney                                              |
+---------+---------------------------------------------------------------+
|New      |ou=New Parent, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o= |
|Superior |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished  name  of  this entry should be cn=Paul|
|results  |McCarney, ou=New Parent, ou=<client-ID>, ou=<vendor-ID>, ou=   |
|         |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
  """

# Rename Subtree of Entries
def blits_test_3_3_6_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that the parent object of a subtree can be renamed.     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Rename the subtree based at the object specified below.        |
+---------+---------------------------------------------------------------+
|Base DN  |ou=Current Subtree, ou=<client-ID>, ou=<vendor-ID>, ou=        |
|         |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
|New RDN  |ou=New Subtree                                                 |
+---------+---------------------------------------------------------------+
|Delete   |FALSE                                                          |
|RDN Flag |                                                               |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished name of objects in this subtree are now|
|results  |rooted at ou=New Subtree, ou=<client-ID>, ou=<vendor-ID>, ou=  |
|         |ModifyDN,  o=IMC,  c=US.  The old base object should not exist.|
|         |The   attribute-value  pair:  ou=Current  Subtree  will  remain|
|         |associated with the entry with the base DN defined above.      |
+---------+---------------------------------------------------------------+
  """

# Move Subtree of Entries
def blits_test_3_3_6_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that subtrees can be moved to a new parent.             |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Move the subtree based at the object specified below.          |
+---------+---------------------------------------------------------------+
|Base DN  |ou=Static, ou=Current Base, ou=<client-ID>, ou=<vendor-ID>, ou=|
|         |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
|New RDN  |ou=Static                                                      |
+---------+---------------------------------------------------------------+
|New      |ou=New Base, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o=   |
|Superior |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|Delete   |TRUE                                                           |
|RDN Flag |                                                               |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished name of objects in this subtree are now|
|results  |rooted at ou=Static, ou=New Base, ou=<client-ID>, ou=<vendor-ID|
|         |>, ou=ModifyDN, o=IMC, c=US. The old base object should not    |
|         |exist. The attribute-value pair: ou=TBD will remain associated |
|         |with the entry with the base DN defined above.                 |
+---------+---------------------------------------------------------------+
  """

# Move a Renamed Subtree of Entries to a New Parent
def blits_test_3_3_6_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that subtrees can be moved to a new parent.             |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.9, pp. 36-37)                          |
+---------+---------------------------------------------------------------+
|Procedure|Move the subtree based at the object specified below.          |
+---------+---------------------------------------------------------------+
|Base DN  |ou=Old Subtree, ou=Old Parent, ou=<client-ID>, ou=<vendor-ID>, |
|         |ou=ModifyDN, o=IMC, c=US                                       |
+---------+---------------------------------------------------------------+
|New RDN  |ou=Not So Old Subtree                                          |
+---------+---------------------------------------------------------------+
|New      |ou=Not So Old Parent, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|Superior |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
|Delete   |TRUE                                                           |
|RDN Flag |                                                               |
+---------+---------------------------------------------------------------+
|Expected |The  new  distinguished name of objects in this subtree are now|
|results  |rooted at ou=Not So Old Subtree, ou=Not So Old Parent, ou=<    |
|         |client-ID>, ou=<vendor-ID>, ou=ModifyDN, o=IMC, c=US. The old  |
|         |base object should not exist. The attribute-value pair: ou=TBD |
|         |will remain associated with the entry with the base DN defined |
|         |above.                                                         |
+---------+---------------------------------------------------------------+
  """

# ModifyDN Errors
def blits_test_3_3_6_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# entryAlreadyExists
def blits_test_3_3_6_7_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the  server  will  generate an entryAlreadyExists|
|         |error   for   ModifyDN   request   including  specification  of|
|         |parameters corresponding to an existing entry.                 |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.9, pp. 36-37)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Attempt to rename an entry to a name that already exists.      |
+---------+---------------------------------------------------------------+
|DN       |cn=Paul Cezanne, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o|
|         |=IMC, c=US                                                     |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Margaret Thatcher                                           |
+---------+---------------------------------------------------------------+
|Expected |Return  code  68  (entryAlreadyExists) should be returned. Both|
|results  |the  entry  for  which the change was intended and the existing|
|         |entry should remain in the directory, unmodified.              |
+---------+---------------------------------------------------------------+
  """

# noSuchObject
def blits_test_3_3_6_7_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate a noSuchObject error for|
|         |Modify   DN   request   that  includes  a  specification  of  a|
|         |non-existant object.                                           |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.9, pp. 36-37)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a name change for an entry that does not exist on this |
|         |server using a Modify DN request.                              |
+---------+---------------------------------------------------------------+
|DN       |cn=No Person, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o=  |
|         |IMC, c=US                                                      |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Does not matter                                             |
+---------+---------------------------------------------------------------+
|Expected |Return  code  32  (noSuchObject) should be returned. No changes|
|results  |should have been made to the directory.                        |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax with Bad DN
def blits_test_3_3_6_7_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for a Delete request including an improperly-formed DN.        |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.9, pp. 36-37)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a DN with bad syntax for a ModifyDN operation.         |
+---------+---------------------------------------------------------------+
|DN       |, ou=<client-ID>, ou=<vendor-ID>, ou=ModifyDN, o=IMC, c=US     |
+---------+---------------------------------------------------------------+
|New RDN  |cn=Missing Person                                              |
+---------+---------------------------------------------------------------+
|Expected |Return code 34 (invalidDNSyntax) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax with Bad RDN
def blits_test_3_3_6_7_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for a Delete request including an improperly-formed RDN.       |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.9, pp. 36-37)                                                |
+---------+---------------------------------------------------------------+
|Procedure|Specify a RDN with bad syntax for a ModifyDN operation.        |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret Thatcher, ou=<client-ID>, ou=<vendor-ID>, ou=      |
|         |ModifyDN, o=IMC, c=US                                          |
+---------+---------------------------------------------------------------+
|New RDN  |Maggy Thatcher                                                 |
+---------+---------------------------------------------------------------+
|Expected |Return code 34 (invalidDNSyntax) should be returned. The entry |
|results  |should not have been deleted from the directory.               |
+---------+---------------------------------------------------------------+
  """

# Compare Operation Tests
def blits_test_3_3_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Comparison with FALSE Return Code
def blits_test_3_3_7_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify return of FALSE return code for Compare request.       |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.10, pp. 37-38)                        |
+----------+--------------------------------------------------------------+
|Procedure |Send  a  Compare  request  to  a  server constructed using the|
|          |information shown below.                                      |
+----------+--------------------------------------------------------------+
|DN        |cn=Margaret  Thatcher,  ou=Help  Desk, ou=IT, ou=Americas, ou=|
|          |Search, o=IMC, c=US                                           |
+----------+--------------------------------------------------------------+
|Attribute |title                                                         |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |Directory  (correct  value is Director; extra 'y' was included|
|value     |in purported title attribute value)                           |
+----------+--------------------------------------------------------------+
|Expected  |Result code 5 (compareFalse) should be returned.              |
|results   |                                                              |
+----------+--------------------------------------------------------------+
  """

# Comparison with TRUE Return Code
def blits_test_3_3_7_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify return of TRUE return code for Compare request.      |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraph 4.10, pp. 37-38)                      |
+------------+------------------------------------------------------------+
|Procedure   |Send  a  Compare  request  to a server constructed using the|
|            |information shown below.                                    |
+------------+------------------------------------------------------------+
|DN          |cn=Margaret Thatcher, ou=Help Desk, ou=IT, ou=Americas, ou= |
|            |Search, o=IMC, c=US                                         |
+------------+------------------------------------------------------------+
|Attribute   |title                                                       |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |Director                                                    |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Result code 6 (compareTrue) should be returned.             |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Compare Errors
def blits_test_3_3_7_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# noSuchAttribute
def blits_test_3_3_7_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  server  generates a noSuchAttribute error message|
|         |for  Compare  request that includes a purported AVA not present|
|         |in an entry.                                                   |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.10, pp. 37-38)                                               |
+---------+---------------------------------------------------------------+
|Procedure|Specify  an  AVA  that  will not match an existing for an entry|
|         |that does not contain that attribute on a Compare request.     |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret  Thatcher,  ou=Help  Desk,  ou=IT, ou=Americas, ou=|
|         |Search, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|internationaliSDNNumber                                        |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|+1 810 555 3333                                                |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 16 (noSuchAttribute) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# noSuchObject
def blits_test_3_3_7_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that the server will generate a noSuchObject error for a|
|         |Compare request that includes a specification of a non-existant|
|         |object.                                                        |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.10, pp. 37-38)                                               |
+---------+---------------------------------------------------------------+
|Procedure|Specify an AVA that will not match an existing directory entry.|
+---------+---------------------------------------------------------------+
|DN       |cn=Nobody Here, ou=Americas, ou=Search, o=IMC, c=US            |
+---------+---------------------------------------------------------------+
|Attribute|sn                                                             |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|Here                                                           |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 32 (noSuchObject) should be returned.              |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# invalidDNSyntax
def blits_test_3_3_7_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  the server will generate an invalidDNSyntax error|
|         |for a Compare request including an improperly-formed DN.       |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.1.10, pp. 16-17), [RFC 2251] (paragraph|
|         |4.10, pp. 37-38)                                               |
+---------+---------------------------------------------------------------+
|Procedure|Specify a DN with bad syntax for a Compare request.            |
+---------+---------------------------------------------------------------+
|DN       |cn=Margaret  Thatcher,  ou=Help  Desk,  ouIT,  ou=Americas, ou=|
|         |Search, o=IMC, c=US                                            |
+---------+---------------------------------------------------------------+
|Attribute|telephoneNumber                                                |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|825-0008                                                       |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Return code 34 (invalidDNSyntax) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Extended Operations Tests
def blits_test_3_3_8(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
TBD, but to be based on the following cases:
   
    sp;*  Test  that  the server returns the correct error for unrecognized
    extended operation [RFC 2251]
  *
  * Test unrecognized critical extension [RFC 2251]
  *
    sp;*  Test  that  the  server does not return an error for unrecognized
    non-critical extension [RFC 2251]
  """

# Charset-Related Tests
def blits_test_3_3_9(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  * Test correct handling of UNICODE composite characters
  """

# DN Quoting Form Tests
def blits_test_3_3_10(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
TBD but based on [RFC 2253].
  """

# Certificate Storage, Retrieval, and Comparison
def blits_test_3_3_11(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
The  descriptions  of these tests assume that the certificates generated by
CA1 are used. These certificates are found in directory certs1 and are as
per the CATS description. A further set of certificates that could equally
well be used, generated by CA2, are provided in directory certs2. Where
other  certificate  generators participate in testing, and are assigned ids
CA3, CA4, etc., the tests can also be performed with their certificates. 
For certificate generator product allocated identity <CA-ID>, the DIT
subtree  rooted  at  ou=<CA-ID>, ou=CAs, o=IMC, c=US is used (eg. for
certificate generator product 3, the DIT subtree rooted at ou=CA3, ou=CAs,
o=IMC, c=US is used.

Note that the certificates in directories certs1 and certs2 are in DER
format.  Equivalent  certificates in PEM format are provided in directories
certs1.pem and certs2.pem.
  """

# Search
def blits_test_3_3_11_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Search for Entry Containing a User Certificate
def blits_test_3_3_11_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entry containing a user certificate.              |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2559] (paragraph 6.2, pp. 6-7)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Certificates, ou=CA1, ou=CAs, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Certificates, dc=CA1, dc=CAs, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(&(sn=Brush)(userCertificate=*))                             |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entry  should  be  returned: Basil Brush. The|
|results    |entry should include two certificates.                       |
+-----------+-------------------------------------------------------------+
  """

# Search for Entry Not Containing a User Certificate
def blits_test_3_3_11_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entry not containing a user certificate.          |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2559] (paragraph 6.2, pp. 6-7)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Certificates, ou=CA1, ou=CAs, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Certificates, dc=CA1, dc=CAs, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(&(sn=Brush)(!(userCertificate=*)))                          |
+-----------+-------------------------------------------------------------+
|Expected   |The  following  entry  should be returned: Bertram Brush. The|
|results    |entry should not include a certificate.                      |
+-----------+-------------------------------------------------------------+
  """

# Search for Entry Containing a CA Certificate
def blits_test_3_3_11_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entry containing a CA certificate.                |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2559] (paragraph 6.2, pp. 6-7)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=CAs, o=IMC, c=US                                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=CAs, dc=Relative, dc=IMC, dc=org                          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |cACertificate=*                                              |
+-----------+-------------------------------------------------------------+
|Expected   |Two entries - CA<n> and BadCA<n> - should be returned for    |
|results    |each  certificate  generator participating in the tests. Each|
|           |entry returned should include a cACertificate attribute.     |
+-----------+-------------------------------------------------------------+
  """

# Search for Entry Not Containing a CA Certificate
def blits_test_3_3_11_1_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entry not containing a CA certificate.            |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2559] (paragraph 6.2, pp. 6-7)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Certificates, ou=CA1, ou=CAs, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Certificates, dc=CA1, dc=CAs, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |(&(sn=Brush)(!(cACertificate=*)))                            |
+-----------+-------------------------------------------------------------+
|Expected   |Two  entries  should  be  returned:  Basil  Brush (This entry|
|results    |should  include  two  user certificates); Bertram Brush (This|
|           |entry should not include a certificate).                     |
+-----------+-------------------------------------------------------------+
  """

# Search for Entry Containing a CRL
def blits_test_3_3_11_1_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entry containing a Certificate Revocation List.   |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2559] (paragraph 6.2, pp. 6-7)                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below.                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=CAs, o=IMC, c=US                                          |
+-----------+-------------------------------------------------------------+
|Base       |dc=CAs, dc=Relative, dc=IMC, dc=org                          |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |certificateRevocationList=*                                  |
+-----------+-------------------------------------------------------------+
|Expected   |An entry - CA<n> - should be returned for each certificate   |
|results    |generator  participating  in  the  tests. Each entry returned|
|           |should include a certificateRevocationList attribute.        |
+-----------+-------------------------------------------------------------+
  """

# Compare
def blits_test_3_3_11_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Compare using userCertificate attribute.                       |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.10, pp. 37-38)                         |
|         |(Note that neither [LDAP_PR] nor [RFC 2559] requires the       |
|         |compare operation to be supported for certificate attributes.) |
+---------+---------------------------------------------------------------+
|Procedure|Send  a  Compare  request  to  a  server  constructed using the|
|         |information shown below.                                       |
+---------+---------------------------------------------------------------+
|DN       |cn=Charles Fox, ou=Certificates, ou=CA1, ou=CAs, o=IMC, c=US   |
+---------+---------------------------------------------------------------+
|Attribute|userCertificate                                                |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|The certificate in file certs1/charles_fox                     |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Result code 6 (compareTrue) should be returned.                |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Add and Modify Entries
def blits_test_3_3_11_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.11.3, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two  parameters  in all of the DNs found in paragraph 3.3.11.3;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10" if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make  appropriate  modifications  to  the  LDIF  file that will be used
    during the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Add Entry with Certificate
def blits_test_3_3_11_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify  capability  to  add  a new entry to the directory with|
|          |userCertificate attribute.                                    |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.7 , pg. 34)                           |
+----------+--------------------------------------------------------------+
|Procedure |Add an entire new directory entry using the information below.|
+----------+--------------------------------------------------------------+
|DN        |cn=Lawrence Lamb, ou=<client-ID>, ou=<vendor-ID>, ou=         |
|          |CertificateAdd, ou=CA1, ou=CAs, o=IMC, c=US                   |
+----------+--------------------------------------------------------------+
|Attribute |objectclass                                                   |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |top person organizationalPerson inetOrgPerson                 |
|values    |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |sn                                                            |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |Lamb                                                          |
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |cn                                                            |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |Lawrence Lamb                                                 |
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |telephoneNumber                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |+ 44 1189 500 001                                             |
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |mail                                                          |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |lawrence@maff.gov.uk                                          |
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |userCertificate                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |The certificate for Lawrence Lamb in file certs1/lawrence_lamb|
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Expected  |A  new  entry  should now be present in the directory with the|
|results   |above attributes.                                             |
+----------+--------------------------------------------------------------+
  """

# Modify-Add Tests
def blits_test_3_3_11_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Create userCertificate Attribute
def blits_test_3_3_11_3_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that a userCertificate attribute type is created when a |
|         |request  is  made  for adding a userCertificate attribute value|
|         |when  the  userCertificate  attribute  type  does not currently|
|         |exist for an entry.                                            |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.6, pp. 32-33)                          |
+---------+---------------------------------------------------------------+
|Procedure|Add the first value of a userCertificate attribute type.       |
+---------+---------------------------------------------------------------+
|DN       |cn=Richard Bird, ou=<client-ID>, ou=<vendor-ID>, ou=           |
|         |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                 |
+---------+---------------------------------------------------------------+
|Attribute|userCertificate                                                |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|The certificate for Richard Bird in file certs1/richard_bird   |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Entry should now include the certificate for Richard Bird.     |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Add userCertificate Value to Existing Attribute
def blits_test_3_3_11_3_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify  that  an  additional value can be added to an existing|
|          |attribute.                                                    |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.6, pp. 32-33)                         |
+----------+--------------------------------------------------------------+
|Procedure |Add a second attribute value of an attribute type.            |
+----------+--------------------------------------------------------------+
|DN        |cn=Michael Fish, ou=<client-ID>, ou=<vendor-ID>, ou=          |
|          |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                |
+----------+--------------------------------------------------------------+
|Attribute |userCertificate                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |The   Michael   Fish   Current  Certificate  in  file  certs1/|
|value     |michael_fish_current                                          |
+----------+--------------------------------------------------------------+
|Expected  |Entry should now have two certificates.                       |
|results   |                                                              |
+----------+--------------------------------------------------------------+
  """

# Create cACertificate Attribute
def blits_test_3_3_11_3_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  a  cACertificate attribute type is created when a|
|         |request is made for adding a cACertificate attribute value when|
|         |the  cACertificate  attribute type does not currently exist for|
|         |an entry.                                                      |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.6, pp. 32-33)                          |
+---------+---------------------------------------------------------------+
|Procedure|Add the first value of a cACertificate attribute type.         |
+---------+---------------------------------------------------------------+
|DN       |ou=Swallow Bank, ou=<client-ID>, ou=<vendor-ID>, ou=           |
|         |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                 |
+---------+---------------------------------------------------------------+
|Attribute|cACertificate                                                  |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|The  CA  certificate  for  the  Swallow  Bank  in  file certs1/|
|value    |swallow_bank                                                   |
+---------+---------------------------------------------------------------+
|Expected |Entry  should  now  include  the CA certificate for the Swallow|
|results  |Bank.                                                          |
+---------+---------------------------------------------------------------+
  """

# Create certificateRevocationList Attribute
def blits_test_3_3_11_3_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  a  certificateRevocationList  attribute  type  is|
|         |created    when    a    request    is   made   for   adding   a|
|         |certificateRevocationList     attribute    value    when    the|
|         |certificateRevocationList  attribute  type  does  not currently|
|         |exist for an entry.                                            |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.6, pp. 32-33)                          |
+---------+---------------------------------------------------------------+
|Procedure|Add  the  first  value of a certificateRevocationList attribute|
|         |type.                                                          |
+---------+---------------------------------------------------------------+
|DN       |ou=Swallow Bank, ou=<client-ID>, ou=<vendor-ID>, ou=           |
|         |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                 |
+---------+---------------------------------------------------------------+
|Attribute|certificateRevocationList                                      |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|The CA CRL in file certs1/swallow_crl                          |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Entry should now include the CRL for the Swallow Bank.         |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Modify-Delete Tests
def blits_test_3_3_11_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Delete One Value of a Multi-valued userCertificate Attribute
def blits_test_3_3_11_3_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify   deletion   of  a  single  value  for  a  multi-valued|
|          |attribute.                                                    |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.6, pp. 32-33)                         |
+----------+--------------------------------------------------------------+
|Procedure |Delete one of two attribute values for an attribute type.     |
+----------+--------------------------------------------------------------+
|DN        |cn=Tony Hart, ou=<client-ID>, ou=<vendor-ID>, ou=             |
|          |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                |
+----------+--------------------------------------------------------------+
|Attribute |userCertificate                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |The   Tony   Hart   Expired   Certificate   in   file  certs1/|
|value     |tony_hart_expired                                             |
+----------+--------------------------------------------------------------+
|Expected  |Entry  should  now have just the certificate contained in file|
|results   |certs1/tony_hart_current                                      |
+----------+--------------------------------------------------------------+
  """

# Delete Single-Valued userCertificate Attribute
def blits_test_3_3_11_3_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify  that  a single-valued userCertificate attribute can be|
|          |deleted using the MODIFY operation.                           |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.6, pp. 32-33)                         |
+----------+--------------------------------------------------------------+
|Procedure |Delete  the  only  attribute  for  a userCertificate attribute|
|          |type.                                                         |
+----------+--------------------------------------------------------------+
|DN        |cn=Quintain Hogg, ou=<client-ID>, ou=<vendor-ID>, ou=         |
|          |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                |
+----------+--------------------------------------------------------------+
|Attribute |userCertificate                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |The certificate stored in certs1/quintain_hogg                |
|value     |                                                              |
+----------+--------------------------------------------------------------+
|Expected  |Entry should now have no userCertificate attributes.          |
|results   |                                                              |
+----------+--------------------------------------------------------------+
  """

# Replace userCertificate Attribute
def blits_test_3_3_11_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify that a userCertificate attribute can be replaced.      |
+----------+--------------------------------------------------------------+
|Procedure |Replace  an  attribute  value  for  an  attribute type using a|
|          |Modify request.                                               |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 4.6, pp. 32-33)                         |
+----------+--------------------------------------------------------------+
|DN        |cn=John Prescott, ou=<client-ID>, ou=<vendor-ID>, ou=         |
|          |CertificateModify, ou=CA1, ou=CAs, o=IMC, c=US                |
+----------+--------------------------------------------------------------+
|Attribute |userCertificate                                               |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |The   John   Prescott  Current  Certificate  in  file  certs1/|
|value     |john_prescott_current                                         |
+----------+--------------------------------------------------------------+
|Expected  |The  value  of the userCertificate attribute should be changed|
|results   |as above.                                                     |
+----------+--------------------------------------------------------------+
  """

# LDAP Extension Tests
def blits_test_3_3_12(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Paged Results
def blits_test_3_3_12_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Page completely through a set.
def blits_test_3_3_12_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Page completely through a multi-page set of results.         |
+-----------+-------------------------------------------------------------+
|Reference  |[PAGING] (paragraphs 2, 3, 4)                                |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for paged results with a page|
|           |size of 3.                                                   |
|           |After initial response, request the next page.               |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber<=91100105                                     |
+-----------+-------------------------------------------------------------+
|Expected   |Initial  request  results in three entries plus an indication|
|results    |of 5 total entries in the search result.                     |
|           |Second  request  results  in  a  further  two entries plus an|
|           |indication that there are no more entries.                   |
+-----------+-------------------------------------------------------------+
  """

# Abort paging part-way through a set.
def blits_test_3_3_12_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------------+---------------------------------------------------------+
|Purpose        |Abort   paging  part-way  through  a  multi-page  set  of|
|               |results.                                                 |
+---------------+---------------------------------------------------------+
|Reference      |[PAGING] (paragraphs 2, 3)                               |
+---------------+---------------------------------------------------------+
|Procedure      |Make  a  search  request  asking for paged results with a|
|               |page size of 3.                                          |
|               |After initial response, request the next page.           |
|               |After second page displayed, abort the search. Then make |
|               |a new search with a different filter.                    |
+---------------+---------------------------------------------------------+
|Base           |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US             |
+---------------+---------------------------------------------------------+
|Base           |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=|
|(dc-naming)    |org                                                      |
+---------------+---------------------------------------------------------+
|Scope          |subtree                                                  |
+---------------+---------------------------------------------------------+
|Filter for     |givenname=Adam                                           |
|First Request  |                                                         |
+---------------+---------------------------------------------------------+
|Filter for     |givenname=Adrian                                         |
|Second Request |                                                         |
+---------------+---------------------------------------------------------+
|Expected       |Initial   request   results  in  three  entries  plus  an|
|results        |indication of 26 total entries in the search result.     |
|               |Second request results in a further three entries plus an|
|               |indication that there are more entries.                  |
|               |Third  request  indicates  that  there  are  no  matching|
|               |entries.                                                 |
+---------------+---------------------------------------------------------+
  """

# Server-Side Sorting
def blits_test_3_3_12_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Sort on Single Numeric Attribute
def blits_test_3_3_12_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Sort a set of results on a single numeric attribute.         |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4)                                  |
+-----------+-------------------------------------------------------------+
|Procedure  |Make a search request asking for sorted results.             |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber<=91100105                                     |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |Five  entries  are displayed in order of employee number (and|
|results    |reverse alphabetical order of name).                         |
+-----------+-------------------------------------------------------------+
  """

# Sort on Single Alphabetic Attribute
def blits_test_3_3_12_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------------+---------------------------------------------------------+
|Purpose        |Sort a set of results on a single alphabetic attribute.  |
+---------------+---------------------------------------------------------+
|Reference      |[SORTING] (paragraphs 3, 4)                              |
+---------------+---------------------------------------------------------+
|Procedure      |Make a search request asking for sorted results.         |
+---------------+---------------------------------------------------------+
|Base           |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US             |
+---------------+---------------------------------------------------------+
|Base           |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=|
|(dc-naming)    |org                                                      |
+---------------+---------------------------------------------------------+
|Scope          |subtree                                                  |
+---------------+---------------------------------------------------------+
|Filter         |employeenumber<=91100105                                 |
+---------------+---------------------------------------------------------+
|Sort Key       |givenname                                                |
+---------------+---------------------------------------------------------+
|Expected       |Five entries are displayed in alphabetical order of name.|
|results        |                                                         |
+---------------+---------------------------------------------------------+
  """

# Sort on Multiple Attributes
def blits_test_3_3_12_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Sort a set of results on multiple attributes.               |
+------------+------------------------------------------------------------+
|Reference   |[SORTING] (paragraphs 3, 4)                                 |
+------------+------------------------------------------------------------+
|Procedure   |Make  a  search  request asking for sorted results using two|
|            |sort keys.                                                  |
+------------+------------------------------------------------------------+
|Base        |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                |
+------------+------------------------------------------------------------+
|Base        |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org|
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |(&(employeenumber>=91100125)(employeenumber<=91100128))     |
+------------+------------------------------------------------------------+
|First Sort  |sn                                                          |
|Key         |                                                            |
+------------+------------------------------------------------------------+
|Second Sort |employeenumber                                              |
|Key         |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Four  entries  are  displayed  in order Zoe York, Yuri York,|
|results     |Belinda Zions, Adam Zions.                                  |
+------------+------------------------------------------------------------+
  """

# Sort in reverse order
def blits_test_3_3_12_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Sort in reverse order.                                       |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4)                                  |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for sorted results in reverse|
|           |order.                                                       |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber<=91100105                                     |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |Five entries are displayed in alphabetical order of name (but|
|results    |reverse order of employee number).                           |
+-----------+-------------------------------------------------------------+
  """

# Feature Interactions with Paged and Sorted Results
def blits_test_3_3_12_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Page a Sorted Set.
def blits_test_3_3_12_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test that a Paged, Sorted Set is in Correct Order.           |
+-----------+-------------------------------------------------------------+
|Reference  |[PAGING] (paragraphs 2, 3) [SORTING] (paragraphs 3, 4, 5)    |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request  asking for results to be sorted and|
|           |paged with a page size of 3.                                 |
|           |Page through the results.                                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter for |givenname=Adam                                               |
|First      |                                                             |
|Request    |                                                             |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |Results  are  displayed in order of employee number (which is|
|results    |inverse  alphabetical  order)  consistently across all pages,|
|           |not just within each page.                                   |
+-----------+-------------------------------------------------------------+
  """

# Scrolling View Browsing of Search Results
def blits_test_3_3_12_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Scroll Completely Through Large Set of Results
def blits_test_3_3_12_4_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Scroll Completely Through Large Set of results.              |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4), [VLV] (paragraph 5)             |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for sorted results in reverse|
|           |order.  When  first  page  of  results is displayed, drag the|
|           |scroll bar slider down to the bottom of its range.           |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber>=0                                            |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |The  first  page  (starting  with  Adam  Adams)  is displayed|
|results    |initially.  When  the  slider  is dragged down, the last page|
|           |(ending with Zoe Zions) is displayed.                        |
+-----------+-------------------------------------------------------------+
  """

# Scroll Incrementally through Set of Results
def blits_test_3_3_12_4_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Scroll incrementally through set of results.                 |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4), [VLV] (paragraph 5)             |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for sorted results in reverse|
|           |order. When the first page of results is displayed, click on |
|           |scroll  bar  just below slider. When a new page is displayed,|
|           |click on scroll bar just above slider.                       |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber>=0                                            |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |The  first  page  (starting  with  Adam  Adams)  is displayed|
|results    |initially.  When  the scroll bar is clicked below the slider,|
|           |the  next  page  is  displayed.  When  the scroll bar is then|
|           |clicked above the slider, the first page is displayed again. |
+-----------+-------------------------------------------------------------+
  """

# Scroll Part Way Through Large Set of Results
def blits_test_3_3_12_4_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Scroll Part Way Through Large Set of results.                |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4), [VLV] (paragraph 5)             |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for sorted results in reverse|
|           |order.  When  first  page  of  results is displayed, drag the|
|           |scroll bar about half way down its range.                    |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber>=0                                            |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |The  first  page  (starting  with  Adam  Adams)  is displayed|
|results    |initially. When the slider is dragged down, a page about half|
|           |way  through  (employees  with surnames starting with M, N or|
|           |similar) is displayed.                                       |
+-----------+-------------------------------------------------------------+
  """

# Go to Arbitrary Place in Large Set of Results
def blits_test_3_3_12_4_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Go to Arbitrary Place in Large Set of results.               |
+-----------+-------------------------------------------------------------+
|Reference  |[SORTING] (paragraphs 3, 4), [VLV] (paragraph 5)             |
+-----------+-------------------------------------------------------------+
|Procedure  |Make  a  search  request asking for sorted results in reverse|
|           |order.   When  first  page  of  results  is  displayed,  type|
|           |"91100533".                                                  |
+-----------+-------------------------------------------------------------+
|Base       |ou=Corporate, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Corporate, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber>=0                                            |
+-----------+-------------------------------------------------------------+
|Sort Key   |employeenumber                                               |
+-----------+-------------------------------------------------------------+
|Expected   |The  first  page  (starting  with  Adam  Adams)  is displayed|
|results    |initially.  After  typing  the  number,  the  page of results|
|           |starting with "Jacky Jones" is displayed.                    |
+-----------+-------------------------------------------------------------+
  """

# Language Tags
def blits_test_3_3_12_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Search for Language Tagged Attributes.
def blits_test_3_3_12_5_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search for entries with attributes having particular language|
|           |tags.                                                        |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2596] (paragraph 3.3)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Make a search request.                                       |
+-----------+-------------------------------------------------------------+
|Base       |ou=Languages, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Languages, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |title;lang-en-us=President                                   |
+-----------+-------------------------------------------------------------+
|Expected   |The  entries  for  George  Washington,  Thomas  Jefferson and|
|results    |Abraham Lincoln are returned.                                |
+-----------+-------------------------------------------------------------+
  """

# Check Attribute Subtype Matching.
def blits_test_3_3_12_5_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-------------+-----------------------------------------------------------+
|Purpose      |Search  for  entries with attributes that are subtypes of a|
|             |tagged type.                                               |
+-------------+-----------------------------------------------------------+
|Reference    |[RFC 2596] (paragraph 3.3)                                 |
+-------------+-----------------------------------------------------------+
|Procedure    |Make a search request.                                     |
+-------------+-----------------------------------------------------------+
|Base         |ou=Languages, ou=ExtendedSearch, o=IMC, c=US               |
+-------------+-----------------------------------------------------------+
|Base         |dc=Languages,  dc=ExtendedSearch,  dc=Relative, dc=IMC, dc=|
|(dc-naming)  |org                                                        |
+-------------+-----------------------------------------------------------+
|Scope        |subtree                                                    |
+-------------+-----------------------------------------------------------+
|Filter       |name;lang-fr=*                                             |
+-------------+-----------------------------------------------------------+
|Expected     |The  entries  for Marie Antoinette and Thomas Jefferson are|
|results      |returned.                                                  |
+-------------+-----------------------------------------------------------+
  """

# Search Without Specifying Language Tags.
def blits_test_3_3_12_5_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Search  entries  whose  attributes have language tags without|
|           |specifying language tags in the search request.              |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2596] (paragraph 3.3)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Make a search request.                                       |
+-----------+-------------------------------------------------------------+
|Base       |ou=Languages, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Languages, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |Title=Queen                                                  |
+-----------+-------------------------------------------------------------+
|Expected   |The entry for Marie Antoinette is returned.                  |
|results    |                                                             |
+-----------+-------------------------------------------------------------+
  """

# Comparison with TRUE Return Code
def blits_test_3_3_12_5_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Verify  return  of  TRUE  return  code  for  Compare request|
|            |including a language tag.                                   |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2596] (paragraph 3.4)                                  |
+------------+------------------------------------------------------------+
|Procedure   |Send  a  Compare  request  to a server constructed using the|
|            |information shown below.                                    |
+------------+------------------------------------------------------------+
|DN          |cn=William Pitt, ou=Languages, ou=ExtendedSearch, o=IMC, c= |
|            |US                                                          |
+------------+------------------------------------------------------------+
|Attribute   |title                                                       |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |lang-en-gb;Prime Minister                                   |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |Result code 6 (compareTrue) should be returned.             |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Comparison with noSuchAttribute Return Code
def blits_test_3_3_12_5_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  server  generates a noSuchAttribute error message|
|         |for Compare request that includes a language tag not present in|
|         |an entry.                                                      |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2596] (paragraph 3.4)                                     |
+---------+---------------------------------------------------------------+
|Procedure|Send  a  Compare  request  to  a  server  constructed using the|
|         |information shown below.                                       |
+---------+---------------------------------------------------------------+
|DN       |cn=William Pitt, ou=Languages, ou=ExtendedSearch, o=IMC, c=US  |
+---------+---------------------------------------------------------------+
|Attribute|title                                                          |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|lang-en;Prime Minister                                         |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |Result code 16 (noSuchAttribute) should be returned.           |
|results  |                                                               |
+---------+---------------------------------------------------------------+
  """

# Search for Tagged Attribute Types
def blits_test_3_3_12_5_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify appropriate behavior when the list of attributes to be|
|           |retrieved  for  an  entry includes an attribute with language|
|           |tags.                                                        |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2596] (paragraph 3.5)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit  a  Search  request with a search filter, base, scope,|
|           |and attributes list as indicated below.                      |
+-----------+-------------------------------------------------------------+
|Base       |ou=Languages, ou=ExtendedSearch, o=IMC, c=US                 |
+-----------+-------------------------------------------------------------+
|Base       |dc=Languages, dc=ExtendedSearch, dc=Relative, dc=IMC, dc=org |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Attributes |cn;lang-en-gb, cn;lang-en-us                                 |
+-----------+-------------------------------------------------------------+
|Filter     |employeenumber<=91101102                                     |
+-----------+-------------------------------------------------------------+
|Expected   |The entries for George Washington and Marie Antoinette should|
|results    |be returned with attributes cn;lang-en-us: George Washington,|
|           |cn;lang-en-GB:   George   Washington  and  cn;lang-en:  Marie|
|           |Antionette.                                                  |
+-----------+-------------------------------------------------------------+
  """

# Add and Modify Entries
def blits_test_3_3_12_5_7(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.12.5.7, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

There  are  two parameters in all of the DNs found in paragraph 3.3.12.5.7;
definitions for these parameters are as follows:

<vendor-ID>
    the  vendor  ID  allocated  to you during the testing event; "Vendor1",
    "Vendor2", etc.
<client-ID>
    a  sequence  of IDs assigned by you to each client you plan on testing;
    "Client1", "Client2", …, "Client10" if you have more than 10 clients
    you  wish  to  test,  please notify the event planners so that they can
    make  appropriate  modifications  to  the  LDIF  file that will be used
    during the testing event.

You  should  replace the bracketed place holder for these parameters in all
DNs found in this paragraph prior to performing the tests.
  """

# Add Entry with Language Tags
def blits_test_3_3_12_5_7_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  capability  to  add a new entry to the directory with|
|           |attributes that have language tags.                          |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2596] (paragraph 3.6)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Add  an  entire  new  directory  entry  using the information|
|           |below.                                                       |
+-----------+-------------------------------------------------------------+
|DN         |cn=Florence Nightingale, ou=<client-ID>, ou=<vendor-ID>, ou= |
|           |ExtendedAdd, o=IMC, c=US                                     |
+-----------+-------------------------------------------------------------+
|Attribute  |objectclass                                                  |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |top person organizationalPerson inetOrgPerson                |
|values     |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |sn                                                           |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |Nightingale                                                  |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |cn                                                           |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |Florence Nightingale                                         |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |telephoneNumber                                              |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |+ 44 171 999 1854                                            |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |mail                                                         |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |florence@nhs.gov.uk                                          |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |description;lang-en                                          |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |The lady with the lamp                                       |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |description;lang-fr                                          |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |La femme au lumiere                                          |
|value      |                                                             |
+-----------+-------------------------------------------------------------+
|Expected   |A  new  entry should now be present in the directory with the|
|results    |above attributes.                                            |
+-----------+-------------------------------------------------------------+
  """

# Modify Entry with Language Tags
def blits_test_3_3_12_5_7_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that a single-valued attribute with language tags can be|
|         |replaced.                                                      |
+---------+---------------------------------------------------------------+
|Procedure|Replace an attribute value for an attribute type using a Modify|
|         |request.                                                       |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.6, pp. 32-33) [RFC 2596] (paragraph    |
|         |3.7)                                                           |
+---------+---------------------------------------------------------------+
|DN       |cn=Tony Blair, ou=<client-ID>, ou=<vendor-ID>, ou=             |
|         |ExtendedModify, o=IMC, c=US                                    |
+---------+---------------------------------------------------------------+
|Attribute|title;lang-en-gb                                               |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|First Minister                                                 |
|value    |                                                               |
+---------+---------------------------------------------------------------+
|Expected |The value of the title;lang-en-gb attribute (but not the title;|
|results  |lang-en-us attribute) should be changed as above.              |
+---------+---------------------------------------------------------------+
  """

# Schema-Related Tests
def blits_test_3_3_13(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  * Demonstrate support for schema publication in servers.
  * Check for support for schema modifications via LDAP.
  * Demonstrate support for the extensibleObjectClass.
      + ExtensibleObject object class on add/modify
  * Demonstrate support for the dynamicObject object class.
      + DynamicObject object class on add/modify

To be completed, but to be based on some or all of the following:
   
  * Demonstrate support for IWPS [11], LIPS [12], X.520 [13], X.521 [14],
    and the X.500(96) User Schema for LDAPv3 [RFC 2256]
  * Demonstrate preservation of defined semantic context for attributes as
    projected to users in clients.
  """

# Schema Access tests.
def blits_test_3_3_13_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# subSchemaSubEntry attribute in root DSE.
def blits_test_3_3_13_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------------+-------------------------------------------------------+
|Purpose          |Verify  that  the  subSchemaSubEntry  is present in the|
|                 |root DSE.                                              |
+-----------------+-------------------------------------------------------+
|Reference        |[RFC 2251] (paragraph 3.4)                             |
+-----------------+-------------------------------------------------------+
|Procedure        |Make a search request.                                 |
+-----------------+-------------------------------------------------------+
|Base             |zero length DN ""                                      |
+-----------------+-------------------------------------------------------+
|Scope            |base                                                   |
+-----------------+-------------------------------------------------------+
|Filter           |(objectclass=*)                                        |
+-----------------+-------------------------------------------------------+
|Requested        |subschemasubentry                                      |
|Attributes       |                                                       |
+-----------------+-------------------------------------------------------+
|Expected results |The  attribute  subschemasubentry  is  returned for the|
|                 |root DSE Entry.                                        |
+-----------------+-------------------------------------------------------+
  """

# subSchemaSubEntry attribute in any entry.
def blits_test_3_3_13_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------------+---------------------------------------------------------+
|Purpose        |Verify that the subSchemaSubEntry is present in any entry|
|               |of the Directory.                                        |
+---------------+---------------------------------------------------------+
|Reference      |[RFC 2251] (paragraph 3.2.1)                             |
+---------------+---------------------------------------------------------+
|Procedure      |Make a search request.                                   |
+---------------+---------------------------------------------------------+
|Base           |ou=Search, o=IMC, c=us                                   |
+---------------+---------------------------------------------------------+
|Base           |dc=Search, dc=Relative, dc=IMC, dc=org                   |
|(dc-naming)    |                                                         |
+---------------+---------------------------------------------------------+
|Scope          |subtree                                                  |
+---------------+---------------------------------------------------------+
|Filter         |(cn=margaret*)                                           |
+---------------+---------------------------------------------------------+
|Requested      |subschemasubentry                                        |
|Attributes     |                                                         |
+---------------+---------------------------------------------------------+
|Expected       |2   entries   are   returned   with  only  the  attribute|
|results        |subschemasubentry.                                       |
+---------------+---------------------------------------------------------+
  """

# Schema publication.
def blits_test_3_3_13_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify that the schema is accessible via LDAP.                |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph 3.2.2)                                  |
+----------+--------------------------------------------------------------+
|Procedure |Make  a  search  request  on  root  DSE  to  get the attribute|
|          |subSchemaSubEntry.  Then  make  a base search request with the|
|          |value of subSchemaSubEntry.                                   |
+----------+--------------------------------------------------------------+
|Base      |zero length DN ""                                             |
+----------+--------------------------------------------------------------+
|Scope     |base                                                          |
+----------+--------------------------------------------------------------+
|Filter    |(objectclass=*)                                               |
+----------+--------------------------------------------------------------+
|Requested |subschemasubentry                                             |
|Attributes|                                                              |
+----------+--------------------------------------------------------------+
|Expected  |The   root   DSE   is   returned   with   only  the  attribute|
|results   |subschemasubentry.                                            |
+----------+--------------------------------------------------------------+
|Second    |                                                              |
|Search    |                                                              |
+----------+--------------------------------------------------------------+
|Base      |The value of the subschemasubentry attribute                  |
+----------+--------------------------------------------------------------+
|Scope     |base                                                          |
+----------+--------------------------------------------------------------+
|Filter    |(objectclass=subschema)                                       |
+----------+--------------------------------------------------------------+
|Requested |objectclasses, attributetypes                                 |
|Attributes|                                                              |
+----------+--------------------------------------------------------------+
|Expected  |the schema entry is returned with the 2 requested attributes. |
|results   |Each attribute contains several values.                       |
+----------+--------------------------------------------------------------+
  """

# Schema Modification tests.
def blits_test_3_3_13_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
To perform the tests in paragraph 3.3.13.2, you must authenticate as:

dn: cn=Directory Manager, o=IMC, c=US

with password: controller

Note  that  these  tests cannot be performed by several clients at the same
time because the schema is in one unique entry.
  """

# Adding an Object class.
def blits_test_3_3_13_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+----------+--------------------------------------------------------------+
|Purpose   |Verify that an objectclass can be added in the schema.        |
+----------+--------------------------------------------------------------+
|Reference |[RFC 2251] (paragraph TBD)                                    |
+----------+--------------------------------------------------------------+
|Procedure |Add an attribute value to the attribute "objectclasses" (using|
|          |the modify-add operation).                                    |
+----------+--------------------------------------------------------------+
|DN        |The   schema   DN   is   read   in  the  root  DSE  (attribute|
|          |subschemasubentry)                                            |
+----------+--------------------------------------------------------------+
|Attribute |objectclasses                                                 |
|type      |                                                              |
+----------+--------------------------------------------------------------+
|Attribute |(    1.1.1.1.1.1111   NAME   'IMCTestObject'   DESC   'Useless|
|Value     |ObjectClass for testing' SUP 'top' MUST ( cn $ telephoneNumber|
|          |) MAY ( description $ seeAlso ) )                             |
+----------+--------------------------------------------------------------+
|Requested |subschemasubentry                                             |
|Attributes|                                                              |
+----------+--------------------------------------------------------------+
|Expected  |The   schema   entry  should  have  one  more  "objectclasses"|
|results   |attribute value containing the above value.                   |
+----------+--------------------------------------------------------------+
  """

# Removing an Object class.
def blits_test_3_3_13_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify that an objectclass can be deleted from the schema.     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph TBD)                                     |
+---------+---------------------------------------------------------------+
|Procedure|Delete  an  attribute  value  to  the attribute "objectclasses"|
|         |(using the modify-delete operation).This test must be run just |
|         |after test 3.3.13.2.1                                          |
+---------+---------------------------------------------------------------+
|DN       |The   schema   DN   is   read   in   the  root  DSE  (attribute|
|         |subschemasubentry)                                             |
+---------+---------------------------------------------------------------+
|Attribute|objectclasses                                                  |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|( 1.1.1.1.1.1111 NAME 'IMCTestObject' DESC 'Useless ObjectClass|
|Value    |for  testing'  SUP  'top'  MUST  ( cn $ telephoneNumber ) MAY (|
|         |description $ seeAlso ) )                                      |
+---------+---------------------------------------------------------------+
|Expected |The schema entry should not have the "objectclasses" attribute |
|results  |value for IMCTestObject.                                       |
+---------+---------------------------------------------------------------+
  """

# Adding an Attribute definition in the schema.
def blits_test_3_3_13_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Verify  that  an  attribute  definition  can  be added in the|
|           |schema.                                                      |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph TBD)                                   |
+-----------+-------------------------------------------------------------+
|Procedure  |Add  an  attribute  value  to  the attribute "attributetypes"|
|           |(using the modify-add operation).                            |
+-----------+-------------------------------------------------------------+
|DN         |The   schema   DN   is   read  in  the  root  DSE  (attribute|
|           |subschemasubentry)                                           |
+-----------+-------------------------------------------------------------+
|Attribute  |attributetypes                                               |
|type       |                                                             |
+-----------+-------------------------------------------------------------+
|Attribute  |(  1.1.1.1.1.1111  NAME 'IMCTestAttr' DESC 'Useless attribute|
|Value      |type for testing' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )     |
+-----------+-------------------------------------------------------------+
|Requested  |subschemasubentry                                            |
|Attributes |                                                             |
+-----------+-------------------------------------------------------------+
|Expected   |The  schema  entry  should  have  one  more  "attributetypes"|
|results    |attribute value containing the above value.                  |
+-----------+-------------------------------------------------------------+
  """

# Removing an Attribute definition from the schema.
def blits_test_3_3_13_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Verify  that  an  attribute  definition can be deleted from the|
|         |schema.                                                        |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph TBD)                                     |
+---------+---------------------------------------------------------------+
|Procedure|Delete  an  attribute  value  to the attribute "attributetypes"|
|         |(using the modify-delete operation).This test must be run just |
|         |after test 3.3.13.2.3                                          |
+---------+---------------------------------------------------------------+
|DN       |The   schema   DN   is   read   in   the  root  DSE  (attribute|
|         |subschemasubentry)                                             |
+---------+---------------------------------------------------------------+
|Attribute|attributetypes                                                 |
|type     |                                                               |
+---------+---------------------------------------------------------------+
|Attribute|(  1.1.1.1.1.1111  NAME  'IMCTestAttr'  DESC 'Useless attribute|
|Value    |type for testing' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 )       |
+---------+---------------------------------------------------------------+
|Expected |The schema entry should not have the "attributetypes" attribute|
|results  |value for IMCTestAttr.                                         |
+---------+---------------------------------------------------------------+
  """

# Referral Tests
def blits_test_3_3_14(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Superior Reference
def blits_test_3_3_14_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
Note  that  RFC  2251  does  not  actually  require  the server to return a
referral  in  this case, and that the referral returned (if one is returned
at all) will be configuration-dependant). 
+------------+------------------------------------------------------------+
|Purpose     |Test return of superior reference referral.                 |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraphs 4.1.11, 4.5.3.1)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |o=IMC, c=US                                                 |
+------------+------------------------------------------------------------+
|Base        |dc=IMC, dc=org                                              |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |ou=Server<n>                                                |
+------------+------------------------------------------------------------+
|Expected    |A referral to another server should be returned.            |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Subordinate Reference
def blits_test_3_3_14_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
Note  that  RFC  2251  does  not  actually  require  the server to return a
referral  in  this case, and that the referral returned (if one is returned
at all) will be configuration-dependant). 
+------------+------------------------------------------------------------+
|Purpose     |Test return of subordinate reference referral.              |
+------------+------------------------------------------------------------+
|Reference   |[RFC 2251] (paragraphs 4.1.11, 4.5.3.1)                     |
+------------+------------------------------------------------------------+
|Procedure   |Submit  a  Search  request  with  a search filter, base, and|
|            |scope as indicated below.                                   |
+------------+------------------------------------------------------------+
|Base        |ou=Referrals, o=IMC, c=US                                   |
+------------+------------------------------------------------------------+
|Base        |dc=Referrals, dc=Relative, dc=IMC, dc=org                   |
|(dc-naming) |                                                            |
+------------+------------------------------------------------------------+
|Scope       |subtree                                                     |
+------------+------------------------------------------------------------+
|Filter      |ou=Server<n>                                                |
+------------+------------------------------------------------------------+
|Expected    |A referral to another server should be returned.            |
|results     |                                                            |
+------------+------------------------------------------------------------+
  """

# Named Referral
def blits_test_3_3_14_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# Base Contains Ref Attribute
def blits_test_3_3_14_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  return  of referral for search operation where the base|
|           |contains a ref attribute.                                    |
+-----------+-------------------------------------------------------------+
|Reference  |[NAMEDREF] (paragraph 5.1.1.2, case 2)                       |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below, when bound to a server other than server<|
|           |n>.                                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Server<n>, ou=Servers, o=IMC, c=US                        |
+-----------+-------------------------------------------------------------+
|Base       |dc=Server<n>, dc=Servers, dc=Relative, dc=IMC, dc=org        |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |base/single-level/subtree                                    |
+-----------+-------------------------------------------------------------+
|Filter     |ou=Server<n>                                                 |
+-----------+-------------------------------------------------------------+
|Expected   |The following referral should be returned:                   |
|results    |   ldap://server<n>.dc.opengroup.org/ou=Server<n>, ou=       |
|           |Servers, o=IMC, c=US (x.500 naming) or                       |
|           |   ldap://server<n>.dc.opengroup.org/dc=Server<n>, dc=       |
|           |Servers, dc=Relative, dc=IMC, dc=org (dc naming)             |
+-----------+-------------------------------------------------------------+
  """

# Target Contains Ref Attribute
def blits_test_3_3_14_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test  return  of  referral  for  modify  operation where the|
|            |target contains a ref attribute.                            |
+------------+------------------------------------------------------------+
|Reference   |[NAMEDREF] (paragraph 5.1.1.2, case 2)                      |
+------------+------------------------------------------------------------+
|Procedure   |Attempt  to  add  an attribute value, when bound to a server|
|            |other than server<n>.                                       |
+------------+------------------------------------------------------------+
|DN (X.500   |ou=Server<n>, ou=Servers, o=IMC, c=US                       |
|naming)     |                                                            |
+------------+------------------------------------------------------------+
|DN (dc      |dc=Server<n>, dc=Servers, dc=Relative, dc=IMC, dc=org       |
|naming)     |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |telephoneNumber                                             |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |+33 1 234 5678                                              |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |The following referral should be returned:                  |
|results     |   ldap://server<n>.dc.opengroup.org/ (x.500 naming) or     |
|            |   ldap://server<n>.dc.opengroup.org/ (dc naming)           |
+------------+------------------------------------------------------------+
  """

# Base Subordinate to Entry that Contains Ref Attribute
def blits_test_3_3_14_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  return  of referral for search operation where the base|
|           |is subordinate to an entry that contains a ref attribute.    |
+-----------+-------------------------------------------------------------+
|Reference  |[NAMEDREF] (paragraph 5.1.1.2, case 3)                       |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below, when bound to a server other than server<|
|           |n>.                                                          |
+-----------+-------------------------------------------------------------+
|Base       |cn=John Humphries, ou=Server<n>, ou=Servers, o=IMC, c=US     |
+-----------+-------------------------------------------------------------+
|Base       |cn=John Humphries, dc=Server<n>, dc=Servers, dc=Relative, dc=|
|(dc-naming)|IMC, dc=org                                                  |
+-----------+-------------------------------------------------------------+
|Scope      |base                                                         |
+-----------+-------------------------------------------------------------+
|Filter     |telephoneNumber=*                                            |
+-----------+-------------------------------------------------------------+
|Expected   |The following referral should be returned:                   |
|results    |   ldap://server<n>.dc.opengroup.org/ou=Server<n>, ou=       |
|           |Servers, o=IMC, c=US (x.500 naming) or                       |
|           |   ldap://server<n>.dc.opengroup.org/dc=Server<n>, dc=       |
|           |Servers, dc=Relative, dc=IMC, dc=org (dc naming)             |
+-----------+-------------------------------------------------------------+
  """

# Target Subordinate to Entry that Contains Ref Attribute
def blits_test_3_3_14_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+------------+------------------------------------------------------------+
|Purpose     |Test  return  of  referral  for  modify  operation where the|
|            |target contains a ref attribute.                            |
+------------+------------------------------------------------------------+
|Reference   |[NAMEDREF] (paragraph 5.1.1.2, case 3)                      |
+------------+------------------------------------------------------------+
|Procedure   |Attempt  to  add  an attribute value, when bound to a server|
|            |other than server<n>.                                       |
+------------+------------------------------------------------------------+
|DN (X.500   |cn=John Humphries, ou=Server<n>, ou=Servers, o=IMC, c=US    |
|naming)     |                                                            |
+------------+------------------------------------------------------------+
|DN (dc      |cn=John Humphries, dc=Server<n>, dc=Servers, dc=Relative, dc|
|naming)     |=IMC, dc=org                                                |
+------------+------------------------------------------------------------+
|Attribute   |facsimileTelephoneNumber                                    |
|type        |                                                            |
+------------+------------------------------------------------------------+
|Attribute   |+44 181 432 2000                                            |
|value       |                                                            |
+------------+------------------------------------------------------------+
|Expected    |The following referral should be returned:                  |
|results     |   ldap://server<n>.dc.opengroup.org/ (x.500 naming) or     |
|            |   ldap://server<n>.dc.opengroup.org/ (dc naming)           |
+------------+------------------------------------------------------------+
  """

# Single-Level Search
def blits_test_3_3_14_3_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test  return  of  referral  for single-level search operation|
|           |where an entry that contains a ref attribute is found.       |
+-----------+-------------------------------------------------------------+
|Reference  |[NAMEDREF] (paragraph 5.1.1.3)                               |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below, when bound to a server other than server<|
|           |n>.                                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Servers, o=IMC, c=US                                      |
+-----------+-------------------------------------------------------------+
|Base       |dc=Servers, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |single-level                                                 |
+-----------+-------------------------------------------------------------+
|Filter     |ou=Server<n>                                                 |
|(X.500     |                                                             |
|naming)    |                                                             |
+-----------+-------------------------------------------------------------+
|Filter (dc |dc=Server<n>                                                 |
|naming)    |                                                             |
+-----------+-------------------------------------------------------------+
|Expected   |The following referral should be returned:                   |
|results    |   ldap://server<n>.dc.opengroup.org/ou=Server<n>,ou=        |
|           |Servers,o=IMC,c=US??base (x.500 naming) or                   |
|           |   ldap://server<n>.dc.opengroup.org/dc=Server<n>, dc=       |
|           |Servers,dc=Relative,dc=IMC,dc=org??base (dc naming)          |
+-----------+-------------------------------------------------------------+
  """

# Subtree Search
def blits_test_3_3_14_3_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Test return of referral for subtree search operation where an|
|           |entry that contains a ref attribute is found.                |
+-----------+-------------------------------------------------------------+
|Reference  |[NAMEDREF] (paragraph 5.1.1.4)                               |
+-----------+-------------------------------------------------------------+
|Procedure  |Submit a Search request with a search filter, base, and scope|
|           |as indicated below, when bound to a server other than server<|
|           |n>.                                                          |
+-----------+-------------------------------------------------------------+
|Base       |ou=Servers, o=IMC, c=US                                      |
+-----------+-------------------------------------------------------------+
|Base       |dc=Servers, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |cn=John Humphries                                            |
+-----------+-------------------------------------------------------------+
|Expected   |The following continuation references should be returned:    |
|results    |   ldap://server<n>.dc.opengroup.org/ou=Server<n>,ou=        |
|           |Servers,o=IMC,c=US (x.500 naming) or                         |
|           |   ldap://server<n>.dc.opengroup.org/dc=Server<n>, dc=       |
|           |Servers,dc=Relative,dc=IMC,dc=org (dc naming)                |
|           |                                                             |
|           |There should be 19 continuation references returned: <n>=1, .|
|           |. 20, except the value of <n> for the server to which the    |
|           |client is bound.                                             |
+-----------+-------------------------------------------------------------+
  """

# Transport Security
def blits_test_3_3_15(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
The  tests  in  this  section  are  designed  to be performed with multiple
certificate  generation  products.  Their  descriptions  refer to "CA1" and
"CA2", but if other sets of certificates as described in CATS are
available, then these could be substituted. See the description in 3.3.11.
Each participating server is allocated a unique number <n>. Server <n>
should use the Server<n> certificate generated by CA1 (in file certs1/ serv
<n>) to secure TLS connections.

Clients  that  can  validate server certificates should be set up to accept
certificates that can be validated by the CA1 root certificate (which is in
file certs1/ca_root).

The servers should be set up as follows:
   
    sp;*  Clients  binding  anonymously should not be required to provide a
    certificate.
  * Clients binding as users with entries in the subtree rooted at ou=
    Security, o=IMC, c=US should not be required to provide a certificate.
  * Clients binding as users with entries in the subtree rooted at ou=CAs,
    o=IMC, c=US should be required to provide a certificate.
  """

# START TLS
def blits_test_3_3_15_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
For the tests in this section, clients should use the START TLS mechanism.
  """

# Anonymous Bind over TLS
def blits_test_3_3_15_1_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS-protected simple anonymous bind.                      |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 5.2), [RFC 2830] (paragraph 2.1) [RFC    |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use  TLS.  Issue  an LDAP anonymous BIND|
|         |request.                                                       |
+---------+---------------------------------------------------------------+
|Expected |The   test   is  successful  if  the  LDAP  connection  can  be|
|results  |established  without  errors.  Search  requests  should  now be|
|         |accepted and processed by the server..                         |
+---------+---------------------------------------------------------------+
  """

# Bind With Password Exchange over TLS
def blits_test_3_3_15_1_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  authenticated  TLS-protected  simple  bind  with  correct|
|         |credentials.                                                   |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 6.2), [RFC 2830] (paragraph 2.1) [RFC    |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS. Test authenticated Bind as 'Henri |
|         |Matisse' with a correct password ('Henri001').                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri001                                                       |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """

# TLS with Certificates
def blits_test_3_3_15_1_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# TLS Bind with Valid Certificate
def blits_test_3_3_15_1_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS Certificate bind with valid certificate.              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2830] (paragraph 2.1), [RFC   |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated  by  product with id CA1 for Pablo|
|         |Picasso  (file  certs1/pablo_picasso).  Configure server to use|
|         |the CA1 Root Certificate (file certs1/ca_root) to authenticate |
|         |clients binding as users with entries in the ou=CA1, ou=CAs, o=|
|         |IMC, c=US subtree of the DIT.                                  |
|         |                                                               |
|         |Test authenticated Bind as user with DN below.                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Pablo Picasso, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US          |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """

# TLS Bind with Expired Certificate
def blits_test_3_3_15_1_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS Certificate bind with expired certificate.            |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2830] (paragraph 2.1), [RFC   |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated  by  product  with id CA1 for John|
|         |Constable (file certs1/john_constable). Configure server to use|
|         |the CA1 Root Certificate (file certs1/ca_root) to authenticate |
|         |clients binding as users with entries in the ou=CA1, ou=CAs, o=|
|         |IMC, c=US subtree of the DIT.                                  |
|         |                                                               |
|         |Test authenticated Bind as user with DN below.                 |
+---------+---------------------------------------------------------------+
|DN       |cn=John Constable, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US         |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# TLS Bind with Certificate Validated via Non-Trivial Path
def blits_test_3_3_15_1_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  TLS  Certificate  bind  with an end-user certificate that|
|         |must be validated by a root certificate generated by a product |
|         |other than that used to generate the end-user certificate.     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2830] (paragraph 2.1), [RFC   |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated by product with id CA2 for William|
|         |CA2  Turner  in  the  CA1  branch  of  the  DIT  (file  certs2/|
|         |william_ca1_turner).  Configure  server  to  use  the  CA1 Root|
|         |Certificate   (file  certs1/ca_root)  to  authenticate  clients|
|         |binding as users with entries in the ou=CA1, ou=CAs, o=IMC, c= |
|         |US subtree of the DIT.                                         |
|         |                                                               |
|         |Test authenticated Bind as user with DN below.                 |
+---------+---------------------------------------------------------------+
|DN       |cn=William CA2 Turner, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US     |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """

# TLS Bind with Revoked Certificate in Validation Path
def blits_test_3_3_15_1_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
(NB - this test will not work with currently supplied CRLs.)

+---------+---------------------------------------------------------------+
|Purpose  |Test  TLS  Certificate bind when there is a revoked certificate|
|         |in the certification path.                                     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2830] (paragraph 2.1), [RFC   |
|         |2251] (paragraph 4.2)                                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated by product with id CA2 for Georges|
|         |CA2 Braque in the CA1 branch of the DIT  (in file certs2/      |
|         |georges_ca1_braque).  Configure  server  to  use  the  CA1 Root|
|         |Certificate   (file  certs1/ca_root)  to  authenticate  clients|
|         |binding as users with entries in the ou=CA1, ou=CAs, o=IMC, c= |
|         |US subtree of the DIT.                                         |
|         |                                                               |
|         |Test authenticated Bind as user with DN below.                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Georges CA2 Braque, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US     |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# Bind with Incorrect Credentials over TLS
def blits_test_3_3_15_1_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  authenticated  TLS-protected  simple  bind with incorrect|
|         |credentials.                                                   |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 6.2), [RFC 2830] (paragraph 2.1), [RFC   |
|         |2251] (paragraphs 4.1.10, 4.2)                                 |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS. Test authenticated Bind as 'Henri |
|         |Matisse' with incorrect password ('Henri111').                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri111                                                       |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# Bind With Insufficiently Strong Authentication
def blits_test_3_3_15_1_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test bind without using TLS when TLS is required.              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraphs 4.1.10, 4.2.3)                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to not use TLS. Test simple authenticated Bind|
|         |as 'Henri Matisse' with a correct password ('Henri001').       |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri001                                                       |
+---------+---------------------------------------------------------------+
|Expected |Result code 8 (strongAuthRequired) should be returned. The Bind|
|results  |should fail. The server may not accept and process requests; if|
|         |they   are  accepted,  they  should  be  treated  as  anonymous|
|         |requests.                                                      |
+---------+---------------------------------------------------------------+
  """

# Abort TLS Session
def blits_test_3_3_15_1_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test abrubt closure of TLS connection.                         |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 6.2), [RFC 2830] (paragraphs 2.1 and 4.2)|
|         |[RFC 2251] (paragraph 4.2)                                     |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS and establish connection. Make any |
|         |search  request  and  await results. Take some action that will|
|         |close the underlying TCP connection. Then make it possible for |
|         |the  TCP  connection to be re-established. Make the same search|
|         |request again.                                                 |
+---------+---------------------------------------------------------------+
|Expected |The test is successful if the second search request is rejected|
|results  |with an indication that the service is not available or if the |
|         |client is required to re-establish credentials.                |
+---------+---------------------------------------------------------------+
  """

# Port 636
def blits_test_3_3_15_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
For the tests in this section, clients should use the "Port 636" mechanism.
(This  mechanism  is  not  described in the standards and is expected to be
phased  out  eventually.) Servers should be configured to use LDAP over TLS
(or SSL) on connections to port 636.
  """

# Anonymous Bind over TLS
def blits_test_3_3_15_2_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS-protected simple anonymous bind.                      |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 5.2),  [RFC 2251] (paragraph 4.2)        |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS. Connect to server using port 636, |
|         |and issue an LDAP anonymous BIND request.                      |
+---------+---------------------------------------------------------------+
|Expected |The   test   is  successful  if  the  LDAP  connection  can  be|
|results  |established  without  errors.  Search  requests  should  now be|
|         |accepted and processed by the server..                         |
+---------+---------------------------------------------------------------+
  """

# Bind With Password Exchange over TLS
def blits_test_3_3_15_2_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  authenticated  TLS-protected  simple  bind  with  correct|
|         |credentials.                                                   |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 6.2), [RFC 2251] (paragraph 4.2)         |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS. Connect to server using port 636, |
|         |and  test  authenticated Bind as 'Henri Matisse' with a correct|
|         |password ('Henri001').                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri001                                                       |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """

# TLS with Certificates
def blits_test_3_3_15_2_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
  """

# TLS Bind with Valid Certificate
def blits_test_3_3_15_2_3_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS Certificate bind with valid certificate.              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 9.1), [RFC 2251] (paragraph 4.2)         |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated  by  product with id CA1 for Pablo|
|         |Picasso  (file  certs1/pablo_picasso).  Configure server to use|
|         |the CA1 Root Certificate (file certs1/ca_root) to authenticate |
|         |clients binding as users with entries in the ou=CA1, ou=CAs, o=|
|         |IMC, c=US subtree of the DIT.                                  |
|         |                                                               |
|         |Connect  to  server using port 636, and test authenticated Bind|
|         |as user with DN below.                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=Pablo Picasso, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US          |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """
  
# TLS Bind with Expired Certificate
def blits_test_3_3_15_2_3_2(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test TLS Certificate bind with expired certificate.            |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2251] (paragraph 4.2)         |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated  by  product  with id CA1 for John|
|         |Constable (file certs1/john_constable). Configure server to use|
|         |the CA1 Root Certificate (file certs1/ca_root) to authenticate |
|         |clients binding as users with entries in the ou=CA1, ou=CAs, o=|
|         |IMC, c=US subtree of the DIT.                                  |
|         |                                                               |
|         |Connect  to  server using port 636, and test authenticated Bind|
|         |as user with DN below.                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=John Constable, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US         |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# TLS Bind with Certificate Validated via Non-Trivial Path
def blits_test_3_3_15_2_3_3(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  TLS  Certificate  bind  with an end-user certificate that|
|         |must be validated by a root certificate generated by a product |
|         |other than that used to generate the end-user certificate.     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2251] (paragraph 4.2)         |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated by product with id CA2 for William|
|         |CA2  Turner  in  the  CA1  branch  of  the  DIT  (file  certs2/|
|         |william_ca1_turner).  Configure  server  to  use  the  CA1 Root|
|         |Certificate   (file  certs1/ca_root)  to  authenticate  clients|
|         |binding as users with entries in the ou=CA1, ou=CAs, o=IMC, c= |
|         |US subtree of the DIT.                                         |
|         |                                                               |
|         |Connect  to  server using port 636, and test authenticated Bind|
|         |as user with DN below.                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=William CA2 Turner, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US     |
+---------+---------------------------------------------------------------+
|Expected |The  test  is  successful  if  the  Bind  is successful. Search|
|results  |requests should now be accepted and processed by the server.   |
+---------+---------------------------------------------------------------+
  """

# TLS Bind with Revoked Certificate in Validation Path
def blits_test_3_3_15_2_3_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
(NB. This test will not work with currently-supplied CRLs).

+---------+---------------------------------------------------------------+
|Purpose  |Test  TLS  Certificate bind when there is a revoked certificate|
|         |in the certification path.                                     |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 7.1), [RFC 2251] (paragraph 4.2)         |
+---------+---------------------------------------------------------------+
|Procedure|Configure  client  to  use TLS with Certificate authentication.|
|         |Load  certificate  generated by product with id CA2 for Georges|
|         |CA2 Braque in the CA1 branch of the DIT  (in file certs2/      |
|         |georges_ca1_braque).  Configure  server  to  use  the  CA1 Root|
|         |Certificate   (file  certs1/ca_root)  to  authenticate  clients|
|         |binding as users with entries in the ou=CA1, ou=CAs, o=IMC, c= |
|         |US subtree of the DIT.                                         |
|         |                                                               |
|         |Connect  to  server using port 636, and test authenticated Bind|
|         |as user with DN below.                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=Georges CA2 Braque, ou=TLS, ou=CA1, ou=CAs, o=IMC, c=US     |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# Bind with Incorrect Credentials over TLS
def blits_test_3_3_15_2_4(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test  authenticated  TLS-protected  simple  bind with incorrect|
|         |credentials.                                                   |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2829] (paragraph 6.2),  [RFC 2251] (paragraphs 4.1.10,    |
|         |4.2)                                                           |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS. Connect to server using port 636, |
|         |and  test  authenticated Bind as 'Henri Matisse' with incorrect|
|         |password ('Henri111').                                         |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri111                                                       |
+---------+---------------------------------------------------------------+
|Expected |Result  code  49  (invalidCredentials)  should be returned. The|
|results  |Bind  should  fail.  The  server  may  not  accept  and process|
|         |requests;  if  they  are  accepted,  they  should be treated as|
|         |anonymous requests.                                            |
+---------+---------------------------------------------------------------+
  """

# Bind With Insufficiently Strong Authentication
def blits_test_3_3_15_2_5(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test bind without using TLS when TLS is required.              |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraphs 4.1.10, 4.2.3)                          |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to not use TLS. Connect to server using normal|
|         |LDAP  port,  and  test  simple  authenticated  Bind  as  'Henri|
|         |Matisse' with a correct password ('Henri001').                 |
+---------+---------------------------------------------------------------+
|DN       |cn=Henri Matisse, ou=Security, o=IMC, c=US                     |
+---------+---------------------------------------------------------------+
|Password |Henri001                                                       |
+---------+---------------------------------------------------------------+
|Expected |Result code 8 (strongAuthRequired) should be returned. The Bind|
|results  |should fail. The server may not accept and process requests; if|
|         |they   are  accepted,  they  should  be  treated  as  anonymous|
|         |requests.                                                      |
+---------+---------------------------------------------------------------+
  """

# Abort TLS Session
def blits_test_3_3_15_2_6(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+---------+---------------------------------------------------------------+
|Purpose  |Test abrupt closure of TLS connection.                         |
+---------+---------------------------------------------------------------+
|Reference|[RFC 2251] (paragraph 4.2)                                     |
+---------+---------------------------------------------------------------+
|Procedure|Configure client to use TLS and establish connection. Make any |
|         |search  request  and  await results. Take some action that will|
|         |close the underlying TCP connection. Then make it possible for |
|         |the  TCP  connection to be re-established. Make the same search|
|         |request again.                                                 |
+---------+---------------------------------------------------------------+
|Expected |The test is successful if the second search request is rejected|
|results  |with an indication that the service is not available or if the |
|         |client is required to re-establish credentials.                |
+---------+---------------------------------------------------------------+
  """

# Server Location
def blits_test_3_3_16(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
The tests in this section are designed to be performed in conjunction with
DNS  servers  that  implement SRV records. Each server participating in the
tests  is  assigned  a server identity server1, server2, . . through server
20.  There  is a specific LDIF file for each server, which should be loaded
by  that  server  prior  to  testing.  Since  the SRV record format assumes
dc-naming (see [SRV] paragraph 2), these LDIF files are provided in dc
format and dc-relative format only.

The  tests  pre-suppose  that  there  is  a DNS available that contains the
following SRV records (<n>=1,  .  .  20).
   
   
    _ldap_tcp.server<n>.Servers.Relative.imc.org. IN SRV 0 0 389 server<n
    >.dc.opengroup.org. 
  """

# Locate Server
def blits_test_3_3_16_1(l,x500=1,dc=1,vendor_id=1,client_id=1):
  """
+-----------+-------------------------------------------------------------+
|Purpose    |Bind  Anonymously  to  an  LDAP  server  which  is located by|
|           |looking up SRV records in the DNS.                           |
+-----------+-------------------------------------------------------------+
|Reference  |[RFC 2251] (paragraph 4.2, pp. 20-23), [SRV] (paragraphs 3,  |
|           |4).                                                          |
+-----------+-------------------------------------------------------------+
|Procedure  |Request  to  bind  anonymously to the server for the DN given|
|           |below.  On  successful  bind,  submit a Search request with a|
|           |filter, base, and scope as indicated below.                  |
+-----------+-------------------------------------------------------------+
|DN (dc     |dc=Server<n>, dc=Servers, dc=Relative, dc=imc, dc=org        |
|naming)    |                                                             |
+-----------+-------------------------------------------------------------+
|Base       |dc=Servers, dc=Relative, dc=IMC, dc=org                      |
|(dc-naming)|                                                             |
+-----------+-------------------------------------------------------------+
|Scope      |subtree                                                      |
+-----------+-------------------------------------------------------------+
|Filter     |cn=John Humphreys                                            |
+-----------+-------------------------------------------------------------+
|Requested  |telephonenumber                                              |
|Attributes |                                                             |
+-----------+-------------------------------------------------------------+
|Expected   |The test is successful if the LDAP connection to server n is |
|Results    |established without errors, and if the search request returns|
|           |a telephone number that ends with <n>. Eg. the telephone     |
|           |number returned by server 3 will be +44 181 432103.          |
+-----------+-------------------------------------------------------------+
  """
