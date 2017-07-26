## this block loads anidb library from LOCAL RELATIVE path
## http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path

import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder ('folder') or parent ('..')
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

# Info:
# cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
# __file__ fails if script is called in different ways on Windows
# __file__ fails if someone does os.chdir() before
# sys.argv[0] also fails because it doesn't not always contains the path

from anidb import *
from config import *
import getopt

class Main(object):
	def __init__(self):
		self.config = Config()
		self.intr=AniDBInterface(dburl=self.config['dburl'],user=self.config['user'],password=self.config['password'],cache_days=self.config['cache_days'],cache_ended=self.config['cache_ended'])
		try:
			opts, args = getopt.getopt(sys.argv[1:],"ha:",['help','adbid='])
		except getopt.GetoptError:
			print sys.argv[0]+' -h'
			sys.exit(2)
		if not opts:
			print "-h for help"
			sys.exit(1)
		for opt, arg in opts:
			if opt in ('-h','--help'):
				print sys.argv[0]+' -a id1[,id2[,..]]'
				print "\t-a cache listed anidbIDs in database"
				sys.exit(1)
			elif opt in ('-a','--adbid'):
				self.adbids = arg.split(',')

	def start(self):
		self.intr.auth(self.config['user'],self.config['password'])
		for id in self.adbids:
			ret = self.intr.anime(aid=id)
			print id,ret.rescode,ret.resstr

try:
	main=Main.__new__(Main)
	main.__init__()
	main.start()
except:
	raise

