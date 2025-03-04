def parse_database_url(url):
	proto,url=url.split('://',1)
	host,url=url.rsplit('/',1)
	db,url=url.split('?',1)
	pars=url.split('&')
	for par in pars:
		key,value=par.split('=',1)
		if key=='user':
			user=value
		elif key=='password':
			password=value
	return proto,host,db,user,password

class Database(object):
	def __init__(self,dbtype,server,database,username,password):
		self.dbtype,self.server,self.database,self.username,self.password=dbtype,server,database,username,password
		if dbtype == 'sqlite3':
			import sqlite3
			import os
			self.connection=sqlite3.connect(os.path.join(server,database))
		elif dbtype == 'mysql':
			#import MySQLdb
			import pymysql
			pymysql.install_as_MySQLdb()
			self.connection=pymysql.connect(host=server,user=username,passwd=password,db=database)
		else:
			raise Exception("Unexpected database type: %s" % dbtype)
		self.db=self.connection.cursor()
		self.log=self.print_log

	def _query(self,*args):
		args=list(args)
		for i in range(args.count('')):
			args.remove('')
		return ' '.join(args)

	def execute(self,query,*args):
		if self.log:
			fmtQuery = query.replace('?','{}')
			self.log("DbIO > {}".format(fmtQuery.format(*args)))
			#self.log("DbIO > {}".format(fmtQuery.format(*self.connection.literal(args))))
		if self.dbtype == 'mysql':
			query = query.replace('?','%s')
		if args==():
			self.db.execute(query)
		else:
			self.db.execute(query,args)
		if self.dbtype == 'sqlite3':
			self.connection.commit()
		result=list(self.db.fetchall())
		if self.log:
			self.log("DbIO < "+str(result))
		return result

	def new(self,table,variable):
		value=self.select(table,"MAX(?)"%(variable),'')[0][0]
		if not value:
			value=0
		return value+1

	def select(self,table,variables,condition,*args):
		qry=self._query("SELECT "+variables,
				"FROM "+table,
				condition and "WHERE "+condition or '')
		return self.execute(qry,*args)

	def insert(self,table,variables,values,*args):
		qry=self._query("INSERT INTO "+table,
				variables and "(%s)"%variables or '',
				"VALUES ("+values+")")
		return self.execute(qry,*args)

	def update(self,table,variables,condition,*args):
		qry=self._query("UPDATE "+table,
				"SET "+variables,
				condition and "WHERE "+condition or '')
		return self.execute(qry,*args)

	def delete(self,table,condition,*args):
		qry=self._query("DELETE FROM "+table,
				condition and "WHERE "+condition or '')
		return self.execute(qry,*args)

	def print_log(self,log):
		print(log)
