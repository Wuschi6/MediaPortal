#	-*-	coding:	utf-8	-*-

import Queue
import threading
from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.playhttpmovie import PlayHttpMovie
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer
from Plugins.Extensions.MediaPortal.resources.coverhelper import CoverHelper
from Plugins.Extensions.MediaPortal.resources.youtubeplayer import YoutubePlayer

if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TMDb/plugin.pyo'):
	from Plugins.Extensions.TMDb.plugin import *
	TMDbPresent = True
elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo'):
	TMDbPresent = False
	IMDbPresent = True
	from Plugins.Extensions.IMDb.plugin import *
else:
	IMDbPresent = False
	TMDbPresent = False

DDLME_Version = "ddl.me v0.97 (experimental)"

DDLME_siteEncoding = 'utf-8'

"""
Sondertastenbelegung:

Genre Auswahl:
	KeyCancel	: Menu Up / Exit
	KeyOK		: Menu Down / Select

Tastenfunktionen in der Filmliste:
	Bouquet +/-				: Seitenweise blättern in 1 Schritten Up/Down
	'1', '4', '7',
	'3', 6', '9'			: blättern in 2er, 5er, 10er Schritten Down/Up
	INFO					: anzeige der IMDB-Bewertung
	KeyYellow				: Sortierung

Stream Auswahl:
	Rot/Blau				: Die Beschreibung Seitenweise scrollen
"""
def DDLME_menuListentry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		]

