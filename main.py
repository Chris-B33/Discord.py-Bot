from discord.ext import commands

TOKEN = open("token.txt", "r").readline()

client = commands.Bot(command_prefix="a!")

@client.event
async def on_ready():
    print(f"{client.user} connected...")

client.run(TOKEN)