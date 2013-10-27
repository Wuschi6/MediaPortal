from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def vibeoListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 850, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def vibeoStreamsListEntry(entry):
	premiumFarbe = 0xCC0000
	if config.mediaportal.premiumize_use.value:
		if re.search('(putlocker|sockshare|bitshare)', entry[0], re.S|re.I):
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 850, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0], premiumFarbe)
				]
		else:
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 850, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
				]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 850, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
			]

class vibeoFilmListeScreen(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True

		self['title'] = Label("vibeo.tv")
		self['ContentTitle'] = Label("Genre:")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		# types:  movies,cinema,series,updates
		self.filmliste =  [("Cinema", "cinema"), ("Movies", "movies"), ("Series", "series"), ("Updates", "updates")]

		self.chooseMenuList.setList(map(vibeoStreamsListEntry, self.filmliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['liste'].getCurrent()[0][0]
		streamLink = self['liste'].getCurrent()[0][1]
		print streamName, streamLink
		self.session.open(vibeoTypeListeScreen, streamName, streamLink)

	def keyCancel(self):
		self.close()

class vibeoTypeListeScreen(Screen):

	def __init__(self, session, filmtitle, filmlink):
		self.session = session
		self.filmlink = filmlink
		self.filmtitle = filmtitle
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up": self.keyUp,
			"down": self.keyDown,
			"right": self.keyRight,
			"left": self.keyLeft
		}, -1)

		self.keyLocked = True
		self['title'] = Label("vibeo.tv")
		self['ContentTitle'] = Label("%s:" % self.filmtitle)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		self['Page'] = Label("")
		self['handlung'] = Label("")

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.keckse = {}

		self.onLayoutFinish.append(self.loadPage)

	#def get_keckse(self):
	#	url = "http://vibeo.tv"
	#	getPage(url, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPage).addErrback(self.dataError)
		
	def loadPage(self):
		print "starte aufruf"
		self.keyLocked = True
		print "keckse:", self.keckse
		
		values = {'bRegex': 'false',
				'bRegex_0': 'false',
				'bRegex_1': 'false',
				'bRegex_2': 'false',
				'bRegex_3': 'false',
				'bRegex_4': 'false',
				'bSearchable_0': 'true',
				'bSearchable_1': 'true',
				'bSearchable_2': 'true',
				'bSearchable_3': 'true',
				'bSearchable_4': 'true',
				'bSortable_0': 'false',
				'bSortable_1': 'true',
				'bSortable_2': 'false',
				'bSortable_3': 'false',
				'bSortable_4': 'true',
				'filter': '',
				'iColumns': '5',
				'iDisplayLength': '100',
				'iDisplayStart': '0',
				'iSortCol_0': '0',
				'iSortingCols': '1',
				'mDataProp_0': '0',
				'mDataProp_1': '1',
				'mDataProp_2': '2',
				'mDataProp_3': '3',
				'mDataProp_4': '4',
				'sColumns': '',
				'sEcho': '1',
				'sSearch': '',
				'sSearch_0': '',
				'sSearch_1': '',
				'sSearch_2': '',
				'sSearch_3': '',
				'sSearch_4': '',
				'sSortDir_0': 'asc',
				'type': self.filmlink}
		url = "http://vibeo.tv/request"
		getPage(url, method='POST', postdata=urlencode(values), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		print "daten bekommen"
		
		if self.filmlink == "updates":
			infos = re.findall('alt=."(Movie|Cinema|Series).".*?=.*?"#tt(.*?).">(.*?)<', data, re.I)
			if infos:
				self.filmliste = []
				for (type,linkid,title) in infos:
					title = "(%s) - %s" % (type, title)
					self.filmliste.append((title,linkid))
				self.chooseMenuList.setList(map(vibeoListEntry, self.filmliste))
				self.loadPic()
				self.keyLocked = False			
		else:
			infos = re.findall('alt=."(Movie|Cinema|Series).".*?/>".*?rel=.*?"#tt(.*?).">(.*?)<.*?/de.png." style=."opacity: (.*?);', data, re.S|re.I)
			if infos:
				self.filmliste = []
				for (type,linkid,title,lang) in infos:
					if lang == "1":
						title = "(%s) - %s" % (type, title)
						self.filmliste.append((title,linkid))
				self.chooseMenuList.setList(map(vibeoListEntry, self.filmliste))
				self.loadPic()
				self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def loadPic(self):
		streamID = self['liste'].getCurrent()[0][1]
		values = {'mID': streamID}
		url = "http://vibeo.tv/request"
		getPage(url, method='POST', postdata=urlencode(values), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.load_info).addErrback(self.dataError)
		
	def load_info(self, data):
		infos = re.findall('"cover":".*?covers..(.*?)".*?"plot":"(.*?)"', data, re.S)
		if infos:
			print infos
			(coverID, handlung) = infos[0]
			streamPic = "http://static.vibeo.tv/covers/%s" % coverID
			self['handlung'].setText(decodeHtml(handlung))
			CoverHelper(self['coverArt']).getCover(streamPic)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.loadPic()

	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.loadPic()

	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		self.loadPic()
		
	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['liste'].getCurrent()[0][0]
		streamLink = self['liste'].getCurrent()[0][1]
		print streamName, streamLink
		if re.match('.*?(Series)', streamName, re.S):
			self.session.open(vibeoEpisdenListeScreen, streamName, streamLink)
		else:
			self.session.open(vibeoStreamListeScreen, streamName, streamLink, 'dump', 'dump')

	def keyCancel(self):
		self.close()

class vibeoEpisdenListeScreen(Screen):

	def __init__(self, session, filmtitle, filmlink):
		self.session = session
		self.filmlink = filmlink
		self.filmtitle = filmtitle
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("vibeo.tv")
		self['ContentTitle'] = Label("Streams for %s:" % self.filmtitle)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		self['Page'] = Label("")
		self['handlung'] = Label("")

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		values = {'mID': self.filmlink}
		url = "http://vibeo.tv/request"
		getPage(url, method='POST', postdata=urlencode(values), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		print "daten bekommen"
		print data
		seasons = re.findall('"seasons":\{(.*?)\}', data, re.S)
		episodes = re.findall('.*?"(.*?)":\[(.*?)\]', seasons[0], re.S)
		if seasons and episodes:
			for s,e in episodes:
				episoden = e.split(',')
				for ep in episoden:
					print s, ep
					self.filmtitle2 = "%s  - S%sE%s" % (self.filmtitle, s, ep)
					self.filmliste.append((self.filmtitle2, self.filmlink, s, ep))
			self.chooseMenuList.setList(map(vibeoListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		if self.keyLocked:
			return
		vtitle = self['liste'].getCurrent()[0][0]
		vlink = self['liste'].getCurrent()[0][1]
		vseason = self['liste'].getCurrent()[0][2]
		vepisode = self['liste'].getCurrent()[0][3]
		print vtitle, vseason, vepisode
		self.session.open(vibeoStreamListeScreen, vtitle, vlink, vseason, vepisode)

	def keyCancel(self):
		self.close()

class vibeoStreamListeScreen(Screen):

	def __init__(self, session, filmtitle, filmlink, season, episode):
		self.session = session
		self.filmlink = filmlink
		self.filmtitle = filmtitle
		self.season = season
		self.episode = episode
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("vibeo.tv")
		self['ContentTitle'] = Label("Streams for %s:" % self.filmtitle)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F1'].hide()
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['page'] = Label("")
		self['Page'] = Label("")
		self['handlung'] = Label("")

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		if re.match('.*?(Series)', self.filmtitle, re.S):
			values = {'language': 'de', 'mID': self.filmlink, 'raw': 'true', 'season': self.season, 'episode': self.episode}
			url = "http://vibeo.tv/request"
			getPage(url, method='POST', postdata=urlencode(values), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

		else:
			values = {'language': 'de', 'mID': self.filmlink, 'raw': 'true'}
			url = "http://vibeo.tv/request"
			getPage(url, method='POST', postdata=urlencode(values), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		print "daten bekommen"
		print data
		streams = re.findall('"name":"(.*?)".*?"URL":"(.*?)"', data, re.S)
		if streams:
			self.filmliste = []
			for (sname, surl) in streams:
				print sname, surl.replace('\\','')
				if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|BitShare|Userporn)', sname, re.S|re.I):
					self.filmliste.append((sname, surl.replace('\\','')))
			self.chooseMenuList.setList(map(vibeoStreamsListEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		if self.keyLocked:
			return
		vibeourl = self['liste'].getCurrent()[0][1]
		print vibeourl
		get_stream_link(self.session).check_link(vibeourl, self.got_link, False)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			self.session.open(SimplePlayer, [(self.filmtitle, stream_url)], showPlaylist=False, ltype='vibeo')

	def keyCancel(self):
		self.close()