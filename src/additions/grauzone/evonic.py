#	-*-	coding:	utf-8	-*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper
from Plugins.Extensions.MediaPortal.resources.yt_url import *

config.entertain = ConfigSubsection()
config.entertain.userName = ConfigText(default="USERNAME", fixed_size=False)
config.entertain.userPass = ConfigText(default="PASSWORD", fixed_size=False)

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

ck = {}

def meListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

def meGenreEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

def meWatchListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]+" - "+entry[1])
		]

def meTimdbEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 70, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
		(eListboxPythonMultiContent.TYPE_TEXT, 70, 0, 550, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]),
		(eListboxPythonMultiContent.TYPE_TEXT, 620, 0, 100, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
		(eListboxPythonMultiContent.TYPE_TEXT, 720, 0, 100, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
		]

def meWatchedListEntry(entry):
	if entry[2]:
		png = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/watched.png"
		watched = LoadPixmap(png)
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 39, 3, 100, 22, watched),
			(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
			]

class showevonicGenre(Screen):

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
			"red": self.keyCancel,
			"green": self.loginSetup,
			"menu": self.loginSetup
		}, -1)

		self.keyLocked = True
		self['title'] = Label("evonic.tv")
		self['ContentTitle'] = Label("Try Login..")
		self['name'] = Label("")
		self['F1'] = Label("Exit")
		self['F2'] = Label("Setup")
		self['F3'] = Label("")
		self['F4'] = Label("")
		self['F3'].hide()
		self['F4'].hide()

		self.loginOK = False
		self.genreliste = []
		self.searchText = ""
		self.stoken = ""
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.onFirstExecBegin.append(self.login)

	def login(self):
		self.username = config.entertain.userName.value
		self.password = config.entertain.userPass.value
		print "Login:", self.username, self.password
		self['ContentTitle'].setText("Try Login..")

		if self.username == "USERNAME" and self.password == "PASSWORD":
			self.session.openWithCallback(self.callBackSetup, meSetupScreen)
		else:
			self.loginUrl = 'http://evonic.tv/forum/login.php?do=login'
			loginData = {'vb_login_username': self.username, 'vb_login_password': self.password, 'do': 'login'}
			getPage(self.loginUrl, method='POST',
					postdata=urlencode(loginData), cookies=ck,
					headers={'Content-Type':'application/x-www-form-urlencoded','User-agent': 'Mozilla/4.0', 'Referer': 'http://www.hellboundhackers.org/index.php', }).addCallback(self.loginRefresh).addErrback(self.dataError)

	def loginRefresh(self, data):
		if "Danke" in str(data):
			self.loginOK = True
			cookieuser = '1'
			password_md5 = md5.md5(self.password).hexdigest()

			loginData = {'vb_login_username': self.username,
						 's': '',
						 'securitytoken': 'guest',
						 'do': 'login',
						 'vb_login_md5password': password_md5,
						 'vb_login_md5password_utf': password_md5,
						 'cookieuser' : cookieuser
						 }

			getPage(self.loginUrl, method="POST",
					postdata=urlencode(loginData), headers={'Content-Type': 'application/x-www-form-urlencoded'},
					followRedirect=True, timeout=30, cookies=ck).addCallback(self.loginDone).addErrback(self.dataError)
		else:
			self.loginOK = False
			self['ContentTitle'].setText("Login fehlgeschlagen !")

	def accountInfos(self, data):
		print "hole member status infos.."
		if re.match('.*?Status:.*?Premium Member', data, re.S|re.I):
			statusUrl = 'http://evonic.tv/forum/payments.php'
			getPage(statusUrl, method="GET",
					headers={'Content-Type': 'application/x-www-form-urlencoded'},
					followRedirect=True, timeout=30, cookies=ck).addCallback(self.accountInfosData).addErrback(self.dataError)
		else:
			self['ContentTitle'].setText("Du bist kein Premium Member !")

	def accountInfosData(self, data):
		print "hole account infos.."
		infos = re.findall('<dt>Startdatum</dt>.*?<dd>(.*?)</dd>.*?<dt>L.*?t aus am</dt>.*?<dd>(.*?)</dd>.*?<p class="description">(.*?)</p>', data, re.S)
		if infos:
			print infos
			(reg, bis, was) = infos[0]
			acci = "Benutzer: %s - %s: Registriert: %s -> %s" % (self.username, was, reg, bis)
			print acci
			self['ContentTitle'].setText(str(acci))

	def loginDone(self, data):
		getPage(self.loginUrl, method="GET", headers={'Content-Type': 'application/x-www-form-urlencoded'},
				followRedirect=True, timeout=30, cookies=ck).addCallback(self.accountInfos).addErrback(self.dataError)

		secutoken = re.findall('var SECURITYTOKEN = "(.*?)"', data, re.S)
		if secutoken:
			self.stoken = secutoken[0]
			print "SECURITYTOKEN:", self.stoken

		self.genreListe = []
		self.genreListe.append(("Watchlist", "dump"))
		self.genreListe.append(("Neueinsteiger", "http://evonic.tv/forum/content.php?r=1969-Aktuelle-HD-Filme&page="))
		self.genreListe.append(("Cineline", "http://evonic.tv/forum/list.php?r=category/169-Cineline&page="))
		self.genreListe.append(("HD-Collection", "http://evonic.tv/forum/content.php?r=3501-hd-collection&page="))
		self.genreListe.append(("HD-Serien", "http://evonic.tv/forum/content.php?r=5993-Serien&page="))
		self.genreListe.append(("Century", "dump"))
		self.genreListe.append(("Imdb", "dump"))
		self.genreListe.append(("Imdb Top 1000", "dump"))
		self.genreListe.append(("Suche", "suche"))
		self.genreListe.append(("3D-Charts", "http://evonic.tv/forum/content.php?r=5440-3d-charts&page="))
		self.genreListe.append(("3D", "http://evonic.tv/forum/content.php?r=4225-3d-filme&page="))
		self.genreListe.append(("HD-Charts", "http://evonic.tv/forum/content.php?r=1989-HD-Charts&page="))
		self.genreListe.append(("Alle HD Premium Streams", "http://evonic.tv/forum/content.php?r=1669-hd-filme&page="))
		self.genreListe.append(("Abenteuer", "http://evonic.tv/forum/list.php?r=category/65-HD-Abenteuer&page="))
		self.genreListe.append(("Action", "http://evonic.tv/forum/list.php?r=category/35-HD-Action&page="))
		self.genreListe.append(("Biografie", "http://evonic.tv/forum/list.php?r=category/70-HD-Biografie&page="))
		self.genreListe.append(("Doku", "http://evonic.tv/forum/list.php?r=category/64-HD-Doku&page="))
		self.genreListe.append(("Drama", "http://evonic.tv/forum/list.php?r=category/36-HD-Drama&page="))
		self.genreListe.append(("Fantasy", "http://evonic.tv/forum/list.php?r=category/37-HD-Fantasy&page="))
		self.genreListe.append(("Horror", "http://evonic.tv/forum/list.php?r=category/38-HD-Horror&page="))
		self.genreListe.append(("Komödie", "http://evonic.tv/forum/list.php?r=category/39-HD-Kom%F6die&page="))
		self.genreListe.append(("Kriegsfilm", "http://evonic.tv/forum/list.php?r=category/66-HD-Kriegsfilm&page="))
		self.genreListe.append(("Krimi", "http://evonic.tv/forum/list.php?r=category/56-HD-Krimi&page="))
		self.genreListe.append(("Mystery", "http://evonic.tv/forum/list.php?r=category/62-HD-Mystery&page="))
		self.genreListe.append(("Romanze", "http://evonic.tv/forum/list.php?r=category/40-HD-Romanze&page="))
		self.genreListe.append(("SciFi", "http://evonic.tv/forum/list.php?r=category/41-HD-SciFi&page="))
		self.genreListe.append(("Thriller", "http://evonic.tv/forum/list.php?r=category/42-HD-Thriller&page="))
		self.genreListe.append(("Zeichentrick", "http://evonic.tv/forum/list.php?r=category/43-HD-Zeichentrick&page="))
		self.chooseMenuList.setList(map(meGenreEntry, self.genreListe))
		self.keyLocked = False

	def keyOK(self):
		if not self.keyLocked and self.loginOK:
			enterAuswahlLabel = self['genreList'].getCurrent()[0][0]
			enterAuswahlLink = self['genreList'].getCurrent()[0][1]

			print "Select:", enterAuswahlLabel, enterAuswahlLink

			if enterAuswahlLabel == "Century":
				self.session.open(meCenturyScreen)
			elif enterAuswahlLabel == "Imdb":
				self.session.open(meImdbScreen)
			elif enterAuswahlLabel == "Watchlist":
				self.session.open(meWatchlistScreen)
			elif enterAuswahlLabel == "Imdb Top 1000":
				self.session.open(meTimdbGenreScreen, self.stoken)
			elif enterAuswahlLabel == "Suche":
				self.session.openWithCallback(self.mySearch, VirtualKeyBoard, title = (_("Suche:")), text = self.searchText)
			else:
				self.session.open(meMovieScreen, enterAuswahlLink, enterAuswahlLabel)

	def mySearch(self, callback = None):
		print 'mySearch'
		if callback != None:
			self.searchTxt = callback
			self.session.open(meSearchScreen, self.searchTxt, self.stoken)

	def dataError(self, error):
		print error

	def loginSetup(self):
		self.session.openWithCallback(self.callBackSetup, meSetupScreen)

	def callBackSetup(self, answer):
		if answer:
			self.login()

	def keyCancel(self):
		self.close()

