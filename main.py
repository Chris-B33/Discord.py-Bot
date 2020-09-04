import discord, json
from discord.ext import commands


with open("settings.json", "r") as data:
    settings = json.load(data)

client = discord.ext.commands.Bot(command_prefix="a!")


@client.event
async def on_ready():
    print(f"{client.user} connected...")

@client.event
async def on_member_join(member):
    await member.send(settings["welcome"])

    # Checks if default role is present
    for role in member.guild.roles:
        name = settings["role"]["name"]
        if role.name == name:
            role = discord.utils.get(member.guild.roles, name=name)
            await member.add_roles(role)
            break
    else:
        role = await member.guild.create_role(
            name        = settings["role"]["name"],
            colour      = discord.Colour(int(settings["role"]["colour"], base=16)),
            permissions = discord.Permissions(settings["role"]["perms"]),
            hoist       = settings["role"]["hoist"],
            mentionable = settings["role"]["mentionable"],
            reason      = settings["role"]["reason"]
        )
        for member in member.guild.members:
            await member.add_roles(role)

@client.event
async def on_guild_remove(guild):
    owner = guild.owner
    await owner.send("Alright then, I see how it is ;(")


client.run(settings["token"])