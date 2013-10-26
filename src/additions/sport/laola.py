# -*- coding: utf-8 -*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper

def laolaOverviewListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[1])
		]

def laolaGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def laolaSubOverviewListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class laolaVideosOverviewScreen(Screen):

	def __init__(self, session):
		print 'laolaVideosOverviewScreen'
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
			"cancel": self.keyCancel
		}, -1)

		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		self.playing = False
		self.keyLocked = True
		self['title'] = Label("Laola1.tv")
		self['ContentTitle'] = Label("")
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
		self.genreliste.append(("Live", "http://www.laola1.tv/de-de/calendar/0.html"))
		self.genreliste.append(("Newest Videos", "http://www.laola1.tv/de-de/home/0.html"))
		self.genreliste.append(("Fußball", "http://www.laola1.tv/de-de/fussball/2.html"))
		self.genreliste.append(("Eishockey", "http://www.laola1.tv/de-de/eishockey/41.html"))
		self.genreliste.append(("Volleyball", "http://www.laola1.tv/de-de/volleyball/56.html"))
		self.genreliste.append(("Beach-Volleyball", "http://www.laola1.tv/de-de/beach-volleyball/101.html"))
		self.genreliste.append(("Handball", "http://www.laola1.tv/de-de/handball/143.html"))
		self.genreliste.append(("Tischtennis", "http://www.laola1.tv/de-de/tischtennis/182.html"))
		self.genreliste.append(("Curling", "http://www.laola1.tv/de-de/curling/248.html"))
		self.genreliste.append(("Motorsport", "http://www.laola1.tv/de-de/motorsport/239.html"))
		self.genreliste.append(("Tennis", "http://www.laola1.tv/de-de/tennis/224.html"))
		self.genreliste.append(("Mehr Sport", "http://www.laola1.tv/de-de/mehr-sport/404.html"))
		self.chooseMenuList.setList(map(laolaGenreListEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		auswahl = self['genreList'].getCurrent()[0][0]
		link = self['genreList'].getCurrent()[0][1]
		print auswahl, link
		if auswahl == "Live":
			self.session.open(laolaLiveScreen, auswahl, link)
		else:
			self.session.open(laolaSelectGenreScreen, auswahl, link)

	def keyCancel(self):
		self.close()

	def dataError(self, error):
		printl(error,self,"E")

class laolaLiveScreen(Screen):

	def __init__(self, session, name, link):
		print 'laolaLiveScreen'
		self.session = session
		self.lname = name
		self.llink = link

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

		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		self.playing = False
		self.keyLocked = True
		self['title'] = Label("Laola1.tv - Live")
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()

		self.genreliste = []

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 21))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		getPage(self.llink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getLiveData).addErrback(self.dataError)

	def getLiveData(self, data):
		live = re.findall('<img\swidth="80"\sheight="45"\ssrc=".*?">.*?<a\shref="(.*?)"><h2>(.*?)</h2>.*?<span\sclass="ititle">Liga:</span><span\sclass="idesc\shalf">(.*?)</span>.*?<span\sclass="ititle\sfull">Streamstart:</span><span\sclass="idesc\sfull">.*?,(.*?)</span>.*?<span\sclass="ititle\sfull">Verf&uuml;gbar\sin:</span><span\sclass="idesc\sfull"><span\sstyle="color:\#0A0;">(.*?)<', data, re.S)
		if live:
			for url,sportart,welche,time,where in live:
				sportart = sportart.replace('<div class="hdkennzeichnung"></div>','')
				title = "%s - %s - %s" % (time, sportart, welche)
				self.genreliste.append((title, url))
			self.chooseMenuList.setList(map(laolaSubOverviewListEntry, self.genreliste))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return
		self.keyLocked = True
		self.auswahl = self['genreList'].getCurrent()[0][0]
		url = self['genreList'].getCurrent()[0][1]
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getLiveData1).addErrback(self.dataError)

	def getLiveData1(self, data):
		if 'Dieser Stream beginnt' in data:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event ist noch nicht gestartet."), MessageBox.TYPE_INFO, timeout=3)
		else:
			match_player = re.search('<iframe.*?class="main_tv_player".*?src="(.*?)"', data, re.S)
			if match_player:
				getPage(match_player.group(1), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getLiveData2).addErrback(self.dataError)
			else:
				self.keyLocked = False
				message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getLiveData2(self, data):
		match_m3u8 = re.search('url: "(.*?)"', data, re.S)
		if match_m3u8:
			url = match_m3u8.group(1).replace('/vod/','/live/')
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getLiveData3).addErrback(self.dataError)
		else:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getLiveData3(self, data):
		match_url = re.search('url="(.*?)"', data, re.S)
		match_auth = re.search('auth="(.*?)"', data, re.S)
		if match_url and match_auth:
				res_url = match_url.group(1)
				url = m3u8_url = res_url+'?hdnea='+match_auth.group(1)
				getPage(url.replace('/vod/','/live/'), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getLiveData4).addErrback(self.dataError)
		else:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getLiveData4(self, data):
		xml = re.findall('CODECS="avc.*?"\n(.*?)\n', data, re.S)
		if xml:
			url = xml[-1]
			self.session.open(SimplePlayer, [(self.auswahl, url)], showPlaylist=False, ltype='laola1')
		else:
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)
		self.keyLocked = False

	def keyCancel(self):
		self.close()

	def dataError(self, error):
		printl(error,self,"E")