class show_DDLME_Genre(Screen):

	def __init__(self, session):
		self.session = session
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultGenreScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up"	: self.keyUp,
			"down"	: self.keyDown,
			"left"	: self.keyLeft,
			"right"	: self.keyRight
		}, -1)

		self['title'] = Label(DDLME_Version)
		self['ContentTitle'] = Label("Genres")
		self['name'] = Label("Auswahl:")
		self['F1'] = Label("Exit")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("")

		self.param_qr = ''
		self.menuLevel = 0
		self.menuMaxLevel = 1
		self.menuIdx = [0,0,0]
		self.keyLocked = True
		self.genreSelected = False
		self.menuListe = []
		self.baseUrl = "http://de.ddl.me"
		self.genreBase = ["/search_99/?q=", "/moviez_", "/episodez_", "/abookz_", "", "", "", "", "", "", ""]
		self.genreName = ["","","",""]
		self.genreUrl = ["","","",""]
		self.genreTitle = ""
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList

		self.genreMenu = [
			[
			("Suche...", ""),
			("Filme", ""),
			("Serien", "")
			#("Hörbücher", "")
			],
			[None,
			[
			("Neue Filme", "/update_0_1"),
			("Alle", "00_%d_1_%d"),
			("Kinofilme", "23_%d_1_%d"),
			("Abenteuer", "01_%d_1_%d"),
			("Action", "02_%d_1_%d"),
			("Animation", "03_%d_1_%d"),
			("Biografie", "04_%d_1_%d"),
			("Blockbuster", "25_%d_1_%d"),
			("Doku", "06_%d_1_%d"),
			("Drama", "07_%d_1_%d"),
			("Familie", "08_%d_1_%d"),
			("Fantasie", "09_%d_1_%d"),
			("Geschichte", "10_%d_1_%d"),
			("Horror", "11_%d_1_%d"),
			("Klassiker", "12_%d_1_%d"),
			("Komödie", "13_%d_1_%d"),
			("Kriegsfilm", "14_%d_1_%d"),
			("Musik", "15_%d_1_%d"),
			("Mystery", "16_%d_1_%d"),
			("Romantisch", "17_%d_1_%d"),
			("SciFi", "18_%d_1_%d"),
			("Sport", "20_%d_1_%d"),
			("Thriller", "21_%d_1_%d"),
			("Western", "22_%d_1_%d")
			],
			[
			("Neue Serien", "/update_0_1"),
			("Alle", "00_%d_1_%d"),
			("Abenteuer", "01_%d_1_%d"),
			("Action", "02_%d_1_%d"),
			("Animation", "03_%d_1_%d"),
			("Doku", "06_%d_1_%d"),
			("Drama", "07_%d_1_%d"),
			("Familie", "08_%d_1_%d"),
			("Fantasie", "09_%d_1_%d"),
			("Geschichte", "10_%d_1_%d"),
			("Horror", "11_%d_1_%d"),
			("Komödie", "13_%d_1_%d"),
			("Mystery", "16_%d_1_%d"),
			("Romantisch", "17_%d_1_%d"),
			("SciFi", "18_%d_1_%d"),
			("Sport", "20_%d_1_%d"),
			("Thriller", "21_%d_1_%d"),
			("Western", "22_%d_1_%d")
			],
			[
			("Alle", "00_%d_1_%d"),
			("Thriller", "01_%d_1_%d"),
			("Krimi", "02_%d_1_%d"),
			("Fantasy", "03_%d_1_%d"),
			("Horror", "04_%d_1_%d"),
			("SciFi", "05_%d_1_%d"),
			("Romane", "06_%d_1_%d"),
			("Historisch", "07_%d_1_%d"),
			("Klassiker", "08_%d_1_%d"),
			("Humor", "09_%d_1_%d"),
			("Bildung & Wissen", "10_%d_1_%d"),
			("Freizeit & Leben", "11_%d_1_%d"),
			("Karriere", "12_%d_1_%d"),
			("Kinder", "13_%d_1_%d"),
			("Jugendliche", "14_%d_1_%d"),
			("Erotik", "15_%d_1_%d")
			]
			],
			[
			None, None, None, None
			]
			]

		self.onLayoutFinish.append(self.loadMenu)

	def setGenreStrTitle(self):
		genreName = self['genreList'].getCurrent()[0][0]
		genreLink = self['genreList'].getCurrent()[0][1]
		if self.menuLevel in range(self.menuMaxLevel+1):
			if self.menuLevel == 0:
				self.genreName[self.menuLevel] = genreName
			else:
				self.genreName[self.menuLevel] = ':'+genreName

			self.genreUrl[self.menuLevel] = genreLink
		self.genreTitle = "%s%s%s" % (self.genreName[0],self.genreName[1],self.genreName[2])
		self['name'].setText("Genre: "+self.genreTitle)

	def loadMenu(self):
		print "ddl.me:"
		self.setMenu(0, True)
		self.keyLocked = False

	def keyUp(self):
		self['genreList'].up()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()

	def keyDown(self):
		self['genreList'].down()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()

	def keyRight(self):
		self['genreList'].pageDown()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()

	def keyLeft(self):
		self['genreList'].pageUp()
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setGenreStrTitle()

	def keyMenuUp(self):
		print "keyMenuUp:"
		if self.keyLocked:
			return
		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(-1)

	def keyOK(self):
		print "keyOK:"
		if self.keyLocked:
			return

		self.menuIdx[self.menuLevel] = self['genreList'].getSelectedIndex()
		self.setMenu(1)

		if self.genreSelected:
			print "Genre selected"
			if re.search('Neue (Filme|Serien)', self.genreTitle):
				genreurl = self.baseUrl+self.genreUrl[0]+self.genreUrl[1]
			else:
				genreurl = self.baseUrl+self.genreBase[self.menuIdx[0]]+self.genreUrl[0]+self.genreUrl[1]
			print genreurl
			if re.search('Suche...', self.genreTitle):
				self.paraQuery()
			else:
				self.session.open(DDLME_FilmListeScreen, genreurl, self.genreTitle)

	def paraQuery(self):
		self.param_qr = ''
		self.session.openWithCallback(self.cb_paraQuery, VirtualKeyBoard, title = (_("Suchanfrage")), text = self.param_qr)

	def cb_paraQuery(self, callback = None, entry = None):
		if callback != None:
			self.param_qr = callback.strip()
			if len(self.param_qr) > 0:
				qr = urllib.quote(self.param_qr)
				genreurl = self.baseUrl+self.genreBase[self.menuIdx[0]]+qr
				self.session.open(DDLME_FilmListeScreen, genreurl, self.genreTitle)

	def setMenu(self, levelIncr, menuInit=False):
		print "setMenu: ",levelIncr
		self.genreSelected = False
		if (self.menuLevel+levelIncr) in range(self.menuMaxLevel+1):
			if levelIncr < 0:
				self.genreName[self.menuLevel] = ""

			self.menuLevel += levelIncr

			if levelIncr > 0 or menuInit:
				self.menuIdx[self.menuLevel] = 0

			if self.menuLevel == 0:
				print "level-0"
				if self.genreMenu[0] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[0]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DDLME_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[0])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					print "No menu entrys!"
			elif self.menuLevel == 1:
				print "level-1"
				if self.genreMenu[1][self.menuIdx[0]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[1][self.menuIdx[0]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DDLME_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[1])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
			elif self.menuLevel == 2:
				print "level-2"
				if self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]] != None:
					self.menuListe = []
					for (Name,Url) in self.genreMenu[2][self.menuIdx[0]][self.menuIdx[1]]:
						self.menuListe.append((Name,Url))
					self.chooseMenuList.setList(map(DDLME_menuListentry, self.menuListe))
					self['genreList'].moveToIndex(self.menuIdx[2])
				else:
					self.genreName[self.menuLevel] = ""
					self.genreUrl[self.menuLevel] = ""
					self.menuLevel -= levelIncr
					self.genreSelected = True
					print "No menu entrys!"
		else:
			print "Entry selected"
			self.genreSelected = True

		print "menuLevel: ",self.menuLevel
		print "mainIdx: ",self.menuIdx[0]
		print "subIdx_1: ",self.menuIdx[1]
		print "subIdx_2: ",self.menuIdx[2]
		print "genreSelected: ",self.genreSelected
		print "menuListe: ",self.menuListe
		print "genreUrl: ",self.genreUrl

		self.setGenreStrTitle()

	def keyCancel(self):
		if self.menuLevel == 0:
			self.close()
		else:
			self.keyMenuUp()


