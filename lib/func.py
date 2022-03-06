import re

# おそらく使わなくなった関数
# ソースコードの#author(...)から最終更新日時を取り出します (形式: xxxx-xx-xxTxx:xx:xx+xx:xx)
def getLastModifiedTime(source):
	m = re.search(r"^#author\(\"(.*?)(?:;.*?)?\",", source)
	return m.group(1)
	
# ソースコードの#author(...)からユーザーネームを取り出します
def getAuthorName(source):
	m = re.search(r"^#author\(\".*?\",\"(.*?)\"", source)
	return m.group(1)
	
# ソースコードの#author(...)からフルネームを取り出します
def getAuthorFullName(source):
	m = re.search(r"^#author\(\".*?\",\".*?\",\"(.*?)\"", source)
	return m.group(1)
	
def convertSourceFromPreSource(str):
	str = str.replace("&amp;", "&")
	str = str.replace("&lt;", "<")
	str = str.replace("&gt;", ">")
	str = str.replace("&quot;", "\"")
	return str
