from Plugins.Extensions.MediaPortal.resources.imports import *
from Plugins.Extensions.MediaPortal.resources.simpleplayer import SimplePlayer

def teleGenreListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 800, 25, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, entry)
		]

def teleListEntry(entry):
	#TYPE_TEXT, x, y, width, height, fnt, flags, string [, color, backColor, backColorSelected, borderWidth, borderColor])
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 800, 25, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0])
		]

class teleGenreScreen(Screen):

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

		self.lastservice = session.nav.getCurrentlyPlayingServiceReference()
		self.playing = False

		self.keyLocked = True
		self['title'] = Label("teledunet.com")
		self['ContentTitle'] = Label("Channels:")
		self['name'] = Label("Channels:")
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
		url = "http://www.teledunet.com/"
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.loadPageData).addErrback(self.dataError)

	def dataError(self, error):
		printl(error,self,"E")

	def loadPageData(self, data):
		print "get channels"
		channels = re.findall('src="(http://www.teledunet.com/tv/icones/.*?)".*?<span id=channel_.*?>(.*?)</span>', data, re.S)
		if channels:
			for image,channelname in channels:
				print channelname
				self.genreliste.append((channelname))
		self.chooseMenuList.setList(map(teleGenreListEntry, self.genreliste))
		self.keyLocked = False

	def keyOK(self):
		if self.keyLocked:
			return

		channelname = self['genreList'].getCurrent()[0]
		print channelname
		url = "http://www.teledunet.com/tv/?channel=%s&no_pub" % channelname.replace(' ','+')
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded', 'referer':'http://www.teledunet.com/'}).addCallback(self.parseData, channelname).addErrback(self.dataError)

	def parseData(self, html, channelname):
		m = re.search('time_player=(.*);', html, re.M | re.I)
		time_player_str = eval(m.group(1))
		m = re.search('curent_media=\'(.*)\';', html, re.M | re.I)
		rtmp_url = m.group(1)
		play_path = rtmp_url[rtmp_url.rfind("/")+1:]
		time_player_id = repr(time_player_str).rstrip('0').rstrip('.')

		print rtmp_url, play_path, time_player_id

		rtmp_params = {
				'rtmp_url': rtmp_url,
				'playpath': play_path,
				'app': 'teledunet',
				'swf_url': ('http://www.teledunet.com/tv/player.swf?'
				'bufferlength=5&'
				'repeat=single&'
				'autostart=true&'
				'id0=%(time_player)s&'
				'streamer=%(rtmp_url)s&'
				'file=%(channel_name)s&'
				'provider=rtmp'
				) % {'time_player': time_player_id, 'channel_name': play_path, 'rtmp_url': rtmp_url},
				'video_page_url': 'http://www.teledunet.com/tv/?channel=%s&no_pub' % play_path,
				'live': '1'
				}

		print "rtmp_params:", rtmp_params

		stream_url = self.rtmpdump_output(rtmp_params)
		print stream_url
		self.session.open(SimplePlayer, [(channelname, stream_url)], showPlaylist=False, ltype='teledunet')

	def rtmpdump_output(self, rtmp_params):
		return (
				'%(rtmp_url)s '
				'app=%(app)s '
				'swfUrl=%(swf_url)s '
				'playpath=%(playpath)s '
				'live=%(live)s '
				'pageUrl=%(video_page_url)s '
				) % rtmp_params

	def keyCancel(self):
		self.close()