def DDLME_FilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]
class DDLME_FilmListeScreen(Screen):

	def __init__(self, session, genreLink, genreName, imgLink=None):
		self.session = session
		self.genreLink = genreLink
		self.genreName = genreName
		self.imgLink = imgLink
		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions","DirectionActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"upUp" : self.key_repeatedUp,
			"rightUp" : self.key_repeatedUp,
			"leftUp" : self.key_repeatedUp,
			"downUp" : self.key_repeatedUp,
			"upRepeated" : self.keyUpRepeated,
			"downRepeated" : self.keyDownRepeated,
			"rightRepeated" : self.keyRightRepeated,
			"leftRepeated" : self.keyLeftRepeated,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"1" : self.key_1,
			"3" : self.key_3,
			"4" : self.key_4,
			"6" : self.key_6,
			"7" : self.key_7,
			"9" : self.key_9,
			"blue" :  self.keyTxtPageDown,
			"red" :  self.keyTxtPageUp,
			"yellow" :  self.keyYellow,
			"info"	: self.keyTMDbInfo
		}, -1)

		self.sortOrderTxt = ['Letztem Update', 'Blockbuster', 'IMDb Rating', 'Jahr']
		self.baseUrl = "http://de.ddl.me"
		self.genreTitle = "Auswahl "
		self['title'] = Label(DDLME_Version)
		self['ContentTitle'] = Label("")
		self['name'] = Label("")
		self['handlung'] = ScrollLabel("")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("Sortierung")
		self['F4'] = Label("Text+")
		self['Page'] = Label("Page")
		self['coverArt'] = Pixmap()

		self.timerStart = False
		self.seekTimerRun = False
		self.filmQ = Queue.Queue(0)
		self.eventL = threading.Event()
		self.keyLocked = True
		self.filmListe = []
		self.keckse = {}
		self.page = 0
		self.pages = 0;
		self.serienEpisoden = re.search('Episoden -', self.genreName)
		self.genreFilme = re.search('Filme', self.genreName)
		self.genreSerien = re.search('Serien', self.genreName)
		self.genreABook = re.search('Hörbücher', self.genreName)
		self.genreSearch = re.search('Suche...', self.genreName)
		self.genreUpdates = re.search('Neue (Filme|Serien)', self.genreName)
		self.genreSpecials = self.serienEpisoden or self.genreSearch or self.genreUpdates

		self.setGenreStrTitle()

		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['liste'] = self.chooseMenuList

		self.onLayoutFinish.append(self.loadPage)

	def setGenreStrTitle(self):
		if self.genreSpecials:
			genreName = "%s%s" % (self.genreTitle,self.genreName)
			self['F3'].hide()
		else:
			self['F3'].show()
			genreName = "%s%s - Sortierung: %s" % (self.genreTitle,self.genreName,self.sortOrderTxt[mp_globals.ddlme_sortOrder])

		#print genreName
		self['ContentTitle'].setText(genreName)

	def loadPage(self):
		print "loadPage:"
		if self.genreSpecials:
			url = self.genreLink
		else:
			page = self.page
			if page < 1:
				page = 1
			url = self.genreLink % (mp_globals.ddlme_sortOrder, page)

		if self.page:
			self['page'].setText("%d / %d" % (self.page,self.pages))

		self.filmQ.put(url)
		if not self.eventL.is_set():
			self.eventL.set()
			self.loadPageQueued()
		print "eventL ",self.eventL.is_set()

	def loadPageQueued(self):
		print "loadPageQueued:"
		self['name'].setText('Bitte warten...')
		while not self.filmQ.empty():
			url = self.filmQ.get_nowait()

		#self.eventL.clear()
		print url
		getPage(url, agent=std_headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		self.eventL.clear()
		print "dataError:"
		printl(error,self,"E")
		self['handlung'].setText("Fehler:\n" + str(error))

	def loadPageData(self, data):
		print "loadPageData:"
		self.filmListe = []

		if self.serienEpisoden:
			info = re.search('var subcats =.*?"info":', data)
			if info:
				self.pages = 1
				self.page = 1
				a = info.start()
				l = len(data)
				h = self.genreLink
				while a<l:
					info = re.search('"info":.*?"name":"(.*?)".*?"nr":"(.*?)".*?"staffel":"(.*?)"', data[a:])
					if info:
						a += info.end()
						nm = decodeHtml(info.group(1))
						i = nm.find('\u')
						if i>0:
							nm = nm[:i]

						t = 'S%02dE%03d - %s' % (int(info.group(3)), int(info.group(2)), nm)
						self.filmListe.append((t, h, self.imgLink, ''))
					else:
						a = l

				#self.filmListe.sort(key=lambda t : t[0].lower())
		elif self.genreUpdates:
			a = 0
			l = len(data)
			m = None
			while a<l:
				mg = re.search("class='submenu'>(.*?)class=\"hr\">", data[a:])
				if mg:
					a += mg.end()
					if re.search('Neue Filme', self.genreName):
						m = re.search(">Neue Filme<", mg.group(1))
					else:
						m = re.search(">Neue Serien<", mg.group(1))

					if m:
						m = re.search("<div id='view'(.*?)class=\"hr\">", data[a:])
						break
				else:
					a = l

			if m:
				print "m found"
				m = re.findall('title=\'(.*?)\'.*?href=\'(.*?)\'.*?<img.*?(http://.*?jpg)', m.group(1))
				if m:
					self.page = 1
					self.pages = 1
					print "movies found"
					for (t, h, i) in m:
						#print "tit.: ",t
						self.filmListe.append((decodeHtml(t), "%s%s" % (self.baseUrl, h), i, ''))
		else:
			print "normal parse"
			if self.genreSearch:
				print "search..."
				mg = re.search("<div id='view'(.*?)class=\"clear\">", data)
			else:
				mg = re.search("<div id='view'(.*?)class='clear'>", data)

			if mg:
				print "mg found"
				if self.genreSearch:
					m = re.findall('title=\'(.*?)\'.*?href=\'(.*?)\'.*?<img.*?src=\'(.*?)\'.*?(>TV<|>Film<)/span>', mg.group(1))
				else:
					m = re.findall('title=\'(.*?)\'.*?href=\'(.*?)\'.*?<img.*?src=\'(.*?)\'', mg.group(1))
				if m:
					print "movies found"
					if self.genreSearch:
						for (t, h, i, sm) in m:
							#print "tit.: ",t
							#print "sm: ",sm
							self.filmListe.append((decodeHtml(t), "%s%s" % (self.baseUrl, h), i, sm))
					else:
						for (t, h, i) in m:
							#print "tit.: ",t
							self.filmListe.append((decodeHtml(t), "%s%s" % (self.baseUrl, h), i, ''))

				if not self.pages:
					m1 = re.search('Seite.*?von(.*?)</h1>', data)

					if m1:
						pages = int(m1.group(1))
					else:
						pages = 1

					if pages > 999:
						self.pages = 999
					else:
						self.pages = pages

					self.page = 1

		print "Page: %d / %d" % (self.page,self.pages)
		self['page'].setText("%d / %d" % (self.page,self.pages))

		if len(self.filmListe) == 0:
			print "No videos found!"
			self.pages = 0
			self.filmListe.append(('Keine Filme / Serien gefunden !','','',''))
		else:
			menu_len = len(self.filmListe)
			print "Videos found: ",menu_len

		self.chooseMenuList.setList(map(DDLME_FilmListEntry, self.filmListe))
		self.loadPic()

	def loadPic(self):
		print "loadPic:"
		streamName = self['liste'].getCurrent()[0][0]
		self['name'].setText(streamName)
		desc = None
		print "streamName: ",streamName
		#print "streamUrl: ",streamUrl
		self.getHandlung(desc)

		if not self.filmQ.empty():
			self.loadPageQueued()
		else:
			self.eventL.clear()
		self.keyLocked	= False

		url = self['liste'].getCurrent()[0][2]
		CoverHelper(self['coverArt']).getCover(url)

	def getHandlung(self, desc):
		print "getHandlung:"
		if desc == None:
			print "No Infos found !"
			self['handlung'].setText("Keine weiteren Info's vorhanden.")
			return
		self.setHandlung(desc)

	def setHandlung(self, data):
		print "setHandlung:"
		self['handlung'].setText(decodeHtml(data))

	def keyOK(self):
		if (self.keyLocked|self.eventL.is_set()):
			return
		title = self['liste'].getCurrent()[0][0]
		url = self['liste'].getCurrent()[0][1]
		img = self['liste'].getCurrent()[0][2]
		sm = self['liste'].getCurrent()[0][3]
		genreSerien = self.genreSerien or sm == '>TV<' or re.search('Neue Serien', self.genreName)

		if not genreSerien:
			self.session.open(DDLMEStreams, url, title, img)
		else:
			self.session.open(DDLME_FilmListeScreen, url, 'Episoden - ' + title, imgLink=img)

	def keyUp(self):
		if self.keyLocked:
			return
		self['liste'].up()

	def keyDown(self):
		if self.keyLocked:
			return
		self['liste'].down()

	def keyUpRepeated(self):
		#print "keyUpRepeated"
		if self.keyLocked:
			return
		self['liste'].up()

	def keyDownRepeated(self):
		#print "keyDownRepeated"
		if self.keyLocked:
			return
		self['liste'].down()

	def key_repeatedUp(self):
		#print "key_repeatedUp"
		if self.keyLocked:
			return
		self.loadPic()

	def keyLeft(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()

	def keyRight(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()

	def keyLeftRepeated(self):
		if self.keyLocked:
			return
		self['liste'].pageUp()

	def keyRightRepeated(self):
		if self.keyLocked:
			return
		self['liste'].pageDown()

	def keyPageDown(self):
		#print "keyPageDown()"
		if self.seekTimerRun:
			self.seekTimerRun = False
		self.keyPageDownFast(1)

	def keyPageUp(self):
		#print "keyPageUp()"
		if self.seekTimerRun:
			self.seekTimerRun = False
		self.keyPageUpFast(1)

	def keyPageUpFast(self,step):
		if self.keyLocked:
			return
		#print "keyPageUpFast: ",step
		oldpage = self.page
		if (self.page + step) <= self.pages:
			self.page += step
		else:
			self.page = 1
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPage()

	def keyPageDownFast(self,step):
		if self.keyLocked:
			return
		print "keyPageDownFast: ",step
		oldpage = self.page
		if (self.page - step) >= 1:
			self.page -= step
		else:
			self.page = self.pages
		#print "Page %d/%d" % (self.page,self.pages)
		if oldpage != self.page:
			self.loadPage()

	def key_1(self):
		#print "keyPageDownFast(2)"
		self.keyPageDownFast(2)

	def key_4(self):
		#print "keyPageDownFast(5)"
		self.keyPageDownFast(5)

	def key_7(self):
		#print "keyPageDownFast(10)"
		self.keyPageDownFast(10)

	def key_3(self):
		#print "keyPageUpFast(2)"
		self.keyPageUpFast(2)

	def key_6(self):
		#print "keyPageUpFast(5)"
		self.keyPageUpFast(5)

	def key_9(self):
		#print "keyPageUpFast(10)"
		self.keyPageUpFast(10)

	def keyTxtPageUp(self):
		self['handlung'].pageUp()

	def keyTxtPageDown(self):
		self['handlung'].pageDown()

	def keyTMDbInfo(self):
		if not self.keyLocked and TMDbPresent:
			title = self['liste'].getCurrent()[0][0]
			self.session.open(TMDbMain, title)
		elif not self.keyLocked and IMDbPresent:
			title = self['liste'].getCurrent()[0][0]
			self.session.open(IMDB, title)

	def keyYellow(self):
		if not (self.keyLocked or self.genreSpecials):
			self.keyLocked = True
			mp_globals.ddlme_sortOrder += 1
			if mp_globals.ddlme_sortOrder > 3:
				mp_globals.ddlme_sortOrder = 0
			self.setGenreStrTitle()
			self.loadPage()

	def keyCancel(self):
		self.close()

def DDLMEStreamListEntry2(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]),
		(eListboxPythonMultiContent.TYPE_TEXT, 220, 0, 200, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[2]),
		(eListboxPythonMultiContent.TYPE_TEXT, 440, 0, 440, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[3])
		]

def DDLMEStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0] + entry[2])
		]

