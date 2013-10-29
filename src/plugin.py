#	-*-	coding:	utf-8	-*-

# General imports
from resources.imports import *
from resources.update import *
from resources.simplelist import *
from resources.simpleplayer import SimplePlaylistIO

try:
	import ast
except:
	print "No 'ast' module"
	astModule = False
else:
	print "Module 'ast' loaded"
	astModule = True

config.mediaportal = ConfigSubsection()

# Fake entry fuer die Kategorien
config.mediaportal.fake_entry = NoSave(ConfigNothing())

# Allgemein
config.mediaportal.version = NoSave(ConfigText(default="492"))
config.mediaportal.versiontext = NoSave(ConfigText(default="4.9.2"))
config.mediaportal.autoupdate = ConfigYesNo(default = True)
config.mediaportal.pincode = ConfigPIN(default = 0000)
config.mediaportal.showporn = ConfigYesNo(default = False)
config.mediaportal.showgrauzone = ConfigYesNo(default = False)
config.mediaportal.pingrauzone = ConfigYesNo(default = False)

skins = []
for skin in os.listdir("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/"):
	if os.path.isdir(os.path.join("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/", skin)) and skin != "simpleplayer":
		skins.append(skin)
config.mediaportal.skin = ConfigSelection(default = "tec", choices = skins)

config.mediaportal.ansicht = ConfigSelection(default = "wall", choices = [("liste", _("Liste")),("wall", _("Wall"))])
config.mediaportal.selektor = ConfigSelection(default = "blue", choices = [("blue", _("blau")),("green", _(u"gr\xfcn")),("red", _("rot")),("turkis", _(u"t\xfcrkis"))])
config.mediaportal.useRtmpDump = ConfigYesNo(default = False)
config.mediaportal.useHttpDump = ConfigYesNo(default = False)
config.mediaportal.storagepath = ConfigText(default="/media/hdd/mediaportal/tmp/", fixed_size=False)
config.mediaportal.autoplayThreshold = ConfigInteger(default = 50, limits = (1,100))
config.mediaportal.filter = ConfigSelection(default = "ALL", choices = [("ALL", ("ALL")), ("Mediathek", ("Mediathek")), ("Grauzone", ("Grauzone")), ("Fun", ("Fun")), ("Sport", ("Sport")), ("Music", ("Music")), ("Porn", ("Porn"))])
config.mediaportal.youtubeprio = ConfigSelection(default = "1", choices = [("0", _("Low")),("1", _("Medium")),("2", _("High"))])
config.mediaportal.videoquali_others = ConfigSelection(default = "1", choices = [("0", _("Low")),("1", _("Medium")),("2", _("High"))])
config.mediaportal.pornpin = ConfigYesNo(default = True)
config.mediaportal.setuppin = ConfigYesNo(default = False)
config.mediaportal.watchlistpath = ConfigText(default="/etc/enigma2/", fixed_size=False)
config.mediaportal.sortplugins = ConfigSelection(default = "abc", choices = [("hits", _("Hits")), ("abc", _("ABC")), ("user", _("User"))])
config.mediaportal.pagestyle = ConfigSelection(default="Graphic", choices = ["Graphic", "Text"])
config.mediaportal.laola1locale = ConfigText(default="de", fixed_size=False)
config.mediaportal.debugMode = ConfigSelection(default="Silent", choices = ["High", "Normal", "Silent", ])
config.mediaportal.font = ConfigSelection(default = "1", choices = [("1", _("Mediaportal 1")),("2", _("Mediaportal 2"))])
config.mediaportal.restorelastservice = ConfigSelection(default = "1", choices = [("1", _("after SimplePlayer quits")),("2", _("after MediaPortal quits"))])
config.mediaportal.filterselector = ConfigYesNo(default = True)

# Konfiguration erfolgt in SimplePlayer
config.mediaportal.sp_randomplay = ConfigYesNo(default = False)
config.mediaportal.sp_scrsaver = ConfigSelection(default = "off", choices = [("on", _("On")),("off", _("Off")),("automatic", _("Automatic"))])
config.mediaportal.sp_on_movie_stop = ConfigSelection(default = "ask", choices = [("ask", _("Ask user")), ("quit", _("Return to previous service"))])
config.mediaportal.sp_on_movie_eof = ConfigSelection(default = "ask", choices = [("ask", _("Ask user")), ("quit", _("Return to previous service")), ("pause", _("Pause movie at end"))])
config.mediaportal.sp_seekbar_sensibility = ConfigInteger(default = 10, limits = (1,50))
config.mediaportal.sp_infobar_cover_off = ConfigYesNo(default = False)
config.mediaportal.sp_show_errors = ConfigYesNo(default = False)
config.mediaportal.sp_use_number_seek = ConfigYesNo(default = True)
config.mediaportal.sp_pl_number = ConfigInteger(default = 1, limits = (1,99))
config.mediaportal.sp_mi_key = ConfigSelection(default = "info", choices = [("info", _("EPG/INFO")),("displayHelp", _("HELP")),("showMovies", _("PVR/VIDEO"))])

# Multihoster premiumize.me
config.mediaportal.premiumize_use = ConfigYesNo(default = False)
config.mediaportal.premiumize_username = ConfigText(default="user!", fixed_size=False)
config.mediaportal.premiumize_password = ConfigText(default="pass!", fixed_size=False)

# Southpark Language
config.mediaportal.southparklang = ConfigText(default="de", fixed_size=False)
config.mediaportal.southparkquality = ConfigText(default="SD", fixed_size=False)

# Sport
#from additions.sport.ran import *
#config.mediaportal.showRan = ConfigYesNo(default = True)
from additions.sport.nhl import *
config.mediaportal.showNhl = ConfigYesNo(default = True)
from additions.sport.spox import *
config.mediaportal.showSpobox = ConfigYesNo(default = True)
from additions.sport.sport1fm import *
config.mediaportal.showsport1fm = ConfigYesNo(default = True)
from additions.sport.laola import *
config.mediaportal.showLaola1 = ConfigYesNo(default = True)

# Music
from additions.music.radio import *
config.mediaportal.showRadio = ConfigYesNo(default = True)
from additions.music.songsto import *
config.mediaportal.showSongsto = ConfigYesNo(default = False)
from additions.music.eighties import *
config.mediaportal.showEighties = ConfigYesNo(default = False)
from additions.music.nuna import *
config.mediaportal.showNuna = ConfigYesNo(default = True)
from additions.music.putpattv import *
config.mediaportal.showputpattv = ConfigYesNo(default = True)
from additions.music.canna import *
config.mediaportal.showCanna = ConfigYesNo(default = False)
from additions.music.myvideoTop100 import *
config.mediaportal.showMyvideoTop100 = ConfigYesNo(default = True)
from additions.music.mtvdecharts import *
config.mediaportal.showMTVdeCharts = ConfigYesNo(default = True)
from additions.music.musicchannels import *
config.mediaportal.showMusicChannels = ConfigYesNo(default = True)
from additions.music.musicstreamcc import *
config.mediaportal.showMusicstreamcc = ConfigYesNo(default = False)
from additions.music.deluxemusic import *
config.mediaportal.showDeluxemusic = ConfigYesNo(default = True)
from additions.music.omr import *
config.mediaportal.showomr = ConfigYesNo(default = False)

# Fun
if astModule:
	from additions.fun.heisevideo import *
	config.mediaportal.showHeiseVideo = ConfigYesNo(default = True)
from additions.fun.retrotv import *
config.mediaportal.showretrotv = ConfigYesNo(default = True)
from additions.fun.galileovl import *
config.mediaportal.showgalileovl = ConfigYesNo(default = True)
from additions.fun.forplayers import *
config.mediaportal.show4Players = ConfigYesNo(default = True)
from additions.fun.dokume import *
config.mediaportal.showDoku = ConfigYesNo(default = True)
from additions.fun.roflvideos import *
config.mediaportal.showRofl = ConfigYesNo(default = True)
from additions.fun.focus import *
config.mediaportal.showFocus = ConfigYesNo(default = True)
from additions.fun.filmon import *
config.mediaportal.showFilmOn = ConfigYesNo(default = True)
from additions.fun.failto import *
config.mediaportal.showFail = ConfigYesNo(default = True)
from additions.fun.sportbild import *
config.mediaportal.showSportBild = ConfigYesNo(default = True)
from additions.fun.filmtrailer import *
config.mediaportal.showTrailer = ConfigYesNo(default = True)
from additions.fun.cczwei import *
config.mediaportal.showCczwei = ConfigYesNo(default = True)
from additions.fun.dreamscreencast import *
config.mediaportal.showDsc = ConfigYesNo(default = True)
from additions.fun.autobild import *
config.mediaportal.showAutoBild = ConfigYesNo(default = True)
from additions.fun.mahlzeittv import *
config.mediaportal.showMahlzeitTV = ConfigYesNo(default = True)
from additions.fun.appletrailers import *
config.mediaportal.showappletrailers = ConfigYesNo(default = True)
from additions.fun.dokuh import *
config.mediaportal.showDOKUh = ConfigYesNo(default = True)
from additions.fun.dokuhouse import *
config.mediaportal.showDokuHouse = ConfigYesNo(default = True)
from additions.fun.liveleak import *
config.mediaportal.showLiveLeak = ConfigYesNo(default = True)
from additions.fun.dokustream import *
config.mediaportal.showDokuStream = ConfigYesNo(default = True)
from additions.fun.sciencetv import *
config.mediaportal.showScienceTV = ConfigYesNo(default = True)
from additions.fun.hoerspielhouse import *
config.mediaportal.showHoerspielHouse = ConfigYesNo(default = True)
from additions.fun.gigatv import *
config.mediaportal.showGIGA = ConfigYesNo(default = True)
from additions.fun.auditv import *
config.mediaportal.showaudi = ConfigYesNo(default = True)
from additions.fun.gronkh import *
config.mediaportal.showgronkh = ConfigYesNo(default = True)
from additions.fun.hoerspielchannels import *
config.mediaportal.showHoerspielChannels = ConfigYesNo(default = True)
from additions.fun.carchannels import *
config.mediaportal.showCarChannels = ConfigYesNo(default = True)
from additions.fun.gamechannels import *
config.mediaportal.showGameChannels = ConfigYesNo(default = True)
from additions.fun.fiwitu import *
config.mediaportal.showFiwitu = ConfigYesNo(default = True)
from additions.fun.userchannels import *
config.mediaportal.showUserChannels = ConfigYesNo(default = True)
from additions.fun.youtube import *
config.mediaportal.showYoutube = ConfigYesNo(default = True)
from additions.fun.teledunet import *
config.mediaportal.showTeledunet = ConfigYesNo(default = True)
from additions.fun.geo_de import *
config.mediaportal.showGEOde = ConfigYesNo(default = True)
from additions.fun.wrestlingnetwork import *
config.mediaportal.showWrestlingnetwork = ConfigYesNo(default = True)
from additions.fun.wissen import *
config.mediaportal.wissen = ConfigYesNo(default = True)
from additions.fun.bild import *
config.mediaportal.bildde = ConfigYesNo(default = True)

# Mediatheken
from additions.mediatheken.southpark import *
config.mediaportal.southpark = ConfigYesNo(default = True)
from additions.mediatheken.myvideo import *
config.mediaportal.showMyvideo = ConfigYesNo(default = True)
from additions.mediatheken.netzkino import *
config.mediaportal.showNetzKino = ConfigYesNo(default = True)
from additions.mediatheken.clipfish import *
config.mediaportal.showClipfish = ConfigYesNo(default = True)
from additions.mediatheken.kinderkino import *
config.mediaportal.showKinderKino = ConfigYesNo(default = True)
from additions.mediatheken.tivi import *
config.mediaportal.showtivi = ConfigYesNo(default = True)
from additions.mediatheken.kika import *
config.mediaportal.showkika = ConfigYesNo(default = True)
from additions.mediatheken.myspass import *
config.mediaportal.showmyspass = ConfigYesNo(default = True)
from additions.mediatheken.voxnow import *
config.mediaportal.showVoxnow = ConfigYesNo(default = True)
from additions.mediatheken.rtlnow import *
config.mediaportal.showRTLnow = ConfigYesNo(default = True)
from additions.mediatheken.ntvnow import *
config.mediaportal.showNTVnow = ConfigYesNo(default = True)
from additions.mediatheken.rtlnitronow import *
config.mediaportal.showRTLnitro = ConfigYesNo(default = True)
from additions.mediatheken.rtl2now import *
config.mediaportal.showRTL2now = ConfigYesNo(default = True)
from additions.mediatheken.superrtlnow import *
config.mediaportal.showSUPERRTLnow = ConfigYesNo(default = True)
from additions.mediatheken.zdf import *
config.mediaportal.showZDF = ConfigYesNo(default = True)
from additions.mediatheken.orf import *
config.mediaportal.showORF = ConfigYesNo(default = True)
from additions.mediatheken.srf import *
config.mediaportal.showSRF = ConfigYesNo(default = True)
from additions.mediatheken.ard import *
config.mediaportal.showARD = ConfigYesNo(default = True)
from additions.mediatheken.dreisat import *
config.mediaportal.showDreisat = ConfigYesNo(default = True)
#from additions.mediatheken.arte import *
#config.mediaportal.showArte = ConfigYesNo(default = True)
from additions.mediatheken.wissensthek import *
config.mediaportal.wissensthek = ConfigYesNo(default = True)
from additions.mediatheken.n24 import *
config.mediaportal.n24 = ConfigYesNo(default = True)
from additions.mediatheken.myvideo_tv import *
config.mediaportal.showmyvideoserien = ConfigYesNo(default = True)
config.mediaportal.showbbcserien = ConfigYesNo(default = True)
config.mediaportal.showyfe = ConfigYesNo(default = True)
config.mediaportal.showsonyretro = ConfigYesNo(default = True)
config.mediaportal.showanimetv = ConfigYesNo(default = True)
config.mediaportal.showProSieben = ConfigYesNo(default = True)
config.mediaportal.showProSiebenMAXX = ConfigYesNo(default = True)
config.mediaportal.showSat1 = ConfigYesNo(default = True)
config.mediaportal.showSat1Gold = ConfigYesNo(default = True)
config.mediaportal.showkabeleins = ConfigYesNo(default = True)
config.mediaportal.showsixx = ConfigYesNo(default = True)
config.mediaportal.showyep = ConfigYesNo(default = True)

# Porn
from additions.porn.x4tube import *
config.mediaportal.show4tube = ConfigYesNo(default = False)
from additions.porn.ahme import *
config.mediaportal.showahme = ConfigYesNo(default = False)
from additions.porn.amateurporn import *
config.mediaportal.showamateurporn = ConfigYesNo(default = False)
from additions.porn.beeg import *
config.mediaportal.showbeeg = ConfigYesNo(default = False)
from additions.porn.drtuber import *
config.mediaportal.showdrtuber = ConfigYesNo(default = False)
from additions.porn.elladies import *
config.mediaportal.showelladies = ConfigYesNo(default = False)
from additions.porn.eporner import *
config.mediaportal.showeporner = ConfigYesNo(default = False)
from additions.porn.eroprofile import *
config.mediaportal.showeroprofile = ConfigYesNo(default = False)
from additions.porn.extremetube import *
config.mediaportal.showextremetube = ConfigYesNo(default = False)
from additions.porn.freeomovie import *
config.mediaportal.showfreeomovie = ConfigYesNo(default = False)
from additions.porn.gstreaminxxx import *
config.mediaportal.showgstreaminxxx = ConfigYesNo(default = False)
from additions.porn.hdporn import *
config.mediaportal.showhdporn = ConfigYesNo(default = False)
from additions.porn.megaskanks import *
config.mediaportal.showmegaskanks = ConfigYesNo(default = False)
from additions.porn.paradisehill import *
config.mediaportal.showparadisehill = ConfigYesNo(default = False)
#from additions.porn.playporn import *
#config.mediaportal.showplayporn = ConfigYesNo(default = False)
from additions.porn.pornerbros import *
config.mediaportal.showpornerbros = ConfigYesNo(default = False)
from additions.porn.pornhub import *
config.mediaportal.showPornhub = ConfigYesNo(default = False)
from additions.porn.pornkino import *
config.mediaportal.showpornkino = ConfigYesNo(default = False)
from additions.porn.pornmvz import *
config.mediaportal.showpornmvz = ConfigYesNo(default = False)
from additions.porn.pornostreams import *
config.mediaportal.showpornostreams = ConfigYesNo(default = False)
from additions.porn.pornrabbit import *
config.mediaportal.showpornrabbit = ConfigYesNo(default = False)
from additions.porn.realgfporn import *
config.mediaportal.showrealgfporn = ConfigYesNo(default = False)
from additions.porn.redtube import *
config.mediaportal.showredtube = ConfigYesNo(default = False)
from additions.porn.sexxxhd import *
config.mediaportal.showsexxxhd = ConfigYesNo(default = False)
from additions.porn.sunporno import *
config.mediaportal.showsunporno = ConfigYesNo(default = False)
from additions.porn.tube8 import *
config.mediaportal.showtube8 = ConfigYesNo(default = False)
from additions.porn.updatetube import *
config.mediaportal.showupdatetube = ConfigYesNo(default = False)
config.mediaportal.showthenewporn = ConfigYesNo(default = False)
config.mediaportal.showpinkrod = ConfigYesNo(default = False)
config.mediaportal.showhotshame = ConfigYesNo(default = False)
from additions.porn.wetplace import *
config.mediaportal.showwetplace = ConfigYesNo(default = False)
from additions.porn.xhamster import *
config.mediaportal.showXhamster = ConfigYesNo(default = False)
from additions.porn.xxxsave import *
config.mediaportal.showxxxsave = ConfigYesNo(default = False)
from additions.porn.youporn import *
config.mediaportal.showyouporn = ConfigYesNo(default = False)
from additions.porn.amateurslust import *
config.mediaportal.amateurslust = ConfigYesNo(default = False)
from additions.porn.pornoid import *
config.mediaportal.pornoid = ConfigYesNo(default = False)
config.mediaportal.befuck = ConfigYesNo(default = False)
from additions.porn.dachix import *
config.mediaportal.dachix = ConfigYesNo(default = False)
from additions.porn.tubewolf import *
config.mediaportal.tubewolf = ConfigYesNo(default = False)

