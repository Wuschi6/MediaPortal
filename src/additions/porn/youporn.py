from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper
from Plugins.Extensions.MediaPortal.resources.twagenthelper import TwAgentHelper

def youpornGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def youpornFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class youpornGenreScreen(Screen):

	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("YouPorn.com")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.suchString = ''

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.keyLocked = True
		url = "http://www.youporn.com/categories/alphabetical/"
		getPage(url, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		phCats = re.findall('class="cat_pic">.*?<a\shref="/category(.*?)".*?<img\ssrc="(.*?)"\salt="(.*?)"><span\sclass="cat_overlay', data, re.S)
		if phCats:
			for (phUrl, phImage, phTitle) in phCats:
				phUrl = "http://www.youporn.com/category" + phUrl + '?page='
				self.genreliste.append((phTitle, phUrl, phImage))
			self.genreliste.sort()
			self.genreliste.insert(0, ("Channels", "http://www.youporn.com/channels/most_subscribed/alltime/?page=", None))
			self.genreliste.insert(0, ("Popular by Country", "http://www.youporn.com/categories/", None))
			self.genreliste.insert(0, ("Most Discussed", "http://www.youporn.com/most_discussed/?page=", None))
			self.genreliste.insert(0, ("Most Favorited", "http://www.youporn.com/most_favorited/?page=", None))
			self.genreliste.insert(0, ("Most Viewed", "http://www.youporn.com/most_viewed/?page=", None))
			self.genreliste.insert(0, ("Top Rated", "http://www.youporn.com/top_rated/?page=", None))
			self.genreliste.insert(0, ("New", "http://www.youporn.com/?page=", None))
			
		self.genreliste.insert(0, ("--- Search ---", "callSuchen", None))
		self.chooseMenuList.setList(map(youpornGenreListEntry, self.genreliste))
		self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		phImage = self['genreList'].getCurrent()[0][2]
		if not phImage == None:
			CoverHelper(self['coverArt']).getCover(phImage)

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreName = self['genreList'].getCurrent()[0][0]
		if streamGenreName == "--- Search ---":
			self.suchen()

		elif streamGenreName == "Channels":
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(youpornChannelScreen, streamGenreLink)

		elif streamGenreName == "Popular by Country":
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(youpornCountryScreen, streamGenreLink)

		else:
			streamGenreLink = self['genreList'].getCurrent()[0][1]
			self.session.open(youpornFilmScreen, streamGenreLink)

	def suchen(self):
		self.session.openWithCallback(self.SuchenCallback, VirtualKeyBoard, title = (_("Suchkriterium eingeben")), text = self.suchString)

	def SuchenCallback(self, callback = None, entry = None):
		if callback is not None and len(callback):
			self.suchString = callback.replace(' ', '+')
			streamGenreLink = 'http://www.youporn.com/search/?query=%s&page=' % (self.suchString)
			self.session.open(youpornFilmScreen, streamGenreLink)

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

class youpornCountryScreen(Screen):

	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("YouPorn.com")
		self['name'] = Label("Country Auswahl")
		self['coverArt'] = Pixmap()
		self.keyLocked = True

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadpage)

	def loadpage(self):
		self.keyLocked = True
		self.genreliste = []
		url = self.phCatLink
		getPage(url, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		parse = re.search('class="countryNameLocation">Popular\sby\sCountry(.*?)</div>', data, re.S)
		phCats = re.findall('<a\shref="(.*?)".*?/span>(.*?)</a>', parse.group(1), re.S)
		if phCats:
			for (phUrl, phTitle) in phCats:
				phUrl = "http://www.youporn.com" + phUrl + "?page="
				self.genreliste.append((phTitle, phUrl))
			self.chooseMenuList.setList(map(youpornFilmListEntry, self.genreliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(youpornFilmScreen, streamGenreLink)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['genreList'].pageUp()

	def keyRight(self):
		if self.keyLocked:
			return
		self['genreList'].pageDown()

	def keyUp(self):
		if self.keyLocked:
			return
		self['genreList'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['genreList'].down()

	def keyCancel(self):
		self.close()

class youpornChannelScreen(Screen):

	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXFilmScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("YouPorn.com")
		self['name'] = Label("Channel Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadpage)

	def loadpage(self):
		self.keyLocked = True
		self.genreliste = []
		url = "%s%s" % (self.phCatLink, str(self.page))
		getPage(url, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.genreData).addErrback(self.dataError)

	def genreData(self, data):
		lastpparse = re.search('id="pagination">(.*)</nav>', data, re.S)
		lastp = re.search('<li>.*">(.*?[0-9])<.*/li>', lastpparse.group(1), re.S)
		if lastp:
			lastp = lastp.group(1)
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))
		phCats = re.findall('<div\sclass="img"><a\shref="(.*?)"><img\ssrc="(.*?)"\salt="(.*?)"', data, re.S)
		if phCats:
			for (phUrl, phImage, phTitle) in phCats:
				phUrl = "http://www.youporn.com" + phUrl + '?page='
				self.genreliste.append((phTitle, phUrl, phImage))
			self.chooseMenuList.setList(map(youpornFilmListEntry, self.genreliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		phImage = self['genreList'].getCurrent()[0][2]
		if not phImage == None:
			CoverHelper(self['coverArt']).getCover(phImage)

	def keyOK(self):
		if self.keyLocked:
			return
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		self.session.open(youpornFilmScreen, streamGenreLink)

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
				self.loadpage()
			else:
				self.page = self.lastpage
				self.loadpage()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()

	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page < self.lastpage:
			self.page += 1
			self.loadpage()

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

class youpornFilmScreen(Screen):

	def __init__(self, session, phCatLink):
		self.session = session
		self.phCatLink = phCatLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/XXXFilmScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/XXXFilmScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok" : self.keyOK,
			"cancel" : self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyPageNumber
		}, -1)

		self['title'] = Label("YouPorn.com")
		self['name'] = Label("Film Auswahl")
		self['views'] = Label("")
		self['runtime'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		self.keyLocked = True
		self.page = 1
		self.lastpage = 1

		self.tw_agent_hlp = TwAgentHelper()
		self.tw_agent_hlp.headers.addRawHeader('Cookie','age_verified=1')
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadpage)

	def loadpage(self):
		self.keyLocked = True
		self['name'].setText('Bitte warten...')
		self.filmliste = []
		url = "%s%s" % (self.phCatLink, str(self.page))
		print url
		#getPage(url, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadData).addErrback(self.dataError)
		self.tw_agent_hlp.getWebPage(self.loadData, self.dataError, url, False)

	def loadData(self, data):
		lastpparse = re.search('id="pagination">(.*)</nav>', data, re.S)
		lastp = re.search('<li>.*">(.*?[0-9])<.*/li>', lastpparse.group(1), re.S)
		if lastp:
			lastp = lastp.group(1)
			print lastp
			self.lastpage = int(lastp)
		else:
			self.lastpage = 1
		self['page'].setText(str(self.page) + ' / ' + str(self.lastpage))
		parse = re.search('Sub menu dropdown.*?/Sub menu dropdown(.*?)Our Friends', data, re.S)
		if not parse:
			parse = re.search('Sub menu dropdown.*?/Sub menu dropdown(.*?)pagination', data, re.S)
		phMovies = re.findall('class="wrapping-video-box">.*?<a\shref="(.*?)">.*?<img\ssrc="(.*?)\?.*?"\salt="(.*?)".*?class="duration">(.*?)<span>length.*?class="views">(.*?)\s<span>views', parse.group(1), re.S)
		if phMovies:
			for (phUrl, phImage, phTitle, phRuntime, phViews) in phMovies:
				self.filmliste.append((decodeHtml(phTitle), phUrl, phImage, phRuntime, phViews))
			self.chooseMenuList.setList(map(youpornFilmListEntry, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		phTitle = self['genreList'].getCurrent()[0][0]
		phImage = self['genreList'].getCurrent()[0][2]
		phRuntime = self['genreList'].getCurrent()[0][3]
		phViews = self['genreList'].getCurrent()[0][4]
		self['name'].setText(phTitle)
		self['runtime'].setText(phRuntime)
		self['views'].setText(phViews)
		CoverHelper(self['coverArt']).getCover(phImage)

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
				self.loadpage()
			else:
				self.page = self.lastpage
				self.loadpage()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadpage()

	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		if self.page < self.lastpage:
			self.page += 1
			self.loadpage()

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
		phTitle = self['genreList'].getCurrent()[0][0]
		phLink = 'http://www.youporn.com' + self['genreList'].getCurrent()[0][1]
		self.keyLocked = True
		getPage(phLink, headers={'Cookie': 'age_verified=1', 'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVideoPage).addErrback(self.dataError)

	def getVideoPage(self, data):
		videoPage = re.findall('video.src\s=\s\'(.*?)\';', data, re.S)
		if videoPage:
			for (phurl) in videoPage:
				url = '%s' % (phurl)
				videos = urllib.unquote(url)
				videos = videos.replace('&amp;','&')
				self.keyLocked = False
				self.play(videos)

	def play(self,file):
		xxxtitle = self['genreList'].getCurrent()[0][0]
		self.session.open(SimplePlayer, [(xxxtitle, file)], showPlaylist=False, ltype='youporn')

	def keyCancel(self):
		self.close()