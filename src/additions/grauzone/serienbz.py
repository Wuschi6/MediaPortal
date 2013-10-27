# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def SerienEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def SerienListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def SerienStreamListEntry(entry):
	if config.mediaportal.premiumize_use.value:
		premiumFarbe = 0xCC0000
		if re.search('(putlocker|sockshare|bitshare)', entry[0], re.S|re.I):
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0], premiumFarbe)
				]
		else:
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
				]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
			]

def sbzWatchListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class SerienFirstScreen(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"	: self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Serien.bz")
		self['ContentTitle'] = Label("Genre:")
		self['name'] = Label("Auswahl:")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.genreliste.append(("Serien A-Z","dump"))
		self.genreliste.append(("Watchlist","dump"))
		self.chooseMenuList.setList(map(SerienEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		Auswahl = self['genreList'].getCurrent()[0][0]
		if Auswahl == "Serien A-Z":
			self.session.open(SerienLetterScreen)
		else:
			self.session.open(sbzWatchlistScreen)

	def keyCancel(self):
		self.close()

class SerienLetterScreen(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"	: self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Serien.bz")
		self['ContentTitle'] = Label("Genre:")
		self['name'] = Label("Auswahl:")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = "http://serien.bz"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('<a class="LetterMode " href="(.*?)">(.*?)<', data, re.S)
		if raw:
			self.filmliste = []
			for (serienUrl, serienTitle) in raw:
				self.filmliste.append((decodeHtml(serienTitle), serienUrl))
			self.chooseMenuList.setList(map(SerienEntry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		if self.keyLocked:
			return
		serienName = self['genreList'].getCurrent()[0][0]
		serienLink = self['genreList'].getCurrent()[0][1]
		self.session.open(SerienSecondScreen, serienLink, serienName)

	def keyCancel(self):
		self.close()

class SerienSecondScreen(Screen):

	def __init__(self, session, serienLink, serienName):
		self.session = session
		self.serienLink = serienLink
		self.serienName = serienName
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
		"ok"	: self.keyOK,
		"cancel": self.keyCancel,
		"up" : self.keyUp,
		"down" : self.keyDown,
		"right" : self.keyRight,
		"left" : self.keyLeft,
		"green" : self.addWatchlist
		}, -1)

		self['title'] = Label("Serien.bz")
		self['ContentTitle'] = Label("Auswahl: %s" % self.serienName)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("Watchlist")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.page = 0
		self.ImageUrl = ""
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		if self.serienName == "Top50":
			url = "http://serien.bz"
		else:
			url = self.serienLink
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('<li><a href="(.*?)".*?>(.*?)</a>', data, re.S)
		if raw:
			self.filmliste = []
			for (serienUrl, serienTitle) in raw:
				self.filmliste.append((decodeHtml(serienTitle), serienUrl))
			self.chooseMenuList.setList(map(SerienListEntry, self.filmliste))
			self.keyLocked = False
			self.loadInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def loadInfos(self):
		serienUrl = self['liste'].getCurrent()[0][1]
		getPage(serienUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.showInfos).addErrback(self.dataError)

	def showInfos(self, data):
		sbzCover = re.findall('<div class="entry">.*?<p.*?src="(.*?)".*?</p>.*?<p.*?</p>.*?<p.*?</p>', data, re.S)
		if sbzCover:
			self.ImageUrl = "http://serien.bz%s" % sbzCover[0]
			CoverHelper(self['coverArt']).getCover(self.ImageUrl)
		else:
			self.ImageUrl = ""
		serienTitle = self['liste'].getCurrent()[0][0]
		if re.match('.*?Sorry, but there.*?category yet.</h2>', data, re.S):
			self['handlung'].setText("Kein Stream vorhanden!")
			self['name'].setText("Kein Stream vorhanden!")
		else:
			self['name'].setText(decodeHtml(serienTitle))
			sbzdescription = re.findall('<div class="entry">.*?<p.*?</p>.*?<p.*?</p>.*?<p style="text-align: left;">(.*?)</p>', data, re.S)
			self.handlung = sbzdescription
			if sbzdescription:
				self['handlung'].setText(decodeHtml(sbzdescription[0]))
			else:
				self['handlung'].setText("Keine Infos gefunden.")

	def addWatchlist(self):
		if self.keyLocked:
			return

		self.serienName = self['liste'].getCurrent()[0][0]
		self.serienLink = self['liste'].getCurrent()[0][1]

		print self.serienName, self.serienLink, self.ImageUrl, self.handlung

		if not fileExists(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist"):
			print "erstelle watchlist"
			open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist","w").close()

		if fileExists(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist"):
			print "schreibe watchlist", self.serienName, self.serienLink, self.ImageUrl, self.handlung
			writePlaylist = open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist","a")
			writePlaylist.write('"%s" "%s" "%s" "%s"\n' % (self.serienName, self.serienLink, self.ImageUrl, self.handlung))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("%s wurde zur watchlist hinzugefuegt." % self.serienName), MessageBox.TYPE_INFO, timeout=3)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.loadInfos()

	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.loadInfos()

	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		self.loadInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		self.loadInfos()

	def keyOK(self):
		if self.keyLocked:
			return
		serienName = self['liste'].getCurrent()[0][0]
		serienLink = self['liste'].getCurrent()[0][1]

		print serienName, serienLink
		
		self.session.open(SerienEpListingScreen, serienLink, serienName, self.ImageUrl)

	def keyCancel(self):
		self.close()

class SerienEpListingScreen(Screen):

	def __init__(self, session, serienLink, serienName, serienPic):
		self.session = session
		self.serienLink = serienLink
		self.serienName = serienName
		self.serienPic = serienPic
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
		"ok"	: self.keyOK,
		"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Serien.bz")
		self['ContentTitle'] = Label("Serie: %s" % self.serienName)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = self.serienLink
		CoverHelper(self['coverArt']).getCover(self.serienPic)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		streams_raw = re.findall('>Staffel:.(.*?)</th>(.*?)</table>', data, re.S)
		if streams_raw:
			self.filmliste = []
			for staffel,ep_raw in streams_raw:
				ep_raw2 = re.findall('<strong>Episode.(.*?)</strong>(.*?</p>)', ep_raw,)
				if ep_raw2:
					for episode,ep_rawData in ep_raw2:
						streams = re.findall('<strong>Stream:</strong> <a href="(.*?)".*?\| (.*?)<', ep_rawData, re.S)
						if streams:
							if int(staffel) < 10:
								s = "S0%s" % str(staffel)
							else:
								s = "S%s" % str(staffel)

							if int(episode) < 10:
								e = "E0%s" % str(episode)
							else:
								e = "E%s" % str(episode)

							title = "%s%s" % (s, e)

							self.filmliste.append((title, streams))
					self.chooseMenuList.setList(map(SerienListEntry, self.filmliste))
					self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		serienName = self['liste'].getCurrent()[0][0]
		serienLink = self['liste'].getCurrent()[0][1]

		print serienName, serienLink

		self.session.open(SerienStreamListingScreen, serienLink, serienName, self.serienPic)

	def keyCancel(self):
		self.close()

class SerienStreamListingScreen(Screen):

	def __init__(self, session, serienLink, serienName, serienPic):
		self.session = session
		self.serienLink = serienLink
		self.serienName = serienName
		self.serienPic = serienPic
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
		"ok"	: self.keyOK,
		"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Serien.bz")
		self['ContentTitle'] = Label("Streams: %s" % self.serienName)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		CoverHelper(self['coverArt']).getCover(self.serienPic)
		for hoster,hostrname in self.serienLink:
			self.filmliste.append((hostrname, hoster))
		self.chooseMenuList.setList(map(SerienStreamListEntry, self.filmliste))
		self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		hostername = self['liste'].getCurrent()[0][0]
		hoster = self['liste'].getCurrent()[0][1]

		print hostername, hoster
		get_stream_link(self.session).check_link(hoster, self.playfile)

	def playfile(self, stream_url):
		if stream_url != None:
			self.session.open(SimplePlayer, [(self.serienName, stream_url, self.serienPic)], showPlaylist=False, ltype='serien.bz', cover=True)

	def keyCancel(self):
		self.close()

class sbzWatchlistScreen(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/m4kdefaultPageListeScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/m4kdefaultPageListeScreen.xml"

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
			"red"	: self.delWatchListEntry
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Watchlist Auswahl:")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.watchListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.watchListe = []
		if fileExists(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist"):
			print "read watchlist"
			readStations = open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist","r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(title, link, image, handlung) = data[0]
					print title, link, image
					self.watchListe.append((title, link, image, handlung))
			print "Load Watchlist.."
			self.watchListe.sort()
			self.chooseMenuList.setList(map(sbzWatchListEntry, self.watchListe))
			readStations.close()
			self.showInfos()
			self.keyLocked = False

	def showInfos(self):
		if fileExists(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist"):
			print "read watchlist"
			readStations = open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist","r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					self.ImageUrl = self['filmList'].getCurrent()[0][2]
					self.Handlung = self['filmList'].getCurrent()[0][3]
					self['handlung'].setText(decodeHtml(self.Handlung))
					CoverHelper(self['coverArt']).getCover(self.ImageUrl)
		else:
			self['handlung'].setText("Keine Infos gefunden.")
			picPath = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/images/no_coverArt.png" % config.mediaportal.skin.value
			self.ShowCoverFile(picPath)

	def ShowCoverFile(self, picPath):
		if fileExists(picPath):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload

	def delWatchListEntry(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		entryDeleted = False
		selectedName = self['filmList'].getCurrent()[0][0]

		writeTmp = open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist.tmp","w")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist"):
			readWatchlist = open(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist","r")
			for rawData in readWatchlist.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(title, link, image, handlung) = data[0]
					if title != selectedName:
						writeTmp.write('"%s" "%s" "%s" "%s"\n' % (title, link, image, handlung))
					else:
						if entryDeleted:
							writeTmp.write('"%s" "%s" "%s" "%s"\n' % (title, link, image, handlung))
						else:
							entryDeleted = True
			readWatchlist.close()
			writeTmp.close()
			shutil.move(config.mediaportal.watchlistpath.value+"mp_sbz_watchlist.tmp", config.mediaportal.watchlistpath.value+"mp_sbz_watchlist")
			self.loadPage()

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.showInfos()

	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.showInfos()

	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.showInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.showInfos()

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		serienName = self['filmList'].getCurrent()[0][0]
		serienLink = self['filmList'].getCurrent()[0][1]
		serienPic = self['filmList'].getCurrent()[0][2]
		self.session.open(SerienEpListingScreen, serienLink, serienName, serienPic)

	def keyCancel(self):
		self.close()