from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def SzeneStreamsGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def SzeneStreamsFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def SzeneStreamsHosterListEntry(entry):
	premiumFarbe = 0xCC0000
	if config.mediaportal.premiumize_use.value:
		if re.search('(putlocker|sockshare|bitshare)', entry[0], re.S|re.I):
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0], premiumFarbe)
				]
		else:
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
				]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
			]

class SzeneStreamsGenreScreen(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/oldGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/oldGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.genreliste.append(("Kinofilme", "http://szene-streams.com/publ/aktuelle_kinofilme/1-"))
		self.genreliste.append(("Last Added", "http://szene-streams.com/publ/0-"))
		self.genreliste.append(("Suche", "http://www.szene-streams.com/publ/"))
		self.genreliste.append(("720p", "http://www.szene-streams.com/publ/720p/26-"))
		self.genreliste.append(("HDRiP", "http://www.szene-streams.com/publ/hd/13-"))
		self.genreliste.append(("Action", "http://www.szene-streams.com/publ/action/2-"))
		self.genreliste.append(("Abenteuer", "http://www.szene-streams.com/publ/abenteuer/3-"))
		self.genreliste.append(("Asia", "http://www.szene-streams.com/publ/asia/4-"))
		self.genreliste.append(("Bollywood", "http://www.szene-streams.com/publ/bollywood/5-"))
		self.genreliste.append(("Biografie", "http://www.szene-streams.com/publ/biografie/6-"))
		self.genreliste.append(("Drama / Romantik", "http://www.szene-streams.com/publ/drama_romantik/8-"))
		self.genreliste.append(("Doku", "http://www.szene-streams.com/publ/dokus_shows/9-"))
		self.genreliste.append(("Familie", "http://www.szene-streams.com/publ/familie/11-"))
		self.genreliste.append(("Geschichte", "http://www.szene-streams.com/publ/geschichte/12-"))
		self.genreliste.append(("HDRiP", "http://www.szene-streams.com/publ/hd/13-"))
		self.genreliste.append(("Horro", "http://www.szene-streams.com/publ/horror/14-"))
		self.genreliste.append(("History", "http://www.szene-streams.com/publ/history/15-"))
		self.genreliste.append(("Komoedie", "http://www.szene-streams.com/publ/komodie/16-"))
		self.genreliste.append(("Krieg", "http://www.szene-streams.com/publ/krieg/17-"))
		self.genreliste.append(("Klassiker", "http://www.szene-streams.com/publ/klassiker/18-"))
		self.genreliste.append(("Mystery", "http://www.szene-streams.com/publ/mystery/19-"))
		self.genreliste.append(("Musik", "http://www.szene-streams.com/publ/musik/20-"))
		self.genreliste.append(("Scifi / Fantasy", "http://www.szene-streams.com/publ/scifi_fantasy/22-"))
		self.genreliste.append(("Thriller / Crime", "http://www.szene-streams.com/publ/thriller_crime/23-"))
		self.genreliste.append(("Wsterm", "http://www.szene-streams.com/publ/western/25-"))
		self.genreliste.append(("Zechentrick / Animation", "http://www.szene-streams.com/publ/zeichentrick_animation/24-"))
		self.chooseMenuList.setList(map(SzeneStreamsGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreName = self['genreList'].getCurrent()[0][0]
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		
		if streamGenreName == "Suche":
			self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Suchbegriff eingeben")), text = "")
		else:
			self.session.open(SzeneStreamsFilmeListeScreen, streamGenreLink)

	def searchCallback(self, callbackStr):
		if callbackStr is not None:
			print callbackStr
			self.session.open(SzeneStreamsSearchScreen, callbackStr)			

	def keyCancel(self):
		self.close()

class SzeneStreamsFilmeListeScreen(Screen):

	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultPageListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultPageListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"red" : self.keyTMDbInfo,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label("Filme Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("1")

		self.keyLocked = True
		self.page = 1
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		if not self.streamGenreLink == "http://szene-streams.com/":
			url = "%s%s" % (self.streamGenreLink, str(self.page))
		else:
			url = self.streamGenreLink
		print url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		printl(error,self,"E")

	def loadPageData(self, data):
		print "daten bekommen"
		movies = re.findall('<div class="ImgWrapNews"><a href="(.*?.[jpg|png])".*?<a class="newstitl entryLink" href="(.*?)"><h2><b>(.*?)</b></h2></a>.*?<div class="MessWrapsNews2" style="height:110px;">(.*?)<', data, re.S)
		if movies:
			self.filmliste = []
			for (image,url,title,h) in movies:
				print title
				self.filmliste.append((decodeHtml(title), url, image, h))
			self.chooseMenuList.setList(map(SzeneStreamsFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		self['page'].setText(str(self.page))
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['filmList'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung.replace('\n','')))
		self.streamPic = self['filmList'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(self.streamPic)

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(SzeneStreamsStreamListeScreen, streamLink, streamName, self.streamPic)

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()

	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()

	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()

	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadPage()

	def keyCancel(self):
		self.close()
		
class SzeneStreamsSearchScreen(Screen):

	def __init__(self, session, streamSearch):
		self.session = session
		self.streamSearch = streamSearch
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultPageListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultPageListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"red" : self.keyTMDbInfo
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label("Filme Auswahl - Search: %s" % self.streamSearch)
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		self['page'] = Label("")

		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print self.streamSearch
		postString = {'a': "2", 'query': self.streamSearch}
		print postString
		getPage("http://www.szene-streams.com/publ/", method='POST', postdata=urlencode(postString), agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		printl(error,self,"E")

	def loadPageData(self, data):
		print "daten bekommen"
		movies = re.findall('<div class="ImgWrapNews"><a href="(.*?.[jpg|png])".*?<a class="newstitl entryLink" href="(.*?)"><h2><b>(.*?)</b></h2></a>.*?<div class="MessWrapsNews2" style="height:110px;">(.*?)<', data, re.S)
		if movies:
			self.filmliste = []
			for (image,url,title,h) in movies:
				print title
				self.filmliste.append((decodeHtml(title), url, image, h))
			self.chooseMenuList.setList(map(SzeneStreamsFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self['name'].setText(streamName)
		streamHandlung = self['filmList'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(streamHandlung.replace('\n','')))
		self.streamPic = self['filmList'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(self.streamPic)

	def keyOK(self):
		if self.keyLocked:
			return
		streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		self.session.open(SzeneStreamsStreamListeScreen, streamLink, streamName, self.streamPic)

	def keyTMDbInfo(self):
		if TMDbPresent:
			title = self['filmList'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()

	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()

	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()

	def keyCancel(self):
		self.close()


class SzeneStreamsStreamListeScreen(Screen):

	def __init__(self, session, streamFilmLink, streamName, streamPic):
		self.session = session
		self.streamFilmLink = streamFilmLink
		self.streamName = streamName
		self.streamPic = streamPic

		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/m4kdefaultListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/m4kdefaultListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Szene-Streams.com")
		self['name'] = Label(self.streamName)
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()

		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		CoverHelper(self['coverArt']).getCover(self.streamPic)
		getPage(self.streamFilmLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		printl(error,self,"E")

	def loadPageData(self, data):
		print "daten bekommen"
		raw = re.findall('(<legend><b><font color="#ff0000">.*?</fieldset></div>)', data, re.S)
		if raw:
			streams = []
			for each in raw:
				if re.match('.*?iframe.*?src', each, re.S|re.I):
					streams += re.findall('<font color="#ff0000">.*?src=".*?/player/(.*?).[gif|jpg|png]".*?<iframe.*?src=["|\'](.*?)["|\']', each, re.S|re.I)
				else:
					streams += re.findall('<font color="#ff0000">.*?src=".*?/player/(.*?).[gif|jpg|png]".*?</font>.*?target="_blank" href=["|\'](.*?)["|\']', each, re.S|re.I)
		if streams:
			for (hostername,stream) in streams:
				#if re.match('.*?(videomega|played|putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|flash x|Divxmov|Putme|mighty|youwatch|fast_stream)', hostername.strip(' '), re.S|re.I):
				print hostername.strip(' '), stream.strip('\n')
				hostername = hostername.replace('_logo','').replace('logo_','').replace('.logo','').replace('.j','').replace('.g','').replace('.p','')
				self.filmliste.append((hostername.strip(' '), stream.strip('\n')))
			self.chooseMenuList.setList(map(SzeneStreamsHosterListEntry, self.filmliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		print self.streamName, streamLink
		get_stream_link(self.session).check_link(streamLink, self.got_link)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			self.session.open(SimplePlayer, [(self.streamName, stream_url, self.streamPic)], showPlaylist=False, ltype='szenestreams', cover=True)

	def keyCancel(self):
		self.close()