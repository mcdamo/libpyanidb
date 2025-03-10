from anidblink import AniDBLink
from database import *
from commands import *
from errors import *

class AniDBInterface:
	def __init__(self,clientname='libpyanidb',clientver='3',server='api.anidb.info',port=9000,listen_port=9876,user=None,password=None,session=None,dburl=None,cache_days=1,cache_ended=False,anime_mask=None):
		self.clientname=clientname
		self.clientver=clientver
		self.anime_mask=anime_mask

		self.link=AniDBLink(server,port,listen_port)
		self.link.session=session
		self.user=user
		self.password=password

		self.mode=1	#mode: 0=queue,1=unlock,2=callback
		self.cache=True
		dburl=dburl and parse_database_url(dburl) or None
		self.dburl=dburl
		self.db=dburl and Database(dburl[0],dburl[1],dburl[2],dburl[3],dburl[4])
		self.db.cache_days=cache_days
		self.db.cache_ended=cache_ended
	
	def handle_response(self,response):
		if response.rescode in ('501','506') and self.user and self.password and response.req.command!='AUTH':
			resp=self.auth(self.user,self.password)
			if resp.rescode not in ('500',):
				response.req.resp=None
				response=self.handle(response.req,response.req.callback)
		if self.db:
			response.req.cache(self,self.db)
	
	def handle(self,command,callback):
		def callback_wrapper(resp):
			self.handle_response(resp)
			if callback:
				callback(resp)
		
		#try to get cached result
		print(command.command)
		if self.cache and self.db and not command.command == 'AUTH':
			cached=command.cached(self,self.db)
			if cached:
				if self.mode==0:
					raise RuntimeError("Mode not yet supported")
				elif self.mode==1:
					return cached
				elif self.mode==2:
					callback_wrapper(cached)
					return

		#auth before request
		if not self.authed() and not command.command == 'AUTH':
			print("auth")
			self.auth(self.user, self.password)
		else:
			print("already auth")
			print(self.authed())
		#make live request
		command.authorize(self.mode,self.link.new_tag(),self.link.session,callback_wrapper)
		self.link.request(command)
		
		#handle mode 1 (wait for response)
		if self.mode==1:
			command.wait_response()
			if self.link.banned:
				raise AniDBError('Banned')
			try:
				command.resp
			except:
				raise AniDBCommandTimeoutError("Command has timed out")
			self.handle_response(command.resp)
			return command.resp

	def authed(self):
		return (self.link.session!=None)

	def auth(self,username,password,nat=None,mtu=None,callback=None):
		"""
		Login to AniDB UDP API
		
		parameters:
		username - your anidb username
		password - your anidb password
		nat	 - if this is 1, response will have "address" in attributes with your "ip:port" (default:0)
		mtu	 - maximum transmission unit (max packet size) (default: 1400)
		
		"""
		return self.handle(AuthCommand(username,password,3,self.clientname,self.clientver,nat,1,'utf8',mtu),callback)
	
	def logout(self,callback=None):
		"""
		Log out from AniDB UDP API
		
		"""
		return self.handle(LogoutCommand(),callback)

	def push(self,notify,msg,buddy=None,callback=None):
		"""
		Subscribe/unsubscribe to/from notifications

		parameters:
		notify	- Notifications about files added?
		msg	- Notifications about message added?
		buddy	- Notifications about buddy events?

		structure of parameters:
		notify msg [buddy]
		
		"""
		return self.handle(PushCommand(notify,msg,buddy),callback)

	def pushack(self,nid,callback=None):
		"""
		Acknowledge notification (do this when you get 271-274)

		parameters:
		nid	- Notification packet id

		structure of parameters:
		nid
		
		"""
		return self.handle(PushAckCommand(nid),callback)

	def notify(self,buddy=None,callback=None):
		"""
		Get number of pending notifications and messages

		parameters:
		buddy	- Also display number of online buddies

		structure of parameters:
		[buddy]
		
		"""
		return self.handle(NotifyCommand(buddy),callback)

	def notifylist(self,callback=None):
		"""
		List all pending notifications/messages
		
		"""
		return self.handle(NotifyListCommand(),callback)

	def notifyget(self,type,id,callback=None):
		"""
		Get notification/message

		parameters:
		type	- (M=message, N=notification)
		id	- message/notification id

		structure of parameters:
		type id
		
		"""
		return self.handle(NotifyGetCommand(type,id),callback)

	def notifyack(self,type,id,callback=None):
		"""
		Mark message read or clear a notification

		parameters:
		type	- (M=message, N=notification)
		id	- message/notification id

		structure of parameters:
		type id
		
		"""
		return self.handle(NotifyAckCommand(type,id),callback)

	def buddyadd(self,uid=None,uname=None,callback=None):
		"""
		Add a user to your buddy list

		parameters:
		uid	- user id
		uname	- name of the user

		structure of parameters:
		(uid|uname)
		
		"""
		return self.handle(BuddyAddCommand(uid,uname),callback)

	def buddydel(self,uid,callback=None):
		"""
		Remove a user from your buddy list

		parameters:
		uid	- user id

		structure of parameters:
		uid
		
		"""
		return self.handle(BuddyDelCommand(uid),callback)

	def buddyaccept(self,uid,callback=None):
		"""
		Accept user as buddy

		parameters:
		uid	- user id

		structure of parameters:
		uid
		
		"""
		return self.handle(BuddyAcceptCommand(uid),callback)

	def buddydeny(self,uid,callback=None):
		"""
		Deny user as buddy

		parameters:
		uid	- user id

		structure of parameters:
		uid
		
		"""
		return self.handle(BuddyDenyCommand(uid),callback)

	def buddylist(self,startat,callback=None):
		"""
		Retrieve your buddy list

		parameters:
		startat	- number of buddy to start listing from

		structure of parameters:
		startat
		
		"""
		return self.handle(BuddyListCommand(startat),callback)

	def buddystate(self,startat,callback=None):
		"""
		Retrieve buddy states

		parameters:
		startat	- number of buddy to start listing from

		structure of parameters:
		startat
		
		"""
		return self.handle(BuddyStateCommand(startat),callback)

	def anime(self,aid=None,aname=None,amask=-1,callback=None):
		"""
		Get information about an anime

		parameters:
		aid	- anime id
		aname	- name of the anime
		amask	- a 7-byte bitfield describing what information you want about the anime - represented as hex string
		
		structure of parameters:
		(aid|aname) [amask]
		
		structure of amask: https://wiki.anidb.net/UDP_API_Definition#ANIME:_Retrieve_Anime_Data
		- starred* rows indicate included by default
		- default amask corresponds to hex 'b2f0e0fc000000'

		byt	bit	key	description
		1*	7	aid			aid
		1	6	-			dateflags
		1*	5	year		year
		1*	4	type		type
		1	3	relatedaids		related aid list
		1	2	relatedtypes	related aid type
		1*	1	-			retired
		1	0	-			retired

		2*	7	romaji		romaji name
		2*	6	kanji		kanji name
		2*	5	name		english name
		2*	4	othername	other name
		2	3	shortnames	short name list
		2	2	synonyms	synonym list
		2	1	-			retired
		2	0	-			retired

		3*	7	totaleps	episodes
		3*	6	eps			highest episode number
		3*	5	specials	special ep count
		3	4	aired		air date
		3	3	ended		end date
		3	2	url			url
		3	1	pic			picname
		3	0	-			retired

		4*	7	rating		rating
		4*	6	votes		vote count
		4*	5	temprating	temp rating
		4*	4	tempvotes	temp vote count
		4*	3	reviewrating	average review rating
		4*	2	reviews		review count
		4	1	awards		award list
		4	0	agerestricted		is 18+ restricted (API does not return any value)

		5	7	-			retired
		5	6	annid		ANN id
		5	5	allcid		allcinema id
		5	4	anfoid		AnimeNfo id
		5	3	tags		tag name list
		5	2	tagids		tag id list
		5	1	tagweights	tag weight list
		5	0	-			date record updated

		6	7	-			character id list
		6	6	-			retired
		6	5	-			retired
		6	4	-			retired
		6	3	-			unused
		6	2	-			unused
		6	1	-			unused
		6	0	-			unused

		7	7	-			specials count
		7	6	-			credits count
		7	5	-			other count
		7	4	-			trailer count
		7	3	-			parody count
		7	2	-			unused
		7	1	-			unused
		7	0	-			unused
		
		NOTE: redundant keys: apid, producernames, producerids
		"""
		return self.handle(AnimeCommand(aid,aname,amask),callback)

	def episode(self,eid=None,aid=None,aname=None,epno=None,callback=None):
		"""
		Get information about an episode

		parameters:
		eid	- episode id
		aid	- anime id
		aname	- name of the anime
		epno	- number of the episode

		structure of parameters:
		eid
		(aid|aname) epno
		
		"""
		return self.handle(EpisodeCommand(eid,aid,aname,epno),callback)
	
	def file(self,fid=None,size=None,ed2k=None,aid=None,aname=None,gid=None,gname=None,epno=None,fmask='79F8FFE90',amask='00000000',callback=None):
		"""
		Get information about a file

		parameters:
		fid	- file id
		size	- size of the file
		ed2k	- ed2k-hash of the file
		aid	- anime id
		aname	- name of the anime
		gid	- group id
		gname	- name of the group
		epno	- number of the episode
		fcode	- a bitfield describing what information you want about the file
		acode	- a bitfield describing what information you want about the anime

		structure of parameters:
		fid [fcode] [acode]
		size ed2k [fcode] [acode]
		(aid|aname) (gid|gname) epno [fcode] [acode]

		structure of fcode:
		bit	key		description
		0	-		-
		1	aid		aid
		2	eid		eid
		3	gid		gid
		4	lid		lid
		5	-		-
		6	-		-
		7	-		-
		8	state		state
		9	size		size
		10	ed2k		ed2k
		11	md5		md5
		12	sha1		sha1
		13	crc32		crc32
		14	-		-
		15	-		-
		16	dublang		dub language
		17	sublang		sub language
		18	quality		quality
		19	source		source
		20	audiocodec	audio codec
		21	audiobitrate	audio bitrate
		22	videocodec		video codec
		23	videobitrate	video bitrate
		24	resolution	video resolution
		25	filetype	file type (extension)
		26	length		length in seconds
		27	description	description
		28	-		-
		29	-		-
		30	filename	anidb file name
		31	-		-
		
		structure of acode:
		bit	key		description
		0	gname		group name
		1	gshortname	group short name
		2	-		-
		3	-		-
		4	-		-
		5	-		-
		6	-		-
		7	-		-
		8	epno		epno
		9	epname		ep english name
		10	epromaji	ep romaji name
		11	epkanji		ep kanji name
		12	-		-
		13	-		-
		14	-		-
		15	-		-
		16	totaleps	anime total episodes
		17	lastep		last episode nr (highest, not special)
		18	year		year
		19	type		type
		20	romaji		romaji name
		21	kanji		kanji name
		22	name		english name
		23	othername	other name
		24	shortnames	short name list
		25	synonyms	synonym list
		26	categories	category list
		27	relatedaids	related aid list
		28	producernames	producer name list
		29	producerids	producer id list
		30	-		-
		31	-		-
		
		"""
		return self.handle(FileCommand(fid,size,ed2k,aid,aname,gid,gname,epno,fmask,amask),callback)
	
	def group(self,gid=None,gname=None,callback=None):
		"""
		Get information about a group

		parameters:
		gid	- group id
		gname	- name of the group

		structure of parameters:
		(gid|gname)
		
		"""
		return self.handle(GroupCommand(gid,gname),callback)
	
	def producer(self,pid=None,pname=None,callback=None):
		"""
		Get information about a producer

		parameters:
		pid	- producer id
		pname	- name of the producer

		structure of parameters:
		(pid|pname)
		
		"""

		return self.handle(ProducerCommand(pid,pname),callback)
	
	def mylist(self,lid=None,fid=None,size=None,ed2k=None,aid=None,aname=None,gid=None,gname=None,epno=None,callback=None):
		"""
		Get information about your mylist

		parameters:
		lid	- mylist id
		fid	- file id
		size	- size of the file
		ed2k	- ed2k-hash of the file
		aid	- anime id
		aname	- name of the anime
		gid	- group id
		gname	- name of the group
		epno	- number of the episode

		structure of parameters:
		lid
		fid
		size ed2k
		(aid|aname) (gid|gname) epno
		
		"""
		return self.handle(MyListCommand(lid,fid,size,ed2k,aid,aname,gid,gname,epno),callback)
	
	def mylistadd(self,lid=None,fid=None,size=None,ed2k=None,aid=None,aname=None,gid=None,gname=None,epno=None,edit=None,state=None,viewed=None,source=None,storage=None,other=None,callback=None):
		"""
		Add/Edit information to/in your mylist

		parameters:
		lid	- mylist id
		fid	- file id
		size	- size of the file
		ed2k	- ed2k-hash of the file
		aid	- anime id
		aname	- name of the anime
		gid	- group id
		gname	- name of the group
		epno	- number of the episode
		edit	- whether to add to mylist or edit an existing entry (0=add,1=edit)
		state	- the location of the file
		viewed	- whether you have watched the file (0=unwatched,1=watched)
		source	- where you got the file (bittorrent,dc++,ed2k,...)
		storage	- for example the title of the cd you have this on
		other	- other data regarding this file

		structure of parameters:
		lid edit=1 [state viewed source storage other]
		fid [state viewed source storage other] [edit]
		size ed2k [state viewed source storage other] [edit]
		(aid|aname) (gid|gname) epno [state viewed source storage other]
		(aid|aname) edit=1 [(gid|gname) epno] [state viewed source storage other]

		structure of state:
		value	meaning
		0	unknown	- state is unknown or the user doesn't want to provide this information
		1	on hdd	- the file is stored on hdd
		2	on cd	- the file is stored on cd
		3	deleted	- the file has been deleted or is not available for other reasons (i.e. reencoded)
		
		structure of epno:
		value	meaning
		x	target episode x
		0	target all episodes
		-x	target all episodes upto x
		
		"""
		return self.handle(MyListAddCommand(lid,fid,size,ed2k,aid,aname,gid,gname,epno,edit,state,viewed,source,storage,other),callback)
	
	def mylistdel(self,lid=None,fid=None,aid=None,aname=None,gid=None,gname=None,epno=None,callback=None):
		"""
		Delete information from your mylist

		parameters:
		lid	- mylist id
		fid	- file id
		size	- size of the file
		ed2k	- ed2k-hash of the file
		aid	- anime id
		aname	- name of the anime
		gid	- group id
		gname	- name of the group
		epno	- number of the episode

		structure of parameters:
		lid
		fid
		(aid|aname) (gid|gname) epno

		"""
		return self.handle(MyListCommand(lid,fid,aid,aname,gid,gname,epno),callback)
	
	def myliststats(self,callback=None):
		"""
		Get summary information of your mylist
		
		"""
		return self.handle(MyListStatsCommand(),callback)
	
	def vote(self,type,id=None,name=None,value=None,epno=None,callback=None):
		"""
		Rate an anime/episode/group

		parameters:
		type	- type of the vote
		id	- anime/group id
		name	- name of the anime/group
		value	- the vote
		epno	- number of the episode

		structure of parameters:
		type (id|name) [value] [epno]

		structure of type:
		value	meaning
		1	rate an anime (episode if you also specify epno)
		2	rate an anime temporarily (you haven't watched it all)
		3	rate a group

		structure of value:
		value	 meaning
		-x	 revoke vote
		0	 get old vote
		100-1000 give vote
		
		"""
		return self.handle(VoteCommand(type,id,name,value,epno),callback)
	
	def randomanime(self,type,callback=None):
		"""
		Get information of random anime
		
		parameters:
		type	- where to take the random anime

		structure of parameters:
		type

		structure of type:
		value   meaning
		0	db
		1	watched
		2	unwatched
		3	mylist
		
		"""
		return self.handle(RandomAnimeCommand(type),callback)
	
	def ping(self,callback=None):
		"""
		Test connectivity to AniDB UDP API
		
		"""
		return self.handle(PingCommand(),callback)

	def encrypt(self,user,apipassword,type=None,callback=None):
		"""
		Encrypt all future traffic

		parameters:
		user	    - your username
		apipassword - your api password
		type	    - type of encoding (1=128bit AES)

		structure of parameters:
		user [type]
		
		"""
		return self.handle(EncryptCommand(user,apipassword,type),callback)

	def encoding(self,name,callback=None):
		"""
		Change encoding used in messages

		parameters:
		name	- name of the encoding

		structure of parameters:
		name

		comments:
		DO NOT USE THIS!
		utf8 is the only encoding which will support all the text in anidb responses
		the responses have japanese, russian, french and probably other alphabets as well
		even if you can't display utf-8 locally, don't change the server-client -connections encoding
		rather, make python convert the encoding when you DISPLAY the text
		it's better that way, let it go as utf8 to databases etc. because then you've the real data stored
		
		"""
		raise AniDBStupidUserError("pylibanidb sets the encoding to utf8 as default and it's stupid to use any other encoding. you WILL lose some data if you use other encodings, and now you've been warned. you will need to modify the code yourself if you want to do something as stupid as changing the encoding")
		return self.handle(EncodingCommand(name),callback)

	def sendmsg(self,to,title,body,callback=None):
		"""
		Send message

		parameters:
		to	- name of the user you want as the recipient
		title	- title of the message
		body	- the message

		structure of parameters:
		to title body
		
		"""
		return self.handle(SendMsgCommand(to,title,body),callback)

	def user(self,user,callback=None):
		"""
		Retrieve user id

		parameters:
		user	- username of the user

		structure of parameters:
		user
		
		"""
		return self.handle(UserCommand(user),callback)

	def uptime(self,callback=None):
		"""
		Retrieve server uptime
		
		"""
		return self.handle(UptimeCommand(),callback)

	def version(self,callback=None):
		"""
		Retrieve server version
		
		"""
		return self.handle(VersionCommand(),callback)

