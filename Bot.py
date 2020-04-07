import asyncio
import discord
import requests
from discord.ext.commands import Bot
from discord import Game
from bs4 import BeautifulSoup
from urllib.parse import unquote

client = Bot(command_prefix = "")

async def Google(q):
	searchpage = requests.get("https://www.google.co.kr/search?q={}".format(q))
	bsoup = BeautifulSoup(searchpage.content, 'html.parser')
	message = ""
	results = bsoup.findAll("div", attrs={"class":"g"})
	for result in results:
		h3 = result.find("h3", attrs={"class":"r"}, recursive=True)
		if h3 != None:
			a = h3.find("a")
			txt = h3.text
			link = a.get("href")
			link = link.replace("/url?q=", "")
			link = link.replace("/search?", "https://www.google.co.kr/search?")
			link = link[:link.rfind("&sa=U")]
			link = unquote(link)
			message += "{}\n{}\n\n".format(txt,link)
			if len(message) > 1600:
				break
	return message

@client.command(pass_context=True)
async def google(context, args="구글"):
    if len(args) > 1:
        try:
            searchQuery = "".join(args[0:])
            messageString = await Google(searchQuery)
            em = discord.embed(title="\"{}\"에 대한 구글 검색결과".format(searchQuery), description=messageString, colour=0x8FACEf)
            await client.send_message(context.message.channel, embed=em)
        except:
            await client.send_message(context.message.channel, "구글로부터 검색 결과를 가져올 수 없습니다")

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="google <검색어>"))
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run("")
