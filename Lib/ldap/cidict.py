# $Id$
"""
	This is a convenience wrapper for dictionaries
	returned from LDAP servers containing attribute
	names of variable case.
"""

__version__ = """$Revision$"""

from UserDict import UserDict
from string import lower

class cidict(UserDict):
	"""Case-insensitive dictionary."""
	def __init__(self, default = {}):
		d = {}
		for k,v in default.items():
			d[lower(k)] = v;
		UserDict.__init__(self, d)
	def __getitem__(self, name):
		return self.data[lower(name)]
	def __setitem__(self, name, value):
		self.data[lower(name)] = value
	def __delitem__(self, name):
		del self.data[lower(name)]
	def has_key(self, name):
		return UserDict.has_key(self, lower(name))

if __name__ == '__main__':
	x = { 'AbCDeF' : 123 }
	cix = cidict(x)
	assert cix["ABCDEF"] == 123
	cix["xYZ"] = 987
	assert cix["XyZ"] == 987
	del cix["abcdEF"]
	assert not cix.has_key("AbCDef")

