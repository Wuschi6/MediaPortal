# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.myvideolink import MyvideoLink
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def myvideotvEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def myvideotvEntry1(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class myvideotvGenreScreen(Screen):

	def __init__(self, session, source, portal):
		self.session = session
		self.source = source
		self.portal = portal
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

		self['title'] = Label("%s" % self.portal)
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
		url = "http://www.myvideo.de/Serien/%s" % self.source
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		raw = re.findall("class='vFullEpisode'.*?<a\shref='(/channel/.*?)'.*?title='(.*?)'><img.*?longdesc='(.*?)'.*?'pChText'>(.*?)</div>", data, re.S)
		if raw:
			for (Url, Title, Image, Handlung) in raw:
				self.filmliste.append((decodeHtml(Title), Url, Image, Handlung))
				self.chooseMenuList.setList(map(myvideotvEntry, self.filmliste))
				self.filmliste.sort(key=lambda t : t[0].lower())
		self.keyLocked = False
		self.showInfos()

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		ImageUrl = self['genreList'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(ImageUrl)

	def keyOK(self):
		Name = self['genreList'].getCurrent()[0][0]
		Link = "http://www.myvideo.de" + self['genreList'].getCurrent()[0][1]
		self.session.open(myvideotvListScreen, Link, Name, self.portal)

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

class myvideotvListScreen(Screen):

	def __init__(self, session, Link, Name, portal):
		self.session = session
		self.Link = Link
		self.Name = Name
		self.portal = portal
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

		self['title'] = Label("%s" % self.portal)
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
		url = self.Link
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		#lastpage = re.search('class="ClnNextNblEnd".*?mode=verpasst([\d]+)\&amp;red', data, re.S)
		#if lastpage:
		#	self.lastpage = int(lastpage.group(1))+1
		#	self['page'].setText("%s / %s" % (str(self.page+1), str(self.lastpage)))
		#else:
		#	lastpage = re.search('ClnInfo.*?class="mediathek_menu_.*?([\d]+)&nbsp;.*?class="ClnNextLock', data, re.S)
		#	if lastpage:
		#		self.lastpage = int(lastpage.group(1))
		#		self['page'].setText("%s / %s" % (str(self.page+1), str(self.lastpage)))
		#	else:
		#		self.lastpage = 0
		#		self['page'].setText("%s / 1" % str(self.page+1))
		parse = re.search('id_full_episodes_content(.*?)CDATA', data, re.S)
		raw = re.findall("class='slThumb.*?href='.*?'\stitle='(.*?)'><img.*?id='(.*?)'.*?longdesc='(.*?)'.*?class='pChText'>(.*?)</div>", parse.group(1), re.S)
		if raw:
			for (Title, id, Image, Handlung) in raw:
				self.filmliste.append((decodeHtml(Title), id, Image, Handlung))
			self.chooseMenuList.setList(map(myvideotvEntry1, self.filmliste))
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
		mvUrl = self['liste'].getCurrent()[0][1]
		id = re.search('\D(\d+)', mvUrl)
		if id:
			url = "http://www.myvideo.de/dynamic/get_player_video_xml.php?ID=" + id.group(1)
			kiTitle = self['liste'].getCurrent()[0][0]
			imgurl = self['liste'].getCurrent()[0][2]
			self.session.open(MyvideoPlayer, [(kiTitle, url, id.group(1), imgurl)])
		else:
			printl('No ID found!', self, 'E')

	def keyCancel(self):
		self.close()

class MyvideoPlayer(SimplePlayer):

	def __init__(self, session, playList):
		print "MyvideoPlayer:"

		SimplePlayer.__init__(self, session, playList, showPlaylist=False, ltype='myvideo', cover=False)

		self.onLayoutFinish.append(self.getVideo)

	def getVideo(self):
		titel = self.playList[self.playIdx][0]
		url = self.playList[self.playIdx][1]
		token = self.playList[self.playIdx][2]
		imgurl = self.playList[self.playIdx][3]
		print titel, url, token

		MyvideoLink(self.session).getLink(self.playStream, self.dataError, titel, url, token, imgurl=imgurl)