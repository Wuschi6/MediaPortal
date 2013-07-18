from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.decrypt import *

def oaseGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class oaseGenreScreen(Screen):
	
	def __init__(self, session):
		self.session = session
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/oaseGenreScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/oaseGenreScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		
		self['title'] = Label("Konzert Oase")
		self['name'] = Label("Genre Auswahl")
		self['coverArt'] = Pixmap()
		
		self.genreliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['genreList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		self.genreliste.append(("Neuesten", "http://konzertoase.cixx6.com/"))
		self.genreliste.append(("Electro", "http://konzertoase.cixx6.com/category/electro/"))
		self.genreliste.append(("Folk", "http://konzertoase.cixx6.com/category/folk/"))
		self.genreliste.append(("Heavy Metal", "http://konzertoase.cixx6.com/category/heavy-metal/"))
		self.genreliste.append(("HipHip Black", "http://konzertoase.cixx6.com/category/hip-hopblack/"))
		self.genreliste.append(("International", "http://konzertoase.cixx6.com/category/international/"))
		self.genreliste.append(("Musical", "http://konzertoase.cixx6.com/category/musical/"))
		self.genreliste.append(("Musikfilme", "http://konzertoase.cixx6.com/category/musikfilme/"))
		self.genreliste.append(("Pop", "http://konzertoase.cixx6.com/category/pop/"))
		self.genreliste.append(("RnB Soul", "http://konzertoase.cixx6.com/category/rbsoul/"))
		self.genreliste.append(("Reggae", "http://konzertoase.cixx6.com/category/reggae/"))
		self.genreliste.append(("Rock", "http://konzertoase.cixx6.com/category/rock/"))
		self.genreliste.append(("Schlager", "http://konzertoase.cixx6.com/category/schlager/"))
		self.genreliste.append(("Singer Songwriter", "http://konzertoase.cixx6.com/category/singersongwriter/"))
		self.genreliste.append(("Sonstige", "http://konzertoase.cixx6.com/category/sonstige/"))
		self.genreliste.append(("Techno", "http://konzertoase.cixx6.com/category/techno/"))
		self.genreliste.append(("Unplugged", "http://konzertoase.cixx6.com/category/unplugged/"))
		self.chooseMenuList.setList(map(oaseGenreListEntry, self.genreliste))

	def keyOK(self):
		streamGenreLink = self['genreList'].getCurrent()[0][1]
		print streamGenreLink
		self.session.open(oaseFilmListeScreen, streamGenreLink)

	def keyCancel(self):
		self.close()

def oaseFilmListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		] 
class oaseFilmListeScreen(Screen):
	
	def __init__(self, session, streamGenreLink):
		self.session = session
		self.streamGenreLink = streamGenreLink
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/oaseFilmListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/oaseFilmListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)

		self['title'] = Label("Konzert Oase")
		self['name'] = Label("Film Auswahl")
		self['handlung'] = Label("")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = True
		self.filmliste = []
		self.keckse = {}
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		print "check", self.streamGenreLink, "ok"
		getPage(self.streamGenreLink, agent=std_headers).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		printl(error,self,"E")
		
	def loadPageData(self, data):
		print "daten bekommen"
		streamFilme = re.findall('<a href="(http://konzertoase.cixx6.com/.*?)" title="(.*?)"><img src="(.*?)"', data)
		if streamFilme:
			for streamLink,streamName,streamPic in streamFilme:
				#print streamLink,streamName,streamPic
				self.filmliste.append((decodeHtml(streamName), streamLink, streamPic))
			self.chooseMenuList.setList(map(oaseFilmListEntry, self.filmliste))
			self.keyLocked = False
			self.loadPic()

	def loadPic(self):
		streamName = self['filmList'].getCurrent()[0][0]
		streamFilmLink = self['filmList'].getCurrent()[0][1]
		self['name'].setText(streamName)
		streamPic = self['filmList'].getCurrent()[0][2]
		downloadPage(streamPic, "/tmp/spIcon.jpg").addCallback(self.ShowCover)
		#print streamPic
		#print streamFilmLink
		getPage(streamFilmLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageInfos).addErrback(self.dataError)
		
	def loadPageInfos(self, data):
		if re.match('.*?Genre :', data, re.S):
			handlung = re.findall('<div class="embed">.*?Genre :.*?<p>(.*?)</p>', data, re.S)
			if handlung:
				print handlung
				self['handlung'].setText(decodeHtml(handlung[0]))
			else:
				self['handlung'].setText("keine infos")
		else:
			#handlung = re.findall('<div class="embed">.*?</div>.*?<p>(.*?)</p>', data, re.S)
			#if handlung:
			#	print handlung
			#	self['handlung'].setText(decodeHtml(handlung[0]))
			self['handlung'].setText("keine infos")
	
	def ShowCover(self, picData):
		if fileExists("/tmp/spIcon.jpg"):
			self['coverArt'].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['coverArt'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/spIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['coverArt'].instance.setPixmap(ptr)
					self['coverArt'].show()
					del self.picload
					
	def keyOK(self):
		if self.keyLocked:
			return
		streamLink = self['filmList'].getCurrent()[0][1]
		print streamLink
		getPage(streamLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.findStreamcloud).addErrback(self.dataError)
		#data = urllib.urlopen(streamLink).read()

	def findStreamcloud(self, data):
		self.streamParts = re.findall('<a title="Streamcloud" href="(http://streamcloud.eu/.*?)"', data)
		if self.streamParts:
			if len(self.streamParts) > 1:
				self.session.open(oaseCDListeScreen, self.streamParts)
			else:
				getPage(self.streamParts[0], cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.readPostData).addErrback(self.dataError)
				
	def readPostData(self, data):
		form_values = {}
		for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', data):
			form_values[i.group(1)] = i.group(2)
				
		form_values = urllib.urlencode(form_values)
		getPage(self.streamParts[0], method='POST', cookies=self.keckse, postdata=form_values.replace('download1','download2'), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.postData).addErrback(self.dataError)

	def postData(self, data):
		streamName = self['filmList'].getCurrent()[0][0]
		streamUrl = re.findall('file: "(.*?)"', data)
		if streamUrl:
			sref = eServiceReference(0x1001, 0, streamUrl[0])
			sref.setName(streamName)
			self.session.open(MoviePlayer, sref)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['filmList'].pageUp()
		self.loadPic()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['filmList'].pageDown()
		self.loadPic()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['filmList'].up()
		self.loadPic()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['filmList'].down()
		self.loadPic()
		
	def keyCancel(self):
		self.close()

def oaseCDListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 900, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry[0])
		] 
