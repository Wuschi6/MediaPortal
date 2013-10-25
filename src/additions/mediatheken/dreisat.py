	# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def dreisatEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def dreisatEntry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class dreisatGenreScreen(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultGenreScreenCover.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreenCover.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"	: self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("3sat Mediathek")
		self['ContentTitle'] = Label("Genre:")
		self['name'] = Label("Auswahl:")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()

		self.keyLocked = True
		self.filmliste = []

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = "http://www.3sat.de/mediathek/?mode=sendungenaz0"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('class="mediatheklistbox.*?_hover".*?href="(.*?)".*?img\sclass=.*?MediathekListPic"\salt="(.*?)"\ssrc="(.*?)"', data, re.S)
		if raw:
			for (Url, Title, Image) in raw:
				self.filmliste.append((decodeHtml(Title), Url, Image))
		url = "http://www.3sat.de/mediathek/?mode=sendungenaz1"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData2).addErrback(self.dataError)

	def parseData2(self, data):
		raw = re.findall('class="mediatheklistbox.*?_hover".*?href="(.*?)".*?img\sclass=.*?MediathekListPic"\salt="(.*?)"\ssrc="(.*?)"', data, re.S)
		if raw:
			for (Url, Title, Image) in raw:
				self.filmliste.append((decodeHtml(Title), Url, Image))
				self.chooseMenuList.setList(map(dreisatEntry, self.filmliste))
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		ImageUrl = "http://www.3sat.de" + self['genreList'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(ImageUrl)

	def keyOK(self):
		Name = self['genreList'].getCurrent()[0][0]
		Link = "http://www.3sat.de/mediathek/" + self['genreList'].getCurrent()[0][1]
		self.session.open(dreisatListScreen, Link, Name)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()
		self.showInfos()

	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()
		self.showInfos()

	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()
		self.showInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()
		self.showInfos()

	def keyCancel(self):
		self.close()

class dreisatListScreen(Screen):

	def __init__(self, session, Link, Name):
		self.session = session
		self.Link = Link
		self.Name = Name
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
		"nextBouquet" : self.keyPageUp,
		"prevBouquet" : self.keyPageDown
		}, -1)

		self['title'] = Label("3sat Mediathek")
		self['ContentTitle'] = Label("Genre: %s" % self.Name)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("Page: ")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.page = 0
		self.lastpage = 0
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		url = self.Link + "&mode=verpasst" + str(self.page)
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		lastpage = re.search('class="ClnNextNblEnd".*?mode=verpasst([\d]+)\&amp;red', data, re.S)
		if lastpage:
			self.lastpage = int(lastpage.group(1))+1
			self['page'].setText("%s / %s" % (str(self.page+1), str(self.lastpage)))
		else:
			lastpage = re.search('ClnInfo.*?class="mediathek_menu_.*?([\d]+)&nbsp;.*?class="ClnNextLock', data, re.S)
			if lastpage:
				self.lastpage = int(lastpage.group(1))
				self['page'].setText("%s / %s" % (str(self.page+1), str(self.lastpage)))
			else:
				self.lastpage = 0
				self['page'].setText("%s / 1" % str(self.page+1))

		raw = re.findall('BoxPicture.*?src="(.*?)".*?BoxHeadline.*?href=".*?obj=(.*?)">(.*?)<.*?FloatText.*?href=".*?">(.*?)</a>', data, re.S)
		if raw:
			for (Image, id, Title, Handlung) in raw:
				self.filmliste.append((decodeHtml(Title), id, Image, Handlung))
			self.chooseMenuList.setList(map(dreisatEntry1, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		coverUrl = "http://www.3sat.de" + self['liste'].getCurrent()[0][2]
		handlung = self['liste'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		CoverHelper(self['coverArt']).getCover(coverUrl)

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 1:
			self.page -= 1
			self.loadPage()

	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page+1 < self.lastpage:
			self.page += 1
			self.loadPage()

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()
		self.showInfos()

	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()
		self.showInfos()

	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()
		self.showInfos()

	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()
		self.showInfos()

	def keyOK(self):
		if self.keyLocked:
			return
		self.title = self['liste'].getCurrent()[0][0]
		id = self['liste'].getCurrent()[0][1].replace('amp;','')
		url = "http://www.3sat.de/mediathek/xmlservice/web/beitragsDetails?ak=web&id=%s" % id
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getDataStream).addErrback(self.dataError)

	def getDataStream(self, data):
		stream = re.findall('basetype="h264_aac_mp4.*?".*?<quality>veryhigh</quality>.*?<url>(http://[nrodl|rodl].*?zdf.de.*?.mp4)</url>', data, re.S)
		if stream:
			playlist = []
			playlist.append((self.title, stream[0]))
			self.session.open(SimplePlayer, playlist, showPlaylist=False, ltype='3sat')

	def keyCancel(self):
		self.close()