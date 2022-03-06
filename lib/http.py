from urllib import request
import urllib.parse
import json
import traceback

# getResponseで得たものをJsonのマップ(辞書型)で返す
def getResponseAsJsonMap(url, header = None, data = None, method = "GET"):
	try:
		res = getResponse(url, header, data, method);
		if res == False:
			return False
		return json.loads(res)
	except:
		traceback.print_exc()
		return False

# Stringをマップ(辞書型)で返す
def toMap(str):
	try:
		if str == False:
			return False
		return json.loads(str)
	except:
		traceback.print_exc()
		return False

# Bot APIとのやり取りをするための関数
def getResponse(url, header = None, data = None, method = "GET"):
	try:
		header2 = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
			"content-type": "application/x-www-form-urlencoded"
		}
		if header != None:
			header2.update(header)
		if data != None:
			data = urllib.parse.urlencode(data).encode('utf-8')
		
		req = urllib.request.Request(url, data=data, headers=header2, method=method)
		res = request.urlopen(req)
		content = res.read()
		res.close()
		return content.decode()
	except urllib.error.HTTPError as e:
		traceback.print_exc()
		content = e.read()
		return content.decode()
	except:
		traceback.print_exc()
		return False