# python

'''PerLDAP-like interface to the Python LDAP library
'''

class Conn:
	def __init__(self, host, port = str(_ldap.PORT), 
			bind = '', pswd = '', cert = ldap.AUTH_SIMPLE):
		self.host, self.port, self.binf = host, port, bind
		self._l = _ldap.open(host, int(port))
		self._l.bind_s(bind, pswd, cert)
	def search(self, base, scope, pattern):
		'''search(base, scope, pattern) -> Entry'''
		self._context = self._l.search(scope, pattern)
		return self.nextEntry()
	def searchURL(self, url):
		'''searchURL(url) -> Entry'''
	def nextEntry(self):
		'''nextEntry() -> Entry'''
		ret = self._l.result(self._context)
		if ret[0] == _ldap.RES_SEARCH_RESULT:
			del self._context
			return None
		assert ret[0] == _ldap.RES_SEARCH_ENTRY
		return Entry(ret[1])
	def update(self, entry):
		'''update(entry) -> int'''
	def add(self, entry):
		'''add(entry) -> int'''
	def delete(self, entry):
		'''delete(entry) -> int'''
	def close(self):
		'''close() -> Entry'''
	def modifyRDN(self, rdn, dn):
		'''modifyRDN(rdn, dn) -> Entry'''
	def isURL(self, url):
		'''isURL(url) -> int'''
	def getLD(self):
		'''getLD() -> fd int'''
	def getErrorCode(self):
		'''getErrorCode() -> int'''
	def getErrorString(self):
		'''getErrorString() -> string'''
	def printError(self):
		'''printError()'''
	def setRebindProc(self, func):
		'''setRebindProc(func)'''
	def setDefaultRebindProc(self):
		'''setDefaultRebindProc()'''

class Entry:
	def attrModified(self, attr):
		'''attrModified(attr)'''
	def isModified(self, attr):
		'''isModified(attr) -> int'''
	def remove(self, attr):
		'''remove(attr)'''
	def removeValue(self, attr, val):
		'''removeValue(attr, val)'''
	def addValue(self, attr, val):
		'''addValue(attr, val)'''
	def hasValue(self, attr, val, ignorecase = 0):
		'''hasValue(attr, val [, ignorecase]) -> int'''
	def matchValue(self, attr, ignorecase = 0):
		'''matchValue(attr [, ignorecase]) -> int'''
	def setDN(self, dn):
		'''setDN(dn)'''
	def getDN(self, dn):
		'''getDN(dn) -> string'''
	def size(self, attr):
		'''size(attr) -> int'''
	def exists(self, attr):
		'''exists(attr) -> int'''
	def printLDIF(self):
		'''printLDIF(self)'''
	def __getitem__(self, attr):
		pass
	def __setitem__(self, attr, value):
		pass
