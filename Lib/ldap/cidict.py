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


def strlist_minus(a,b):
  """
  Return list of all items in a which are not in b (a - b).
  a,b are supposed to be lists of case-insensitive strings.
  """
  temp = cidict()
  for elt in b:
    temp[elt] = elt
  result = [
    elt
    for elt in a
    if not temp.has_key(elt)
  ]
  return result


def strlist_intersection(a,b):
  """
  Return intersection of two lists of case-insensitive strings a,b.
  """
  temp = cidict()
  for elt in a:
    temp[elt] = elt
  result = [
    temp[elt]
    for elt in b
    if temp.has_key(elt)
  ]
  return result


def strlist_union(a,b):
  """
  Return union of two lists of case-insensitive strings a,b.
  """
  temp = cidict()
  for elt in a:
    temp[elt] = elt
  for elt in b:
    temp[elt] = elt
  return temp.values()


if __name__ == '__main__':
	x = { 'AbCDeF' : 123 }
	cix = cidict(x)
	assert cix["ABCDEF"] == 123
	assert cix.get("ABCDEF",None) == 123
	assert cix.get("not existent",None) is None
	cix["xYZ"] = 987
	assert cix["XyZ"] == 987
	assert cix.get("XyZ",None) == 987
	del cix["abcdEF"]
	assert not cix.has_key("AbCDef")

