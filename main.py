import json
import discord
from discord.ext.commands import Bot
import re
from aiohttp import web
import asyncio

intents = discord.Intents().all()
client = Bot(intents=intents, command_prefix="*")
with open('config.json') as file:
    config_data = json.load(file)
TOKEN = config_data["token"]
guild = None

async def check_user_status(request):
    userid = request.match_info.get('userid')
    if not re.match(r'^\d+$', userid):
        return web.Response(text="Wrong ID format")

    user = guild.get_member(int(userid))
    if user is None:
        return web.Response(text="User is not in my server")
    else:
        return web.Response(text=str(user.status))

async def start_bot():
    global guild
    await client.wait_until_ready()
    guild = client.get_guild(int(config_data["guild"]))
    print(guild)

    app = web.Application()
    app.router.add_get('/{userid}', check_user_status)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 9069)
    await site.start()

@client.event
async def on_ready():
    await client.get_channel(int(config_data["messagechannel"])).send("Stalking Echo")
    await start_bot()

async def main():
    await client.start(TOKEN)

asyncio.run(main())
