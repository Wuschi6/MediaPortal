from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def movie2kGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def movie2kListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

#(url, date, hostername, quali)
def movie2kStreamListEntry(entry):
	premiumFarbe = 0xCC0000
	if config.mediaportal.premiumize_use.value:
		if re.search('(putlocker|sockshare|bitshare)', entry[2], re.S|re.I):
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 150, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1], premiumFarbe),
				(eListboxPythonMultiContent.TYPE_TEXT, 200, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2], premiumFarbe),
				(eListboxPythonMultiContent.TYPE_TEXT, 400, 0, 400, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3], premiumFarbe)
				]
		else:
			return [entry,
				(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 150, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
				(eListboxPythonMultiContent.TYPE_TEXT, 200, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
				(eListboxPythonMultiContent.TYPE_TEXT, 400, 0, 400, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
				]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 150, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
			(eListboxPythonMultiContent.TYPE_TEXT, 200, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
			(eListboxPythonMultiContent.TYPE_TEXT, 400, 0, 400, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
			]

class movie2kGenreScreen(Screen):

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

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Movie2k.tl")
		self['ContentTitle'] = Label("Auswahl:")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()

		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.genreliste = [('Kinofilme',"http://www.movie2k.tl"),
							('Videofilme',"http://www.movie2k.tl")]

		self.chooseMenuList.setList(map(movie2kGenreListEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		self.movie2kName = self['genreList'].getCurrent()[0][0]
		movie2kUrl = self['genreList'].getCurrent()[0][1]
		print self.movie2kName, movie2kUrl

		self.session.open(movie2kListeScreen, self.movie2kName, movie2kUrl)


	def keyCancel(self):
		self.close()

class movie2kListeScreen(Screen):

	def __init__(self, session, movie2kName, movie2kUrl):
		self.session = session
		self.movie2kName = movie2kName
		self.movie2kUrl = movie2kUrl

		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListWideScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListWideScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"up": self.keyUp,
			"down": self.keyDown,
			"right": self.keyRight,
			"left": self.keyLeft,
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Movie2k.tl")
		self['ContentTitle'] = Label("Videos - %s" % self.movie2kName)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['Page'] = Label("")
		self['coverArt'] = Pixmap()

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "hole daten.."
		getPage(self.movie2kUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		if self.movie2kName == "Kinofilme":
			self.kinofilme(data)
		elif self.movie2kName == "Videofilme":
			self.videofilme(data)

	def kinofilme(self, data):
		kino = re.findall('<div style="float:left">.*?<a href="(.*?)">.*?<img src="(.*?)".*?alt="(.*?).kostenlos".*?Description:</strong><br>(.*?)<', data, re.S)
		if kino:
			self.kinoliste = []
			for (url, img, title, desc) in kino:
				self.kinoliste.append((decodeHtml(title), url, img, desc))

			self.chooseMenuList.setList(map(movie2kListEntry, self.kinoliste))
			self.loadPic()
			self.keyLocked = False

	def videofilme(self, data):
		video = re.findall('<div style="float: left;".*?<a href="(.*?)">.*?<img src="(.*?)".*?alt="(.*?)"', data, re.S)
		if video:
			self.videoliste = []
			for (url, img, title) in video:
				self.videoliste.append((decodeHtml(title), url, img))

			self.chooseMenuList.setList(map(movie2kListEntry, self.videoliste))
			self.loadPic()
			self.keyLocked = False

	def loadPic(self):
		print self.movie2kName
		streamPic = self['liste'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(streamPic)

		if self.movie2kName == "Kinofilme":
			handlung = self['liste'].getCurrent()[0][3]
			self['handlung'].setText(decodeHtml(handlung))

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
		title = self['liste'].getCurrent()[0][0]
		url = self['liste'].getCurrent()[0][1]
		image = self['liste'].getCurrent()[0][2]

		print title, url, image
		self.session.open(movie2kStreamListeScreen, title, url, image)

	def dataError(self, error):
		printl(error,self,"E")

	def keyCancel(self):
		self.close()

class movie2kStreamListeScreen(Screen):

	def __init__(self, session, movie2kName, movie2kUrl, movie2kImage):
		self.session = session
		self.movie2kName = movie2kName
		self.movie2kUrl = movie2kUrl
		self.movie2kImage = movie2kImage

		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListWideScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListWideScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Movie2k.tl")
		self['ContentTitle'] = Label("Streams")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['Page'] = Label("")
		self['coverArt'] = Pixmap()

		self.streamliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "hole daten.."
		getPage(self.movie2kUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		hoster = re.findall('<tr id=.*?tablemoviesindex2.*?>.*?td height="20" width="150">.*?<a href.*?"(.*?.html).*?>(.*?)<img.*?/>&#160;(.*?)</a>.*?title="Movie quality (.*?)"', data, re.S)
		if hoster:
			self.streamliste = []
			for (url, date, hostername, quali) in hoster:
				self.streamliste.append((url, date, hostername, quali))

			self.chooseMenuList.setList(map(movie2kStreamListEntry, self.streamliste))
			self.loadPic()
			self.keyLocked = False

	def loadPic(self):
		CoverHelper(self['coverArt']).getCover(self.movie2kImage)

	def keyOK(self):
		if self.keyLocked:
			return

		url = self['liste'].getCurrent()[0][0]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.get_hoster_link).addErrback(self.dataError)

	def get_hoster_link(self, data):
		hoster_link = re.findall('</div><br />\r\n\r\n\t\r\n\t\t\t\t\t\t\t<a href="(.*?)" target="_BLANK"><img src="http://www.movie2k.tl/assets/img/click_link.jpg" border="0" /></a>', data, re.S)
		if hoster_link:
			print hoster_link[0]
			get_stream_link(self.session).check_link(hoster_link[0], self.got_link, False)

	def got_link(self, stream_url):
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			self.session.open(SimplePlayer, [(self.movie2kName, stream_url, self.movie2kImage)], showPlaylist=False, ltype='movie2k', cover=True)

	def dataError(self, error):
		printl(error,self,"E")

	def keyCancel(self):
		self.close()