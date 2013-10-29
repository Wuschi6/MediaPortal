#	-*-	coding:	utf-8	-*-


import base64
from twisted import __version__
__TW_VER__ = tuple([int(x) for x in __version__.split('.')])

try:
	from twisted.internet.endpoints import TCP4ClientEndpoint
except:
	twEndpoints = False
	print 'Error: twisted endpoints not imported'
else:
	twEndpoints = True
	
from twisted.web.client import Agent, RedirectAgent, getPage, ProxyAgent
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.web import http
from urlparse import urlunparse

agent_headers = {
	#'User-Agent': ['Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6'],
	#'Accept-Charset': ['ISO-8859-1,utf-8;q=0.7,*;q=0.7'],
	#'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
	#'Accept-Language': ['en-us,en;q=0.5'],
	'Content-Type': ['application/x-www-form-urlencoded']
}

class GetResource(Protocol):
	def __init__(self, finished):
		print "GetResource:"
		self.data = ""
		self.finished = finished

	def dataReceived(self, data):
		#print "dataReceived:"
		self.data += data
		#print data

	def connectionLost(self, reason):
		print "connectionLost: ", reason
		self.finished.callback(self.data)

class TwAgentHelper:

	def __init__(self, proxy_host="scorpion.premiumize.me", use_proxy=False, p_user='', p_pass=''):
		print "Twisted Agent in use", __TW_VER__
		# can not follow rel. url redirects (location header)
		self.headers = Headers(agent_headers)
		self.useProxy = use_proxy and twEndpoints
		if self.useProxy:
			self.endpoint = TCP4ClientEndpoint(reactor, proxy_host, 80)
			self.agent = RedirectAgent(ProxyAgent(self.endpoint))
			auth = base64.b64encode("%s:%s" % (p_user, p_pass))
			self.headers.addRawHeader('Proxy-Authorization', 'Basic ' + auth.strip())
		else:
			self.agent = RedirectAgent(Agent(reactor))
			
	def getRedirectedUrl(self, callback, cb_err, url, *args, **kwargs):
		print "getRedirectedUrl: ", url
		self._rd_callback = callback
		self.url = url
		self.data = ""

		self.agent.request('HEAD', url, headers=self.headers).addCallback(self.__getResponse, *args, **kwargs).addErrback(cb_err)

	def __getResponse(self, response, *args, **kwargs):
		print "__getResponse:"
		print "Status code: ", response.phrase
		for header, value in response.headers.getAllRawHeaders():
			print header, value

		r = response.headers.getRawHeaders("location")
		if r:
			r_url = r[0]
			p = self._parse(r_url)

			if b'http' not in p[0]:
				print "Rel. URL correction"
				scheme, host, port, path = self._parse(self.url)
				r_url = b'%s://%s/%s' % (scheme, host, r_url)
		else:
			r_url = self.url
		print "Location: ", r_url

		self._rd_callback(r_url, *args, **kwargs)

	def getWebPage(self, callback, cb_err, url, follow_redir, *args, **kwargs):
		print "getWebPage: ", url
		self._wp_callback = callback
		self._errback = cb_err
		self.data = ""
		if follow_redir:
			self.getRedirectedUrl(self.__getWebPageDef, cb_err, url, *args, **kwargs)
		else:
			self.__getWebPageDef(url, *args, **kwargs)

	def __getWebPageDef(self, url, *args, **kwargs):
		d = self.agent.request('GET', url, headers=self.headers)
		d.addCallback(self.__getResource)
		d.addCallbacks(self._wp_callback, self._errback, callbackArgs=args, callbackKeywords=kwargs)
		
	"""
	def __getWebPageDef(self, url, *args, **kwargs):
		#getPage(url, followRedirect=True, agent=self.headers, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self._wp_callback, *args, **kwargs).addErrback(self._errback)
		getPage(url, followRedirect=True, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self._wp_callback, *args, **kwargs).addErrback(self._errback)
	"""
	
	def __getResource(self, response):
		print "__getResource:"
		finished = Deferred()
		response.deliverBody(GetResource(finished))
		return finished

	@staticmethod
	def _parse(url, defaultPort=None):
		url = url.strip()
		parsed = http.urlparse(url)
		scheme = parsed[0]
		path = urlunparse(('', '') + parsed[2:])

		if defaultPort is None:
			if scheme == 'https':
				defaultPort = 443
			else:
				defaultPort = 80

		host, port = parsed[1], defaultPort
		if ':' in host:
			host, port = host.split(':')
			try:
				port = int(port)
			except ValueError:
				port = defaultPort

		if path == '':
			path = '/'

		return scheme, host, port, path