class meSearchScreen(Screen):

	def __init__(self, session, search, stoken):
		self.session = session
		self.search = search
		self.stoken = stoken
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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Search Auswahl: %s" % self.search)
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.searchList = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		url = "http://evonic.tv/forum/ajaxlivesearch.php?do=search"
		print self.search, self.stoken

		postData = {'do': 'search',
					 'keyword': self.search,
					 'lsasort': 'lastpost',
					 'lsasorttype': 'DESC',
					 'lsatype': 0,
					 'lsawithword': 1,
					 'lsazone': '',
					 's': '',
					 'securitytoken': self.stoken
					 }

		getPage(url, method="POST", postdata=urlencode(postData), cookies=ck,
			headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://evonic.tv/forum/content.php'},
			followRedirect=True, timeout=30).addCallback(self.loadData).addErrback(self.dataError)

	def loadData(self, data):
		found = re.findall('<span><a href=".*?" title="Stream">Stream</a></span>.*?<a href="(http://evonic.tv/forum/showthread.php\?t=.*?)" title="(.*?)">', data, re.S)
		if found:
			self.searchList = []
			for link,title in found:
				print title, link
				self.searchList.append((title,link))
		self.chooseMenuList.setList(map(meListEntry, self.searchList))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink

		getPage(streamLink, method="GET", cookies=ck,
			headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://evonic.tv/forum/content.php'},
			followRedirect=True, timeout=30).addCallback(self.loadRefreshData).addErrback(self.dataError)

	def loadRefreshData(self, data):
		refreshUrl = re.findall('<meta http-equiv="refresh" content="0; URL=(.*?)">', data, re.S)
		if refreshUrl:
			print refreshUrl

			if re.match('.*?Collection', self.streamName, re.S|re.I):
				print "Collection"
				self.session.open(meCollectionScreen, self.streamName, refreshUrl[0], "")
			else:
				getPage(refreshUrl[0], cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)

	def getStream(self, data):
		print data
		self.genreListe2 = []
		findStream = re.findall('"(http://evonic.tv/server/Premium.*?)"', data)
		if findStream:
			print "Premium", findStream
			self.genreListe2.append(("Premium", findStream[0].replace('"','')))

		findStream2 = re.findall('"http://evonic.tv/server/Free-Member.php.mov=.*?"', data)
		if findStream2:
			print "Free", findStream2
			self.genreListe2.append(("Free", findStream2[0].replace('"','')))

		print self.genreListe2
		self.session.open(meHosterScreen, self.streamName, self.genreListe2, "")

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meMovieScreen(Screen):

	def __init__(self, session, enterAuswahlLink, enterAuswahlLabel):
		self.session = session
		self.enterAuswahlLink = enterAuswahlLink
		self.enterAuswahlLabel = enterAuswahlLabel

		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/m4kdefaultPageListeScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/m4kdefaultPageListeScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		#self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.addWatchlist
		}, -1)

		self.keyLocked = True
		self.showStreams = False
		self['title'] = Label("evonic.tv - Filme Auswahl:")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.page = 1
		self.genreListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print self.enterAuswahlLink, self.enterAuswahlLabel
		self.showStreams = False
		url = "%s%s" % (self.enterAuswahlLink,str(self.page))
		print url
		getPage(url, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def loadPageData(self, data):
		self.genreListe = []
		print 'loadPageData', self.enterAuswahlLink
		if self.enterAuswahlLabel == "Aktuelle Filme":

			print "Aktuelle Filme"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			search = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if search:
				for enterLink,enterName,enterImdb,enterPic in search:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv'), enterImdb))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()
			else:
				print "kacke"

		elif self.enterAuswahlLabel == "3D-Charts":
			print "3D Charts"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			search3D = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if search3D:
				for enterLink,enterName,enterImdb,enterPic in search3D:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()

		elif self.enterAuswahlLabel == "HD-Charts":
			print "HD Charts"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			searchHD = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if searchHD:
				for enterLink,enterName,enterImdb,enterPic in searchHD:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()

		elif self.enterAuswahlLabel == "3D":
			print "3D"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			movies3D = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if movies3D:
				self.genreListe = []
				for enterLink,enterName,enterImdb,enterPic in movies3D:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()
			else:
				self.lastPage = self.page

		elif self.enterAuswahlLabel == "Alle HD Premium Streams":
			print "Alle Premium"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			movies3D = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if movies3D:
				self.genreListe = []
				for enterLink,enterName,enterImdb,enterPic in movies3D:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()
			else:
				self.lastPage = self.page

		elif self.enterAuswahlLabel == "HD-Serien":
			print "HD-Serien"
			totalPages = re.findall('<span class="first_last"><a href=".*?page=(.*?)"', data, re.S)
			if totalPages:
				print totalPages
				self['page'].setText("%s / %s" % (self.page, totalPages[0]))

			result = re.findall('<h3 class="article_preview">.*?<a href="(.*?)">.*?<span>[A-Z][A-Z][:](.*?)</span>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau" />', data, re.S)
			if result:
				for enterLink, enterName, enterPic in result:
					enterName = decodeHtml2(enterName)
					self.genreListe.append((enterName, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.loadHandlung()
				self.loadPic()
				self.keyLocked = False
			else:
				self['handlung'].setText("Nichts gefunden...")

		else:
			print "Sonstige Genres"
			totalPages = re.search('>Seite \d+ von (\d+)</a>', data, re.S)
			if totalPages:
				print "Last page:",totalPages.group(1)
				self['page'].setText("%s / %s" % (self.page, totalPages.group(1)))

			movies = re.findall('<h3 class="article_preview">.*?<a href="(.*?)"><span>[AZ:]?(.*?)</span></a>.*?<div class="cms_article_section_location">.*?>IMDB(.*?)</a>.*?<img class="cms_article_preview_image" src="(.*?)" alt="Vorschau"', data,re.S)
			if movies:
				self.genreListe = []
				for enterLink,enterName,enterImdb,enterPic in movies:
					enterName = decodeHtml2(enterName)
					enterTitle = enterName.replace("HD:", "").strip() + ' (IMDB:' + enterImdb + ')'
					self.genreListe.append((enterTitle, enterLink, enterPic.replace('http://my-entertainment.biz','http://evonic.tv')))
				self.chooseMenuList.setList(map(meListEntry, self.genreListe))
				self.keyLocked = False
				self.loadPic()
				self.loadHandlung()

	def addWatchlist(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.enterAuswahlLabel, self.streamName, streamLink

		if not fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist"):
			print "erstelle watchlist"
			open(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist","w").close()

		if fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist"):
			print "schreibe watchlist", self.enterAuswahlLabel, self.streamName, streamLink
			writePlaylist = open(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist","a")
			writePlaylist.write('"%s" "%s" "%s"\n' % (self.enterAuswahlLabel, self.streamName, streamLink))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("%s wurde zur watchlist hinzugefuegt." % self.streamName), MessageBox.TYPE_INFO, timeout=3)

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink

		if self.enterAuswahlLabel == "HD-Serien":
			self.session.open(meSerienScreen, self.streamName, streamLink, self.streamPic)
		elif self.enterAuswahlLabel == "HD-Collection":
			self.session.open(meCollectionScreen, self.streamName, streamLink, self.streamPic)
		else:
			getPage(streamLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)

	def getStream(self, data):
		self.genreListe2 = []
		findStream = re.findall('"(http://evonic.tv/server/Premium.*?)"', data)
		if findStream:
			print "Premium", findStream
			self.genreListe2.append(("Premium", findStream[0].replace('"','')))

		findStream2 = re.findall('"http://evonic.tv/server/Free-Member.php.mov=.*?"', data)
		if findStream2:
			print "Free", findStream2
			self.genreListe2.append(("Free", findStream2[0].replace('"','')))

		print self.genreListe2
		self.session.open(meHosterScreen, self.streamName, self.genreListe2, self.streamPic)

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		self.streamPic = self['filmList'].getCurrent()[0][2]
		self['name'].setText(self.enterAuswahlLabel)
		CoverHelper(self['coverArt']).getCover(self.streamPic)

	def loadHandlung(self):
		streamFilmLink = self['filmList'].getCurrent()[0][1]
		print "loadHandlung...", streamFilmLink
		getPage(streamFilmLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.setHandlung).addErrback(self.dataError)

	def setHandlung(self, data):
		handlung = re.findall('<div class="bbcode_quote_container"></div>(.*?)<', data, re.S)
		if handlung:
			handlung = re.sub(r"\s+", " ", handlung[0])
			handlung = decodeHtml2(handlung)
			self['handlung'].setText(handlung.strip())
		else:
			self['handlung'].setText("Keine infos gefunden.")

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		self.loadHandlung()

	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		self.loadHandlung()

	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()
		self.loadHandlung()

	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
		self.loadHandlung()

	def keyPageDown(self):
		print "PageDown", self.page
		if self.keyLocked:
			return

		if not self.page < 2:
			self.page -= 1
			self.loadPage()

	def keyPageUp(self):
		print "PageUp", self.page
		if self.keyLocked:
			return

		if self.page:
			self.page += 1
			self.loadPage()
		else:
			return

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meSerienScreen(Screen):

	def __init__(self, session, eName, eLink, streamPic):
		self.session = session
		self.eName = eName
		self.eLink = eLink
		self.streamPic = streamPic

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("%s - Episoden Auswahl:" % self.eName)
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.page = 1
		self.eListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		CoverHelper(self['coverArt']).getCover(self.streamPic)
		getPage(self.eLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getEpisoden).addErrback(self.dataError)

	def getEpisoden(self, data):
		self.watched_liste = []
		self.mark_last_watched = []
		if not fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watched"):
			open(config.mediaportal.watchlistpath.value+"mp_evonic_watched","w").close()
		if fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watched"):
			leer = os.path.getsize(config.mediaportal.watchlistpath.value+"mp_evonic_watched")
			if not leer == 0:
				self.updates_read = open(config.mediaportal.watchlistpath.value+"mp_evonic_watched" , "r")
				for lines in sorted(self.updates_read.readlines()):
					line = re.findall('"(.*?)"', lines)
					if line:
						self.watched_liste.append("%s" % (line[0]))
				self.updates_read.close()

		staffeln = re.findall('<img src="http://evonic.tv/images/unbenanyn.jpg"(.*?)<iframe src="http://evonic.tv/images/hdtvschaer.jpg"', data, re.S)
		if staffeln:
			staffelcount = 0
			for each in staffeln:
				staffelcount += 1
				eps = re.findall('<a href="(.*?)" target="Videoframe.*?"><b><span style="color: black;">(.*?)</span>', each, re.S)
				if eps:
					for link,epTitle in eps:
						if int(staffelcount) < 10:
							setStaffel = "S0%s" % str(staffelcount)
						else:
							setStaffel = "S%s" % str(staffelcount)
						print "Staffel "+setStaffel, epTitle, link

						dupe_streamname = "%s - %s" % (self.eName, setStaffel + "E" + epTitle)
						if dupe_streamname in self.watched_liste:
							self.eListe.append((setStaffel + "E" + epTitle, link, True))
						else:
							self.eListe.append((setStaffel + "E" + epTitle, link, False))
					self.chooseMenuList.setList(map(meWatchedListEntry, self.eListe))
					self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print self.streamName, streamLink
		getPage(streamLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamUrl).addErrback(self.dataError)

	def getStreamUrl(self, data):
		print "get Stream Url.."
		if self.streamName == "Premium":
			stream_url = re.findall('src="(.*?)"', data, re.S)
			if stream_url:
				print stream_url
				self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)
				self.markAsWatched()
		else:
			print data
			stream_url = re.findall('src="(.*?)"', data, re.S)
			if stream_url:
				print stream_url
				self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)
				self.markAsWatched()

	def markAsWatched(self):
		self.stream_name = "%s - %s" % (self.eName, self.streamName)
		print self.stream_name
		if not fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watched"):
			open(config.mediaportal.watchlistpath.value+"mp_evonic_watched","w").close()

		self.update_liste = []
		leer = os.path.getsize(config.mediaportal.watchlistpath.value+"mp_evonic_watched")
		if not leer == 0:
			self.updates_read = open(config.mediaportal.watchlistpath.value+"mp_evonic_watched" , "r")
			for lines in sorted(self.updates_read.readlines()):
				line = re.findall('"(.*?)"', lines)
				if line:
					print line[0]
					self.update_liste.append("%s" % (line[0]))
			self.updates_read.close()

			updates_read2 = open(config.mediaportal.watchlistpath.value+"mp_evonic_watched" , "a")
			check = ("%s" % self.stream_name)
			if not check in self.update_liste:
				print "update add: %s" % (self.stream_name)
				updates_read2.write('"%s"\n' % (self.stream_name))
				updates_read2.close()
			else:
				print "dupe %s" % (self.stream_name)
		else:
			updates_read3 = open(config.mediaportal.watchlistpath.value+"mp_evonic_watched" , "a")
			print "[update add: %s" % (self.stream_name)
			updates_read3.write('"%s"\n' % (self.stream_name))
			updates_read3.close()

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meCenturyScreen(Screen):

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Century Auswahl:")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.yearList = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.yearList = []
		self.yearList.append(('Jahr 2013','http://evonic.tv/forum/list.php?r=category/217&page='))
		self.yearList.append(('Jahr 2012','http://evonic.tv/forum/list.php?r=category/216&page='))
		self.yearList.append(('Jahr 2011','http://evonic.tv/forum/list.php?r=category/215&page='))
		self.yearList.append(('Jahr 2010','http://evonic.tv/forum/list.php?r=category/214&page='))
		self.yearList.append(('Jahr 2009','http://evonic.tv/forum/list.php?r=category/213&page='))
		self.yearList.append(('Jahr 2008','http://evonic.tv/forum/list.php?r=category/212&page='))
		self.yearList.append(('Jahr 2007','http://evonic.tv/forum/list.php?r=category/211&page='))
		self.yearList.append(('Jahr 2006','http://evonic.tv/forum/list.php?r=category/210&page='))
		self.yearList.append(('Jahr 2005','http://evonic.tv/forum/list.php?r=category/209&page='))
		self.yearList.append(('Jahr 2004','http://evonic.tv/forum/list.php?r=category/208&page='))
		self.yearList.append(('Jahr 2003','http://evonic.tv/forum/list.php?r=category/207&page='))
		self.yearList.append(('Jahr 2002','http://evonic.tv/forum/list.php?r=category/206&page='))
		self.yearList.append(('Jahr 2001','http://evonic.tv/forum/list.php?r=category/205&page='))
		self.yearList.append(('Jahr 2000','http://evonic.tv/forum/list.php?r=category/204&page='))
		self.yearList.append(('Jahr 1990','http://evonic.tv/forum/list.php?r=category/203&page='))
		self.yearList.append(('Jahr 1980','http://evonic.tv/forum/list.php?r=category/202&page='))
		self.yearList.append(('Jahr 1970','http://evonic.tv/forum/list.php?r=category/201&page='))
		self.yearList.append(('Jahr 1960','http://evonic.tv/forum/list.php?r=category/200&page='))
		self.yearList.append(('Jahr 1950','http://evonic.tv/forum/list.php?r=category/199&page='))
		self.chooseMenuList.setList(map(meGenreEntry, self.yearList))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink
		self.session.open(meMovieScreen, streamLink, self.streamName)

	def keyCancel(self):
		self.close()

class meImdbScreen(Screen):

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Century Auswahl:")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.imdbList = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.imdbList = []
		self.imdbList.append(('IMDB 8.0','http://evonic.tv/forum/list.php?r=category/161&page='))
		self.imdbList.append(('IMDB 7.0','http://evonic.tv/forum/list.php?r=category/162&page='))
		self.imdbList.append(('IMDB 6.0','http://evonic.tv/forum/list.php?r=category/163&page='))
		self.imdbList.append(('IMDB 5.0','http://evonic.tv/forum/list.php?r=category/164&page='))
		self.imdbList.append(('IMDB 4.0','http://evonic.tv/forum/list.php?r=category/165&page='))
		self.imdbList.append(('IMDB 3.0','http://evonic.tv/forum/list.php?r=category/166&page='))
		self.imdbList.append(('IMDB 2.0','http://evonic.tv/forum/list.php?r=category/167&page='))
		self.chooseMenuList.setList(map(meGenreEntry, self.imdbList))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink
		self.session.open(meMovieScreen, streamLink, self.streamName)

	def keyCancel(self):
		self.close()

class meCollectionScreen(Screen):

	def __init__(self, session, eName, eLink, streamPic):
		self.session = session
		self.eName = eName
		self.eLink = eLink
		self.streamPic = streamPic

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("%s - Collection Auswahl:" % self.eName)
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.page = 1
		self.eListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		CoverHelper(self['coverArt']).getCover(self.streamPic)
		getPage(self.eLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getEpisoden).addErrback(self.dataError)

	def getEpisoden(self, data):
		self.eListe = []
		titles = re.findall('>*\s*\r*\n<.*?>*\r*\n*\s(.*?)<.*?>*\r*\n*\s*<*>*\r*\n*<div style="margin: 5px;">', data)
		if titles[0] == "":
			titles = re.findall('<font size="4">(.*?)</font><br />', data, re.S)
			print titles

		if titles:
			for title in titles:
				raw = re.findall(title.replace('(','\(').replace(')','\)')+'(.*?)(<div class="spoiler" style="display: none;">Platzhalter</div>|<iframe src="http://my-entertainment.biz/images/hdtvschaer.jpg"|<iframe src="http://evonic.tv/images/hdtvschaer.jpg")', data, re.S)
				if raw:
					if "Platzhalter" in raw[0][1]:
						print title, "Platzhalter"
						self.eListe.append((title+" - Nicht vorhanden.", "Platzhalter"))
					else:
						servers = re.findall('<a href="(http://evonic.tv/server/.*?)"', raw[0][0], re.S)
						if servers:
							print title, servers
							self.eListe.append((title, servers))

			self.chooseMenuList.setList(map(meListEntry, self.eListe))
			self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink
		self.session.open(meServerScreen, self.streamName, streamLink, self.streamPic)

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meTimdbGenreScreen(Screen):

	def __init__(self, session, stoken):
		self.session = session
		self.stoken = stoken

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
		"ok"	: self.keyOK,
		"cancel": self.keyCancel,
		"up" : self.keyUp,
		"down" : self.keyDown,
		"right" : self.keyRight,
		"left" : self.keyLeft,
		"nextBouquet" : self.keyPageUp,
		"prevBouquet" : self.keyPageDown
		}, -1)

		self.keyLocked = True
		self['title'] = Label("IMDb - Top 1000 Suche")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.filmliste = []
		self.page = 1
		self.lastpage = 20

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.keyLocked = True
		self.filmliste = []
		self.start = 1
		self.start = (self.page * 50) - 49

		url = "http://www.imdb.de/search/title?groups=top_1000&sort=user_rating,desc&start=%s" % str(self.start)
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded', 'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0', 'Accept-Language':'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		movies = re.findall('<td class="number">(.*?)</td>.*?<img src="(.*?)".*?<a href="/title/.*?">(.*?)</a>.*?<span class="year_type">(.*?)</span><br>.*?<div class="rating rating-list".*?title="Users rated this (.*?\/)', data, re.S)
		if movies:
			for place,image,title,year,rates in movies:
				rates = "%s10" % rates
				image_raw = image.split('@@')
				image = "%s@@._V1_SX214_.jpg" % image_raw[0]
				self.filmliste.append((place, decodeHtml(title), year, rates, image))
				self.chooseMenuList.setList(map(meTimdbEntry, self.filmliste))
			self.showInfos()
			self.keyLocked = False

	def dataError(self, error):
		printl(error,self,"E")

	def showInfos(self):
		coverUrl = self['filmList'].getCurrent()[0][4]
		self['page'].setText("%s / 20" % str(self.page))
		CoverHelper(self['coverArt']).getCover(coverUrl)

	def keyOK(self):
		if self.keyLocked:
			return

		self.searchTitle = self['filmList'].getCurrent()[0][1]
		print self.searchTitle

		self.session.openWithCallback(self.mySearch, VirtualKeyBoard, title = (_("Suche:")), text = self.searchTitle)

	def mySearch(self, callback = None):
		print 'mySearch'
		if callback != None:
			self.session.open(meSearchScreen, callback, self.stoken)

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

	def keyCancel(self):
		self.close()

class meWatchlistScreen(Screen):

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
		if fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist"):
			print "read watchlist"
			readStations = open(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist","r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(which, title, link) = data[0]
					print which, title, link
					self.watchListe.append((which, title, link))
			print "Load Watchlist.."
			self.watchListe.sort()
			self.chooseMenuList.setList(map(meWatchListEntry, self.watchListe))
			readStations.close()
			self.keyLocked = False

	def delWatchListEntry(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		entryDeleted = False
		selectedName = self['filmList'].getCurrent()[0][1]

		writeTmp = open(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist.tmp","w")
		if fileExists(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist"):
			readWatchlist = open(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist","r")
			for rawData in readWatchlist.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(genre, title, link) = data[0]
					if title != selectedName:
						writeTmp.write('"%s" "%s" "%s"\n' % (genre, title, link))
					else:
						if entryDeleted:
							writeTmp.write('"%s" "%s" "%s"\n' % (genre, title, link))
						else:
							entryDeleted = True
			readWatchlist.close()
			writeTmp.close()
			shutil.move(config.mediaportal.watchlistpath.value+"mp_evonic_watchlist.tmp", config.mediaportal.watchlistpath.value+"mp_evonic_watchlist")
			self.loadPage()

	def keyOK(self):
		exist = self['filmList'].getCurrent()
		if self.keyLocked or exist == None:
			return

		streamWhich = self['filmList'].getCurrent()[0][0]
		self.streamName = self['filmList'].getCurrent()[0][1]
		streamLink = self['filmList'].getCurrent()[0][2]

		print streamWhich, self.streamName, streamLink

		if re.match('.*?Serien', streamWhich, re.S|re.I):
			self.session.open(meSerienScreen, self.streamName, streamLink, "")
		elif re.match('.*?Collection', streamWhich, re.S|re.I):
			self.session.open(meCollectionScreen, self.streamName, streamLink, "")
		else:
			getPage(streamLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStream).addErrback(self.dataError)

	def getStream(self, data):
		self.genreListe2 = []
		findStream = re.findall('"(http://evonic.tv/server/Premium.*?)"', data)
		if findStream:
			print "Premium", findStream
			self.genreListe2.append(("Premium", findStream[0].replace('"','')))

		findStream2 = re.findall('"http://evonic.tv/server/Free-Member.php.mov=.*?"', data)
		if findStream2:
			print "Free", findStream2
			self.genreListe2.append(("Free", findStream2[0].replace('"','')))

		print self.genreListe2
		self.session.open(meHosterScreen, self.streamName, self.genreListe2, "")

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meServerScreen(Screen):

	def __init__(self, session, eName, eLink, streamPic):
		self.session = session
		self.eName = eName
		self.eLink = eLink
		self.streamPic = streamPic

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("%s - Collection Auswahl:" % self.eName)
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.page = 1
		self.eListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.eListe = []
		CoverHelper(self['coverArt']).getCover(self.streamPic)
		print self.eLink
		for server in self.eLink:
			print server
			if "Free-Member" in server:
				self.eListe.append(("Free-Member", server))
			elif "Premium-Member" in server:
				self.eListe.append(("Premium-Member", server))
		self.chooseMenuList.setList(map(meGenreEntry, self.eListe))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]

		print self.streamName, streamLink
		getPage(streamLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamUrl).addErrback(self.dataError)

	def getStreamUrl(self, data):
		print "get Stream Url.."
		if self.streamName == "Premium":
			stream_url = re.findall('src="(http://.*?)"', data, re.S)
			if stream_url:
				print stream_url
				self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)
		else:
			print data
			stream_url = re.findall('src="(http://.*?)"', data, re.S)
			if stream_url:
				print stream_url
				self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meHosterScreen(Screen):

	def __init__(self, session, eName, eListe, streamPic):
		self.session = session
		self.eName = eName
		self.eListe = eListe
		self.streamPic = streamPic

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
			"cancel": self.keyCancel
		}, -1)

		self.keyLocked = True
		self['title'] = Label("Stream Auswahl:")
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("")
		self['coverArt'] = Pixmap()

		self.page = 1
		self.genreListe = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		self.chooseMenuList.setList(map(meGenreEntry, self.eListe))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		self.streamName = self['filmList'].getCurrent()[0][0]
		streamLink = self['filmList'].getCurrent()[0][1]
		print self.streamName, streamLink
		getPage(streamLink, cookies=ck, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getStreamUrl).addErrback(self.dataError)

	def getStreamUrl(self, data):
		print "get Stream Url.."
		if self.streamName == "Premium":
			stream_url = re.findall('src="(http://.*?)"', data, re.S)
			if stream_url:
				print stream_url
				self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)
		else:
			print data
			stream_url = re.findall('source src="(http://.*?)"', data, re.S)
			print stream_url
			self.session.open(SimplePlayer, [(self.eName + " " + self.streamName, stream_url[0], self.streamPic)], showPlaylist=False, ltype='ME', cover=True)

	def dataError(self, error):
		print error

	def keyCancel(self):
		self.close()

class meSetupScreen(Screen, ConfigListScreen):

	skin = """
		<screen position="center,center" size="450,140" title="Premium Setup">
			<ePixmap position="15,4" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/username.png" alphatest="blend" />
			<ePixmap position="15,29" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/password.png" alphatest="blend" />
			<widget name="config" position="50,0" size="400,50" scrollbarMode="showOnDemand" />
		        <eLabel text="Nach 5 fehlerhaften Login Versuchen ist eine Anmeldung f\xc3\xbcr die n\xc3\xa4chsten 15 Minuten nicht mehr m\xc3\xb6glich." position="25,67" size="410,66" font="mediaportal;17" valign="center" halign="center" transparent="1" foregroundColor="#FF0000" />
                </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		self.list = []
		ConfigListScreen.__init__(self, self.list)

		self.list.append(getConfigListEntry("Username:", config.entertain.userName))
		self.list.append(getConfigListEntry("Password:", config.entertain.userPass))
		self["config"].setList(self.list)

		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"ok":		self.saveConfig,
			"cancel":	self.exit
		}, -1)

	def saveConfig(self):
		print "save"
		for x in self["config"].list:
			x[1].save()
		configfile.save()
		self.close(True)

	def exit(self):
		self.close(False)
