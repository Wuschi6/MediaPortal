# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def tubewolfEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def tubewolfEntry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class tubewolfGenreScreen(Screen):

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

		self['title'] = Label("Tubewolf.com")
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
		self.suchString = ''

		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = "http://www.tubewolf.com/categories/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		parse = re.search('class="categories"(.*?)class="link-view-all"', data, re.S)
		cat = re.findall('<li><a\shref="(.*?)".*?<strong>(.*?)<span>\((.*?)\)</span>', parse.group(1), re.S)
		if cat:
			self.filmliste = []
			for (Url, Title, Count) in cat:
				self.filmliste.append((decodeHtml(Title), Url, Count))
			self.filmliste.sort()
			self.filmliste.insert(0, ("Top Rated", "http://www.tubewolf.com/top-rated", 78400))
			self.filmliste.insert(0, ("Most Popular", "http://www.tubewolf.com/most-popular", 78400))
			self.filmliste.insert(0, ("Newest", "http://www.tubewolf.com/latest-updates", 78400))
			self.filmliste.insert(0, ("--- Search ---", "callSuchen", None))
			self.chooseMenuList.setList(map(tubewolfEntry, self.filmliste))
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		Title = self['genreList'].getCurrent()[0][0]
		self['name'].setText(Title)

	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			Link = '?q=%s' % (self.suchString)
			Name = self['genreList'].getCurrent()[0][0]
			count = None
			self.session.open(tubewolfListScreen, Link, Name, count)

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
		if Name == "--- Search ---":
			self.suchen()
		else:
			Link = self['genreList'].getCurrent()[0][1]
			count = self['genreList'].getCurrent()[0][2]
			self.session.open(tubewolfListScreen, Link, Name, count)

	def keyCancel(self):
		self.close()

class tubewolfListScreen(Screen):

	def __init__(self, session, Link, Name, Count):
		self.session = session
		self.Link = Link
		self.Name = Name
		self.Count = Count
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
		"prevBouquet" : self.keyPageDown,
		"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("Tubewolf.com")
		self['ContentTitle'] = Label("Genre: %s" % self.Name)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("Page")
		self['F3'] = Label("")
		self['F4'] = Label("")
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
		if self.Name == "--- Search ---":
			url = "http://www.tubewolf.com/search/%s/%s" % (self.page, self.Link)
		else:
			url = self.Link + "/" + str(self.page) + "/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		if self.Count:
			self.lastpage = int(round((float(self.Count) / 109) + 0.5))
			self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))
		else:
			self.lastpage = 999
			self['page'].setText(str(self.page))

		raw = re.findall('class=".*?thumb">.*?<a\shref="(http://www.tubewolf.com/movies.*?)".*?title="(.*?)"><img.*?src="(.*?)".*?class="time">\s{0,2}(.*?)</span>.*?user-views"><em>(.*?)\sviews</em>\s{0,1}(.*?)</span>', data, re.S)
		if raw:
			for (Link, Title, Image, Duration, Views, Added) in raw:
				self.filmliste.append((decodeHtml(Title), Link, Image, Duration, Views, Added))
			self.chooseMenuList.setList(map(tubewolfEntry1, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		runtime = self['liste'].getCurrent()[0][3]
		views = self['liste'].getCurrent()[0][4]
		added = self['liste'].getCurrent()[0][5]
		self['handlung'].setText("\n\nRuntime: %s\nViews: %s\nAdded: %s" % (runtime, views, added))
		coverUrl = self['liste'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(coverUrl)

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = str(self.page))

	def callbackkeyPageNumber(self, answer):
		if answer is not None:
			answer = re.findall('\d+', answer)
		else:
			return
		if answer:
			if int(answer[0]) < self.lastpage + 1:
				self.page = int(answer[0])
				self.loadPage()
			else:
				self.page = self.lastpage
				self.loadPage()

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
		if self.page:
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
		raw = re.findall("video_url:\s'(.*?)',", data, re.S)
		if raw:
			self.session.open(SimplePlayer, [(self.title, raw[0])], showPlaylist=False, ltype='tubewolf')

	def keyCancel(self):
		self.close()