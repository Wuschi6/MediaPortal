#	-*-	coding:	utf-8	-*-

from Components.Button import Button
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.ActionMap import NumberActionMap, ActionMap
from Components.config import config, ConfigInteger, ConfigSelection, getConfigListEntry, ConfigText, ConfigDirectory, ConfigYesNo, configfile, ConfigSelection, ConfigSubsection, ConfigPIN, NoSave, ConfigNothing
from Components.FileList import FileList, FileEntryComponent
from Components.GUIComponent import GUIComponent
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap, MovingPixmap
from Components.PluginList import PluginEntryComponent, PluginList
# All import which are necessary
from Components.Language import language
from Components.AVSwitch import AVSwitch
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase

from enigma import gFont, addFont, eTimer, eConsoleAppContainer, ePicLoad, loadPNG, getDesktop, eServiceReference, iPlayableService, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListbox, gPixmapPtr, getPrevAsciiCode
from Plugins.Plugin import PluginDescriptor

from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.InputBox import PinInput
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarNotifications
from Screens.InfoBar import MoviePlayer, InfoBar
from Screens.Standby import TryQuitMainloop
from twisted.web.client import downloadPage, getPage, error
from twisted.internet import reactor, defer
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN, createDir
from Tools.LoadPixmap import LoadPixmap

from jsunpacker import cJsUnpacker

import re, urllib, urllib2, os, cookielib, time, socket, sha, shutil, base64, datetime, math, hashlib, random, json, md5, string
from urllib2 import Request, URLError, urlopen as urlopen2
from socket import gaierror, error
from urllib import quote, unquote_plus, unquote, urlencode
from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
from base64 import b64decode
from binascii import unhexlify
from urlparse import parse_qs
from streams import get_stream_link
from time import *

from Screens.VirtualKeyBoard import VirtualKeyBoard

from debuglog import printlog as printl
import mp_globals
from Components.ScrollLabel import ScrollLabel

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

def registerFont(file, name, scale, replacement):
		try:
				addFont(file, name, scale, replacement)
		except Exception, ex: #probably just openpli
				addFont(file, name, scale, replacement, 0)

def decodeHtml(text):
	text = text.replace('&auml;','ä')
	text = text.replace('\u00e4','ä')
	text = text.replace('&#228;','ä')

	text = text.replace('&Auml;','Ä')
	text = text.replace('\u00c4','Ä')
	text = text.replace('&#196;','Ä')

	text = text.replace('&ouml;','ö')
	text = text.replace('\u00f6','ö')
	text = text.replace('&#246;','ö')

	text = text.replace('&ouml;','Ö')
	text = text.replace('\u00d6','Ö')
	text = text.replace('&#214;','Ö')

	text = text.replace('&uuml;','ü')
	text = text.replace('\u00fc','ü')
	text = text.replace('&#252;','ü')

	text = text.replace('&Uuml;','Ü')
	text = text.replace('\u00dc','Ü')
	text = text.replace('&#220;','Ü')

	text = text.replace('&szlig;','ß')
	text = text.replace('\u00df','ß')
	text = text.replace('&#223;','ß')

	text = text.replace('&amp;','&')
	text = text.replace('&quot;','\"')
	text = text.replace('&gt;','>')
	text = text.replace('&apos;',"'")
	text = text.replace('&acute;','\'')
	text = text.replace('&ndash;','-')
	text = text.replace('&bdquo;','"')
	text = text.replace('&rdquo;','"')
	text = text.replace('&ldquo;','"')
	text = text.replace('&lsquo;','\'')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&#034;','\'')
	text = text.replace('&#038;','&')
	text = text.replace('&#039;','\'')
	text = text.replace('&#160;',' ')
	text = text.replace('\u00a0',' ')
	text = text.replace('&#174;','')
	text = text.replace('&#225;','a')
	text = text.replace('&#233;','e')
	text = text.replace('&#243;','o')
	text = text.replace('&#8211;',"-")
	text = text.replace('\u2013',"-")
	text = text.replace('&#8216;',"'")
	text = text.replace('&#8217;',"'")
	text = text.replace('&#8220;',"'")
	text = text.replace('&#8221;','"')
	text = text.replace('&#8222;',',')
	
	text = text.replace('&#xC4;','Ä')
	text = text.replace('&#xD6;','Ö')
	text = text.replace('&#xDC;','Ü')
	text = text.replace('&#xE4;','ä')
	text = text.replace('&#xF6;','ö')
	text = text.replace('&#xFC;','ü')
	text = text.replace('&#xDF;','ß')
	text = text.replace('&#xE9;','é')
	text = text.replace('&#xB7;','·')
	text = text.replace("&#x27;","'")
	text = text.replace("&#x26;","&")
	text = text.replace("&#xFB;","û")
	text = text.replace("&#xF8;","ø")
	text = text.replace("&#x21;","!")
	text = text.replace("&#x3f;","?")

	text = text.replace('&#8230;','...')
	text = text.replace('\u2026','...')
	text = text.replace('&hellip;','...')
	return text

def iso8859_Decode(txt):
	txt = txt.replace('\xe4','ä').replace('\xf6','ö').replace('\xfc','ü').replace('\xdf','ß')
	txt = txt.replace('\xc4','Ä').replace('\xd6','Ö').replace('\xdc','Ü')
	#txt.decode('iso-8859-1').encode('utf-8')
	return txt

def decodeHtml2(txt):
	txt = iso8859_Decode(txt)
	txt = decodeHtml(txt).strip()
	return txt