users = [
  1054703619640938506, # akkuメイン垢
  1133269027658149918, # サブ
  1190660123211874317, # あかり
]

import discord
import os
import aiohttp
import tempfile
import re
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(msg:discord.Message):
  if msg.author.id not in users:
    return
  if re.match("^:.*?:$", msg.content):
    emoji:list = msg.content.removeprefix(":").removesuffix(":").split("@")
    if(len(emoji)==1):
      emoji[1] = "misskey.io"
    with tempfile.TemporaryFile(mode="w+b") as fp:
      async with aiohttp.ClientSession() as aio:
        async with aio.get("https://"+emoji[1]+"/emoji/"+emoji[0]+".webp") as resp:
          if resp.status == 200:
            fp.write(await resp.read())
            fp.seek(0)
          else:
            return
      await msg.channel.send(file=discord.File(fp, filename = f'emoji-{emoji[0]}-{emoji[1]}.webp', spoiler=False))

client.run(str(TOKEN))