# Grauzone
from additions.grauzone.evonic import *
config.mediaportal.showevonic = ConfigYesNo(default = False)
from additions.grauzone.streamoase import *
config.mediaportal.showStreamOase = ConfigYesNo(default = False)
from additions.grauzone.kinokiste import *
config.mediaportal.showKinoKiste = ConfigYesNo(default = False)
from additions.grauzone.baskino import *
config.mediaportal.showBaskino = ConfigYesNo(default = False)
from additions.grauzone.kinoxto import *
config.mediaportal.showKinox = ConfigYesNo(default = False)
config.mediaportal.showKinoxWatchlist = ConfigYesNo(default = False)
from additions.grauzone.movie4k import *
config.mediaportal.showM4k = ConfigYesNo(default = False)
config.mediaportal.showM4kWatchlist = ConfigYesNo(default = False)
config.mediaportal.showM4kPorn = ConfigYesNo(default = False)
from additions.grauzone.streamit import *
config.mediaportal.showstreamit = ConfigYesNo(default = False)
config.mediaportal.showstreamitPorn = ConfigYesNo(default = False)
from additions.grauzone.watchseries import *
config.mediaportal.showWatchseries = ConfigYesNo(default = False)
from additions.grauzone.szenestreams import *
config.mediaportal.showSzeneStreams = ConfigYesNo(default = False)
from additions.grauzone.vibeo import *
config.mediaportal.showVibeo = ConfigYesNo(default = False)
from additions.grauzone.burningseries import *
config.mediaportal.showBs = ConfigYesNo(default = False)
from additions.grauzone.primewire import *
config.mediaportal.showprimewire = ConfigYesNo(default = False)
from additions.grauzone.mlehd import *
config.mediaportal.showmlehd = ConfigYesNo(default = False)
from additions.grauzone.ddl_me import *
config.mediaportal.showDdlme = ConfigYesNo(default = False)
from additions.grauzone.movie25 import *
config.mediaportal.showMovie25 = ConfigYesNo(default = False)
from additions.grauzone.movie2k import *
config.mediaportal.movie2k = ConfigYesNo(default = False)
from additions.grauzone.serienbz import *
config.mediaportal.serienbz = ConfigYesNo(default = False)
from additions.grauzone.topimdb import *
config.mediaportal.topimdb = ConfigYesNo(default = False)

class CheckPathes:
	def __init__(self, session):
		self.session = session
		self.cb = None

	def checkPathes(self, cb):
		self.cb = cb
		res, msg = SimplePlaylistIO.checkPath(config.mediaportal.watchlistpath.value, '', True)
		if not res:
			self.session.openWithCallback(self._callback, MessageBox, msg, MessageBox.TYPE_ERROR)

		if config.mediaportal.useRtmpDump.value or config.mediaportal.useHttpDump.value:
			res, msg = SimplePlaylistIO.checkPath(config.mediaportal.storagepath.value, '', True)
			if not res:
				self.session.openWithCallback(self._callback, MessageBox, msg, MessageBox.TYPE_ERROR)

	def _callback(self, answer):
		if self.cb:
			self.cb()

class hauptScreenSetup(Screen, ConfigListScreen):

	def __init__(self, session):
		self.session = session

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/hauptScreenSetup.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/hauptScreenSetup.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self.configlist = []
		self.sport = []
		self.music = []
		self.fun = []
		self.mediatheken = []
		self.porn = []
		self.grauzone = []
		ConfigListScreen.__init__(self, self.configlist)

		skins = []
		for skin in os.listdir("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/"):
			if os.path.isdir(os.path.join("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/", skin)) and skin != "simpleplayer":
				skins.append(skin)
		config.mediaportal.skin.setChoices(skins)

		### Allgemein
		self.configlist.append(getConfigListEntry("----- Allgemein -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Automatic Update Check:", config.mediaportal.autoupdate))
		self.configlist.append(getConfigListEntry("Hauptansicht Style:", config.mediaportal.ansicht))
		self.configlist.append(getConfigListEntry("Filtermenü aktivieren:", config.mediaportal.filterselector))
		self.configlist.append(getConfigListEntry("Wall-Selektor-Farbe:", config.mediaportal.selektor))
		self.configlist.append(getConfigListEntry("Page Display Style:", config.mediaportal.pagestyle))
		self.configlist.append(getConfigListEntry("Skin:", config.mediaportal.skin))
		self.configlist.append(getConfigListEntry("Skin-Schriftart:", config.mediaportal.font))
		self.configlist.append(getConfigListEntry("Restore last service:", config.mediaportal.restorelastservice))
		self.configlist.append(getConfigListEntry("----- Jugendschutz -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Pincode:", config.mediaportal.pincode))
		self.configlist.append(getConfigListEntry("Setup-Pincodeabfrage:", config.mediaportal.setuppin))
		self.configlist.append(getConfigListEntry("XXX-Erweiterungen sichtbar:", config.mediaportal.showporn))
		self.configlist.append(getConfigListEntry("XXX-Pincodeabfrage:", config.mediaportal.pornpin))
		self.configlist.append(getConfigListEntry("----- Sonstiges -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("HTTPDump verwenden:", config.mediaportal.useHttpDump))
		self.configlist.append(getConfigListEntry("RTMPDump verwenden:", config.mediaportal.useRtmpDump))
		self.configlist.append(getConfigListEntry("RTMPDump Cachepath:", config.mediaportal.storagepath))
		self.configlist.append(getConfigListEntry("Autoplay Threshold [%]:", config.mediaportal.autoplayThreshold))
		self.configlist.append(getConfigListEntry("Videoqualität (Youtube):", config.mediaportal.youtubeprio))
		self.configlist.append(getConfigListEntry("Videoqualität (andere Anbieter):", config.mediaportal.videoquali_others))
		self.configlist.append(getConfigListEntry("Watchlist/Playlist/Userchan path:", config.mediaportal.watchlistpath))
		self.configlist.append(getConfigListEntry("Grauzone aktivieren:", config.mediaportal.showgrauzone))
		self.configlist.append(getConfigListEntry("----- Multihoster -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Premiumize.me:", config.mediaportal.premiumize_use))
		self.configlist.append(getConfigListEntry("Premiumize.me Username:", config.mediaportal.premiumize_username))
		self.configlist.append(getConfigListEntry("Premiumize.me Password:", config.mediaportal.premiumize_password))

		### Sport
		self.sport.append(getConfigListEntry("NHL", config.mediaportal.showNhl))
		self.sport.append(getConfigListEntry("Spobox", config.mediaportal.showSpobox))
		self.sport.append(getConfigListEntry("Laola1", config.mediaportal.showLaola1))
		self.sport.append(getConfigListEntry("Sport1.fm", config.mediaportal.showsport1fm))
		#self.sport.append(getConfigListEntry("Ran.de", config.mediaportal.showRan))
		self.sport.sort(key=lambda t : t[0].lower())

		### Music
		self.music.append(getConfigListEntry("Deluxemusic", config.mediaportal.showDeluxemusic))
		self.music.append(getConfigListEntry("MTV.de Charts", config.mediaportal.showMTVdeCharts))
		self.music.append(getConfigListEntry("MUSIC-Channels", config.mediaportal.showMusicChannels))
		self.music.append(getConfigListEntry("MyVideo Top 100", config.mediaportal.showMyvideoTop100))
		self.music.append(getConfigListEntry("Nuna", config.mediaportal.showNuna))
		self.music.append(getConfigListEntry("putpat.tv", config.mediaportal.showputpattv))
		if config.mediaportal.showgrauzone.value:
			self.music.append(getConfigListEntry("80s & 90s Music", config.mediaportal.showEighties))
			self.music.append(getConfigListEntry("Canna-Power", config.mediaportal.showCanna))
			self.music.append(getConfigListEntry("Musicstream.cc", config.mediaportal.showMusicstreamcc))
			self.music.append(getConfigListEntry("Songs.to", config.mediaportal.showSongsto))
			self.music.append(getConfigListEntry("OnlineMusicRecorder.com", config.mediaportal.showomr))
		self.music.sort(key=lambda t : t[0].lower())

		### Fun
		self.fun.append(getConfigListEntry("Rofl.to", config.mediaportal.showRofl))
		self.fun.append(getConfigListEntry("Fail.to", config.mediaportal.showFail))
		self.fun.append(getConfigListEntry("LiveLeak", config.mediaportal.showLiveLeak))
		self.fun.append(getConfigListEntry("Radio.de", config.mediaportal.showRadio))
		self.fun.append(getConfigListEntry("FilmOn", config.mediaportal.showFilmOn))
		self.fun.append(getConfigListEntry("Focus", config.mediaportal.showFocus))
		self.fun.append(getConfigListEntry("HörspielHouse", config.mediaportal.showHoerspielHouse))
		self.fun.append(getConfigListEntry("Hörspiel-Channels", config.mediaportal.showHoerspielChannels))
		self.fun.append(getConfigListEntry("CAR-Channels", config.mediaportal.showCarChannels))
		self.fun.append(getConfigListEntry("GAME-Channels", config.mediaportal.showGameChannels))
		self.fun.append(getConfigListEntry("USER-Channels", config.mediaportal.showUserChannels))
		self.fun.append(getConfigListEntry("Clipfish", config.mediaportal.showClipfish))
		self.fun.append(getConfigListEntry("YouTube", config.mediaportal.showYoutube))
		self.fun.append(getConfigListEntry("Teledunet", config.mediaportal.showTeledunet))
		self.fun.append(getConfigListEntry("GEOde", config.mediaportal.showGEOde))
		self.fun.append(getConfigListEntry("Wrestling Network", config.mediaportal.showWrestlingnetwork))
		self.fun.append(getConfigListEntry("retro-tv", config.mediaportal.showretrotv))
		self.fun.append(getConfigListEntry("Galileo-Videolexikon", config.mediaportal.showgalileovl))
		self.fun.append(getConfigListEntry("Dreamscreencast", config.mediaportal.showDsc))
		self.fun.append(getConfigListEntry("CCZwei", config.mediaportal.showCczwei))
		self.fun.append(getConfigListEntry("Filmtrailer", config.mediaportal.showTrailer))
		self.fun.append(getConfigListEntry("ScienceTV", config.mediaportal.showScienceTV))
		self.fun.append(getConfigListEntry("Doku.me", config.mediaportal.showDoku))
		self.fun.append(getConfigListEntry("DokuStream", config.mediaportal.showDokuStream))
		self.fun.append(getConfigListEntry("4Players", config.mediaportal.show4Players))
		self.fun.append(getConfigListEntry("GIGA.de", config.mediaportal.showGIGA))
		self.fun.append(getConfigListEntry("Audi.tv", config.mediaportal.showaudi))
		self.fun.append(getConfigListEntry("gronkh.de", config.mediaportal.showgronkh))
		self.fun.append(getConfigListEntry("mahlzeit.tv", config.mediaportal.showMahlzeitTV))
		self.fun.append(getConfigListEntry("fiwitu.tv", config.mediaportal.showFiwitu))
		self.fun.append(getConfigListEntry("Apple Movie Trailers", config.mediaportal.showappletrailers))
		self.fun.append(getConfigListEntry("DOKUh", config.mediaportal.showDOKUh))
		self.fun.append(getConfigListEntry("DokuHouse", config.mediaportal.showDokuHouse))
		self.fun.append(getConfigListEntry("AutoBild", config.mediaportal.showAutoBild))
		self.fun.append(getConfigListEntry("SportBild", config.mediaportal.showSportBild))
		self.fun.append(getConfigListEntry("Wissen", config.mediaportal.wissen))
		self.fun.append(getConfigListEntry("Bild.de", config.mediaportal.bildde))
		self.fun.append(getConfigListEntry("Southpark.de", config.mediaportal.southpark))
		if astModule:
			self.fun.append(getConfigListEntry("HeiseVideo", config.mediaportal.showHeiseVideo))
		self.fun.sort(key=lambda t : t[0].lower())

		### Mediatheken
		self.mediatheken.append(getConfigListEntry("ARD Mediathek", config.mediaportal.showARD))
		#self.mediatheken.append(getConfigListEntry("arte Mediathek", config.mediaportal.showArte))
		self.mediatheken.append(getConfigListEntry("KIKA+", config.mediaportal.showkika))
		self.mediatheken.append(getConfigListEntry("KinderKino", config.mediaportal.showKinderKino))
		self.mediatheken.append(getConfigListEntry("MyVideo", config.mediaportal.showMyvideo))
		self.mediatheken.append(getConfigListEntry("NetzKino", config.mediaportal.showNetzKino))
		self.mediatheken.append(getConfigListEntry("N-TVNOW", config.mediaportal.showNTVnow))
		self.mediatheken.append(getConfigListEntry("ORF TVthek", config.mediaportal.showORF))
		self.mediatheken.append(getConfigListEntry("RTLNOW", config.mediaportal.showRTLnow))
		self.mediatheken.append(getConfigListEntry("MyVideo Serien", config.mediaportal.showmyvideoserien))
		self.mediatheken.append(getConfigListEntry("BBC Serien", config.mediaportal.showbbcserien))
		self.mediatheken.append(getConfigListEntry("Your Family Entertainment", config.mediaportal.showyfe))
		self.mediatheken.append(getConfigListEntry("Sony Retro", config.mediaportal.showsonyretro))
		self.mediatheken.append(getConfigListEntry("Anime TV", config.mediaportal.showanimetv))
		self.mediatheken.append(getConfigListEntry("ProSieben Mediathek", config.mediaportal.showProSieben))
		self.mediatheken.append(getConfigListEntry("ProSieben MAXX Mediathek", config.mediaportal.showProSiebenMAXX))
		self.mediatheken.append(getConfigListEntry("Sat.1 Mediathek", config.mediaportal.showSat1))
		self.mediatheken.append(getConfigListEntry("Sat.1 Gold Mediathek", config.mediaportal.showSat1Gold))
		self.mediatheken.append(getConfigListEntry("kabeleins Mediathek", config.mediaportal.showkabeleins))
		self.mediatheken.append(getConfigListEntry("YEP! Mediathek", config.mediaportal.showyep))
		self.mediatheken.append(getConfigListEntry("RTL2NOW", config.mediaportal.showRTL2now))
		self.mediatheken.append(getConfigListEntry("RTLNITRONOW", config.mediaportal.showRTLnitro))
		self.mediatheken.append(getConfigListEntry("SRF Player", config.mediaportal.showSRF))
		self.mediatheken.append(getConfigListEntry("SUPERRTLNOW", config.mediaportal.showSUPERRTLnow))
		self.mediatheken.append(getConfigListEntry("ZDFtivi", config.mediaportal.showtivi))
		self.mediatheken.append(getConfigListEntry("VOXNOW", config.mediaportal.showVoxnow))
		self.mediatheken.append(getConfigListEntry("ZDF Mediathek", config.mediaportal.showZDF))
		self.mediatheken.append(getConfigListEntry("MySpass", config.mediaportal.showmyspass))
		self.mediatheken.append(getConfigListEntry("3Sat Mediathek", config.mediaportal.showDreisat))
		self.mediatheken.append(getConfigListEntry("Welt der Wunder", config.mediaportal.wissensthek))
		self.mediatheken.append(getConfigListEntry("N24 Mediathek", config.mediaportal.n24))
		self.mediatheken.sort(key=lambda t : t[0].lower())

		### Porn
		self.porn.append(getConfigListEntry("4Tube", config.mediaportal.show4tube))
		self.porn.append(getConfigListEntry("Ah-Me", config.mediaportal.showahme))
		self.porn.append(getConfigListEntry("AmateurPorn", config.mediaportal.showamateurporn))
		self.porn.append(getConfigListEntry("beeg", config.mediaportal.showbeeg))
		self.porn.append(getConfigListEntry("DrTuber", config.mediaportal.showdrtuber))
		self.porn.append(getConfigListEntry("El-Ladies", config.mediaportal.showelladies))
		self.porn.append(getConfigListEntry("Eporner", config.mediaportal.showeporner))
		self.porn.append(getConfigListEntry("EroProfile", config.mediaportal.showeroprofile))
		self.porn.append(getConfigListEntry("ExtremeTube", config.mediaportal.showextremetube))
		self.porn.append(getConfigListEntry("HDPorn", config.mediaportal.showhdporn))
		self.porn.append(getConfigListEntry("hotshame", config.mediaportal.showhotshame))
		self.porn.append(getConfigListEntry("Pinkrod", config.mediaportal.showpinkrod))
		self.porn.append(getConfigListEntry("PornerBros", config.mediaportal.showpornerbros))
		self.porn.append(getConfigListEntry("Pornhub", config.mediaportal.showPornhub))
		self.porn.append(getConfigListEntry("PornRabbit", config.mediaportal.showpornrabbit))
		self.porn.append(getConfigListEntry("RealGFPorn", config.mediaportal.showrealgfporn))
		self.porn.append(getConfigListEntry("RedTube", config.mediaportal.showredtube))
		self.porn.append(getConfigListEntry("SeXXX-HD", config.mediaportal.showsexxxhd))
		self.porn.append(getConfigListEntry("SunPorno", config.mediaportal.showsunporno))
		self.porn.append(getConfigListEntry("TheNewPorn", config.mediaportal.showthenewporn))
		self.porn.append(getConfigListEntry("Tube8", config.mediaportal.showtube8))
		self.porn.append(getConfigListEntry("UpdateTube", config.mediaportal.showupdatetube))
		self.porn.append(getConfigListEntry("WetPlace", config.mediaportal.showwetplace))
		self.porn.append(getConfigListEntry("xHamster", config.mediaportal.showXhamster))
		self.porn.append(getConfigListEntry("YouPorn", config.mediaportal.showyouporn))
		self.porn.append(getConfigListEntry("AmateursLust", config.mediaportal.amateurslust))
		self.porn.append(getConfigListEntry("Pornoid", config.mediaportal.pornoid))
		self.porn.append(getConfigListEntry("BeFuck", config.mediaportal.befuck))
		self.porn.append(getConfigListEntry("DaChix", config.mediaportal.dachix))
		self.porn.append(getConfigListEntry("TubeWolf", config.mediaportal.tubewolf))
		if config.mediaportal.showgrauzone.value:
			#self.porn.append(getConfigListEntry("PlayPorn", config.mediaportal.showplayporn))
			self.porn.append(getConfigListEntry("PORNMVZ", config.mediaportal.showpornmvz))
			self.porn.append(getConfigListEntry("PornoStreams", config.mediaportal.showpornostreams))
			self.porn.append(getConfigListEntry("MegaSkanks", config.mediaportal.showmegaskanks))
			self.porn.append(getConfigListEntry("STREAMIT-XXX", config.mediaportal.showstreamitPorn))
			self.porn.append(getConfigListEntry("Movie4k-XXX", config.mediaportal.showM4kPorn))
			self.porn.append(getConfigListEntry("ParadiseHill", config.mediaportal.showparadisehill))
			self.porn.append(getConfigListEntry("Free Online Movies", config.mediaportal.showfreeomovie))
			self.porn.append(getConfigListEntry("G-Stream-XXX", config.mediaportal.showgstreaminxxx))
			self.porn.append(getConfigListEntry("PornKino", config.mediaportal.showpornkino))
			self.porn.append(getConfigListEntry("XXXSaVe", config.mediaportal.showxxxsave))
		self.porn.sort(key=lambda t : t[0].lower())

		### Grauzone
		if config.mediaportal.showgrauzone.value:
			self.grauzone.append(getConfigListEntry("SzeneStreams", config.mediaportal.showSzeneStreams))
			self.grauzone.append(getConfigListEntry("Evonic.tv", config.mediaportal.showevonic))
			self.grauzone.append(getConfigListEntry("STREAMIT", config.mediaportal.showstreamit))
			self.grauzone.append(getConfigListEntry("Baskino", config.mediaportal.showBaskino))
			self.grauzone.append(getConfigListEntry("KinoKiste", config.mediaportal.showKinoKiste))
			self.grauzone.append(getConfigListEntry("Stream-Oase", config.mediaportal.showStreamOase))
			self.grauzone.append(getConfigListEntry("Burning-Series", config.mediaportal.showBs))
			self.grauzone.append(getConfigListEntry("Kinox", config.mediaportal.showKinox))
			self.grauzone.append(getConfigListEntry("Movie4k", config.mediaportal.showM4k))
			self.grauzone.append(getConfigListEntry("MLE-HD", config.mediaportal.showmlehd))
			self.grauzone.append(getConfigListEntry("PrimeWire", config.mediaportal.showprimewire))
			self.grauzone.append(getConfigListEntry("ddl.me", config.mediaportal.showDdlme))
			self.grauzone.append(getConfigListEntry("movie25", config.mediaportal.showMovie25))
			self.grauzone.append(getConfigListEntry("watchseries", config.mediaportal.showWatchseries))
			self.grauzone.append(getConfigListEntry("Vibeo", config.mediaportal.showVibeo))
			self.grauzone.append(getConfigListEntry("Movie2k", config.mediaportal.movie2k))
			self.grauzone.append(getConfigListEntry("Serien.bz", config.mediaportal.serienbz))
			self.grauzone.append(getConfigListEntry("Top1000 IMDb", config.mediaportal.topimdb))
			self.grauzone.sort(key=lambda t : t[0].lower())

		self.configlist.append(getConfigListEntry("----- Sport -----", config.mediaportal.fake_entry))
		for x in self.sport:
			self.configlist.append(("Zeige "+x[0]+":",x[1]))

		self.configlist.append(getConfigListEntry("----- Music -----", config.mediaportal.fake_entry))
		for x in self.music:
			self.configlist.append(("Zeige "+x[0]+":",x[1]))

		self.configlist.append(getConfigListEntry("----- Fun -----", config.mediaportal.fake_entry))
		for x in self.fun:
			self.configlist.append(("Zeige "+x[0]+":",x[1]))

		self.configlist.append(getConfigListEntry("----- Mediatheken -----", config.mediaportal.fake_entry))
		for x in self.mediatheken:
			self.configlist.append(("Zeige "+x[0]+":",x[1]))

		self.configlist.append(getConfigListEntry("----- Porn -----", config.mediaportal.fake_entry))
		for x in self.porn:
			self.configlist.append(("Zeige "+x[0]+":",x[1]))

		if config.mediaportal.showgrauzone.value:
			self.configlist.append(getConfigListEntry("----- Grauzone -----", config.mediaportal.fake_entry))
			for x in self.grauzone:
				self.configlist.append(("Zeige "+x[0]+":",x[1]))
			self.configlist.append(getConfigListEntry("----- Watchlist -----", config.mediaportal.fake_entry))
			self.configlist.append(getConfigListEntry("Kinox Watchlist", config.mediaportal.showKinoxWatchlist))
			self.configlist.append(getConfigListEntry("Movie4k Watchlist", config.mediaportal.showM4kWatchlist))

		self.configlist.append(getConfigListEntry("----- Debug -----", config.mediaportal.fake_entry))
		self.configlist.append(getConfigListEntry("Debug-Mode:", config.mediaportal.debugMode))

		self["config"].setList(self.configlist)

		self['title'] = Label("MediaPortal - Setup - (Version %s)" % config.mediaportal.versiontext.value)
		self['name'] = Label("Setup")

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions", "HelpActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyOK,
			"nextBouquet": self.keyDown,
			"prevBouquet": self.keyUp
		}, -1)

	def keyDown(self):
		current = self["config"].getCurrentIndex()
		self["config"].setCurrentIndex(current+20)

	def keyUp(self):
		current = self["config"].getCurrentIndex()
		self["config"].setCurrentIndex(current-20)

	def keyOK(self):
		if config.mediaportal.watchlistpath.value[-1] != '/':
			config.mediaportal.watchlistpath.value = config.mediaportal.watchlistpath.value + '/'
		if config.mediaportal.storagepath.value[-1] != '/':
			config.mediaportal.storagepath.value = config.mediaportal.storagepath.value + '/'
		if (config.mediaportal.showporn.value == False and config.mediaportal.filter.value == 'Porn'):
			config.mediaportal.filter.value = 'ALL'
		if (config.mediaportal.showgrauzone.value == False and config.mediaportal.filter.value == 'Grauzone'):
			config.mediaportal.filter.value = 'ALL'

		CheckPathes(self.session).checkPathes(self.cb_checkPathes)

		if (config.mediaportal.showgrauzone.value and not config.mediaportal.pingrauzone.value):
			self.a = str(random.randint(1,9))
			self.b = str(random.randint(0,9))
			self.c = str(random.randint(0,9))
			self.d = str(random.randint(0,9))
			message = "Some of the plugins may not be legally used in your country!\n\nIf you accept this then enter the following code now:\n\n%s %s %s %s" % (self.a,self.b,self.c,self.d)
			self.session.openWithCallback(self.keyOK2,MessageBox,_(message), MessageBox.TYPE_YESNO)
		else:
			self.confSave()

	def cb_checkPathes(self):
		pass

	def keyOK2(self, answer):
		if answer is True:
			self.session.openWithCallback(self.validcode, PinInput, pinList = [(int(self.a+self.b+self.c+self.d))], triesEntry = self.getTriesEntry(), title = _("Please enter the correct code"), windowTitle = _("Enter code"))
		else:
			config.mediaportal.showgrauzone.value = False
			config.mediaportal.showgrauzone.save()
			config.mediaportal.pingrauzone.value = False
			config.mediaportal.pingrauzone.save()
			self.confSave()

	def getTriesEntry(self):
		return config.ParentalControl.retries.setuppin

	def validcode(self, code):
		if code:
			config.mediaportal.pingrauzone.value = True
			config.mediaportal.pingrauzone.save()
			self.confSave()
		else:
			config.mediaportal.showgrauzone.value = False
			config.mediaportal.showgrauzone.save()
			config.mediaportal.pingrauzone.value = False
			config.mediaportal.pingrauzone.save()
			self.confSave()

	def confSave(self):
		for x in self["config"].list:
			x[1].save()
		configfile.save()
		self.close()

