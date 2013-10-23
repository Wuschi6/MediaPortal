# 	-*-	coding:	utf-8	-*-
from Plugins.Extensions.MediaPortal.resources.imports import *
from Tools.Directories import pathExists
from thread import allocate_lock
#import thread

# teilweise von movie2k geliehen
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

class ShowThumbscreen(Screen):
	
	NO_COVER_PIC_PATH = "/images/no_coverArt.png"

	def __init__(self, session, callbacknewpage=None, filmList=[], filmnamePos=0, filmurlPos=1, filmimageurlPos=2, filmnameaddPos=3, pageregex=None, filmpage=1, filmpages=999):
		self.session = session
		self._callbacknewpage = callbacknewpage
		self._no_picPath = "%s/skins/%s%s" % (mp_globals.pluginPath, config.mediaportal.skin.value, self.NO_COVER_PIC_PATH)

		# groesse der Thumbs definieren
		textsize = 18
		self.spaceX = 8
		self.picX = 200
		self.spaceY = 40
		self.picY = 260
		# Thumbs Geometrie, groesse und Anzahl berechnen
		size_w = getDesktop(0).size().width()
		size_h = getDesktop(0).size().height()
		self.thumbsX = size_w / (self.spaceX + self.picX)  # thumbnails in X
		self.thumbsY = size_h / (self.spaceY + self.picY)  # thumbnails in Y
		self.thumbsC = self.thumbsX * self.thumbsY  # all thumbnails
			
		# Skin XML der Thumbs erstellen 
		self.positionlist = []
		skincontent = ""
		posX = -1
		for x in range(self.thumbsC):
			posY = x / self.thumbsX
			posX += 1
			if posX >= self.thumbsX:
				posX = 0
			absX = self.spaceX + (posX * (self.spaceX + self.picX))
			absY = self.spaceY + (posY * (self.spaceY + self.picY))
			self.positionlist.append((absX, absY))  # Postition der Thumbs speichern um spaeter das Movingimage darzustellen
			skincontent += "<widget source=\"label" + str(x) + "\" render=\"Label\" position=\"" + str(absX + 2) + "," + str(absY + self.picY - 2) + "\" size=\"" + str(self.picX - 2) + "," + str(textsize * 2) + "\" font=\"mediaportal;16\" zPosition=\"3\" transparent=\"1\" valign=\"top\" halign=\"center\" foregroundColor=\"" + "#00ffffff" + "\" />"
			skincontent += "<widget name=\"thumb" + str(x) + "\" position=\"" + str(absX + 5) + "," + str(absY + 5) + "\" size=\"" + str(self.picX - 10) + "," + str(self.picY - 10) + "\" zPosition=\"2\" transparent=\"1\" alphatest=\"blend\" />"

		# Load Bottons Skin XML
		self.skin_path = mp_globals.pluginPath + "/skins"
		path = "%s/%s/ThumbsScreen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/ThumbsScreen.xml"
		print path
		with open(path, "r") as f:
			skinmain = f.read()
			f.close()
					
		# Skin komlett aufbauen 
		self.skin_dump = skinmain
		self.skin_dump += "<widget name=\"frame\" position=\"" + str(absX + 5) + "," + str(absY + 5) + "\" size=\"" + str(self.picX) + "," + str(self.picY) + "\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/pic_frame.png\" zPosition=\"1\" transparent=\"0\" alphatest=\"blend\" />"
		self.skin_dump += skincontent
		self.skin_dump += "</screen>"
		self.skin = self.skin_dump
			
		Screen.__init__(self, session)
		
		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"cancel": self.keyCancel,
			"ok": self.keyOK,
			"left": self.key_left,
			"right": self.key_right,
			"up": self.key_up,
			"down": self.key_down,
			"green" : self.keyPageNumber,
			"info" :  self.keyTMDbInfo
		}, -1)

		# Skin Variablen zuweisen	
		self['F1'] = Label("Exit")
		self['F2'] = Label("Page ?")
		self['F3'] = Label("")
		self['F4'] = Label("")
		#self['F1'].hide()
		#self['F2'].hide()
		self['F3'].hide()
		self['F4'].hide()
		self['Page'] = Label("Page:")
		self['page'] = Label("1/X")
		self['Thumb'] = Label("Load:")
		self['thumb'] = Label("1/X")			

		self["frame"] = MovingPixmap()
		for x in range(self.thumbsC):
			self["label" + str(x)] = StaticText()
			self["thumb" + str(x)] = Pixmap()

		self.keyLocked = True
		self.onLayoutFinish.append(self.dir)
		self.makeThumb(filmList, filmnamePos, filmurlPos, filmimageurlPos, filmnameaddPos, pageregex, filmpage, filmpages)
		self.keyLocked = False

	def makeThumb(self, filmList, filmnamePos, filmurlPos, filmimageurlPos=None, filmnameaddPos=None, pageregex=None, filmpage=1, filmpages=999):
		self.filmList = filmList
		self.thumbfilmliste = []
		self.filmpage = filmpage
		if filmpages == 0:
			self.filmpages = 999
		else:
			self.filmpages = filmpages	
		thumbsFilmname = []
		for item in filmList:
			if not filmnameaddPos:
				thumbsFilmname = item[filmnamePos]
			else:
				thumbsFilmname = item[filmnamePos]+" "+item[filmnameaddPos].replace(' ','')
			if filmimageurlPos:
				self.thumbfilmliste.append((thumbsFilmname, item[filmurlPos], item[filmimageurlPos],pageregex),)
			else:
				self.thumbfilmliste.append((thumbsFilmname, item[filmurlPos], item[filmurlPos], pageregex),)
		
		index = 0
		framePos = 0
		Page = 0
		self.filelist = []
		for x in self.thumbfilmliste:
				self.filelist.append((index, framePos))
				index += 1
				framePos += 1
				if framePos > (self.thumbsC - 1):
					framePos = 0
					Page += 1
		self.maxentry = len(self.filelist) - 1
		self.page = 0
		self.index = 0
		self.layoutThumBFinished()
		self.paintFrame()

	def keyOK(self):
		if self.keyLocked:
			return
		filmnummer = self.page * self.thumbsC + self.index
		self._callbacknewpage(filmnummer=filmnummer, listmove=None, thumbcallback=self.makeThumb)
		
	def keyCancel(self):
		self.close(None, -9, None)

	def keyPageNumber(self):
		self.session.openWithCallback(self.callbackkeyPageNumber, VirtualKeyBoard, title = (_("Seitennummer eingeben")), text = "")

	def callbackkeyPageNumber(self, answer):
		if (answer is not None) and (answer.isdigit()):
			self._callbacknewpage(filmnummer = None, listmove=int(answer)-1, thumbcallback=self.makeThumb)

	def key_left(self):
		self.index -= 1
		if self.index < 0:
			self.page -= 1
			if self.page < 0:
				if self.filmpages == 1:
					self.page = int(self.maxentry / self.thumbsC)
					self.index = self.maxentry - self.page * self.thumbsC
					self.layoutThumBFinished()
				else:
					if self.filmpage == 1:
						if not self.filmpages == 999:
							self._callbacknewpage(filmnummer = None, listmove=self.filmpages-1, thumbcallback=self.makeThumb)
						else:
							self.index += 1
							self.page += 1
					else:
						self._callbacknewpage(filmnummer = None, listmove=self.filmpage-2, thumbcallback=self.makeThumb)
			else:
				self.index = self.thumbsC -1
				self.layoutThumBFinished()
		self.paintFrame()

	def key_right(self):
		self.index += 1
		if self.page * self.thumbsC + self.index > self.maxentry:
			if self.filmpage == self.filmpages:
				if self.filmpages > 1:
					self._callbacknewpage(filmnummer = None, listmove=0, thumbcallback=self.makeThumb)
				else:
					self.page = 0
					self.layoutThumBFinished()
					self.index = 0						
			else:
				self._callbacknewpage(filmnummer = None, listmove=self.filmpage, thumbcallback=self.makeThumb)
		elif self.index > self.thumbsC - 1:
			self.page += 1
			self.layoutThumBFinished()
			self.index = 0
		if self.index >= self.thumbsC:
			self.index = 0
		self.paintFrame()

	def key_up(self):
		self.index -= self.thumbsX
		if self.index < 0:
			if self.page > 0:
				self.page -= 1
				self.index = 0
				self.layoutThumBFinished()
			elif self.filmpage == 1:
				if self.filmpages > 1:
					if not self.filmpages == 999:
						self._callbacknewpage(filmnummer=None, listmove=self.filmpages-1, thumbcallback=self.makeThumb)
					else:
						self.index += self.thumbsX
				else:
					self.page = int(self.maxentry / self.thumbsC)
					self.index = 0
					self.layoutThumBFinished()
			else:
				self._callbacknewpage(filmnummer=None, listmove=self.filmpage-2, thumbcallback=self.makeThumb)
		self.paintFrame()

	def key_down(self):
		self.index += self.thumbsX
		if self.page * self.thumbsC + self.index > self.maxentry:
			if self.filmpage == self.filmpages:
				if self.filmpage > 1:
					self._callbacknewpage(filmnummer = None, listmove=0, thumbcallback=self.makeThumb)
				else:
					self.page = 0
					self.layoutThumBFinished()
					self.index = 0						
			else:
				self._callbacknewpage(filmnummer = None, listmove=self.filmpage, thumbcallback=self.makeThumb)
		elif self.index > self.thumbsC - 1:
			self.page += 1
			self.index = 0
			self.layoutThumBFinished()
		self.paintFrame()
		
	def keyTMDbInfo(self):
		if not self.keyLocked and TMDbPresent:
			title = self.thumbfilmliste[self.page * self.thumbsC + self.index][0]
			self.session.open(TMDbMain, title)
		elif not self.keyLocked and IMDbPresent:
			title = self.thumbfilmliste[self.page * self.thumbsC + self.index][0]
			self.session.open(IMDB, title)		
	
	def paintFrame(self):
		if self.maxentry < self.index or self.index < 0:
			return
		pos = self.positionlist[self.filelist[self.index][1]]
		self["frame"].moveTo(pos[0], pos[1], 1)
		self["frame"].startMoving()
		if self.page * self.thumbsC + self.thumbsC  > self.maxentry+1:
			pagerangend = self.maxentry+1
		else:
			pagerangend = self.page * self.thumbsC + self.thumbsC	
		if self.filmpages == 999:
			showfilmpages = "?"
		else:
			showfilmpages = self.filmpages
		if self.page:
			self['page'].setText("%d von %d  |  Index: %d von %s  |  Film: %d bis %d von %d" % (self.page + 1 , int(self.maxentry / self.thumbsC) + 1, self.filmpage, showfilmpages, self.page * self.thumbsC +1, pagerangend , self.maxentry+1))
		else:
			self['page'].setText("%d von %d  |  Index: %d von %s  |  Film: %d bis %d von %d" % (1 , int(self.maxentry / self.thumbsC) + 1, self.filmpage, showfilmpages, self.page * self.thumbsC +1, pagerangend , self.maxentry+1))
	
	def dir(self):
		baseDir = "/tmp"
		logDir = baseDir + "/mediaportal"
		coverDir = baseDir + "/mediaportal/cover"

		try:
			os.makedirs(baseDir)
		except OSError, e:
			pass
	
		try:
			os.makedirs(logDir)
		except OSError, e:
			pass

		try:
			os.makedirs(coverDir)
		except OSError, e:
			pass
	
	def layoutThumBFinished(self):
		self.count = len(self.thumbfilmliste)
		self.url_list = []	
		self.filmnummer = 0
		for each in range(self.page * self.thumbsC, self.page * self.thumbsC + self.thumbsC):
			try:
				title, filmlink, jpglink, imageregex = self.thumbfilmliste[each]
				jpg_store = '/tmp/mediaportal/cover/%s.jpg' % str(self.filmnummer)
				self.filmnummer += 1
				self.url_list.append((title,jpg_store,filmlink,jpglink,imageregex))
			except IndexError:
				print "ENDE der Liste"
		self.showCoversLine()
		
	def showCoversLine(self):
		self.lock = allocate_lock()
		self.loadnumcounter = 0
		ds = defer.DeferredSemaphore(tokens=12)
		if len(self.url_list) != 0:
			nr = 0
			downloads = []
			for x in range(nr,self.thumbsC):
				self["label" + str(x)].setText("")
				self["thumb" + str(x)].hide()
			for x in self.url_list:
				if not self.url_list[nr][4]:
					#print "[MediaPortal] ohne linkparser"
					listhelper = ds.run(self.download, self.url_list[nr][3], self.url_list[nr][1]).addCallback(self.ShowCoverFile, self.url_list[nr][0], self.url_list[nr][1], self.url_list[nr][2], self.url_list[nr][3], nr).addErrback(self.dataError, self.url_list[nr][0], nr)
				else:
					#print "[MediaPortal] mit linkparser"
					listhelper = ds.run(getPage, self.url_list[nr][3], headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseUrldata, self.url_list[nr][4], self.url_list[nr][3]).addCallback(self.download, self.url_list[nr][1]).addCallback(self.ShowCoverFile, self.url_list[nr][0], self.url_list[nr][1], self.url_list[nr][2], self.url_list[nr][3], nr).addErrback(self.dataError, self.url_list[nr][0], nr)
				downloads.append(listhelper)
				nr += 1

	def parseUrldata(self, data, imageregex, url):
		filmimagelink = re.findall(imageregex, data, re.S)
		if re.match('http;//', filmimagelink[0]):
			return filmimagelink[0]
		else:
			path = re.findall('(http://.*?)/',url)
			filmimage = "%s%s" % (path[0], filmimagelink[0]) 
			return filmimage
		
	def ShowCoverFile(self, data, title, picPath, filmlink, jpglink, nr):
		if data == 'no_cover':
			picPath = self._no_picPath
		self['label' + str(nr)].setText(title)
		if fileExists(picPath):
			self['thumb' + str(nr)].instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['thumb' + str(nr)].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode(picPath, 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['thumb' + str(nr)].instance.setPixmap(ptr)
					self['thumb' + str(nr)].show()
					del self.picload
					self.lock.acquire()
					self.loadnumcounter += 1
					self.lock.release() 
					self['thumb'].setText("%d / %d" % (self.loadnumcounter , self.filmnummer))
																				
	def download(self, image, jpg_store):
		if image == '':
			return ('no_cover')
		else:
			return downloadPage(image, jpg_store)

	def dataError(self, error, title, nr):
		self.lock.acquire()
		self.loadnumcounter += 1
		self.lock.release() 
		self['thumb'].setText("%d / %d" % (self.loadnumcounter , self.filmnummer))
		self['label' + str(nr)].setText(title)
		print "dataError:"