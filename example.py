from lib import pukibot

# PukiWikiのURL
URL = "https://pukiwiki.example.com/"

bot = pukibot.PukiBot(URL, 'MDhEOTQ2MjE4NjJDRjAwRjdGNzhCNDlEQTgxN0RBMzk')

print(bot.getPage("FrontPage")['source'])