class HelpScreen(Screen):

	def __init__(self, session):
		self.session = session

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/help.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/help.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)

	def keyOK(self):
		self.close()

	def keyCancel(self):
		self.close()

class chooseMenuList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("mediaportal", 20))
		self.l.setItemHeight(44)

class haupt_Screen(Screen, ConfigListScreen):
	def __init__(self, session):
		self.session = session
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/haupt_Screen.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/haupt_Screen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		registerFont("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/mediaportal%s.ttf" % config.mediaportal.font.value, "mediaportal", 100, False)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions", "HelpActions", "InfobarActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" :	self.keyPageDown,
			"prevBouquet" :	self.keyPageUp,
			"menu" : self.keySetup,
			"info" : self.showPorn,
			"showMovies" : self.keySimpleList,
			"displayHelp" : self.keyHelp
		}, -1)

		self['title'] = Label("MediaPortal v%s" % config.mediaportal.versiontext.value)

		self['name'] = Label("Plugin Auswahl")

		self['funsport'] = chooseMenuList([])
		self['Funsport'] = Label("Fun/Music/Sport")

		self['grauzone'] = chooseMenuList([])
		self['Grauzone'] = Label("")

		self['mediatheken'] = chooseMenuList([])
		self['Mediatheken'] = Label("Mediatheken")

		self['porn'] = chooseMenuList([])
		self['Porn'] = Label("")

		self.currentlist = "porn"

		self.onLayoutFinish.append(self.layoutFinished)
		self.onFirstExecBegin.append(self.checkPathes)

	def layoutFinished(self):
		if config.mediaportal.autoupdate.value:
			checkupdate(self.session).checkforupdate()

		self.mediatheken = []
		self.grauzone = []
		self.funsport = []
		self.porn = []

		# Fun/Music/Sport
		if config.mediaportal.showputpattv.value:
			self.funsport.append(self.hauptListEntry("putpat.tv", "putpattv"))
		if config.mediaportal.showLaola1.value:
			self.funsport.append(self.hauptListEntry("Laola1", "laola1"))
		if config.mediaportal.showNhl.value:
			self.funsport.append(self.hauptListEntry("NHL", "nhl"))
		if config.mediaportal.showRofl.value:
			self.funsport.append(self.hauptListEntry("Rofl.to", "rofl"))
		if config.mediaportal.showFail.value:
			self.funsport.append(self.hauptListEntry("Fail.to", "fail"))
		if config.mediaportal.showLiveLeak.value:
			self.funsport.append(self.hauptListEntry("LiveLeak", "liveleak"))
		if config.mediaportal.showFilmOn.value:
			self.funsport.append(self.hauptListEntry("FilmOn", "filmon"))
		if config.mediaportal.showRadio.value:
			self.funsport.append(self.hauptListEntry("Radio.de", "radiode"))
		if config.mediaportal.showSpobox.value:
			self.funsport.append(self.hauptListEntry("Spobox", "spobox"))
		if config.mediaportal.showHoerspielHouse.value:
			self.funsport.append(self.hauptListEntry("HörspielHouse", "hoerspielhouse"))
		if config.mediaportal.showHoerspielChannels.value:
			self.funsport.append(self.hauptListEntry("Hörspiel-Channels", "hoerspielchannels"))
		if config.mediaportal.showCarChannels.value:
			self.funsport.append(self.hauptListEntry("CAR-Channels", "carchannels"))
		if config.mediaportal.showGameChannels.value:
			self.funsport.append(self.hauptListEntry("GAME-Channels", "gamechannels"))
		if config.mediaportal.showMusicChannels.value:
			self.funsport.append(self.hauptListEntry("MUSIC-Channels", "musicchannels"))
		if config.mediaportal.showUserChannels.value:
			self.funsport.append(self.hauptListEntry("USER-Channels", "userchannels"))
		if config.mediaportal.showYoutube.value:
			self.funsport.append(self.hauptListEntry("YouTube", "youtube"))
		#if config.mediaportal.showRan.value:
		#	self.funsport.append(self.hauptListEntry("Ran.de", "ran"))
		if config.mediaportal.showGEOde.value:
			self.funsport.append(self.hauptListEntry("GEO.de", "geo_de"))
		if config.mediaportal.showTeledunet.value:
			self.funsport.append(self.hauptListEntry("Teledunet", "teledunet"))
		if config.mediaportal.showDeluxemusic.value:
			self.funsport.append(self.hauptListEntry("Deluxemusic", "deluxemusic"))
		if config.mediaportal.showNuna.value:
			self.funsport.append(self.hauptListEntry("Nuna", "nuna"))
		if config.mediaportal.showMyvideoTop100.value:
			self.funsport.append(self.hauptListEntry("Myvideo Top 100", "myvideotop100"))
		if config.mediaportal.showMTVdeCharts.value:
			self.funsport.append(self.hauptListEntry("MTV.de Charts", "mtvdecharts"))
		if config.mediaportal.wissen.value:
			self.funsport.append(self.hauptListEntry("Wissen.de", "wissen"))
		if config.mediaportal.show4Players.value:
			self.funsport.append(self.hauptListEntry("4Players", "4players"))
		if config.mediaportal.showGIGA.value:
			self.funsport.append(self.hauptListEntry("GIGA.de", "gigatv"))
		if config.mediaportal.showaudi.value:
			self.funsport.append(self.hauptListEntry("Audi.tv", "auditv"))
		if config.mediaportal.showgronkh.value:
			self.funsport.append(self.hauptListEntry("gronkh.de", "gronkh"))
		if config.mediaportal.showappletrailers.value:
			self.funsport.append(self.hauptListEntry("AppleTrailer", "appletrailers"))
		if config.mediaportal.showAutoBild.value:
			self.funsport.append(self.hauptListEntry("AutoBild", "autobild"))
		if config.mediaportal.showCczwei.value:
			self.funsport.append(self.hauptListEntry("CCZwei", "cczwei"))
		if config.mediaportal.showDoku.value:
			self.funsport.append(self.hauptListEntry("Doku.me", "doku"))
		if config.mediaportal.showDOKUh.value:
			self.funsport.append(self.hauptListEntry("DOKUh", "dokuh"))
		if config.mediaportal.showDokuHouse.value:
			self.funsport.append(self.hauptListEntry("DokuHouse", "dokuhouse"))
		if config.mediaportal.showDokuStream.value:
			self.funsport.append(self.hauptListEntry("DokuStream", "dokustream"))
		if config.mediaportal.showDsc.value:
			self.funsport.append(self.hauptListEntry("Dreamscreencast", "dreamscreencast"))
		if config.mediaportal.showTrailer.value:
			self.funsport.append(self.hauptListEntry("Filmtrailer", "trailer"))
		if config.mediaportal.showFocus.value:
			self.funsport.append(self.hauptListEntry("Focus", "focus"))
		if config.mediaportal.showMahlzeitTV.value:
			self.funsport.append(self.hauptListEntry("mahlzeit.tv", "mahlzeit"))
		if config.mediaportal.showFiwitu.value:
			self.funsport.append(self.hauptListEntry("fiwitu.tv", "fiwitu"))
		if config.mediaportal.showScienceTV.value:
			self.funsport.append(self.hauptListEntry("ScienceTV", "sciencetv"))
		if config.mediaportal.showSportBild.value:
			self.funsport.append(self.hauptListEntry("SportBild", "sportbild"))
		if config.mediaportal.showWrestlingnetwork.value:
			self.funsport.append(self.hauptListEntry("Wrestlingnetwork", "wrestlingnetwork"))
		if config.mediaportal.showretrotv.value:
			self.funsport.append(self.hauptListEntry("retro-tv", "retrotv"))
		if config.mediaportal.showgalileovl.value:
			self.funsport.append(self.hauptListEntry("Galileo-Videolexikon", "galileovl"))
		if config.mediaportal.showsport1fm.value:
			self.funsport.append(self.hauptListEntry("Sport1.fm", "sport1fm"))
		if config.mediaportal.bildde.value:
			self.funsport.append(self.hauptListEntry("Bild.de", "bild"))
		if config.mediaportal.showgrauzone.value:
			if config.mediaportal.showMusicstreamcc.value:
				self.funsport.append(self.hauptListEntry("Musicstream.cc", "musicstreamcc"))
			if config.mediaportal.showEighties.value:
				self.funsport.append(self.hauptListEntry("80s & 90s Music", "eighties"))
			if config.mediaportal.showCanna.value:
				self.funsport.append(self.hauptListEntry("Canna-Power", "canna"))
			if config.mediaportal.showomr.value:
				self.funsport.append(self.hauptListEntry("OnlineMusicRecorder", "omr"))
			if config.mediaportal.showSongsto.value:
				self.funsport.append(self.hauptListEntry("Songs.to", "songsto"))
		if astModule:
			if config.mediaportal.showHeiseVideo.value:
				self.funsport.append(self.hauptListEntry("heiseVIDEO", "heisevideo"))

		# Mediatheken
		if config.mediaportal.showMyvideo.value:
			self.mediatheken.append(self.hauptListEntry("MyVideo", "myvideo"))
		if config.mediaportal.showClipfish.value:
			self.mediatheken.append(self.hauptListEntry("Clipfish", "clipfish"))
		if config.mediaportal.showKinderKino.value:
			self.mediatheken.append(self.hauptListEntry("KinderKino", "kinderkino"))
		if config.mediaportal.showNetzKino.value:
			self.mediatheken.append(self.hauptListEntry("NetzKino", "netzkino"))
		if config.mediaportal.showtivi.value:
			self.mediatheken.append(self.hauptListEntry("ZDFtivi", "tivi"))
		if config.mediaportal.showkika.value:
			self.mediatheken.append(self.hauptListEntry("KIKA+", "kika"))
		if config.mediaportal.showVoxnow.value:
			self.mediatheken.append(self.hauptListEntry("VOXNOW", "voxnow"))
		if config.mediaportal.showRTLnow.value:
			self.mediatheken.append(self.hauptListEntry("RTLNOW", "rtlnow"))
		if config.mediaportal.showmyvideoserien.value:
			self.mediatheken.append(self.hauptListEntry("MyVideo Serien", "myvideoserien"))
		if config.mediaportal.showbbcserien.value:
			self.mediatheken.append(self.hauptListEntry("BBC Serien", "bbcserien"))
		if config.mediaportal.showyfe.value:
			self.mediatheken.append(self.hauptListEntry("Your Family Entertainment", "yfe"))
		if config.mediaportal.showsonyretro.value:
			self.mediatheken.append(self.hauptListEntry("Sony Retro", "sonyretro"))
		if config.mediaportal.showanimetv.value:
			self.mediatheken.append(self.hauptListEntry("Anime TV", "animetv"))
		if config.mediaportal.showProSieben.value:
			self.mediatheken.append(self.hauptListEntry("ProSieben Mediathek", "prosieben"))
		if config.mediaportal.showProSiebenMAXX.value:
			self.mediatheken.append(self.hauptListEntry("ProSieben MAXX Mediathek", "prosiebenmaxx"))
		if config.mediaportal.showSat1.value:
			self.mediatheken.append(self.hauptListEntry("Sat.1 Mediathek", "sat1"))
		if config.mediaportal.showSat1Gold.value:
			self.mediatheken.append(self.hauptListEntry("Sat.1 Gold Mediathek", "sat1gold"))
		if config.mediaportal.showkabeleins.value:
			self.mediatheken.append(self.hauptListEntry("kabeleins Mediathek", "kabeleins"))
		if config.mediaportal.showsixx.value:
			self.mediatheken.append(self.hauptListEntry("sixx Mediathek", "sixx"))
		if config.mediaportal.showyep.value:
			self.mediatheken.append(self.hauptListEntry("YEP! Mediathek", "yep"))
		if config.mediaportal.showNTVnow.value:
			self.mediatheken.append(self.hauptListEntry("N-TVNOW", "ntvnow"))
		if config.mediaportal.showRTL2now.value:
			self.mediatheken.append(self.hauptListEntry("RTL2NOW", "rtl2now"))
		if config.mediaportal.showRTLnitro.value:
			self.mediatheken.append(self.hauptListEntry("RTLNITRONOW", "rtlnitro"))
		if config.mediaportal.showSUPERRTLnow.value:
			self.mediatheken.append(self.hauptListEntry("SUPERRTLNOW", "superrtlnow"))
		if config.mediaportal.showZDF.value:
			self.mediatheken.append(self.hauptListEntry("ZDF Mediathek", "zdf"))
		if config.mediaportal.showORF.value:
			self.mediatheken.append(self.hauptListEntry("ORF TVthek", "orf"))
		if config.mediaportal.showSRF.value:
			self.mediatheken.append(self.hauptListEntry("SRF Player", "srf"))
		if config.mediaportal.showmyspass.value:
			self.mediatheken.append(self.hauptListEntry("MySpass", "myspass"))
		if config.mediaportal.showARD.value:
			self.mediatheken.append(self.hauptListEntry("ARD Mediathek", "ard"))
		if config.mediaportal.showDreisat.value:
			self.mediatheken.append(self.hauptListEntry("3sat Mediathek", "3sat"))
		#if config.mediaportal.showArte.value:
		#	self.mediatheken.append(self.hauptListEntry("arte Mediathek", "arte"))
		if config.mediaportal.wissensthek.value:
			self.mediatheken.append(self.hauptListEntry("Welt der Wunder", "wissensthek"))
		if config.mediaportal.n24.value:
			self.mediatheken.append(self.hauptListEntry("N24 Mediathek", "n24"))
		if config.mediaportal.southpark.value:
			self.mediatheken.append(self.hauptListEntry("Southpark.de", "southpark"))

		# Porn
		if config.mediaportal.showporn.value:
			if config.mediaportal.show4tube.value:
				self.porn.append(self.hauptListEntry("4Tube", "4tube"))
			if config.mediaportal.showahme.value:
				self.porn.append(self.hauptListEntry("Ah-Me", "ahme"))
			if config.mediaportal.showamateurporn.value:
				self.porn.append(self.hauptListEntry("AmateurPorn", "amateurporn"))
			if config.mediaportal.showbeeg.value:
				self.porn.append(self.hauptListEntry("beeg", "beeg"))
			if config.mediaportal.showdrtuber.value:
				self.porn.append(self.hauptListEntry("DrTuber", "drtuber"))
			if config.mediaportal.showelladies.value:
				self.porn.append(self.hauptListEntry("El-Ladies", "elladies"))
			if config.mediaportal.showeporner.value:
				self.porn.append(self.hauptListEntry("Eporner", "eporner"))
			if config.mediaportal.showeroprofile.value:
				self.porn.append(self.hauptListEntry("EroProfile", "eroprofile"))
			if config.mediaportal.showextremetube.value:
				self.porn.append(self.hauptListEntry("ExtremeTube", "extremetube"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showfreeomovie.value:
					self.porn.append(self.hauptListEntry("Free Online Movies", "freeomovie"))
				if config.mediaportal.showgstreaminxxx.value:
					self.porn.append(self.hauptListEntry("G-Stream-XXX", "gstreaminxxx"))
			if config.mediaportal.showhdporn.value:
				self.porn.append(self.hauptListEntry("HDPorn", "hdporn"))
			if config.mediaportal.showhotshame.value:
				self.porn.append(self.hauptListEntry("hotshame", "hotshame"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showmegaskanks.value:
					self.porn.append(self.hauptListEntry("MegaSkanks", "megaskanks"))
				if config.mediaportal.showstreamitPorn.value:
					self.porn.append(self.hauptListEntry("STREAMIT-XXX", "streamitporn"))
				if config.mediaportal.showM4kPorn.value:
					self.porn.append(self.hauptListEntry("Movie4k-XXX", "movie4kporn"))
				if config.mediaportal.showparadisehill.value:
					self.porn.append(self.hauptListEntry("ParadiseHill", "paradisehill"))
			if config.mediaportal.showpinkrod.value:
				self.porn.append(self.hauptListEntry("Pinkrod", "pinkrod"))
			#if config.mediaportal.showgrauzone.value:
			#	if config.mediaportal.showplayporn.value:
			#		self.porn.append(self.hauptListEntry("PlayPorn", "playporn"))
			if config.mediaportal.showpornerbros.value:
				self.porn.append(self.hauptListEntry("PornerBros", "pornerbros"))
			if config.mediaportal.showPornhub.value:
				self.porn.append(self.hauptListEntry("Pornhub", "pornhub"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showpornkino.value:
					self.porn.append(self.hauptListEntry("PornKino", "pornkino"))
				if config.mediaportal.showpornmvz.value:
					self.porn.append(self.hauptListEntry("PORNMVZ", "pornmvz"))
				if config.mediaportal.showpornostreams.value:
					self.porn.append(self.hauptListEntry("PornoStreams", "pornostreams"))
			if config.mediaportal.showpornrabbit.value:
				self.porn.append(self.hauptListEntry("PornRabbit", "pornrabbit"))
			if config.mediaportal.showrealgfporn.value:
				self.porn.append(self.hauptListEntry("RealGFPorn", "realgfporn"))
			if config.mediaportal.showredtube.value:
				self.porn.append(self.hauptListEntry("RedTube", "redtube"))
			if config.mediaportal.showsexxxhd.value:
				self.porn.append(self.hauptListEntry("SeXXX-HD", "sexxxhd"))
			if config.mediaportal.showsunporno.value:
				self.porn.append(self.hauptListEntry("SunPorno", "sunporno"))
			if config.mediaportal.showthenewporn.value:
				self.porn.append(self.hauptListEntry("TheNewPorn", "thenewporn"))
			if config.mediaportal.showtube8.value:
				self.porn.append(self.hauptListEntry("Tube8", "tube8"))
			if config.mediaportal.showupdatetube.value:
				self.porn.append(self.hauptListEntry("UpdateTube", "updatetube"))
			if config.mediaportal.showwetplace.value:
				self.porn.append(self.hauptListEntry("WetPlace", "wetplace"))
			if config.mediaportal.showXhamster.value:
				self.porn.append(self.hauptListEntry("xHamster", "xhamster"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showxxxsave.value:
					self.porn.append(self.hauptListEntry("XXXSaVe", "xxxsave"))
			if config.mediaportal.showyouporn.value:
				self.porn.append(self.hauptListEntry("YouPorn", "youporn"))
			if config.mediaportal.amateurslust.value:
				self.porn.append(self.hauptListEntry("AmateursLust", "amateurslust"))
			if config.mediaportal.pornoid.value:
				self.porn.append(self.hauptListEntry("Pornoid", "pornoid"))
			if config.mediaportal.befuck.value:
				self.porn.append(self.hauptListEntry("BeFuck", "befuck"))
			if config.mediaportal.dachix.value:
				self.porn.append(self.hauptListEntry("DaChix", "dachix"))
			if config.mediaportal.tubewolf.value:
				self.porn.append(self.hauptListEntry("TubeWolf", "tubewolf"))

		# Grauzone
		if config.mediaportal.showgrauzone.value:
			if config.mediaportal.showSzeneStreams.value:
				self.grauzone.append(self.hauptListEntry("SzeneStreams", "szenestreams"))
			if config.mediaportal.showmlehd.value:
				self.grauzone.append(self.hauptListEntry("MLE-HD", "mlehd"))
			if config.mediaportal.showStreamOase.value:
				self.grauzone.append(self.hauptListEntry("StreamOase", "streamoase"))
			if config.mediaportal.showevonic.value:
				self.grauzone.append(self.hauptListEntry("Evonic.tv", "evonic"))
			if config.mediaportal.showM4k.value:
				self.grauzone.append(self.hauptListEntry("Movie4k", "movie4k"))
			if config.mediaportal.showKinox.value:
				self.grauzone.append(self.hauptListEntry("Kinox", "kinox"))
			if config.mediaportal.showKinoKiste.value:
				self.grauzone.append(self.hauptListEntry("KinoKiste", "kinokiste"))
			if config.mediaportal.showstreamit.value:
				self.grauzone.append(self.hauptListEntry("STREAMIT", "streamit"))
			if config.mediaportal.showBs.value:
				self.grauzone.append(self.hauptListEntry("Burning-Series", "burningseries"))
			if config.mediaportal.showBaskino.value:
				self.grauzone.append(self.hauptListEntry("Baskino", "baskino"))
			if config.mediaportal.showprimewire.value:
				self.grauzone.append(self.hauptListEntry("PrimeWire", "primewire"))
			if config.mediaportal.showM4kWatchlist.value:
				self.grauzone.append(self.hauptListEntry("Movie4k Watchlist", "movie4kwatchlist"))
			if config.mediaportal.showKinoxWatchlist.value:
				self.grauzone.append(self.hauptListEntry("Kinox Watchlist", "kinoxwatchlist"))
			if config.mediaportal.showDdlme.value:
				self.grauzone.append(self.hauptListEntry("ddl.me", "ddl_me"))
			if config.mediaportal.showMovie25.value:
				self.grauzone.append(self.hauptListEntry("Movie25", "movie25"))
			if config.mediaportal.showWatchseries.value:
				self.grauzone.append(self.hauptListEntry("Watchseries", "watchseries"))
			if config.mediaportal.showVibeo.value:
				self.grauzone.append(self.hauptListEntry("Vibeo", "vibeo"))
			if config.mediaportal.movie2k.value:
				self.grauzone.append(self.hauptListEntry("Movie2k.tl", "movie2k"))
			if config.mediaportal.serienbz.value:
				self.grauzone.append(self.hauptListEntry("Serien.bz", "serienbz"))
			if config.mediaportal.topimdb.value:
				self.grauzone.append(self.hauptListEntry("Top1000 IMDb", "topimdb"))

		if len(self.porn) < 1:
			self['Porn'].hide()
		else:
			self['Porn'].setText("Porn")

		if len(self.grauzone) < 1:
			self['Grauzone'].hide()
		else:
			self['Grauzone'].setText("Grauzone")

		self.mediatheken.sort(key=lambda t : t[0][0].lower())
		self.grauzone.sort(key=lambda t : t[0][0].lower())
		self.funsport.sort(key=lambda t : t[0][0].lower())
		self.porn.sort(key=lambda t : t[0][0].lower())

		self["mediatheken"].setList(self.mediatheken)
		self["mediatheken"].l.setItemHeight(44)
		self["grauzone"].setList(self.grauzone)
		self["grauzone"].l.setItemHeight(44)
		self["funsport"].setList(self.funsport)
		self["funsport"].l.setItemHeight(44)
		self["porn"].setList(self.porn)
		self["porn"].l.setItemHeight(44)
		self.keyRight()

	def checkPathes(self):
		CheckPathes(self.session).checkPathes(self.cb_checkPathes)

	def cb_checkPathes(self):
		self.session.openWithCallback(self.restart, hauptScreenSetup)

	def hauptListEntry(self, name, jpg):
		res = [(name, jpg)]
		icon = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/icons/%s.png" % jpg
		if not fileExists(icon):
			icon = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/icons/no_icon.png"
		res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 1), size=(75, 40), png=loadPNG(icon)))
		res.append(MultiContentEntryText(pos=(80, 10), size=(200, 40), font=0, text=name, flags=RT_HALIGN_LEFT))
		return res

	def showPorn(self):
		if config.mediaportal.showporn.value:
			config.mediaportal.showporn.value = False
			config.mediaportal.showporn.save()
			configfile.save()
			self.restart()
		else:
			self.session.openWithCallback(self.showPornOK, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))

	def showPornOK(self, pincode):
		if pincode:
			config.mediaportal.showporn.value = True
			config.mediaportal.showporn.save()
			configfile.save()
			self.restart()

	def keySetup(self):
		if config.mediaportal.setuppin.value:
			self.session.openWithCallback(self.pinok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
		else:
			self.session.openWithCallback(self.restart, hauptScreenSetup)

	def keyHelp(self):
		self.session.open(HelpScreen)

	def keySimpleList(self):
		mp_globals.activeIcon = "simplelist"
		self.session.open(simplelistGenreScreen)

	def getTriesEntry(self):
		return config.ParentalControl.retries.setuppin

	def pinok(self, pincode):
		if pincode:
			self.session.openWithCallback(self.restart, hauptScreenSetup)

	def keyUp(self):
		exist = self[self.currentlist].getCurrent()
		if exist == None:
			return
		self[self.currentlist].up()
		auswahl = self[self.currentlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)

	def keyDown(self):
		exist = self[self.currentlist].getCurrent()
		if exist == None:
			return
		self[self.currentlist].down()
		auswahl = self[self.currentlist].getCurrent()[0][0]
		self.title = auswahl
		self['name'].setText(auswahl)

	def keyPageUp(self):
		self[self.currentlist].pageUp()

	def keyPageDown(self):
		self[self.currentlist].pageDown()

	def keyRight(self):
		self.cur_idx = self[self.currentlist].getSelectedIndex()
		self["mediatheken"].selectionEnabled(0)
		self["grauzone"].selectionEnabled(0)
		self["funsport"].selectionEnabled(0)
		self["porn"].selectionEnabled(0)
		if self.currentlist == "mediatheken":
			if len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			elif len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			elif len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			else:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
		elif self.currentlist == "grauzone":
			if len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			elif len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			elif len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			else:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
		elif self.currentlist == "funsport":
			if len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			elif len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			elif len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			else:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
		elif self.currentlist == "porn":
			if len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			elif len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			elif len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			else:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)

		cnt_tmp_ls = int(cnt_tmp_ls)
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currentlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currentlist].moveToIndex(int(idx))

		if cnt_tmp_ls > 0:
			auswahl = self[self.currentlist].getCurrent()[0][0]
			self.title = auswahl
			self['name'].setText(auswahl)

	def keyLeft(self):
		self.cur_idx = self[self.currentlist].getSelectedIndex()
		self["mediatheken"].selectionEnabled(0)
		self["grauzone"].selectionEnabled(0)
		self["funsport"].selectionEnabled(0)
		self["porn"].selectionEnabled(0)
		if self.currentlist == "porn":
			if len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			elif len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			elif len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			else:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
		elif self.currentlist == "funsport":
			if len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			elif len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			elif len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			else:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
		elif self.currentlist == "grauzone":
			if len(self.mediatheken) > 0:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)
			elif len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			elif len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			else:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
		elif self.currentlist == "mediatheken":
			if len(self.porn) > 0:
				self["porn"].selectionEnabled(1)
				self.currentlist = "porn"
				cnt_tmp_ls = len(self.porn)
			elif len(self.funsport) > 0:
				self["funsport"].selectionEnabled(1)
				self.currentlist = "funsport"
				cnt_tmp_ls = len(self.funsport)
			elif len(self.grauzone) > 0:
				self["grauzone"].selectionEnabled(1)
				self.currentlist = "grauzone"
				cnt_tmp_ls = len(self.grauzone)
			else:
				self["mediatheken"].selectionEnabled(1)
				self.currentlist = "mediatheken"
				cnt_tmp_ls = len(self.mediatheken)

		cnt_tmp_ls = int(cnt_tmp_ls)
		print self.cur_idx, cnt_tmp_ls
		if int(self.cur_idx) < int(cnt_tmp_ls):
			self[self.currentlist].moveToIndex(int(self.cur_idx))
		else:
			idx = int(cnt_tmp_ls) -1
			self[self.currentlist].moveToIndex(int(idx))

		if cnt_tmp_ls > 0:
			auswahl = self[self.currentlist].getCurrent()[0][0]
			self.title = auswahl
			self['name'].setText(auswahl)

	def keyOK(self):
		exist = self[self.currentlist].getCurrent()
		if exist == None:
			return
		print self.currentlist
		auswahl = self[self.currentlist].getCurrent()[0][0]
		icon = self[self.currentlist].getCurrent()[0][1]
		mp_globals.activeIcon = icon
		self.pornscreen = None
		self.cat = ""
		print auswahl
		if auswahl == "Doku.me":
			self.session.open(dokuScreen)
		elif auswahl == "Rofl.to":
			self.session.open(roflScreen)
		elif auswahl == "Fail.to":
			self.session.open(failScreen)
		elif auswahl == "KinderKino":
			self.session.open(kinderKinoScreen)
		elif auswahl == "MyVideo":
			self.session.open(myVideoGenreScreen)
		elif auswahl == "SportBild":
			self.session.open(sportBildScreen)
		elif auswahl == "Laola1":
			self.session.open(laolaVideosOverviewScreen)
		elif auswahl == "KinoKiste":
			self.session.open(kinokisteGenreScreen)
		elif auswahl == "Burning-Series":
			self.session.open(bsMain)
		elif auswahl == "PrimeWire":
			self.session.open(PrimeWireGenreScreen)
		elif auswahl == "Focus":
			self.session.open(focusGenre)
		elif auswahl == "FilmOn":
			self.session.open(filmON)
		elif auswahl == "NetzKino":
			self.session.open(netzKinoGenreScreen)
		elif auswahl == "Spobox":
			self.session.open(spoboxGenreScreen)
		elif auswahl == "Radio.de":
			self.session.open(Radiode)
		elif auswahl == "CCZwei":
			self.session.open(cczwei)
		elif auswahl == "Filmtrailer":
			self.session.open(trailer)
		elif auswahl == "Baskino":
			self.session.open(baskino)
		elif auswahl == "Kinox":
			self.session.open(kxMain)
		elif auswahl == "Kinox Watchlist":
			self.session.open(kxWatchlist)
		elif auswahl == "Dreamscreencast":
			self.session.open(dreamscreencast)
		elif auswahl == "StreamOase":
			self.session.open(oasetvGenreScreen)
		elif auswahl == "AutoBild":
			self.session.open(autoBildGenreScreen)
		elif auswahl == "NHL":
			self.session.open(nhlGenreScreen)
		elif auswahl == "4Players":
			self.session.open(forPlayersGenreScreen)
		elif auswahl == "GIGA.de":
			self.session.open(gigatvGenreScreen)
		elif auswahl == "Audi.tv":
			self.session.open(auditvGenreScreen)
		elif auswahl == "gronkh.de":
			self.session.open(gronkhGenreScreen)
		elif auswahl == "ZDFtivi":
			self.session.open(tiviGenreListeScreen)
		elif auswahl == "Evonic.tv":
			self.session.open(showevonicGenre)
		elif auswahl == "Songs.to":
			self.session.open(showSongstoGenre)
		elif auswahl == "Movie4k":
			self.session.open(m4kGenreScreen, "default")
		elif auswahl == "Movie4k Watchlist":
			self.session.open(m4kWatchlist)
		elif auswahl == "STREAMIT":
			self.session.open(showstreamitGenre, "default")
		elif auswahl == "mahlzeit.tv":
			self.session.open(mahlzeitMainScreen)
		elif auswahl == "fiwitu.tv":
			self.session.open(fiwituGenreScreen)
		elif auswahl == "AppleTrailer":
			self.session.open(appletrailersGenreScreen)
		elif auswahl == "DOKUh":
			self.session.open(showDOKUHGenre)
		elif auswahl == "DokuHouse":
			self.session.open(show_DH_Genre)
		elif auswahl == "putpat.tv":
			self.session.open(putpattvGenreScreen)
		elif auswahl == "LiveLeak":
			self.session.open(LiveLeakScreen)
		elif auswahl == "DokuStream":
			self.session.open(show_DS_Genre)
		elif auswahl == "ScienceTV":
			self.session.open(scienceTvGenreScreen)
		elif auswahl == "SzeneStreams":
			self.session.open(SzeneStreamsGenreScreen)
		elif auswahl == "MLE-HD":
			self.session.open(mlehdGenreScreen)
		elif auswahl == "HörspielHouse":
			self.session.open(show_HSH_Genre)
		elif auswahl == "KIKA+":
			self.session.open(kikaGenreScreen)
		elif auswahl == "Hörspiel-Channels":
			self.session.open(show_HSC_Genre)
		elif auswahl == "CAR-Channels":
			self.session.open(show_CAR_Genre)
		elif auswahl == "GAME-Channels":
			self.session.open(show_GAME_Genre)
		elif auswahl == "MUSIC-Channels":
			self.session.open(show_MUSIC_Genre)
		elif auswahl == "USER-Channels":
			self.session.open(show_USER_Genre)
		elif auswahl == "YouTube":
			self.session.open(youtubeGenreScreen)
		elif auswahl == "Clipfish":
			self.session.open(show_CF_Genre)
		elif auswahl == "ddl.me":
			self.session.open(show_DDLME_Genre)
		elif auswahl == "Canna-Power":
			self.session.open(cannaGenreScreen)
		elif auswahl == "OnlineMusicRecorder":
			self.session.open(omrGenreScreen)
		#elif auswahl == "Ran.de":
		#	self.session.open(ranGenreScreen)
		elif auswahl == "Movie25":
			self.session.open(movie25GenreScreen)
		elif auswahl == "80s & 90s Music":
			self.session.open(eightiesGenreScreen)
		elif auswahl == "GEO.de":
			self.session.open(GEOdeGenreScreen)
		elif auswahl == "Teledunet":
			self.session.open(teleGenreScreen)
		elif auswahl == "Deluxemusic":
			self.session.open(deluxemusicGenreScreen)
		elif auswahl == "Nuna":
			self.session.open(nunaGenreScreen)
		elif auswahl == "Watchseries":
			self.session.open(watchseriesGenreScreen)
		elif auswahl == "Myvideo Top 100":
			self.session.open(myvideoTop100GenreScreen)
		elif auswahl == "MTV.de Charts":
			self.session.open(MTVdeChartsGenreScreen)
		elif auswahl == "Musicstream.cc":
			self.session.open(show_MSCC_Genre)
		elif auswahl == "Vibeo":
			self.session.open(vibeoFilmListeScreen)
		elif auswahl == "heiseVIDEO":
			self.session.open(HeiseTvGenreScreen)
		elif auswahl == "Wissen.de":
			self.session.open(wissenListeScreen)
		elif auswahl == "Movie2k.tl":
			self.session.open(movie2kGenreScreen)
		elif auswahl == "VOXNOW":
			self.session.open(VOXnowGenreScreen)
		elif auswahl == "RTLNOW":
			self.session.open(RTLnowGenreScreen)
		elif auswahl == "MyVideo Serien":
			self.session.open(myvideotvGenreScreen, "Weitere_Serien", "MyVideo Serien")
		elif auswahl == "BBC Serien":
			self.session.open(myvideotvGenreScreen, "BBC", "BBC Serien")
		elif auswahl == "Your Family Entertainment":
			self.session.open(myvideotvGenreScreen, "Your_Family_Entertainment", "Your Family Entertainment")
		elif auswahl == "Sony Retro":
			self.session.open(myvideotvGenreScreen, "Sony_Retro", "Sony Retro")
		elif auswahl == "Anime TV":
			self.session.open(myvideotvGenreScreen, "Anime_TV", "Anime TV")
		elif auswahl == "ProSieben Mediathek":
			self.session.open(myvideotvGenreScreen, "ProSieben", "ProSieben Mediathek")
		elif auswahl == "ProSieben MAXX Mediathek":
			self.session.open(myvideotvGenreScreen, "ProSieben_MAXX", "ProSieben MAXX Mediathek")
		elif auswahl == "Sat.1 Mediathek":
			self.session.open(myvideotvGenreScreen, "Sat_1", "Sat.1 Mediathek")
		elif auswahl == "Sat.1 Gold Mediathek":
			self.session.open(myvideotvGenreScreen, "Sat_1_Gold", "Sat.1 Gold Mediathek")
		elif auswahl == "kabeleins Mediathek":
			self.session.open(myvideotvGenreScreen, "kabel_eins", "kabeleins Mediathek")
		elif auswahl == "sixx Mediathek":
			self.session.open(myvideotvGenreScreen, "sixx", "sixx Mediathek")
		elif auswahl == "YEP! Mediathek":
			self.session.open(myvideotvGenreScreen, "YEP", "YEP! Mediathek")
		elif auswahl == "N-TVNOW":
			self.session.open(NTVnowGenreScreen)
		elif auswahl == "RTL2NOW":
			self.session.open(RTL2nowGenreScreen)
		elif auswahl == "RTLNITRONOW":
			self.session.open(RTLNITROnowGenreScreen)
		elif auswahl == "SUPERRTLNOW":
			self.session.open(SUPERRTLnowGenreScreen)
		elif auswahl == "ZDF Mediathek":
			self.session.open(ZDFGenreScreen)
		elif auswahl == "ORF TVthek":
			self.session.open(ORFGenreScreen)
		elif auswahl == "SRF Player":
			self.session.open(SRFGenreScreen)
		elif auswahl == "Wrestlingnetwork":
			self.session.open(wrestlingnetworkGenreScreen)
		elif auswahl == "retro-tv":
			self.session.open(retrotvFilmListeScreen)
		elif auswahl == "Galileo-Videolexikon":
			self.session.open(galileovlGenreScreen)
		elif auswahl == "Sport1.fm":
			self.session.open(sport1fmGenreScreen)
		elif auswahl == "MySpass":
			self.session.open(myspassGenreScreen)
		elif auswahl == "ARD Mediathek":
			self.session.open(ARDGenreScreen)
		elif auswahl == "Bild.de":
			self.session.open(bildFirstScreen)
		elif auswahl == "3sat Mediathek":
			self.session.open(dreisatGenreScreen)
		#elif auswahl == "arte Mediathek":
		#	self.session.open(arteFirstScreen)
		elif auswahl == "Serien.bz":
			self.session.open(SerienFirstScreen)
		elif auswahl == "Top1000 IMDb":
			self.session.open(timdbGenreScreen)
		elif auswahl == "Welt der Wunder":
			self.session.open(wissensthekGenreScreen)
		elif auswahl == "N24 Mediathek":
			self.session.open(n24GenreScreen)
		elif auswahl == "Southpark.de":
			self.session.open(SouthparkGenreScreen)

		# Porn
		elif auswahl == "4Tube":
			self.pornscreen = fourtubeGenreScreen
		elif auswahl == "Ah-Me":
			self.pornscreen = ahmeGenreScreen
		elif auswahl == "AmateurPorn":
			self.pornscreen = amateurpornGenreScreen
		elif auswahl == "beeg":
			self.pornscreen = beegGenreScreen
		elif auswahl == "DrTuber":
			self.pornscreen = drtuberGenreScreen
		elif auswahl == "El-Ladies":
			self.pornscreen = elladiesGenreScreen
		elif auswahl == "Eporner":
			self.pornscreen = epornerGenreScreen
		elif auswahl == "EroProfile":
			self.pornscreen = eroprofileGenreScreen
		elif auswahl == "ExtremeTube":
			self.pornscreen = extremetubeGenreScreen
		elif auswahl == "Free Online Movies":
			self.pornscreen = freeomovieGenreScreen
		elif auswahl == "G-Stream-XXX":
			self.pornscreen = gstreaminxxxGenreScreen
		elif auswahl == "HDPorn":
			self.pornscreen = hdpornGenreScreen
		elif auswahl == "MegaSkanks":
			self.pornscreen = megaskanksGenreScreen
		elif auswahl == "STREAMIT-XXX":
			self.pornscreen = showstreamitGenre
			self.cat = "porn"
		elif auswahl == "Movie4k-XXX":
			self.pornscreen = m4kGenreScreen
			self.cat = "porn"
		elif auswahl == "ParadiseHill":
			self.pornscreen = paradisehillGenreScreen
		#elif auswahl == "PlayPorn":
		#	self.pornscreen = playpornGenreScreen
		elif auswahl == "PornerBros":
			self.pornscreen = pornerbrosGenreScreen
		elif auswahl == "Pornhub":
			self.pornscreen = pornhubGenreScreen
		elif auswahl == "PornKino":
			self.pornscreen = pornkinoGenreScreen
		elif auswahl == "PORNMVZ":
			self.pornscreen = pornmvzGenreScreen
		elif auswahl == "PornoStreams":
			self.pornscreen = pornostreamsGenreScreen
		elif auswahl == "PornRabbit":
			self.pornscreen = pornrabbitGenreScreen
		elif auswahl == "RealGFPorn":
			self.pornscreen = realgfpornGenreScreen
		elif auswahl == "RedTube":
			self.pornscreen = redtubeGenreScreen
		elif auswahl == "SeXXX-HD":
			self.pornscreen = sexxxhdGenreScreen
		elif auswahl == "SunPorno":
			self.pornscreen = sunpornoGenreScreen
		elif auswahl == "Tube8":
			self.pornscreen = tube8GenreScreen
		elif auswahl == "UpdateTube":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "updatetube"
		elif auswahl == "hotshame":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "hotshame"
		elif auswahl == "TheNewPorn":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "thenewporn"
		elif auswahl == "Pinkrod":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "pinkrod"
		elif auswahl == "WetPlace":
			self.pornscreen = wetplaceGenreScreen
		elif auswahl == "xHamster":
			self.pornscreen = xhamsterGenreScreen
		elif auswahl == "XXXSaVe":
			self.pornscreen = xxxsaveFilmScreen
		elif auswahl == "YouPorn":
			self.pornscreen = youpornGenreScreen
		elif auswahl == "AmateursLust":
			self.pornscreen = amateurslustGenreScreen
		elif auswahl == "Pornoid":
			self.pornscreen = pornoidGenreScreen
			self.cat = "pornoid"
		elif auswahl == "BeFuck":
			self.pornscreen = pornoidGenreScreen
			self.cat = "befuck"
		elif auswahl == "DaChix":
			self.pornscreen = dachixGenreScreen
		elif auswahl == "TubeWolf":
			self.pornscreen = tubewolfGenreScreen

		if self.pornscreen:
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pincheckok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				if self.cat == "":
					self.session.open(self.pornscreen)
				else:
					self.session.open(self.pornscreen, self.cat)

	def pincheckok(self, pincode):
		if pincode:
			if self.cat == "":
				self.session.open(self.pornscreen)
			else:
				self.session.open(self.pornscreen, self.cat)

	def keyCancel(self):
		self.session.nav.playService(self.lastservice)
		self.close(self.session, True)

	def restart(self):
		self.session.nav.playService(self.lastservice)
		self.close(self.session, False)

class pluginSort(Screen):

	def __init__(self, session):
		self.session = session

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"

		path = "%s/%s/pluginSortScreen.xml" % (self.skin_path, config.mediaportal.skin.value)

		if not fileExists(path):
			path = self.skin_path + "/original/pluginSortScreen.xml"

		with open(path, "r") as f:
			self.skin = f.read()
			f.close()

		Screen.__init__(self, session)

		self.list = []
		self["config2"] = chooseMenuList([])
		self.plugin_path = ""
		self.selected = False
		self.move_on = False

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "HelpActions"], {
			"ok":	self.select,
			"cancel": self.keyCancel
		}, -1)

		self.readconfig()

	def select(self):
		if not self.selected:
			self.last_newidx = self["config2"].getSelectedIndex()
			self.last_plugin_name = self["config2"].getCurrent()[0][0]
			self.last_plugin_pic = self["config2"].getCurrent()[0][1]
			self.last_plugin_genre = self["config2"].getCurrent()[0][2]
			self.last_plugin_hits = self["config2"].getCurrent()[0][3]
			self.last_plugin_msort = self["config2"].getCurrent()[0][4]
			print "Select:", self.last_plugin_name, self.last_newidx
			self.selected = True
			self.readconfig()
		else:
			self.now_newidx = self["config2"].getSelectedIndex()
			self.now_plugin_name = self["config2"].getCurrent()[0][0]
			self.now_plugin_pic = self["config2"].getCurrent()[0][1]
			self.now_plugin_genre = self["config2"].getCurrent()[0][2]
			self.now_plugin_hits = self["config2"].getCurrent()[0][3]
			self.now_plugin_msort = self["config2"].getCurrent()[0][4]

			count_move = 0
			config_tmp = open("/etc/enigma2/mp_pluginliste.tmp" , "w")
			# del element from list
			del self.config_list_select[int(self.last_newidx)];
			# add element to list at the right place
			self.config_list_select.insert(int(self.now_newidx), (self.last_plugin_name, self.last_plugin_pic, self.last_plugin_genre, self.last_plugin_hits, self.now_newidx));

			# liste neu nummerieren
			for (name, pic, genre, hits, msort) in self.config_list_select:
				count_move += 1
				config_tmp.write('"%s" "%s" "%s" "%s" "%s"\n' % (name, pic, genre, hits, count_move))

			print "change:", self.last_newidx+1, "with", self.now_newidx+1, "total:", len(self.config_list_select)

			config_tmp.close()
			shutil.move("/etc/enigma2/mp_pluginliste.tmp", "/etc/enigma2/mp_pluginliste")
			self.selected = False
			self.readconfig()

	def readconfig(self):
		config_read = open("/etc/enigma2/mp_pluginliste","r")
		self.config_list = []
		self.config_list_select = []
		print "Filter:", config.mediaportal.filter.value
		for line in config_read.readlines():
			ok = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)"', line, re.S)
			if ok:
				(name, pic, genre, hits, msort) = ok[0]
				if config.mediaportal.filter.value != "ALL":
					if genre == config.mediaportal.filter.value:
						self.config_list_select.append((name, pic, genre, hits, msort))
						self.config_list.append(self.show_menu(name, pic, genre, hits, msort))
				else:
					self.config_list_select.append((name, pic, genre, hits, msort))
					self.config_list.append(self.show_menu(name, pic, genre, hits, msort))

		self.config_list.sort(key=lambda x: int(x[0][4]))
		self.config_list_select.sort(key=lambda x: int(x[4]))
		self["config2"].l.setList(self.config_list)
		self["config2"].l.setItemHeight(25)
		config_read.close()

	def show_menu(self, name, pic, genre, hits, msort):
		res = [(name, pic, genre, hits, msort)]
		res.append(MultiContentEntryText(pos=(100, 0), size=(390, 22), font=0, text=name, flags=RT_HALIGN_LEFT))
		if self.selected and name == self.last_plugin_name:
			res.append(MultiContentEntryPixmapAlphaTest(pos=(70, 2), size=(20, 20), png=loadPNG("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/images/select.png")))
		return res

	def keyCancel(self):
		config.mediaportal.sortplugins.value = "user"
		self.close()