class laolaSelectGenreScreen(Screen):

	def __init__(self, session, name, link):
		print 'laolaLiveScreen'
		self.session = session
		self.lname = name
		self.llink = link

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
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)

		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		self.playing = False
		self.keyLocked = True
		self['title'] = Label("Laola1.tv - %s" % self.lname)
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()
		self['coverArt'] = Pixmap()
		self['Page'] = Label("Page: ")
		self['page'] = Label("")
		self['handlung'] = Label("")
		self.page = 1

		self.genreliste = []

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 21))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def char_gen(self, size=1, chars=string.ascii_uppercase):
		return ''.join(random.choice(chars) for x in range(size))

	def loadPage(self):
		self['page'].setText("%s" % (str(self.page)))
		getPage(self.llink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getKey).addErrback(self.dataError)
		
	def getKey(self, data):
		parse = re.search('data-stageid=\s"(.*?)".*?data-call="(.*?)".*?data-page="(.*?)".*?data-filterpage="(.*?)".*?data-startvids="(.*?)".*?data-htag="(.*?)"', data, re.S).groups()

		if "Newest Videos" in self.lname:
			stageid = 1184
		else:
			stageid = int(parse[0])+3
			
		info = urlencode({
		'anzahlblock': 2+(self.page-1)*10,
		'call': parse[1],
		'filterid': "0",
		'filterpage': parse[3],
		'htag': parse[5],
		'page': self.page,
		'selectionid': "0",
		'stageid': stageid,
		'startvids': parse[4]
		})

		url = "http://www.laola1.tv/de-de/nourish.php?key=" + parse[5]
		getPage(url, agent=std_headers, method='POST', postdata=info, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getEventData).addErrback(self.dataError)

	def getEventData(self, data):
		self.genreliste = []
		events = re.findall('<span\sclass="category">(.*?)</span>.*?<span\sclass="date">.*?,(.*?)</span>.*?<h2>(.*?)</h2></a>.*?<a\shref="/(.*?)">.*?src="(.*?)"', data, re.S)
		if events:
			for genre,time,desc,url,image in events:
				desc = desc.replace('<div class="hdkenn_list"></div>','')
				genre = genre.replace("Tennis/",'').replace("Eishockey/",'').replace("Fussball/",'').replace("Beach Volleyball/",'').replace("Curling/",'').replace("Tischtennis/",'').replace("Handball/",'').replace("Motorsport/",'').replace("Volleyball/",'')
				title = "%s %s, %s" % (time, decodeHtml(genre), decodeHtml(desc))
				url = "http://www.laola1.tv/%s" % url
				self.genreliste.append((title, url, genre, image))
			self.chooseMenuList.setList(map(laolaSubOverviewListEntry, self.genreliste))
			self.chooseMenuList.moveToIndex(0)
			self.keyLocked = False
			self.showInfos()

	def keyOK(self):
		if self.keyLocked:
			return
		self.keyLocked = True
		self.auswahl = self['liste'].getCurrent()[0][0]
		url = self['liste'].getCurrent()[0][1]
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getData).addErrback(self.dataError)

	def getData(self, data):
		match_player = re.search('<iframe.*?class="main_tv_player".*?src="(.*?)"', data, re.S)
		if match_player:
			getPage(match_player.group(1), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getData2).addErrback(self.dataError)
		else:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getData2(self, data):
		match_m3u8 = re.search('url: "(.*?)"', data, re.S)
		if match_m3u8:
			getPage(match_m3u8.group(1), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getData3).addErrback(self.dataError)
		else:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getData3(self, data):
		match_url = re.search('url="(.*?)"', data, re.S)
		match_auth = re.search('auth="(.*?)"', data, re.S)
		if match_url and match_auth:
			res_url = match_url.group(1)
			url = res_url+'?hdnea='+match_auth.group(1)+'&g='+self.char_gen(12)+'&hdcore=3.1.0'
			getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getData4).addErrback(self.dataError)
		else:
			self.keyLocked = False
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)

	def getData4(self, data):
		xml = re.findall('CODECS="avc.*?"\n(.*?)\n', data, re.S)
		if xml:
			url = xml[-1]
			self.session.open(SimplePlayer, [(self.auswahl, url)], showPlaylist=False, ltype='laola1')
		else:
			message = self.session.open(MessageBox, _("Event nicht verfügbar."), MessageBox.TYPE_INFO, timeout=3)
		self.keyLocked = False

	def showInfos(self):
		self.ImageUrl = self['liste'].getCurrent()[0][3]
		CoverHelper(self['coverArt']).getCover(self.ImageUrl)

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

	def keyCancel(self):
		self.close()

	def dataError(self, error):
		printl(error,self,"E")