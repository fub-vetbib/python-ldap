"""
This is a convenience wrapper for dictionaries
returned from LDAP servers containing attribute
names of variable case.

$Id$
"""

__version__ = """$Revision$"""

from UserDict import UserDict
from string import lower

class cidict(UserDict):
  """
  Case-insensitive bud case-respecting dictionary.
  """

  def __init__(self,default = {}):
    self._keys = {}
    d = {}
    for k,v in default.items():
      lower_k = lower(k)
      self._keys[lower_k] = k
      d[lower_k] = v
    UserDict.__init__(self,d)

  def __getitem__(self,key):
    return self.data[lower(key)]

  def __setitem__(self,key,value):
    lower_key = lower(key)
    self._keys[lower_key] = key
    self.data[lower_key] = value

  def __delitem__(self,key):
    del self.data[lower(key)]

  def has_key(self,key):
    return UserDict.has_key(self,lower(key))

  def get(self,key,failobj):
    try:
      return self[key]
    except KeyError:
      return failobj

  def keys(self):
    return self._keys.values()

  def items(self):
    result = []
    for k in self._keys.values():
      result.append((k,self[k]))
    return result


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


if __debug__ and __name__ == '__main__':
  x = { 'AbCDeF' : 123 }
  cix = cidict(x)
  assert cix["ABCDEF"] == 123
  assert cix.get("ABCDEF",None) == 123
  assert cix.get("not existent",None) is None
  cix["xYZ"] = 987
  assert cix["XyZ"] == 987
  assert cix.get("XyZ",None) == 987
  cix_keys = cix.keys()
  cix_keys.sort()
  assert cix_keys==['AbCDeF','xYZ'],ValueError(repr(cix_keys))
  cix_items = cix.items()
  cix_items.sort()
  assert cix_items==[('AbCDeF',123),('xYZ',987)],ValueError(repr(cix_items))
  del cix["abcdEF"]
  assert not cix.has_key("AbCDef")