class haupt_Screen_Wall(Screen, ConfigListScreen):
	def __init__(self, session, filter):
		self.session = session
		self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()

		self.plugin_liste = []

		# Sport
		if config.mediaportal.showLaola1.value:
			self.plugin_liste.append(("Laola1", "laola1", "Sport"))
		if config.mediaportal.showNhl.value:
			self.plugin_liste.append(("NHL", "nhl", "Sport"))
		if config.mediaportal.showSpobox.value:
			self.plugin_liste.append(("Spobox", "spobox", "Sport"))
		#if config.mediaportal.showRan.value:
		#	self.plugin_liste.append(("Ran.de", "ran", "Sport"))
		if config.mediaportal.showsport1fm.value:
			self.plugin_liste.append(("Sport1.fm", "sport1fm", "Sport"))


		# Music
		if config.mediaportal.showDeluxemusic.value:
			self.plugin_liste.append(("Deluxemusic", "deluxemusic", "Music"))
		if config.mediaportal.showNuna.value:
			self.plugin_liste.append(("Nuna", "nuna", "Music"))
		if config.mediaportal.showMyvideoTop100.value:
			self.plugin_liste.append(("Myvideo Top 100", "myvideotop100", "Music"))
		if config.mediaportal.showMTVdeCharts.value:
			self.plugin_liste.append(("MTV.de Charts", "mtvdecharts", "Music"))
		if config.mediaportal.showMusicChannels.value:
			self.plugin_liste.append(("MUSIC-Channels", "musicchannels", "Music"))
		if config.mediaportal.showRadio.value:
			self.plugin_liste.append(("Radio.de", "radiode", "Music"))
		if config.mediaportal.showputpattv.value:
			self.plugin_liste.append(("putpat.tv", "putpattv", "Music"))
		if config.mediaportal.showgrauzone.value:
			if config.mediaportal.showSongsto.value:
				self.plugin_liste.append(("Songs.to", "songsto", "Music"))
			if config.mediaportal.showCanna.value:
				self.plugin_liste.append(("Canna-Power", "canna", "Music"))
			if config.mediaportal.showomr.value:
				self.plugin_liste.append(("OnlineMusicRecorder", "omr", "Music"))
			if config.mediaportal.showEighties.value:
				self.plugin_liste.append(("80s & 90s Music", "eighties", "Music"))
			if config.mediaportal.showMusicstreamcc.value:
				self.plugin_liste.append(("Musicstream.cc", "musicstreamcc", "Music"))

		# Fun
		if config.mediaportal.showDoku.value:
			self.plugin_liste.append(("Doku.me", "doku", "Fun"))
		if config.mediaportal.showSportBild.value:
			self.plugin_liste.append(("SportBild", "sportbild", "Fun"))
		if config.mediaportal.showAutoBild.value:
			self.plugin_liste.append(("AutoBild", "autobild", "Fun"))
		if config.mediaportal.showFocus.value:
			self.plugin_liste.append(("Focus", "focus", "Fun"))
		if config.mediaportal.showCczwei.value:
			self.plugin_liste.append(("CCZwei", "cczwei", "Fun"))
		if config.mediaportal.showTrailer.value:
			self.plugin_liste.append(("Filmtrailer", "trailer", "Fun"))
		if config.mediaportal.showDsc.value:
			self.plugin_liste.append(("Dreamscreencast", "dreamscreencast", "Fun"))
		if config.mediaportal.show4Players.value:
			self.plugin_liste.append(("4Players", "4players", "Fun"))
		if config.mediaportal.showGIGA.value:
			self.plugin_liste.append(("GIGA.de", "gigatv", "Fun"))
		if config.mediaportal.showaudi.value:
			self.plugin_liste.append(("Audi.tv", "auditv", "Fun"))
		if config.mediaportal.showgronkh.value:
			self.plugin_liste.append(("gronkh.de", "gronkh", "Fun"))
		if config.mediaportal.showMahlzeitTV.value:
			self.plugin_liste.append(("mahlzeit.tv", "mahlzeit", "Fun"))
		if config.mediaportal.showFiwitu.value:
			self.plugin_liste.append(("fiwitu.tv", "fiwitu", "Fun"))
		if config.mediaportal.showappletrailers.value:
			self.plugin_liste.append(("AppleTrailer", "appletrailers", "Fun"))
		if config.mediaportal.showDOKUh.value:
			self.plugin_liste.append(("DOKUh", "dokuh", "Fun"))
		if config.mediaportal.showDokuHouse.value:
			self.plugin_liste.append(("DokuHouse", "dokuhouse", "Fun"))
		if config.mediaportal.showRofl.value:
			self.plugin_liste.append(("Rofl.to", "rofl", "Fun"))
		if config.mediaportal.showFail.value:
			self.plugin_liste.append(("Fail.to", "fail", "Fun"))
		if config.mediaportal.showFilmOn.value:
			self.plugin_liste.append(("FilmOn", "filmon", "Fun"))
		if config.mediaportal.showLiveLeak.value:
			self.plugin_liste.append(("LiveLeak", "liveleak", "Fun"))
		if config.mediaportal.showDokuStream.value:
			self.plugin_liste.append(("DokuStream", "dokustream", "Fun"))
		if config.mediaportal.showScienceTV.value:
			self.plugin_liste.append(("ScienceTV", "sciencetv", "Fun"))
		if config.mediaportal.showHoerspielHouse.value:
			self.plugin_liste.append(("HörspielHouse", "hoerspielhouse", "Fun"))
		if config.mediaportal.showHoerspielChannels.value:
			self.plugin_liste.append(("Hörspiel-Channels", "hoerspielchannels", "Fun"))
		if config.mediaportal.showCarChannels.value:
			self.plugin_liste.append(("CAR-Channels", "carchannels", "Fun"))
		if config.mediaportal.showGameChannels.value:
			self.plugin_liste.append(("GAME-Channels", "gamechannels", "Fun"))
		if config.mediaportal.showUserChannels.value:
			self.plugin_liste.append(("USER-Channels", "userchannels", "Fun"))
		if config.mediaportal.showYoutube.value:
			self.plugin_liste.append(("YouTube", "youtube", "Fun"))
		if config.mediaportal.showTeledunet.value:
			self.plugin_liste.append(("Teledunet", "teledunet", "Fun"))
		if config.mediaportal.showGEOde.value:
			self.plugin_liste.append(("GEO.de", "geo_de", "Fun"))
		if config.mediaportal.showWrestlingnetwork.value:
			self.plugin_liste.append(("Wrestlingnetwork", "wrestlingnetwork", "Fun"))
		if config.mediaportal.showretrotv.value:
			self.plugin_liste.append(("retro-tv", "retrotv", "Fun"))
		if config.mediaportal.showgalileovl.value:
			self.plugin_liste.append(("Galileo-Videolexikon", "galileovl", "Fun"))
		if config.mediaportal.wissen.value:
			self.plugin_liste.append(("Wissen.de", "wissen", "Fun"))
		if config.mediaportal.bildde.value:
			self.plugin_liste.append(("Bild.de", "bild", "Fun"))
		if astModule:
			if config.mediaportal.showHeiseVideo.value:
				self.plugin_liste.append(("heiseVIDEO", "heisevideo", "Fun"))

		# Mediatheken
		if config.mediaportal.showClipfish.value:
			self.plugin_liste.append(("Clipfish", "clipfish", "Mediathek/Fun/Music"))
		if config.mediaportal.showKinderKino.value:
			self.plugin_liste.append(("KinderKino", "kinderkino", "Mediathek"))
		if config.mediaportal.showtivi.value:
			self.plugin_liste.append(("ZDFtivi", "tivi", "Mediathek"))
		if config.mediaportal.showkika.value:
			self.plugin_liste.append(("KIKA+", "kika", "Mediathek"))
		if config.mediaportal.showMyvideo.value:
			self.plugin_liste.append(("MyVideo", "myvideo", "Mediathek"))
		if config.mediaportal.showNetzKino.value:
			self.plugin_liste.append(("NetzKino", "netzkino", "Mediathek"))
		if config.mediaportal.showVoxnow.value:
			self.plugin_liste.append(("VOXNOW", "voxnow", "Mediathek"))
		if config.mediaportal.showRTLnow.value:
			self.plugin_liste.append(("RTLNOW", "rtlnow", "Mediathek"))
		if config.mediaportal.showmyvideoserien.value:
			self.plugin_liste.append(("MyVideo Serien", "myvideoserien", "Mediathek"))
		if config.mediaportal.showbbcserien.value:
			self.plugin_liste.append(("BBC Serien", "bbcserien", "Mediathek"))
		if config.mediaportal.showyfe.value:
			self.plugin_liste.append(("Your Family Entertainment", "yfe", "Mediathek"))
		if config.mediaportal.showsonyretro.value:
			self.plugin_liste.append(("Sony Retro", "sonyretro", "Mediathek"))
		if config.mediaportal.showanimetv.value:
			self.plugin_liste.append(("Anime TV", "animetv", "Mediathek"))
		if config.mediaportal.showProSieben.value:
			self.plugin_liste.append(("ProSieben Mediathek", "prosieben", "Mediathek"))
		if config.mediaportal.showProSiebenMAXX.value:
			self.plugin_liste.append(("ProSieben MAXX Mediathek", "prosiebenmaxx", "Mediathek"))
		if config.mediaportal.showSat1.value:
			self.plugin_liste.append(("Sat.1 Mediathek", "sat1", "Mediathek"))
		if config.mediaportal.showSat1Gold.value:
			self.plugin_liste.append(("Sat.1 Gold Mediathek", "sat1gold", "Mediathek"))
		if config.mediaportal.showkabeleins.value:
			self.plugin_liste.append(("kabeleins Mediathek", "kabeleins", "Mediathek"))
		if config.mediaportal.showsixx.value:
			self.plugin_liste.append(("sixx Mediathek", "sixx", "Mediathek"))
		if config.mediaportal.showyep.value:
			self.plugin_liste.append(("YEP! Mediathek", "yep", "Mediathek"))
		if config.mediaportal.showNTVnow.value:
			self.plugin_liste.append(("N-TVNOW", "ntvnow", "Mediathek"))
		if config.mediaportal.showRTL2now.value:
			self.plugin_liste.append(("RTL2NOW", "rtl2now", "Mediathek"))
		if config.mediaportal.showRTLnitro.value:
			self.plugin_liste.append(("RTLNITRONOW", "rtlnitro", "Mediathek"))
		if config.mediaportal.showSUPERRTLnow.value:
			self.plugin_liste.append(("SUPERRTLNOW", "superrtlnow", "Mediathek"))
		if config.mediaportal.showZDF.value:
			self.plugin_liste.append(("ZDF Mediathek", "zdf", "Mediathek"))
		if config.mediaportal.showORF.value:
			self.plugin_liste.append(("ORF TVthek", "orf", "Mediathek"))
		if config.mediaportal.showSRF.value:
			self.plugin_liste.append(("SRF Player", "srf", "Mediathek"))
		if config.mediaportal.showARD.value:
			self.plugin_liste.append(("ARD Mediathek", "ard", "Mediathek"))
		if config.mediaportal.showmyspass.value:
			self.plugin_liste.append(("MySpass", "myspass", "Mediathek"))
		if config.mediaportal.showDreisat.value:
			self.plugin_liste.append(("3sat Mediathek", "3sat", "Mediathek"))
		#if config.mediaportal.showArte.value:
		#	self.plugin_liste.append(("arte Mediathek", "arte", "Mediathek"))
		if config.mediaportal.wissensthek.value:
			self.plugin_liste.append(("Welt der Wunder", "wissensthek", "Mediathek"))
		if config.mediaportal.n24.value:
			self.plugin_liste.append(("N24 Mediathek", "n24", "Mediathek"))
		if config.mediaportal.southpark.value:
			self.plugin_liste.append(("Southpark.de", "southpark", "Mediathek"))

		# Porn
		if (config.mediaportal.showporn.value == False and config.mediaportal.filter.value == 'Porn'):
			config.mediaportal.filter.value = 'ALL'
		if config.mediaportal.showporn.value:
			if config.mediaportal.show4tube.value:
				self.plugin_liste.append(("4Tube", "4tube", "Porn"))
			if config.mediaportal.showahme.value:
				self.plugin_liste.append(("Ah-Me", "ahme", "Porn"))
			if config.mediaportal.showamateurporn.value:
				self.plugin_liste.append(("AmateurPorn", "amateurporn", "Porn"))
			if config.mediaportal.showbeeg.value:
				self.plugin_liste.append(("beeg", "beeg", "Porn"))
			if config.mediaportal.showdrtuber.value:
				self.plugin_liste.append(("DrTuber", "drtuber", "Porn"))
			if config.mediaportal.showelladies.value:
				self.plugin_liste.append(("El-Ladies", "elladies", "Porn"))
			if config.mediaportal.showeporner.value:
				self.plugin_liste.append(("Eporner", "eporner", "Porn"))
			if config.mediaportal.showeroprofile.value:
				self.plugin_liste.append(("EroProfile", "eroprofile", "Porn"))
			if config.mediaportal.showextremetube.value:
				self.plugin_liste.append(("ExtremeTube", "extremetube", "Porn"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showfreeomovie.value:
					self.plugin_liste.append(("Free Online Movies", "freeomovie", "Porn"))
				if config.mediaportal.showgstreaminxxx.value:
					self.plugin_liste.append(("G-Stream-XXX", "gstreaminxxx", "Porn"))
			if config.mediaportal.showhdporn.value:
				self.plugin_liste.append(("HDPorn", "hdporn", "Porn"))
			if config.mediaportal.showhotshame.value:
				self.plugin_liste.append(("hotshame", "hotshame", "Porn"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showmegaskanks.value:
					self.plugin_liste.append(("MegaSkanks", "megaskanks", "Porn"))
				if config.mediaportal.showstreamitPorn.value:
					self.plugin_liste.append(("STREAMIT-XXX", "streamitporn", "Porn"))
				if config.mediaportal.showM4kPorn.value:
					self.plugin_liste.append(("Movie4k-XXX", "movie4kporn", "Porn"))
				if config.mediaportal.showparadisehill.value:
					self.plugin_liste.append(("ParadiseHill", "paradisehill", "Porn"))
			if config.mediaportal.showpinkrod.value:
				self.plugin_liste.append(("Pinkrod", "pinkrod", "Porn"))
			#if config.mediaportal.showgrauzone.value:
			#	if config.mediaportal.showplayporn.value:
			#		self.plugin_liste.append(("PlayPorn", "playporn", "Porn"))
			if config.mediaportal.showpornerbros.value:
				self.plugin_liste.append(("PornerBros", "pornerbros", "Porn"))
			if config.mediaportal.showPornhub.value:
				self.plugin_liste.append(("Pornhub", "pornhub", "Porn"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showpornkino.value:
					self.plugin_liste.append(("PornKino", "pornkino", "Porn"))
				if config.mediaportal.showpornmvz.value:
					self.plugin_liste.append(("PORNMVZ", "pornmvz", "Porn"))
				if config.mediaportal.showpornostreams.value:
					self.plugin_liste.append(("PornoStreams", "pornostreams", "Porn"))
			if config.mediaportal.showpornrabbit.value:
				self.plugin_liste.append(("PornRabbit", "pornrabbit", "Porn"))
			if config.mediaportal.showrealgfporn.value:
				self.plugin_liste.append(("RealGFPorn", "realgfporn", "Porn"))
			if config.mediaportal.showredtube.value:
				self.plugin_liste.append(("RedTube", "redtube", "Porn"))
			if config.mediaportal.showsexxxhd.value:
				self.plugin_liste.append(("SeXXX-HD", "sexxxhd", "Porn"))
			if config.mediaportal.showsunporno.value:
				self.plugin_liste.append(("SunPorno", "sunporno", "Porn"))
			if config.mediaportal.showthenewporn.value:
				self.plugin_liste.append(("TheNewPorn", "thenewporn", "Porn"))
			if config.mediaportal.showtube8.value:
				self.plugin_liste.append(("Tube8", "tube8", "Porn"))
			if config.mediaportal.showupdatetube.value:
				self.plugin_liste.append(("UpdateTube", "updatetube", "Porn"))
			if config.mediaportal.showwetplace.value:
				self.plugin_liste.append(("WetPlace", "wetplace", "Porn"))
			if config.mediaportal.showXhamster.value:
				self.plugin_liste.append(("xHamster", "xhamster", "Porn"))
			if config.mediaportal.showgrauzone.value:
				if config.mediaportal.showxxxsave.value:
					self.plugin_liste.append(("XXXSaVe", "xxxsave", "Porn"))
			if config.mediaportal.showyouporn.value:
				self.plugin_liste.append(("YouPorn", "youporn", "Porn"))
			if config.mediaportal.amateurslust.value:
				self.plugin_liste.append(("AmateursLust", "amateurslust", "Porn"))
			if config.mediaportal.pornoid.value:
				self.plugin_liste.append(("Pornoid", "pornoid", "Porn"))
			if config.mediaportal.befuck.value:
				self.plugin_liste.append(("BeFuck", "befuck", "Porn"))
			if config.mediaportal.dachix.value:
				self.plugin_liste.append(("DaChix", "dachix", "Porn"))
			if config.mediaportal.tubewolf.value:
				self.plugin_liste.append(("TubeWolf", "tubewolf", "Porn"))

		# Grauzone
		if (config.mediaportal.showgrauzone.value == False and config.mediaportal.filter.value == 'Grauzone'):
			config.mediaportal.filter.value = 'ALL'
		if config.mediaportal.showgrauzone.value:
			if config.mediaportal.showevonic.value:
				self.plugin_liste.append(("Evonic.tv", "evonic", "Grauzone"))
			if config.mediaportal.showM4k.value:
				self.plugin_liste.append(("Movie4k", "movie4k", "Grauzone"))
			if config.mediaportal.showstreamit.value:
				self.plugin_liste.append(("STREAMIT", "streamit", "Grauzone"))
			if config.mediaportal.showSzeneStreams.value:
				self.plugin_liste.append(("SzeneStreams", "szenestreams", "Grauzone"))
			if config.mediaportal.showmlehd.value:
				self.plugin_liste.append(("MLE-HD", "mlehd", "Grauzone"))
			if config.mediaportal.showDdlme.value:
				self.plugin_liste.append(("ddl.me", "ddl_me", "Grauzone"))
			if config.mediaportal.showMovie25.value:
				self.plugin_liste.append(("Movie25", "movie25", "Grauzone"))
			if config.mediaportal.showWatchseries.value:
				self.plugin_liste.append(("Watchseries", "watchseries", "Grauzone"))
			if config.mediaportal.showVibeo.value:
				self.plugin_liste.append(("Vibeo", "vibeo", "Grauzone"))
			if config.mediaportal.showBaskino.value:
				self.plugin_liste.append(("Baskino", "baskino", "Grauzone"))
			if config.mediaportal.showKinox.value:
				self.plugin_liste.append(("Kinox", "kinox", "Grauzone"))
			if config.mediaportal.showStreamOase.value:
				self.plugin_liste.append(("StreamOase", "streamoase", "Grauzone"))
			if config.mediaportal.showKinoKiste.value:
				self.plugin_liste.append(("KinoKiste", "kinokiste", "Grauzone"))
			if config.mediaportal.showBs.value:
				self.plugin_liste.append(("Burning-Series", "burningseries", "Grauzone"))
			if config.mediaportal.showprimewire.value:
				self.plugin_liste.append(("PrimeWire", "primewire", "Grauzone"))
			if config.mediaportal.movie2k.value:
				self.plugin_liste.append(("Movie2k.tl", "movie2k", "Grauzone"))
			if config.mediaportal.serienbz.value:
				self.plugin_liste.append(("Serien.bz", "serienbz", "Grauzone"))
			if config.mediaportal.topimdb.value:
				self.plugin_liste.append(("Top1000 IMDb", "topimdb", "Grauzone"))

		# Watchlisten - Grauzone
			if config.mediaportal.showM4kWatchlist.value:
				self.plugin_liste.append(("Movie4k Watchlist", "movie4kwatchlist", "Grauzone"))
			if config.mediaportal.showKinoxWatchlist.value:
				self.plugin_liste.append(("Kinox Watchlist", "kinoxwatchlist", "Grauzone"))

		# Plugin Sortierung
		if config.mediaportal.sortplugins != "default":

			# Erstelle Pluginliste falls keine vorhanden ist.
			self.sort_plugins_file = "/etc/enigma2/mp_pluginliste"
			if not fileExists(self.sort_plugins_file):
				print "Erstelle Wall-Pluginliste."
				open(self.sort_plugins_file,"w").close()

			pluginliste_leer = os.path.getsize(self.sort_plugins_file)
			if pluginliste_leer == 0:
				print "1st time - Schreibe Wall-Pluginliste."
				first_count = 0
				read_pluginliste = open(self.sort_plugins_file,"a")
				for name,picname,genre in self.plugin_liste:
					print name
					read_pluginliste.write('"%s" "%s" "%s" "%s" "%s"\n' % (name, picname, genre, "0", str(first_count)))
					first_count += 1
				read_pluginliste.close()
				print "Wall-Pluginliste wurde erstellt."

			# Lese Pluginliste ein.
			if fileExists(self.sort_plugins_file):

				count_sort_plugins_file = len(open(self.sort_plugins_file).readlines())
				count_plugin_liste = len(self.plugin_liste)

				print count_plugin_liste, count_sort_plugins_file
				if int(count_plugin_liste) != int(count_sort_plugins_file):
					print "Ein Plugin wurde aktiviert oder deaktiviert.. erstelle neue pluginliste."

					read_pluginliste_tmp = open(self.sort_plugins_file+".tmp","w")
					read_pluginliste = open(self.sort_plugins_file,"r")
					p_dupeliste = []

					for rawData in read_pluginliste.readlines():
						data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)

						if data:
							(p_name, p_picname, p_genre, p_hits, p_sort) = data[0]
							pop_count = 0
							for pname, ppic, pgenre in self.plugin_liste:
								if p_name not in p_dupeliste:
									if p_name == pname:
										read_pluginliste_tmp.write('"%s" "%s" "%s" "%s" "%s"\n' % (p_name, p_picname, pgenre, p_hits, p_sort))
										p_dupeliste.append((p_name))
										print pop_count
										self.plugin_liste.pop(int(pop_count))

									pop_count += 1

					if len(self.plugin_liste) != 0:
						for pname, ppic, pgenre in self.plugin_liste:
							read_pluginliste_tmp.write('"%s" "%s" "%s" "%s" "%s"\n' % (pname, ppic, pgenre, "0", "99"))

					read_pluginliste.close()
					read_pluginliste_tmp.close()
					shutil.move(self.sort_plugins_file+".tmp", self.sort_plugins_file)

				self.new_pluginliste = []
				read_pluginliste = open(self.sort_plugins_file,"r")
				for rawData in read_pluginliste.readlines():
					data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
					if data:
						(p_name, p_picname, p_genre, p_hits, p_sort) = data[0]
						self.new_pluginliste.append((p_name, p_picname, p_genre, p_hits, p_sort))
				read_pluginliste.close()

			# Sortieren nach hits
			if config.mediaportal.sortplugins.value == "hits":
				self.new_pluginliste.sort(key=lambda x: int(x[3]))
				self.new_pluginliste.reverse()

			# Sortieren nach abcde..
			elif config.mediaportal.sortplugins.value == "abc":
				self.new_pluginliste.sort(key=lambda x: str(x[0]).lower())

			elif config.mediaportal.sortplugins.value == "user":
				self.new_pluginliste.sort(key=lambda x: int(x[4]))

			self.plugin_liste = self.new_pluginliste

		skincontent = ""

		posx = 22
		posy = 210
		for x in range(1,len(self.plugin_liste)+1):
			skincontent += "<widget name=\"zeile" + str(x) + "\" position=\"" + str(posx) + "," + str(posy) + "\" size=\"150,80\" zPosition=\"1\" transparent=\"0\" alphatest=\"blend\" />"
			posx += 155
			if x in [8, 16, 24, 32, 48, 56, 64, 72, 88, 96, 104, 112, 128, 136, 144, 152]:
				posx = 22
				posy += 85
			elif x in [40, 80, 120, 160, 200]:
				posx = 22
				posy = 210

		# Appe Page Style
		if config.mediaportal.pagestyle.value == "Graphic":
			self.dump_liste_page_tmp = self.plugin_liste
			if config.mediaportal.filter.value != "ALL":
				self.plugin_liste_page_tmp = []
				self.plugin_liste_page_tmp = [x for x in self.dump_liste_page_tmp if re.search(config.mediaportal.filter.value, x[2])]
			else:
				self.plugin_liste_page_tmp = self.plugin_liste

			if len(self.plugin_liste_page_tmp) != 0:
				self.counting_pages = (len(self.plugin_liste_page_tmp)-1) / 40
				print "COUNTING PAGES:", self.counting_pages
				pagebar_size = int(self.counting_pages) * 30
				rest_size = 1280 - int(pagebar_size)
				start_pagebar = int(rest_size) / 2 - 9

				for x in range(1,self.counting_pages+2):
					if config.mediaportal.skin.value == "original":
						normal = 650
					else:
						normal = 669
					print x, start_pagebar, normal
					skincontent += "<widget name=\"page_empty" + str(x) + "\" position=\"" + str(start_pagebar) + "," + str(normal) + "\" size=\"18,18\" zPosition=\"2\" transparent=\"1\" alphatest=\"blend\" />"
					skincontent += "<widget name=\"page_sel" + str(x) + "\" position=\"" + str(start_pagebar) + "," + str(normal) + "\" size=\"18,18\" zPosition=\"2\" transparent=\"1\" alphatest=\"blend\" />"
					start_pagebar += 30

		self.skin_dump = ""
		self.skin_dump += "<widget name=\"frame\" position=\"22,210\" size=\"150,80\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/icons_wall/Selektor_%s.png\" zPosition=\"2\" transparent=\"0\" alphatest=\"blend\" />" % config.mediaportal.selektor.value
		self.skin_dump += skincontent
		self.skin_dump += "</screen>"

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		self.images_path = path = "%s/%s/images" % (self.skin_path, config.mediaportal.skin.value)

		path = "%s/%s/hauptScreenWall.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/hauptScreenWall.xml"

		with open(path, "r") as f:
			self.skin_dump2 = f.read()
			self.skin_dump2 += self.skin_dump
			self.skin = self.skin_dump2
			f.close()

		Screen.__init__(self, session)

		registerFont("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/resources/mediaportal%s.ttf" % config.mediaportal.font.value, "mediaportal", 100, False)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions", "HelpActions", "InfobarActions"], {
			"ok"    : self.keyOK,
			"up"    : self.keyUp,
			"down"  : self.keyDown,
			"cancel": self.keyCancel,
			"left"  : self.keyLeft,
			"right" : self.keyRight,
			"nextBouquet" :	self.page_next,
			"prevBouquet" :	self.page_back,
			"menu" : self.keySetup,
			"info" : self.showPorn,
			"showMovies" : self.keySimpleList,
			"displayHelp" : self.keyHelp,
			"blue" : self.changeFilter,
			"green" : self.chSort,
			"yellow": self.manuelleSortierung,
			"red": self.premiumize
		}, -1)

		self['name'] = Label("Plugin Auswahl")
		self['blue'] = Label("")
		self['green'] = Label("")
		self['page'] = Label("")
		self["frame"] = MovingPixmap()

		for x in range(1,len(self.plugin_liste)+1):
			self["zeile"+str(x)] = Pixmap()
			self["zeile"+str(x)].show()

		# Apple Page Style
		if config.mediaportal.pagestyle.value == "Graphic" and len(self.plugin_liste_page_tmp) != 0:
			for x in range(1,self.counting_pages+2):
				self["page_empty"+str(x)] = Pixmap()
				self["page_empty"+str(x)].show()
				self["page_sel"+str(x)] = Pixmap()
				self["page_sel"+str(x)].show()

		self.selektor_index = 1
		self.select_list = 0

		self.onFirstExecBegin.append(self._onFirstExecBegin)
		self.onFirstExecBegin.append(self.checkPathes)

	def premiumize(self):
		if config.mediaportal.premiumize_use.value:
			self.puser = config.mediaportal.premiumize_username.value
			self.ppass = config.mediaportal.premiumize_password.value
			url = "https://api.premiumize.me/pm-api/v1.php?method=accountstatus&params[login]=%s&params[pass]=%s" % (self.puser, self.ppass)
			getPage(url, method="GET", timeout=15).addCallback(self.premiumizeData).addErrback(self.dataError)
		else:
			self.session.open(MessageBox, "Premiumize.me ist nicht aktivivert.", MessageBox.TYPE_ERROR)
	
	def premiumizeData(self, data):
		if re.search('status":200', data):
			infos = re.findall('"account_name":"(.*?)","type":"(.*?)","expires":(.*?),".*?trafficleft_gigabytes":(.*?)}', data, re.S|re.I)
			if infos:
				(a_name, a_type, a_expires, a_left) = infos[0]
				print a_name, a_type, a_expires, a_left
				deadline = datetime.datetime.fromtimestamp(int(a_expires)).strftime('%d-%m-%Y')
				pmsg = "User: %s\nType: %s\nExpires: %s\nTraffic: %s GB" % (a_name, a_type, deadline, int(float(a_left)))
				self.session.open(MessageBox, pmsg , MessageBox.TYPE_INFO)
			else:
				self.session.open(MessageBox, "Premiumize.me failed.", MessageBox.TYPE_ERROR)
			
		elif re.search('status":400', data):
			self.session.open(MessageBox, _("Premiumize: Ungueltiger Link !"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":401', data):
			self.session.open(MessageBox, _("Premiumize: Login fehlgeschlagen !"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":402', data):
			self.session.open(MessageBox, _("Premiumize: Du bist kein Premium-User"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":403', data):
			self.session.open(MessageBox, _("Premiumize: forbidden !"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":404', data):
			self.session.open(MessageBox, _("Premiumize: File not found !"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":428', data):
			self.session.open(MessageBox, _("Premiumize: unsupported Streamhoster"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":502', data):
			self.session.open(MessageBox, _("Premiumize: Maintenance !"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":503', data):
			self.session.open(MessageBox, _("Premiumize: unsupported Streamhoster"), MessageBox.TYPE_INFO, timeout=3)
		elif re.search('status":509', data):
			self.session.open(MessageBox, _("Premiumize: Dein traffic ist verbraucht !"), MessageBox.TYPE_INFO, timeout=3)

	def dataError(self, error):
		print error

	def checkPathes(self):
		CheckPathes(self.session).checkPathes(self.cb_checkPathes)

	def cb_checkPathes(self):
		self.session.openWithCallback(self.restart, hauptScreenSetup)

	def manuelleSortierung(self):
		self.session.openWithCallback(self.restart, pluginSort)

	def hit_plugin(self, pname):
		if fileExists(self.sort_plugins_file):
			read_pluginliste = open(self.sort_plugins_file,"r")
			read_pluginliste_tmp = open(self.sort_plugins_file+".tmp","w")
			for rawData in read_pluginliste.readlines():
				data = re.findall('"(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(p_name, p_picname, p_genre, p_hits, p_sort) = data[0]
					if pname == p_name:
						new_hits = int(p_hits)+1
						read_pluginliste_tmp.write('"%s" "%s" "%s" "%s" "%s"\n' % (p_name, p_picname, p_genre, str(new_hits), p_sort))
					else:
						read_pluginliste_tmp.write('"%s" "%s" "%s" "%s" "%s"\n' % (p_name, p_picname, p_genre, p_hits, p_sort))
			read_pluginliste.close()
			read_pluginliste_tmp.close()
			shutil.move(self.sort_plugins_file+".tmp", self.sort_plugins_file)

	def _onFirstExecBegin(self):
		if config.mediaportal.autoupdate.value:
			checkupdate(self.session).checkforupdate()

		# load plugin icons
		print "Set Filter:", config.mediaportal.filter.value
		self['blue'].setText(config.mediaportal.filter.value)
		self.sortplugin = config.mediaportal.sortplugins.value
		if self.sortplugin == "hits":
			self.sortplugin = "Hits"
		elif self.sortplugin == "abc":
			self.sortplugin = "ABC"
		elif self.sortplugin == "user":
			self.sortplugin = "User"
		self['green'].setText(self.sortplugin)
		self.dump_liste = self.plugin_liste
		if config.mediaportal.filter.value != "ALL":
			self.plugin_liste = []
			self.plugin_liste = [x for x in self.dump_liste if re.search(config.mediaportal.filter.value, x[2])]
		if len(self.plugin_liste) == 0:
			self.chFilter()
			self['blue'].setText(config.mediaportal.filter.value)

		if config.mediaportal.sortplugins.value == "hits":
			self.plugin_liste.sort(key=lambda x: int(x[3]))
			self.plugin_liste.reverse()

		# Sortieren nach abcde..
		elif config.mediaportal.sortplugins.value == "abc":
			self.plugin_liste.sort(key=lambda t : t[0].lower())

		elif config.mediaportal.sortplugins.value == "user":
			self.plugin_liste.sort(key=lambda x: int(x[4]))

		print "rolle weiter.."

		for x in range(1,len(self.plugin_liste)+1):
			postername = self.plugin_liste[int(x)-1][1]
			poster_path = "%s/%s.png" % ("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/icons_wall", postername)
			if not fileExists(poster_path):
				poster_path = "/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/icons_wall/no_icon.png"

			self["zeile"+str(x)].instance.setPixmap(gPixmapPtr())
			self["zeile"+str(x)].hide()
			pic = LoadPixmap(cached=True, path=poster_path)
			if pic != None:
				self["zeile"+str(x)].instance.setPixmap(pic)
				if x <= 40:
					self["zeile"+str(x)].show()

		if config.mediaportal.pagestyle.value == "Graphic" and len(self.plugin_liste_page_tmp) != 0:
			for x in range(1,self.counting_pages+2):
				poster_path = "%s/page_select.png" % (self.images_path)
				#print "postername:", postername, poster_path
				self["page_sel"+str(x)].instance.setPixmap(gPixmapPtr())
				self["page_sel"+str(x)].hide()
				pic = LoadPixmap(cached=True, path=poster_path)
				if pic != None:
					self["page_sel"+str(x)].instance.setPixmap(pic)
					if x == 1:
						self["page_sel"+str(x)].show()

			for x in range(1,self.counting_pages+2):
				poster_path = "%s/page.png" % (self.images_path)
				self["page_empty"+str(x)].instance.setPixmap(gPixmapPtr())
				self["page_empty"+str(x)].hide()
				pic = LoadPixmap(cached=True, path=poster_path)
				if pic != None:
					self["page_empty"+str(x)].instance.setPixmap(pic)
					if x > 1:
						self["page_empty"+str(x)].show()

		# erstelle mainlist
		self.widget_list()

	def widget_list(self):
		count = 1
		counting = 1
		self.mainlist = []
		list_dummy = []
		self.plugin_counting = len(self.plugin_liste)

		for x in range(1,int(self.plugin_counting)+1):
			if count == 40:
				count += 1
				counting += 1
				list_dummy.append(x)
				self.mainlist.append(list_dummy)
				count = 1
				list_dummy = []
			else:
				count += 1
				counting += 1
				list_dummy.append(x)
				if int(counting) == int(self.plugin_counting)+1:
					self.mainlist.append(list_dummy)

		print self.mainlist
		if config.mediaportal.pagestyle.value == "Graphic":
			pageinfo = ""
		else:
			pageinfo = "Page %s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		plugin_name = self.plugin_liste[int(select_nr)-1][0]
		self['name'].setText(plugin_name)

	def move_selector(self):
		#print "mainlist:", self.mainlist[int(self.select_list)]
		#print "selektor", self.selektor_index
		#print "gucken", self.selektor_index, len(self.mainlist[int(self.select_list)])
		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		plugin_name = self.plugin_liste[int(select_nr)-1][0]
		self['name'].setText(plugin_name)
		position = self["zeile"+str(self.selektor_index)].instance.position()
		self["frame"].moveTo(position.x(), position.y(), 1)
		self["frame"].show()
		self["frame"].startMoving()

	def keyOK(self):
		if self.check_empty_list():
			return

		select_nr = self.mainlist[int(self.select_list)][int(self.selektor_index)-1]
		auswahl = self.plugin_liste[int(select_nr)-1][0]
		icon = self.plugin_liste[int(select_nr)-1][1]
		mp_globals.activeIcon = icon
		print "Plugin:", auswahl

		self.pornscreen = None
		self.cat = ""
		self.hit_plugin(auswahl)
		if auswahl == "Doku.me":
			self.session.open(dokuScreen)
		elif auswahl == "Rofl.to":
			self.session.open(roflScreen)
		elif auswahl == "Fail.to":
			self.session.open(failScreen)
		elif auswahl == "KinderKino":
			self.session.open(kinderKinoScreen)
		elif auswahl == "MyVideo":
			self.session.open(myVideoGenreScreen)
		elif auswahl == "SportBild":
			self.session.open(sportBildScreen)
		elif auswahl == "Laola1":
			self.session.open(laolaVideosOverviewScreen)
		elif auswahl == "KinoKiste":
			self.session.open(kinokisteGenreScreen)
		elif auswahl == "Burning-Series":
			self.session.open(bsMain)
		elif auswahl == "PrimeWire":
			self.session.open(PrimeWireGenreScreen)
		elif auswahl == "Focus":
			self.session.open(focusGenre)
		elif auswahl == "FilmOn":
			self.session.open(filmON)
		elif auswahl == "NetzKino":
			self.session.open(netzKinoGenreScreen)
		elif auswahl == "Spobox":
			self.session.open(spoboxGenreScreen)
		elif auswahl == "Radio.de":
			self.session.open(Radiode)
		elif auswahl == "CCZwei":
			self.session.open(cczwei)
		elif auswahl == "Filmtrailer":
			self.session.open(trailer)
		elif auswahl == "Baskino":
			self.session.open(baskino)
		elif auswahl == "Kinox":
			self.session.open(kxMain)
		elif auswahl == "Kinox Watchlist":
			self.session.open(kxWatchlist)
		elif auswahl == "Dreamscreencast":
			self.session.open(dreamscreencast)
		elif auswahl == "StreamOase":
			self.session.open(oasetvGenreScreen)
		elif auswahl == "AutoBild":
			self.session.open(autoBildGenreScreen)
		elif auswahl == "NHL":
			self.session.open(nhlGenreScreen)
		elif auswahl == "4Players":
			self.session.open(forPlayersGenreScreen)
		elif auswahl == "GIGA.de":
			self.session.open(gigatvGenreScreen)
		elif auswahl == "Audi.tv":
			self.session.open(auditvGenreScreen)
		elif auswahl == "gronkh.de":
			self.session.open(gronkhGenreScreen)
		elif auswahl == "ZDFtivi":
			self.session.open(tiviGenreListeScreen)
		elif auswahl == "Evonic.tv":
			self.session.open(showevonicGenre)
		elif auswahl == "Songs.to":
			self.session.open(showSongstoGenre)
		elif auswahl == "Movie4k":
			self.session.open(m4kGenreScreen, "default")
		elif auswahl == "Movie4k Watchlist":
			self.session.open(m4kWatchlist)
		elif auswahl == "STREAMIT":
			self.session.open(showstreamitGenre, "default")
		elif auswahl == "mahlzeit.tv":
			self.session.open(mahlzeitMainScreen)
		elif auswahl == "fiwitu.tv":
			self.session.open(fiwituGenreScreen)
		elif auswahl == "AppleTrailer":
			self.session.open(appletrailersGenreScreen)
		elif auswahl == "DOKUh":
			self.session.open(showDOKUHGenre)
		elif auswahl == "DokuHouse":
			self.session.open(show_DH_Genre)
		elif auswahl == "putpat.tv":
			self.session.open(putpattvGenreScreen)
		elif auswahl == "LiveLeak":
			self.session.open(LiveLeakScreen)
		elif auswahl == "DokuStream":
			self.session.open(show_DS_Genre)
		elif auswahl == "ScienceTV":
			self.session.open(scienceTvGenreScreen)
		elif auswahl == "SzeneStreams":
			self.session.open(SzeneStreamsGenreScreen)
		elif auswahl == "HörspielHouse":
			self.session.open(show_HSH_Genre)
		elif auswahl == "Hörspiel-Channels":
			self.session.open(show_HSC_Genre)
		elif auswahl == "CAR-Channels":
			self.session.open(show_CAR_Genre)
		elif auswahl == "GAME-Channels":
			self.session.open(show_GAME_Genre)
		elif auswahl == "MUSIC-Channels":
			self.session.open(show_MUSIC_Genre)
		elif auswahl == "USER-Channels":
			self.session.open(show_USER_Genre)
		elif auswahl == "YouTube":
			self.session.open(youtubeGenreScreen)
		elif auswahl == "Clipfish":
			self.session.open(show_CF_Genre)
		elif auswahl == "ddl.me":
			self.session.open(show_DDLME_Genre)
		elif auswahl == "MLE-HD":
			self.session.open(mlehdGenreScreen)
		elif auswahl == "Canna-Power":
			self.session.open(cannaGenreScreen)
		elif auswahl == "OnlineMusicRecorder":
			self.session.open(omrGenreScreen)
		#elif auswahl == "Ran.de":
		#	self.session.open(ranGenreScreen)
		elif auswahl == "Movie25":
			self.session.open(movie25GenreScreen)
		elif auswahl == "80s & 90s Music":
			self.session.open(eightiesGenreScreen)
		elif auswahl == "Teledunet":
			self.session.open(teleGenreScreen)
		elif auswahl == "GEO.de":
			self.session.open(GEOdeGenreScreen)
		elif auswahl == "Deluxemusic":
			self.session.open(deluxemusicGenreScreen)
		elif auswahl == "Nuna":
			self.session.open(nunaGenreScreen)
		elif auswahl == "Watchseries":
			self.session.open(watchseriesGenreScreen)
		elif auswahl == "Myvideo Top 100":
			self.session.open(myvideoTop100GenreScreen)
		elif auswahl == "MTV.de Charts":
			self.session.open(MTVdeChartsGenreScreen)
		elif auswahl == "Musicstream.cc":
			self.session.open(show_MSCC_Genre)
		elif auswahl == "Vibeo":
			self.session.open(vibeoFilmListeScreen)
		elif auswahl == "heiseVIDEO":
			self.session.open(HeiseTvGenreScreen)
		elif auswahl == "Wissen.de":
			self.session.open(wissenListeScreen)
		elif auswahl == "Movie2k.tl":
			self.session.open(movie2kGenreScreen)
		elif auswahl == "Bild.de":
			self.session.open(bildFirstScreen)
		elif auswahl == "Serien.bz":
			self.session.open(SerienFirstScreen)
		elif auswahl == "Top1000 IMDb":
			self.session.open(timdbGenreScreen)
		elif auswahl == "Southpark.de":
			self.session.open(SouthparkGenreScreen)

		# mediatheken
		elif auswahl == "VOXNOW":
			self.session.open(VOXnowGenreScreen)
		elif auswahl == "RTLNOW":
			self.session.open(RTLnowGenreScreen)
		elif auswahl == "MyVideo Serien":
			self.session.open(myvideotvGenreScreen, "Weitere_Serien", "MyVideo Serien")
		elif auswahl == "BBC Serien":
			self.session.open(myvideotvGenreScreen, "BBC", "BBC Serien")
		elif auswahl == "Your Family Entertainment":
			self.session.open(myvideotvGenreScreen, "Your_Family_Entertainment", "Your Family Entertainment")
		elif auswahl == "Sony Retro":
			self.session.open(myvideotvGenreScreen, "Sony_Retro", "Sony Retro")
		elif auswahl == "Anime TV":
			self.session.open(myvideotvGenreScreen, "Anime_TV", "Anime TV")
		elif auswahl == "ProSieben Mediathek":
			self.session.open(myvideotvGenreScreen, "ProSieben", "ProSieben Mediathek")
		elif auswahl == "ProSieben MAXX Mediathek":
			self.session.open(myvideotvGenreScreen, "ProSieben_MAXX", "ProSieben MAXX Mediathek")
		elif auswahl == "Sat.1 Mediathek":
			self.session.open(myvideotvGenreScreen, "Sat_1", "Sat.1 Mediathek")
		elif auswahl == "Sat.1 Gold Mediathek":
			self.session.open(myvideotvGenreScreen, "Sat_1_Gold", "Sat.1 Gold Mediathek")
		elif auswahl == "kabeleins Mediathek":
			self.session.open(myvideotvGenreScreen, "kabel_eins", "kabeleins Mediathek")
		elif auswahl == "sixx Mediathek":
			self.session.open(myvideotvGenreScreen, "sixx", "sixx Mediathek")
		elif auswahl == "YEP! Mediathek":
			self.session.open(myvideotvGenreScreen, "YEP", "YEP! Mediathek")
		elif auswahl == "N-TVNOW":
			self.session.open(NTVnowGenreScreen)
		elif auswahl == "RTL2NOW":
			self.session.open(RTL2nowGenreScreen)
		elif auswahl == "RTLNITRONOW":
			self.session.open(RTLNITROnowGenreScreen)
		elif auswahl == "SUPERRTLNOW":
			self.session.open(SUPERRTLnowGenreScreen)
		elif auswahl == "ZDF Mediathek":
			self.session.open(ZDFGenreScreen)
		elif auswahl == "ORF TVthek":
			self.session.open(ORFGenreScreen)
		elif auswahl == "SRF Player":
			self.session.open(SRFGenreScreen)
		elif auswahl == "KIKA+":
			self.session.open(kikaGenreScreen)
		elif auswahl == "Wrestlingnetwork":
			self.session.open(wrestlingnetworkGenreScreen)
		elif auswahl == "retro-tv":
			self.session.open(retrotvFilmListeScreen)
		elif auswahl == "ARD Mediathek":
			self.session.open(ARDGenreScreen)
		elif auswahl == "Galileo-Videolexikon":
			self.session.open(galileovlGenreScreen)
		elif auswahl == "Sport1.fm":
			self.session.open(sport1fmGenreScreen)
		elif auswahl == "MySpass":
			self.session.open(myspassGenreScreen)
		elif auswahl == "3sat Mediathek":
			self.session.open(dreisatGenreScreen)
		#elif auswahl == "arte Mediathek":
		#	self.session.open(arteFirstScreen)
		elif auswahl == "Welt der Wunder":
			self.session.open(wissensthekGenreScreen)
		elif auswahl == "N24 Mediathek":
			self.session.open(n24GenreScreen)

		# porn
		elif auswahl == "4Tube":
			self.pornscreen = fourtubeGenreScreen
		elif auswahl == "Ah-Me":
			self.pornscreen = ahmeGenreScreen
		elif auswahl == "AmateurPorn":
			self.pornscreen = amateurpornGenreScreen
		elif auswahl == "beeg":
			self.pornscreen = beegGenreScreen
		elif auswahl == "DrTuber":
			self.pornscreen = drtuberGenreScreen
		elif auswahl == "El-Ladies":
			self.pornscreen = elladiesGenreScreen
		elif auswahl == "Eporner":
			self.pornscreen = epornerGenreScreen
		elif auswahl == "EroProfile":
			self.pornscreen = eroprofileGenreScreen
		elif auswahl == "ExtremeTube":
			self.pornscreen = extremetubeGenreScreen
		elif auswahl == "Free Online Movies":
			self.pornscreen = freeomovieGenreScreen
		elif auswahl == "G-Stream-XXX":
			self.pornscreen = gstreaminxxxGenreScreen
		elif auswahl == "HDPorn":
			self.pornscreen = hdpornGenreScreen
		elif auswahl == "MegaSkanks":
			self.pornscreen = megaskanksGenreScreen
		elif auswahl == "STREAMIT-XXX":
			self.pornscreen = showstreamitGenre
			self.cat = "porn"
		elif auswahl == "Movie4k-XXX":
			self.pornscreen = m4kGenreScreen
			self.cat = "porn"
		elif auswahl == "ParadiseHill":
			self.pornscreen = paradisehillGenreScreen
		#elif auswahl == "PlayPorn":
		#	self.pornscreen = playpornGenreScreen
		elif auswahl == "PornerBros":
			self.pornscreen = pornerbrosGenreScreen
		elif auswahl == "Pornhub":
			self.pornscreen = pornhubGenreScreen
		elif auswahl == "PornKino":
			self.pornscreen = pornkinoGenreScreen
		elif auswahl == "PORNMVZ":
			self.pornscreen = pornmvzGenreScreen
		elif auswahl == "PornoStreams":
			self.pornscreen = pornostreamsGenreScreen
		elif auswahl == "PornRabbit":
			self.pornscreen = pornrabbitGenreScreen
		elif auswahl == "RealGFPorn":
			self.pornscreen = realgfpornGenreScreen
		elif auswahl == "RedTube":
			self.pornscreen = redtubeGenreScreen
		elif auswahl == "SeXXX-HD":
			self.pornscreen = sexxxhdGenreScreen
		elif auswahl == "SunPorno":
			self.pornscreen = sunpornoGenreScreen
		elif auswahl == "Tube8":
			self.pornscreen = tube8GenreScreen
		elif auswahl == "UpdateTube":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "updatetube"
		elif auswahl == "TheNewPorn":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "thenewporn"
		elif auswahl == "Pinkrod":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "pinkrod"
		elif auswahl == "hotshame":
			self.pornscreen = updatetubeGenreScreen
			self.cat = "hotshame"
		elif auswahl == "WetPlace":
			self.pornscreen = wetplaceGenreScreen
		elif auswahl == "xHamster":
			self.pornscreen = xhamsterGenreScreen
		elif auswahl == "XXXSaVe":
			self.pornscreen = xxxsaveFilmScreen
		elif auswahl == "YouPorn":
			self.pornscreen = youpornGenreScreen
		elif auswahl == "AmateursLust":
			self.pornscreen = amateurslustGenreScreen
		elif auswahl == "Pornoid":
			self.pornscreen = pornoidGenreScreen
			self.cat = "pornoid"
		elif auswahl == "BeFuck":
			self.pornscreen = pornoidGenreScreen
			self.cat = "befuck"
		elif auswahl == "DaChix":
			self.pornscreen = dachixGenreScreen
		elif auswahl == "TubeWolf":
			self.pornscreen = tubewolfGenreScreen

		if self.pornscreen:
			if config.mediaportal.pornpin.value:
				self.session.openWithCallback(self.pincheckok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
			else:
				if self.cat == "":
					self.session.open(self.pornscreen)
				else:
					self.session.open(self.pornscreen, self.cat)

	def pincheckok(self, pincode):
		if pincode:
			if self.cat == "":
				self.session.open(self.pornscreen)
			else:
				self.session.open(self.pornscreen, self.cat)

	def	keyLeft(self):
		if self.check_empty_list():
			return
		if self.selektor_index > 1:
			self.selektor_index -= 1
			self.move_selector()
		else:
			self.page_back()

	def	keyRight(self):
		if self.check_empty_list():
			return
		if self.selektor_index < 40 and self.selektor_index != len(self.mainlist[int(self.select_list)]):
			self.selektor_index += 1
			self.move_selector()
		else:
			self.page_next()

	def keyUp(self):
		if self.check_empty_list():
			return
		if self.selektor_index-8 > 1:
			self.selektor_index -=8
			self.move_selector()
		else:
			self.selektor_index = 1
			self.move_selector()

	def keyDown(self):
		if self.check_empty_list():
			return
		if self.selektor_index+8 <= len(self.mainlist[int(self.select_list)]):
			self.selektor_index +=8
			self.move_selector()
		else:
			self.selektor_index = len(self.mainlist[int(self.select_list)])
			self.move_selector()

	def page_next(self):
		if self.check_empty_list():
			return
		if self.select_list < len(self.mainlist)-1:
			self.paint_hide()
			self.select_list += 1
			self.paint_new()

	def page_back(self):
		if self.check_empty_list():
			return
		if self.select_list > 0:
			self.paint_hide()
			self.select_list -= 1
			self.paint_new_last()

	def check_empty_list(self):
		if len(self.plugin_liste) == 0:
			self['name'].setText('Keine Plugins der Kategorie %s aktiviert!' % config.mediaportal.filter.value)
			self["frame"].hide()
			return True
		else:
			return False

	def paint_hide(self):
		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].hide()

	def paint_new_last(self):
		if config.mediaportal.pagestyle.value == "Graphic":
			pageinfo = ""
		else:
			pageinfo = "Page %s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		self.selektor_index = len(self.mainlist[int(self.select_list)])
		#self.selektor_index = self.mainlist[int(self.select_list)][-1]
		print self.selektor_index
		self.move_selector()
		# Apple Page Style
		if config.mediaportal.pagestyle.value == "Graphic" and len(self.plugin_liste_page_tmp) != 0:
			self.refresh_apple_page_bar()

		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].show()

	def paint_new(self):
		if config.mediaportal.pagestyle.value == "Graphic":
			pageinfo = ""
		else:
			pageinfo = "Page %s / %s" % (self.select_list+1, len(self.mainlist))
		self['page'].setText(pageinfo)
		self.selektor_index = 1
		self.move_selector()
		# Apple Page Style
		if config.mediaportal.pagestyle.value == "Graphic" and len(self.plugin_liste_page_tmp) != 0:
			self.refresh_apple_page_bar()

		for x in self.mainlist[int(self.select_list)]:
			self["zeile"+str(x)].show()

	# Apple Page Style
	def refresh_apple_page_bar(self):
		for x in range(1,len(self.mainlist)+1):
			if x == self.select_list+1:
				self["page_empty"+str(x)].hide()
				self["page_sel"+str(x)].show()
			else:
				self["page_sel"+str(x)].hide()
				self["page_empty"+str(x)].show()

	def keySetup(self):
		if config.mediaportal.setuppin.value:
			self.session.openWithCallback(self.pinok, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))
		else:
			self.session.openWithCallback(self.restart, hauptScreenSetup)

	def keyHelp(self):
		self.session.open(HelpScreen)

	def keySimpleList(self):
		mp_globals.activeIcon = "simplelist"
		self.session.open(simplelistGenreScreen)

	def getTriesEntry(self):
		return config.ParentalControl.retries.setuppin

	def pinok(self, pincode):
		if pincode:
			self.session.openWithCallback(self.restart, hauptScreenSetup)

	def chSort(self):
		print "Sort: %s" % config.mediaportal.sortplugins.value

		if config.mediaportal.sortplugins.value == "hits":
			config.mediaportal.sortplugins.value = "abc"
		elif config.mediaportal.sortplugins.value == "abc":
			config.mediaportal.sortplugins.value = "user"
		elif config.mediaportal.sortplugins.value == "user":
			config.mediaportal.sortplugins.value = "hits"

		print "Sort changed:", config.mediaportal.sortplugins.value
		self.restart()

	def changeFilter(self):
		if config.mediaportal.filterselector.value:
			self.startChoose()
		else:
			self.chFilter()

	def chFilter(self):
		print "Filter:", config.mediaportal.filter.value

		if config.mediaportal.filter.value == "ALL":
			config.mediaportal.filter.value = "Mediathek"
		elif config.mediaportal.filter.value == "Mediathek":
			config.mediaportal.filter.value = "Grauzone"
		elif config.mediaportal.filter.value == "Grauzone":
			config.mediaportal.filter.value = "Sport"
		elif config.mediaportal.filter.value == "Sport":
			config.mediaportal.filter.value = "Music"
		elif config.mediaportal.filter.value == "Music":
			config.mediaportal.filter.value = "Fun"
		elif config.mediaportal.filter.value == "Fun":
			config.mediaportal.filter.value = "Porn"
		elif config.mediaportal.filter.value == "Porn":
			config.mediaportal.filter.value = "ALL"

		print "Filter changed:", config.mediaportal.filter.value
		self.restartAndCheck()

	def restartAndCheck(self):
		if config.mediaportal.filter.value != "ALL":
			dump_liste2 = self.dump_liste
			self.plugin_liste = []
			self.plugin_liste = [x for x in dump_liste2 if re.search(config.mediaportal.filter.value, x[2])]
			if len(self.plugin_liste) == 0:
				print "Filter ist deaktviert.. recheck..: %s" % config.mediaportal.filter.value
				self.chFilter()
			else:
				print "Mediaportal restart."
				config.mediaportal.filter.save()
				configfile.save()
				self.close(self.session, False)
		else:
			print "Mediaportal restart."
			config.mediaportal.filter.save()
			configfile.save()
			self.close(self.session, False)

	def showPorn(self):
		if config.mediaportal.showporn.value:
			config.mediaportal.showporn.value = False
			if config.mediaportal.filter.value == "Porn":
				self.chFilter()
			config.mediaportal.showporn.save()
			config.mediaportal.filter.save()
			configfile.save()
			self.restart()
		else:
			self.session.openWithCallback(self.showPornOK, PinInput, pinList = [(config.mediaportal.pincode.value)], triesEntry = self.getTriesEntry(), title = _("Please enter the correct pin code"), windowTitle = _("Enter pin code"))

	def showPornOK(self, pincode):
		if pincode:
			config.mediaportal.showporn.value = True
			config.mediaportal.showporn.save()
			configfile.save()
			self.restart()

	def keyCancel(self):
		config.mediaportal.filter.save()
		configfile.save()
		self.session.nav.playService(self.lastservice)
		self.close(self.session, True)

	def restart(self):
		print "Mediaportal restart."
		config.mediaportal.filter.save()
		config.mediaportal.sortplugins.save()
		configfile.save()
		self.session.nav.playService(self.lastservice)
		self.close(self.session, False)

	def startChoose(self):
		self.session.openWithCallback(self.gotFilter, chooseFilter, self.dump_liste, config.mediaportal.filter.value)

	def gotFilter(self, filter):
		if filter != True:
			print "Set new filter to:", filter
			config.mediaportal.filter.value = filter
			print "Filter changed:", config.mediaportal.filter.value
			self.restartAndCheck()

class chooseFilter(Screen, ConfigListScreen):
	def __init__(self, session, plugin_liste, old_filter):
		self.session = session
		self.plugin_liste = plugin_liste
		self.old_filter = old_filter

		self.dupe = []
		self.dupe.append("ALL")
		for (pname, iname, filter, hits, count) in self.plugin_liste:
			#check auf mehrere filter
			if re.search('/', filter):
				mfilter_raw = re.split('/', filter)
				for mfilter in mfilter_raw:
					if not mfilter in self.dupe:
						self.dupe.append(mfilter)
			else:
				if not filter in self.dupe:
					self.dupe.append(filter)

		# menu abc sorting
		self.dupe.sort()

		hoehe = 197
		breite = 531
		skincontent = ""
		for x in range(1,len(self.dupe)+1):
			skincontent += "<widget name=\"menu" + str(x) + "\" position=\"" + str(breite) + "," + str(hoehe) + "\" size=\"218,38\" zPosition=\"1\" transparent=\"0\" alphatest=\"blend\" />"
			hoehe += 48

		self.skin_dump = ""
		self.skin_dump += "<widget name=\"frame\" position=\"531,197\" size=\"218,38\" pixmap=\"/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins/tec/images/category_selector_%s.png\" zPosition=\"2\" transparent=\"0\" alphatest=\"blend\" />" % config.mediaportal.selektor.value
		self.skin_dump += skincontent
		self.skin_dump += "</screen>"

		self.plugin_path = mp_globals.pluginPath
		self.skin_path = mp_globals.pluginPath + "/skins"
		self.images_path = path = "%s/%s/images" % (self.skin_path, config.mediaportal.skin.value)

		path = "%s/%s/category_selector.xml" % (self.skin_path, config.mediaportal.skin.value)
		if not fileExists(path):
			path = self.skin_path + "/original/category_selector.xml"

		with open(path, "r") as f:
			self.skin_dump2 = f.read()
			self.skin_dump2 += self.skin_dump
			self.skin = self.skin_dump2
			f.close()

		Screen.__init__(self, session)

		self["actions"] = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions", "HelpActions", "InfobarActions"], {
			"ok": self.keyOk,
			"cancel": self.keyCancel,
			"up": self.keyup,
			"down": self.keydown
		}, -1)

		self["frame"] = MovingPixmap()
		self["frame"].hide()

		for x in range(1,len(self.dupe)+1):
			self["menu"+str(x)] = Pixmap()
			self["menu"+str(x)].show()

		self.onFirstExecBegin.append(self.loadPage)

	def loadPage(self):
		for x in range(1,len(self.dupe)+1):
			filtername = self.dupe[int(x)-1]
			poster_path = "%s/tec/images/category_selector_%s.png" % (self.skin_path, filtername.lower())
			if fileExists(poster_path):
				self["menu"+str(x)].instance.setPixmap(gPixmapPtr())
				self["menu"+str(x)].hide()
				pic = LoadPixmap(cached=True, path=poster_path)
				if pic != None:
					self["menu"+str(x)].instance.setPixmap(pic)
					self["menu"+str(x)].show()

		self.getstartframe()

	def getstartframe(self):
		x = 1
		for fname in self.dupe:
			if fname == self.old_filter:
				position = self["menu"+str(x)].instance.position()
				self["frame"].moveTo(position.x(), position.y(), 1)
				self["frame"].show()
				self["frame"].startMoving()
				self.selektor_index = x
			x += 1

	def moveframe(self):
		position = self["menu"+str(self.selektor_index)].instance.position()
		self["frame"].moveTo(position.x(), position.y(), 1)
		self["frame"].show()
		self["frame"].startMoving()

	def keyOk(self):
		print self.dupe[self.selektor_index-1]
		self.close(self.dupe[self.selektor_index-1])

	def keyup(self):
		if int(self.selektor_index) != 1:
			self.selektor_index -= 1
			self.moveframe()

	def keydown(self):
		if int(self.selektor_index) != len(self.dupe):
			self.selektor_index += 1
			self.moveframe()

	def keyCancel(self):
		self.close(True)

def exit(session, result):
	if not result:
		if config.mediaportal.ansicht.value == "liste":
			session.openWithCallback(exit, haupt_Screen)
		else:
			session.openWithCallback(exit, haupt_Screen_Wall, config.mediaportal.filter.value)

def main(session, **kwargs):
	if config.mediaportal.ansicht.value == "liste":
		session.openWithCallback(exit, haupt_Screen)
	else:
		session.openWithCallback(exit, haupt_Screen_Wall, config.mediaportal.filter.value)

def Plugins(path, **kwargs):
	mp_globals.pluginPath = path

	return PluginDescriptor(name=_("MediaPortal"), description="MediaPortal", where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon="plugin.png", fnc=main)
