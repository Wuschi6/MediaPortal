import math
import re
import urllib2
from urllib import unquote, urlencode
from urllib2 import urlopen, Request, HTTPError, URLError
import datetime
import Cookie
import time
from debuglog import printlog as printl

class UrllibHelper(object):

	DEBUGLEVEL = 0

	headers = [
		('Accept', ('text/html,application/xhtml+xml,'
					'application/xml;q=0.9,*/*;q=0.8')),
		('User-Agent', ('Mozilla/5.0 (Windows NT 6.1; WOW64) '
						'AppleWebKit/537.36 (KHTML, like Gecko) '
						'Chrome/27.0.1453.15 Safari/537.36')),
		('Accept-Language', 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4')
	]

	handlers = [
		urllib2.HTTPHandler(debuglevel=DEBUGLEVEL),
		#urllib2.HTTPCookieProcessor(cj)
    ]

	def __init__(self, referrer=None):
		self.referer = referrer
		self.cookie = Cookie.SimpleCookie()
		self.rcookie = None
		self.opener = urllib2.build_opener(*self.handlers)
		self.opener.addheaders = self.headers

	def setCookie(self, name, value, expires=None, path=None, domain=None, secure=None):
		self.cookie[name] = value
		if expires:
			expiration = datetime.datetime.now() + datetime.timedelta(minutes=int(expires))
			self.cookie[name]['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S")
		if path:
			self.cookie[name]['path'] = path
		if domain:
			self.cookie[name]['domain'] = domain
		if secure:
			self.cookie[name]['secure'] = secure

	def joinCookies(self):
		ck = ''
		if self.rcookie:
			ck = self.rcookie[0]
			for s in self.rcookie[1:]:
				ck += '\r\n%s' % s
		if self.cookie:
			if ck:
				ck += '\r\n'
			ck += self.cookie.output(header='').strip()
		return ck

	def getData(self, url, postdata=None, headers=None):

		data = None
		if not url:
			printl("No URL given", self, "E")
			return data

		if postdata:
			postdata = urlencode(postdata)
		request = Request(url, data=postdata)
		if headers:
			for header, val in headers:
				request.add_header(header, val)
		if self.referer:
			request.add_header('Referer', self.referer)
		ck = self.joinCookies()
		if ck:
			request.add_header('Cookie', ck)
		try:
			response = self.opener.open(request)
			data = response.read()
			printl("Data length: %s" % len(data), self)
		except HTTPError, error:
			printl('HTTPError: %s' % error, self, "E")
		except URLError, error:
			printl('URLError: %s' % error, self, "E")
		except ValueError, error:
			printl('ValueError: %s' % error, self, "E")
		except:
			printl('Unknown error', self, "E")
		else:
			self.referer = url
			self.rcookie = response.info().getheaders('Set-Cookie')

		return data

class Flashx(UrllibHelper):

	def __init__(self):
		UrllibHelper.__init__(self)

	def __c(self, c):
		d = ""
		for i in range(0, len(c)):
			if i % 3 == 0:
				d += '%'
			else:
				d += c[i]
		return d

	def __x(self, x, t):
		l = len(x)
		b = 1024
		i = j = p = s = w = 0
		j = math.ceil(l / b)
		r = ""
		while j > 0:
			j -= 1
			i = min(l, b)
			while i > 0:
				i -= 1
				l -= 1
				w |= t[ord(x[p]) - 48] << s
				p += 1
				if s:
					r += chr(165 ^ w & 255)
					w >>= 8
					s -= 2
				else:
					s = 6

		return r

	def __t(self, d):
		data = unquote(d)
		arr = re.findall('Array\((.*?)\)', data)
		if arr:
			t = [int(x) for x in re.findall("\d+", arr[0])]
			return t
		else:
			return []

	def __decodeX(self, c, x):
		d = self.__c(c)
		t = self.__t(d)
		html = self.__x(x, t)
		return html

	def __parseCKS(self, data):
		m = re.findall('Set_Cookie\((.*?)\);', data)
		if m:
			for p in m:
				pars = p.split(',')
				arg1 = pars[0].strip().replace("'","")
				arg2 = pars[1].strip().replace("'","")
				if 'referrer' in arg2:
					arg2 = ''
				arg3 = pars[2].strip().replace("'","")
				arg4 = pars[3].strip().replace("'","")
				arg5 = pars[4].strip().replace("'","")
				arg6 = pars[5].strip().replace("'","")
				self.setCookie(arg1,arg2,arg3,arg4,arg5,arg6)

	def __getData(self, url, decode=False, postdata=None):
		if not url:
			printl("No URL given", self, "E")
			return None

		data = self.getData(url, postdata)
		if data:
			self.__parseCKS(data)

			if decode:
				js = re.findall('<script language=javascript>c="(.*?)";.*?x\("(.*?)"', data)
				if js:
					c = js[0][0]
					x = js[0][1]
					data = self.__decodeX(c,x)

		return data

	def getVidUrl(self, url):
		html = self.__getData(url, False)
		vidUrl = None
		if html:
			js = re.search('class="auto-style6".*?<a href=(.*?)</span><br', html, re.S)
			if js:
				m = re.search('action="(.*?)".*?="id" value="(.*?)">.*?="sec" value="(.*?)">', html, re.S)
				if m:
					pdata = {}
					pdata['id'] = m.group(2)
					pdata['sec'] = m.group(3)
					url = 'http://play.flashx.tv/player/%s' % m.group(1)
					html = self.__getData(url, postdata=pdata)
					if html:
						js = re.search('data="(.*?)\?config=', html)
						if js:
							url = js.group(1)
						else:
							return vidUrl
						js = re.search('.swf\?config=(.*?)"', html)
						if js:
							self.__getData(url)
							html = self.__getData(js.group(1))
							if html:
								js = re.search('<file>(.*?)</file>', html)
								if js:
									vidUrl = js.group(1)

		return vidUrl

