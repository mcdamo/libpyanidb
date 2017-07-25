from defaultdict import DefaultDict
import os

class Config(DefaultDict):
	__slots__=[]
	def __init__(self):
		DefaultDict.__init__(self)
		self.load()

	def load(self):
		f=file(os.path.expanduser("~/.libpyanidb"))
		for line in f:
			line=line.strip()
			if line.startswith('#'):
				continue
			if line=='':
				continue
			key,value=line.split('=',1)
			self[key]=value
		f.close()

	def save(self):
		f=file(os.path.expanduser("~/.libpyanidb"),'w')
		for key in self:
			f.write(str(key)+'='+str(self[key])+'\n')
		f.close()

