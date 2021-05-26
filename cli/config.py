from defaultdict import DefaultDict
import os

class Config(DefaultDict):
	__slots__=[]
	def __init__(self):
		DefaultDict.__init__(self)
		self.load()

	def load(self):
		path="~/.libpyanidb"
		try:
			f=open(os.path.expanduser(path))
		except (OSError, IOError) as e:
			try:
				path="/etc/libpyanidb.conf"
				f=open(os.path.expanduser(path))
			except (OSError, IOError) as e:
				print("Config not found")
				exit(2)
		for line in f:
			line=line.strip()
			if line.startswith('#'):
				continue
			if line=='':
				continue
			key,value=line.split('=',1)
			if key=='cache_days':
				value=int(value)
			if key=='cache_ended':
				if value.lower()=='true' or value.lower()=='yes' or value=='1':
					value=True
				else:
					value=False
			if key=='listen_port':
				value=int(value)
			self[key]=value
		f.close()

	def save(self):
		f=open(os.path.expanduser("~/.libpyanidb"),'w')
		for key in self:
			f.write(str(key)+'='+str(self[key])+'\n')
		f.close()