class DDLMEStreams(Screen, ConfigListScreen):

	def __init__(self, session, filmUrl, filmName, imageLink):
		self.session = session
		self.filmUrl = filmUrl
		self.filmName = filmName
		self.imageUrl = imageLink

		self.plugin_path = mp_globals.pluginPath
		self.skin_path =  mp_globals.pluginPath + "/skins"

		path = "%s/%s/defaultListScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/defaultListScreen.xml"

		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"red" 		: self.keyTxtPageUp,
			"blue" 		: self.keyTxtPageDown,
			"green" 	: self.keyTrailer,
			"ok"    	: self.keyOK,
			"cancel"	: self.keyCancel
		}, -1)

		self['title'] = Label(DDLME_Version)
		self['ContentTitle'] = Label("Stream Auswahl")
		self['coverArt'] = Pixmap()
		self['handlung'] = ScrollLabel("")
		self['name'] = Label(filmName)
		self['Page'] = Label("")
		self['page'] = Label("")
		self['F1'] = Label("Text-")
		self['F2'] = Label("")
		self['F3'] = Label("")
		self['F4'] = Label("Text+")

		self.trailerId = None
		self.streamListe = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('mediaportal', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['liste'] = self.streamMenuList
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)

	def loadPage(self):
		print "loadPage:"
		streamUrl = self.filmUrl
		#print "FilmUrl: %s" % self.filmUrl
		#print "FilmName: %s" % self.filmName
		getPage(streamUrl, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)

	def parseData(self, data):
		print "parseData:"
		mdesc = re.search('class=\'detailCover\'.*?jpg\'.*?> (.*?)<br><br>', data, re.S)
		if mdesc:
			#print "Descr. found"
			desc = mdesc.group(1).strip()
			desc = decodeHtml(desc)
		else:
			desc = "Keine weiteren Info's !"

		m = re.search('http://www.youtube.com/watch\?v=(.*?)\'', data)
		if m:
			self.trailerId = m.group(1)
			self['F2'].setText('Trailer')

		self.streamListe = []
		info = re.search('var subcats =.*?"info":', data)
		if info:
			#print "s-streams"
			a = info.start()
			l = len(data)
			epi = re.search('S(\d{2})E(\d{3})', self.filmName)
			if epi:
				st = int(epi.group(1))
				ep = int(epi.group(2))
				#print "st: ",st
				#print "ep: ",ep
				while a<l:
					info = re.search('"info":.*?"nr":"(\d+)".*?"staffel":"(\d+)".*?links":{(.*?)}}', data[a:])
					if info:
						#print "s-info found"
						a += info.end()
						st_ = int(info.group(2))
						ep_ = int(info.group(1))
						#print "st_: ",st_
						#print "ep_: ",ep_
						if st == st_ and ep == ep_:
							#print "episode found"
							a2=0
							l2=len(info.group(3))
							while a2<l2:
								mg = re.search('"(.*?)":\[(\[.*?\])\]', info.group(3)[a2:])
								if mg:
									#print "hoster found"
									a2 += mg.end()
									streams = re.findall('"(http:.*?)".*?"stream"\]', mg.group(2))

									if streams:
										#print "Streams found"
										s = mg.group(1)
										if re.search('(played|putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Click.*?Play|BitShare)', s, re.I):
											#print s

											for h in streams:
												url = h.replace('\\', '')
												#print url
												self.streamListe.append((s,url,'',''))
										else:
											print "No supported hoster:",s
								else:
									a2 = l2
							a = l
					else:
						a = l

			if len(self.streamListe) == 0:
				self.streamListe.append(("No streams found!","","",""))

			self.streamMenuList.setList(map(DDLMEStreamListEntry, self.streamListe))
		else:
			print "norm. streams"
			np = re.search('var subcats =', data)
			if np:
				k = np.end()
				kl = len(data)
			else:
				k = kl = 0

			while k < kl:
				np = re.search('{"0":"(.*?)","1":"(\d)"', data[k:])
				if np:
					k += np.end()
					print "np found"
					kap = np.group(1)
					n = int(np.group(2))
				else:
					k = kl
					continue

				ls = re.search('"links":{(.*?)}}', data)
				if ls:
					print "links found"
					links = ls.group(1)
					l=len(links)
				else:
					continue

				a=0
				while a<l:
					mg = re.search('"(.*?)":\[(\[.*?\])\]', links[a:])
					if mg:
						print "hoster found"
						a += mg.end()

						streams = re.findall('\["(.*?)".*?"(http:.*?)".*?"stream"\]', mg.group(2))

						if streams:
							print "Streams found"
							s = mg.group(1)
							if re.search('(played|putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx|Divxmov|Putme|Click.*?Play|BitShare)', s, re.I):
								#print s
								part = ''
								for (p,h) in streams:
									url = h.replace('\\', '')
									if n > 1:
										part = "Part " + p
									else:
										part = "One Part"

									#if re.match('apitel (\d)',kap):
									#	kap = self._insert(kap, 'K', 0)

									#print url
									#print part
									self.streamListe.append((s,url,part,kap))
							else:
								print "No supported hoster:",s
					else:
						a = l

			if len(self.streamListe) == 0:
				self.streamListe.append(("No streams found!","","",""))

			self.streamMenuList.setList(map(DDLMEStreamListEntry2, self.streamListe))

		self['handlung'].setText(decodeHtml(desc))
		self.keyLocked = False
		print "imageUrl: ",self.imageUrl
		CoverHelper(self['coverArt']).getCover(self.imageUrl)

	def _insert(self, ori, ins, pos):
		return ori[:pos] + ins + ori[pos:]

	def dataError(self, error):
		print "dataError:"
		printl(error,self,"E")
		self.streamListe.append(("Read error !","","",""))
		self.streamMenuList.setList(map(DDLMEStreamListEntry, self.streamListe))

	def got_link(self, stream_url):
		print "got_link:"
		if stream_url == None:
			message = self.session.open(MessageBox, _("Stream not found, try another Stream Hoster."), MessageBox.TYPE_INFO, timeout=3)
		else:
			if not re.match('One', self['liste'].getCurrent()[0][2]):
				title = self.filmName + ' - ' + self['liste'].getCurrent()[0][2]
			else:
				title = self.filmName

			if config.mediaportal.useHttpDump.value:
				movieinfo = [stream_url,self.filmName,""]
				self.session.open(PlayHttpMovie, movieinfo, title)
			else:
				self.session.open(SimplePlayer, [(title, stream_url, self.imageUrl)], showPlaylist=False, ltype='ddl.me', cover=True)

	def keyTrailer(self):
		if self.trailerId:
			self.session.open(
				YoutubePlayer,
				[(self.filmName, '', self.trailerId, self.imageUrl)],
				playAll = False,
				showPlaylist=False,
				showCover=True
				)

	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['liste'].getCurrent()[0][1]
		print "get_streamLink:"
		get_stream_link(self.session).check_link(streamLink, self.got_link)

	def keyTxtPageUp(self):
		self['handlung'].pageUp()

	def keyTxtPageDown(self):
		self['handlung'].pageDown()

	def keyCancel(self):
		self.close()
