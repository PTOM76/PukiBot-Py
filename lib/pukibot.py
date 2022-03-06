from urllib import request
import urllib.parse
import re
import hashlib
import json
from . import http
from . import permission

class PukiBot:
	
	url = None
	token = None
	
	# キャッシュ
	cache_info = None
	cache_permission = None
	
	def __init__(this, url = None, token = None):
		this.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
		if url != None:
			this.setUrl(url)
		if token != None:
			this.setToken(token)
	
	# ユーザーエージェントを設定
	def setUserAgent(this, agent):
		this.userAgent = agent
	
	# ユーザーエージェントを取得
	def getUserAgent(this):
		return this.userAgent
	
	# URLを設定
	def setUrl(this, url):
		this.url = url
	
	# URLを取得
	def getUrl(this):
		return this.url
	
	# URLを設定
	def setToken(this, token):
		this.token = token
	
	# URLを取得
	def getToken(this):
		return this.token
	
	# Infoデータ取得
	def getInfo(this, dict = True, cache = True) -> dict:
		"""Get permission data
		
		Args:
			dict (boolean): true → return info data as dict / false → return info data as string
			cache (boolean): caching permission data
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getInfo()['pukiwiki']['version'])
			   1.5.3
		"""
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		url = this.getUrl() + "?cmd=bot&api=info" + authorization
		if dict:
			# Dict型
			data = http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
			if cache:
				this.cache_info = data
			return data
		else:
			# String型
			data = http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
			if cache:
				this.cache_info = http.toMap(data)
			return data
	
	# PukiWikiのバージョンを取得
	def getPukiWikiVersion(this):
		return this.getInfo()['pukiwiki']['version']
	
	# Wikiのタイトルを取得
	def getWikiTitle(this):
		return this.getInfo()['page_title']
	
	# 管理人の名前を取得
	def getWikiAdmin(this):
		return this.getInfo()['modifier']
	
	# 管理人のサイトを取得
	def getWikiAdminSite(this):
		return this.getInfo()['modifierlink']
	
	# パーミッションのデータ取得 (含まれるデータ: 自身のパーミッション, フラグの数値, 権限の有無)
	def getPermission(this, cache = True, dict = True) -> dict:
		"""Get permission data
		
		Args:
			dict (boolean): true → return permission data as dict / false → return permission data as string
			cache (boolean): caching permission data
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPermission()['permissions']['BOT_PERMISSION_NONE'])
			   0
		"""
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		url = this.getUrl() + "?cmd=bot&api=permission" + authorization
		if dict:
			# Dict型
			data = http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
			if cache:
				this.cache_permission = data
			return data
		else:
			# String型
			data = http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
			if cache:
				this.cache_permission = http.toMap(data)
			return data
	
	# ページのデータ取得 (含まれるデータ: ソース, ページの添付ファイルリスト, 詳細)
	def getPage(this, page, dict = True, permitCheck = False) -> dict:
		"""Get page data
		
		Args:
			page (string): wiki page name
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPage('FrontPage'))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.page.canRead() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.page.canRead() == False:
					return False
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		url = this.getUrl() + "?cmd=bot&api=page" + authorization + "&name=" + page
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		
	# ページの書き込み (含まれるデータ: )
	def writePage(this, page, source, permitCheck = False, notimestamp = False, dict = True) -> dict:
		"""Write page
		
		Args:
			page (string): wiki page name
			source (string): data written to the page
			permitCheck (boolean): check if the bot has permission
			notimestamp (boolean): notimestamp
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.writePage('TestPage', "* Hello, World!\n- HogeHoge"))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.page.canEdit() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.page.canEdit() == False:
					return False
		data = {'name': page, 'source': source, 'notimestamp': notimestamp}
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		url = this.getUrl() + "?cmd=bot&api=page" + authorization
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, data, "PUT")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, data, "PUT")
		
	# ページの書き込み (含まれるデータ: )
	def deletePage(this, page, permitCheck = False, dict = True) -> dict:
		"""Delete page
		
		Args:
			page (string): wiki page name
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.writePage('TestPage', "* Hello, World!\n- HogeHoge"))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.page.canEdit() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.page.canEdit() == False:
					return False
		data = {'name': page}
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		url = this.getUrl() + "?cmd=bot&api=page" + authorization
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, data, "DELETE")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, data, "DELETE")
		
	def getPages(this, permitCheck = False, limit = None, pos = None, dict = True) -> dict:
		"""Get page list
		
		Args:
			permitCheck (boolean): check if the bot has permission
			limit (int): number of pages
			pos (int): page's number pos
			
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPageList())
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.page.canGetList() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.page.canGetList() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		limitParam = ''
		if this.getToken():
			limitParam = "&limit=" + limit
		posParam = ''
		if this.getToken():
			posParam = "&pos=" + pos
		
		url = this.getUrl() + "?cmd=bot&api=pagelist" + authorization + limitParam + posParam
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	def getPageList(this, permitCheck = False, limit = None, pos = None, dict = True) -> dict:
		return this.getPages(permitCheck, limit, pos)
	
	def existPage(this, page, permitCheck = False) -> bool:
		"""Check exist page (Get exist api data)
		
		Args:
			page (string): wiki page name
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.existPage("FrontPage"))
		"""
		return this.getExistPageData(page, permitCheck)['exist']
	
	def getExistPageData(this, page, permitCheck = False, dict = True) -> dict:

		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.page.canExistCheck() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.page.canExistCheck() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=exist" + authorization + "&type=page&name=" + page
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	def existPlugin(this, plugin, permitCheck = False) -> bool:
		"""Check exist page (Get exist api data)
		
		Args:
			plugin (string): plugin name
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.existPlugin("bot"))
		"""
		return this.getExistPluginData(plugin, permitCheck)['exist']
	
	def getExistPluginData(this, plugin, permitCheck = False, dict = True):
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.plugin.canExistCheck() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.plugin.canExistCheck() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=exist" + authorization + "&type=plugin&name=" + plugin
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")


	def getPluginList(this, permitCheck = False, dict = True) -> dict:
		"""Get plugin list
		
		Args:
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPluginList())
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.plugin.canGetList() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.plugin.canGetList() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=pluginlist" + authorization
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	# 検索して検索した結果のページ一覧を取得する
	def getSearchPageList(this, word, permitCheck = False, dict = True) -> dict:
		"""
		Search pages by word and return resulting page list
		Args:
			word (string): keyword to searching page
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getSearchPageList("PukiWiki"))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.plugin.canSearch() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.plugin.canSearch() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=search" + authorization + "&word=" + word
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	# 差分のデータを取得する
	def getPageDiff(this, page, permitCheck = False, dict = True) -> dict:
		"""
		Get page difference source
		Args:
			page (string): wiki page name
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPageDiff("FrontPage"))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.diff.canRead() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.diff.canRead() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=diff" + authorization + "&name=" + page
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	# バックアップのデータを取得する (ageが指定されていない場合、ページのバックアップリストが返される)
	def getPageBackup(this, page, age = None, permitCheck = False, dict = True) -> dict:
		"""
		Get page backup data or Get page backup list
		Args:
			page (string): wiki page name
			age (int): backup age
			permitCheck (boolean): check if the bot has permission
		
		Examples:
			>>> bot = pukibot.PukiBot(URL)
				print(bot.getPageBackup("FrontPage", 1))
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.backup.canRead() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.backup.canRead() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		ageParam = ''
		if age != None:
			ageParam = "&age=" + str(age)
		
		url = this.getUrl() + "?cmd=bot&api=backup" + authorization + "&name=" + page + ageParam
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	# プラグインを実行する
	def executePlugin(this, plugin, type = "action" , params = None, permitCheck = False, dict = True) -> dict:
		"""
		Execute plugin
		Args:
			plugin (string): plugin name
			type (string): plugin type (convert, inline, action)
			params (dict): get parameter
			permitCheck (boolean): check if the bot has permission
		"""
		if permitCheck:
			if this.cache_permission:
				if this.cache_permission.permission.plugin.canExecute() == False:
					return False
			elif this.getPermission():
				if this.cache_permission.permission.plugin.canExecute() == False:
					return False
		
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		param = ''
		if params != None:
			for key, value in params.items():
				param += "&" + key + "=" + value
			
		
		url = this.getUrl() + "?cmd=bot&api=plugin" + authorization + "&plugin_type=" + type + "&plugin_name=" + plugin + param
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	# プラグインのコマンドを送信する (executePluginとは違ってAPIを使わずにそのままactionを送信する)
	def actionCmd(this, plugin, params = None) -> str:
		"""
		Execute plugin
		Args:
			plugin (string): command name
			params (dict): get parameter
		"""
		param = ''
		if params != None:
			for key, value in params.items():
				param += "&" + key + "=" + value
			
		
		url = this.getUrl() + "?cmd=" + plugin + param
		return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	def getPageTotal(this, permitCheck = False) -> bool:
		"""Get number of all pages
		
		Args:
			permitCheck (boolean): check if the bot has permission
		"""
		return this.getTotalData("page", permitCheck)['total']
	
	def getPluginTotal(this, permitCheck = False) -> bool:
		"""Get number of all plugins
		
		Args:
			permitCheck (boolean): check if the bot has permission
		"""
		return this.getTotalData("plugin", permitCheck)['total']
	
	def getAttachTotal(this, permitCheck = False) -> bool:
		"""Get number of all attaches
		
		Args:
			permitCheck (boolean): check if the bot has permission
		"""
		return this.getTotalData("attach", permitCheck)['total']
	
	def getBackupTotal(this, permitCheck = False) -> bool:
		"""Get number of all page backups
		
		Args:
			permitCheck (boolean): check if the bot has permission
		"""
		return this.getTotalData("backup", permitCheck)['total']
	
	def getDiffTotal(this, permitCheck = False) -> bool:
		"""Get number of all page differences
		
		Args:
			permitCheck (boolean): check if the bot has permission
		"""
		return this.getTotalData("diff", permitCheck)['total']
	
	
	
	def getTotalData(this, type, permitCheck = False, dict = True) -> dict:
		if permitCheck:
			if this.cache_permission:
				if type == "page":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "plugin":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "attach":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "backup":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "diff":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
			elif this.getPermission():
				if type == "page":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "plugin":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "attach":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "backup":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
				if type == "diff":
					if this.cache_permission.permission.page.canGetTotal() == False:
						return False
		authorization = ''
		if this.getToken():
			authorization = "&authorization=" + this.getToken()
		
		url = this.getUrl() + "?cmd=bot&api=total" + authorization + "&type=" + type
		if dict:
			# Dict型
			return http.getResponseAsJsonMap(url, {'User-Agent': this.getUserAgent()}, None, "GET")
		else:
			# String型
			return http.getResponse(url, {'User-Agent': this.getUserAgent()}, None, "GET")
	
	
	