class oaseCDListeScreen(Screen):
	
	def __init__(self, session, parts):
		self.session = session
		self.streamParts = parts
		path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/%s/oaseCDListeScreen.xml" % config.mediaportal.skin.value
		if not fileExists(path):
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/original/oaseCDListeScreen.xml"
		print path
		with open(path, "r") as f:
			self.skin = f.read()
			f.close()
			
		Screen.__init__(self, session)
		
		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

		self['title'] = Label("Konzert Oase")
		self['name'] = Label("Part Auswahl")
		self['coverArt'] = Pixmap()
		
		self.keyLocked = False
		self.keckse = {}
		self.filmliste = []
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.chooseMenuList.l.setFont(0, gFont('mediaportal', 23))
		self.chooseMenuList.l.setItemHeight(25)
		self['filmList'] = self.chooseMenuList
		
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		streamPart = 0
		for part in self.streamParts:
			streamPart += 1
			self.filmliste.append(("Part #"+str(streamPart), part))
		self.chooseMenuList.setList(map(oaseCDListEntry, self.filmliste))		
		
	def keyOK(self):
		if self.keyLocked:
			return
		
		self.streamLink = self['filmList'].getCurrent()[0][1]
		self.keyLocked = True
		getPage(self.streamLink, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.readPostData).addErrback(self.dataError)
				
	def readPostData(self, data):
		form_values = {}
		for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', data):
			form_values[i.group(1)] = i.group(2)
				
		form_values = urllib.urlencode(form_values)
		getPage(self.streamLink, method='POST', cookies=self.keckse, postdata=form_values.replace('download1','download2'), headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.postData).addErrback(self.dataError)

	def postData(self, data):
		streamName = self['filmList'].getCurrent()[0][0]
		streamUrl = re.findall('file: "(.*?)"', data)
		if streamUrl:
			sref = eServiceReference(0x1001, 0, streamUrl[0])
			sref.setName(streamName)
			self.session.open(MoviePlayer, sref)
			
		self.keyLocked = False

	def dataError(self, error):
		self.keyLocked = False
		printl(error,self,"E")
		
	def keyCancel(self):
		self.close()
