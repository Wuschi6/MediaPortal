# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.playrtmpmovie import PlayRtmpMovie
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def Entry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def Entry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class SouthparkGenreScreen(Screen):

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

		self['title'] = Label("Southpark.de")
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
		url = "http://www.southpark.de/alle-episoden"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('<a\sclass="seasonbtn.*?"\shref="(.*?)">(.*?)</a>.*?</li>', data, re.S)
		if raw:
			self.filmliste = []
			for (Url, Title) in raw:
				Title = "Staffel " + Title
				self.filmliste.append((Title, Url))
			self.chooseMenuList.setList(map(Entry, self.filmliste))
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def keyOK(self):
		Name = self['genreList'].getCurrent()[0][0]
		Link = self['genreList'].getCurrent()[0][1]
		self.session.open(SouthparkListScreen, Link, Name)

	def keyCancel(self):
		self.close()

class SouthparkListScreen(Screen):

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
		"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Southpark.de")
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
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		url = self.Link
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall('<li>.*?<a\sclass="content_eppreview"\shref="(.*?episoden/)(.*?)-(.*?)"><img\ssrc="(.*?)"width="120".*?<h5>(.*?)</h5>.*?<p>(.*?)</p>', data, re.S)
		if raw:
			for (Link1, Episode, Link2, Image, Title, Handlung) in raw:
				Title = Episode.upper() + " - " + Title
				Link = Link1 + Episode + "-" + Link2
				Image = Image.replace("width=120","width=320")
				self.filmliste.append((decodeHtml(Title), Link, Image, Handlung))
			self.filmliste.sort()
			self.chooseMenuList.setList(map(Entry1, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		coverUrl = self['liste'].getCurrent()[0][2]
		handlung = self['liste'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		CoverHelper(self['coverArt']).getCover(coverUrl)

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
		Name = self['liste'].getCurrent()[0][0]
		Link = self['liste'].getCurrent()[0][1]
		Pic = self['liste'].getCurrent()[0][2]
		Handlung = self['liste'].getCurrent()[0][3]
		self.session.open(SouthparkAktScreen, Link, Name, Pic, Handlung)

	def keyCancel(self):
		self.close()

class SouthparkAktScreen(Screen):

	def __init__(self, session, Link, Name, Pic, Handlung):
		self.session = session
		self.Link = Link
		self.Name = Name
		self.Pic = Pic
		self.Handlung = Handlung
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
		"green"	: self.keyLocale,
		"yellow": self.keyQuality
		}, -1)

		self.locale = config.mediaportal.southparklang.value
		self.quality = config.mediaportal.southparkquality.value

		self['title'] = Label("Southpark.de")
		self['ContentTitle'] = Label("Folge: %s" % self.Name)
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label(self.locale)
		self['F3'] = Label(self.quality)
		self['F4'] = Label("")
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("")
		self['page'] = Label("")
		self['handlung'] = Label("")

		self.keyLocked = True

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		url = self.Link
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getVidId).addErrback(self.dataError)

	def getVidId(self, data):
		vidid = re.findall('<script\ssrc="http://activities.niagara.comedycentral.com/register/spsi-de-DE/episodes/(.*?)"\stype="text/javascript"></script>', data, re.S)
		if vidid:
			url = "http://www.southpark.de/feeds/video-player/mrss/mgid:arc:episode:southpark.de:" + vidid[0]
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getxmls).addErrback(self.dataError)
		else:
			message = self.session.open(MessageBox, _("Sorry, this video is not found or no longer available due to date or rights restrictions."), MessageBox.TYPE_INFO, timeout=5)
			self.keyLocked = False
			self.close()

	def getxmls(self, data):
		print "locale: " + self.locale
		if self.locale == "de":
			self.lang = "&dubbed=preferred"
		else:
			self.lang = ""
		xmls = re.findall('<item>.*?<title>(.*?)</title>.*?<media:category\sscheme="urn:mtvn:id">mgid:arc:video:southparkstudios.com:(.*?)</media:category>', data, re.S)
		if xmls:
			for title, id in xmls:
				if not re.match(".*?Intro\sHD", title):
					if self.quality == "HD":
						url = "http://www.southpark.de/feeds/video-player/mediagen?uri=mgid:arc:episode:southpark.de:%s&suppressRegisterBeacon=true&suppressRegisterBeacon=true&acceptMethods=fms%s" % (id, self.lang)
					else:
						url = "http://www.southpark.de/feeds/video-player/mediagen?uri=mgid:arc:episode:southpark.de:%s&suppressRegisterBeacon=true&suppressRegisterBeacon=true&acceptMethods=hdn1%s" % (id, self.lang)
						print url
					self.filmliste.append((decodeHtml(title), url, self.Link))
			self.chooseMenuList.setList(map(Entry1, self.filmliste))
			self.chooseMenuList.moveToIndex(0)
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		coverUrl = self.Pic
		handlung = self.Handlung
		self['handlung'].setText(decodeHtml(handlung))
		CoverHelper(self['coverArt']).getCover(coverUrl)

	def keyOK(self):
		if self.keyLocked:
			return
		self.keyLocked = True
		self.link = self['liste'].getCurrent()[0][1]
		if self.quality == "HD":
			getPage(self.link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.StartStreamRtmp).addErrback(self.dataError)
		else:
			getPage(self.link, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.StartStreamHttp).addErrback(self.dataError)

	def StartStreamRtmp(self, data):
		title = self['liste'].getCurrent()[0][0]
		rtmpe_data = re.findall('<rendition.*?bitrate="(450|750|1000|1200)".*?<src>(rtmpe://.*?ondemand/)(.*?.mp4)</src>.*?</rendition>', data, re.S|re.I)
		if rtmpe_data:
			(quality, host, playpath) = rtmpe_data[-1]
			final = "%s' --playpath=mp4:%s'" % (host, playpath)
			movieinfo = [final, title]
			self.session.open(PlayRtmpMovie, movieinfo, title)
		else:
			message = self.session.open(MessageBox, _("Sorry, this video is not found or no longer available due to date or rights restrictions."), MessageBox.TYPE_INFO, timeout=5)
		self.keyLocked = False

	def StartStreamHttp(self, data):
		title = self['liste'].getCurrent()[0][0]
		http_data = re.findall('<rendition.*?bitrate=".*?".*?<src>(.*?)</src>.*?</rendition>', data, re.S|re.I)
		if http_data:
			idx = self['liste'].getSelectedIndex()
			self.session.open(SouthparkPlayer, self.filmliste, int(idx) , True, False)
		else:
			message = self.session.open(MessageBox, _("Sorry, this video is not found or no longer available due to date or rights restrictions."), MessageBox.TYPE_INFO, timeout=5)
		self.keyLocked = False

	def keyLocale(self):
		if self.keyLocked:
			return
		self.keyLocked = True
		if self.locale == "de":
			self.locale = "en"
			config.mediaportal.southparklang.value = "en"
		elif self.locale == "en":
			self.locale = "de"
			config.mediaportal.southparklang.value = "de"

		config.mediaportal.southparklang.save()
		configfile.save()
		self['F2'].setText(self.locale)
		self.loadPage()

	def keyQuality(self):
		if self.keyLocked:
			return
		self.keyLocked = True
		if self.quality == "SD":
			self.quality = "HD"
			config.mediaportal.southparkquality.value = "HD"
		elif self.quality == "HD":
			self.quality = "SD"
			config.mediaportal.southparkquality.value = "SD"

		config.mediaportal.southparkquality.save()
		configfile.save()
		self['F3'].setText(self.quality)
		self.loadPage()

	def keyCancel(self):
		self.close()

class SouthparkPlayer(SimplePlayer):

	def __init__(self, session, playList, playIdx=0, playAll=True, showPlaylist=False):
		print "SouthparkPlayer:"

		SimplePlayer.__init__(self, session, playList, playIdx=playIdx, playAll=playAll, showPlaylist=showPlaylist, ltype='southpark')

		self.onLayoutFinish.append(self.getVideo)

	def getVideo(self):
		self.title = self.playList[self.playIdx][0]
		self.pageurl = self.playList[self.playIdx][2]
		url = self.playList[self.playIdx][1]
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.gotVideo).addErrback(self.dataError)

	def gotVideo(self, data):
		http_data = re.findall('<rendition.*?bitrate=".*?".*?<src>(.*?)</src>.*?</rendition>', data, re.S|re.I)
		self.playStream(self.title, http_data[-1])