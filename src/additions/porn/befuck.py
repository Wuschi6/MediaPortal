# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def befuckEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def befuckEntry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class befuckGenreScreen(Screen):

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

		self['title'] = Label("BeFuck.com")
		self['ContentTitle'] = Label("Genre:")
		self['name'] = Label("")
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
		url = "http://www.befuck.com/categories/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('class="ic">.*?<a\shref="(.*?)".*?src="(.*?)">.*?<figcaption>(.*?)</figcaption>.*?</span><b>(.*?)</b></p>', data, re.S)
		if raw:
			self.filmliste = []
			for (Url, Image, Title, Videos) in raw:
				self.filmliste.append((decodeHtml(Title), Url, Image, Videos))
			self.chooseMenuList.setList(map(befuckEntry, self.filmliste))
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		Title = self['genreList'].getCurrent()[0][0].strip()
		ImageUrl = self['genreList'].getCurrent()[0][2]
		self['name'].setText(Title)
		CoverHelper(self['coverArt']).getCover(ImageUrl)

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

	def keyOK(self):
		if self.keyLocked:
			return
		Name = self['genreList'].getCurrent()[0][0]
		Link = self['genreList'].getCurrent()[0][1]
		self.session.open(befuckListScreen, Link, Name)

	def keyCancel(self):
		self.close()

class befuckListScreen(Screen):

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

		self['title'] = Label("BeFuck.com")
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
		self.page = 1
		self.lastpage = 1
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		url = self.Link + str(self.page) + "/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		parselastpage = re.findall('<nav\sid="pgn">(.*?)</nav>', data, re.S)
		lastpage = re.findall('<a href=".*?" title=".*?">(.*?)</a>', parselastpage[0], re.S)
		if lastpage:
			self.lastpage = int(lastpage[-1])
			self['page'].setText("%s / %s" % (str(self.page), str(self.lastpage)))
		else:
			self.lastpage = 1
			self['page'].setText("%s / 1" % str(self.page))

		raw = re.findall('<div\sclass="ic">.*?</div>.*?href="(.*?)" title="(.*?)">.*?src="(.*?)".*?<span>(.*?)</span>', data, re.S)
		if raw:
			for (Link, Title, Image, Lenght) in raw:
				Title = Title.strip()
				self.filmliste.append((decodeHtml(Title), Link, Image, Lenght))
			self.chooseMenuList.setList(map(befuckEntry1, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		coverUrl = self['liste'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(coverUrl)

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
		if self.page < self.lastpage:
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
		Link = self['liste'].getCurrent()[0][1]
		getPage(Link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamData).addErrback(self.dataError)

	def getStreamData(self, data):
		self.title = self['liste'].getCurrent()[0][0]
		videoLink = re.findall("video_url:\s'(.*?)'", data, re.S)
		if videoLink:
			self.session.open(SimplePlayer, [(self.title, videoLink[0])], showPlaylist=False, ltype='befuck')

	def keyCancel(self):
		self.close()