
import _ldap

ts = _ldap.init_templates(open("/home/d/src/ports/openldap/work/openldap-1.2.11/libraries/libldap/ldaptemplates.conf").read())

for t in ts:
	print t.name
	for r in t.items:
		print ":"
		for c in r:
			print ".", id(c), type(c)
			print c
		print 

print "end"
