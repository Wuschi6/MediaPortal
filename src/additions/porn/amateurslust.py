# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def amateurslustEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def amateurslustEntry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class amateurslustGenreScreen(Screen):

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

		self['title'] = Label("AmateursLust.com")
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
		url = "http://www.amateurslust.com/categories.html"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		parse = re.findall('<h1>Porn\sCategories</h1>(.*?)id="right-banners-main', data, re.S)
		raw = re.findall('<a\shref="(.*?)".*?<h3>(.*?)</h3>.*?src="(.*?)"\s/>', parse[0], re.S)
		if raw:
			self.filmliste = []
			for (Url, Title, Image) in raw:
				self.filmliste.append((decodeHtml(Title), Url, Image))
			self.chooseMenuList.setList(map(amateurslustEntry, self.filmliste))
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
		self.session.open(amateurslustListScreen, Link, Name)

	def keyCancel(self):
		self.close()

class amateurslustListScreen(Screen):

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

		self['title'] = Label("AmateursLust.com")
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
		url = "http://www.amateurslust.com" + self.Link + "page" + str(self.page) + "/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		parselastpage = re.findall('<ul\sclass="paging">(.*?)<div\sclass="banners-horizontal">', data, re.S)
		lastpage = re.findall('<li><a\shref=".*?"\stitle="View page.*?">(.*?)</a></li>', parselastpage[0], re.S)
		if lastpage:
			self.lastpage = int(lastpage[-1])
			self['page'].setText("%s / %s" % (str(self.page), str(self.lastpage)))
		else:
			self.lastpage = 1
			self['page'].setText("%s / 1" % str(self.page))

		parse = re.findall('<h1>.*?videos</h1>(.*?)id="right-banners-main', data, re.S)
		raw = re.findall('<a\shref="(.*?)".*?<h3>(.*?)</h3>.*?src="(.*?)"\s/>.*?<span>(.*?)</span>', parse[0], re.S)
		if raw:
			for (Link, Title, Image, Duration) in raw:
				self.filmliste.append((decodeHtml(Title), Link, Image, Duration))
			self.chooseMenuList.setList(map(amateurslustEntry1, self.filmliste))
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
		Link = "http://www.amateurslust.com" + self['liste'].getCurrent()[0][1]
		getPage(Link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamData).addErrback(self.dataError)

	def getStreamData(self, data):
		self.title = self['liste'].getCurrent()[0][0]
		videoLink = re.findall("'video'.*?:.*?'(.*?)'", data, re.S)
		url = videoLink[0] + "?start=0"
		if url:
			self.session.open(SimplePlayer, [(self.title, url)], showPlaylist=False, ltype='amateurslust')

	def keyCancel(self):
		self.close()