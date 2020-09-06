import discord, json, threading, time, datetime
from discord.ext.commands import Bot


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
        default = create_new_role(member.guild, settings["default"])
        for member in member.guild.members:
            await member.add_roles(default)

@client.event
async def on_guild_remove(guild):
    owner = guild.owner
    await owner.send("Alright then, I see how it is ;(")


@client.command()
async def create_server(ctx, num: int):
    guild = ctx.guild

    # Load matching preset
    with open("presets.json", "r") as server:
        sets = json.load(server)

    await ctx.send("Loading preset...")
    preset = sets["presets"][num-1]

    # Create and Add roles
    await ctx.send("Creating roles...")
    admin = await create_new_role(guild, settings["admin"])
    bots = await create_new_role(guild, settings["bots"])
    default = await create_new_role(guild, settings["default"])

    await guild.owner.add_roles(admin)
    for member in guild.members:
        if member.bot:
            await member.add_roles(bots)
        else:
            await member.add_roles(default)

    # Create categories and channels
    await ctx.send("Adding categories and channels...")
    for category in preset["categories"]:
        cat = await guild.create_category(category["name"])
        for channel in category["channels"]:
            if channel[1] == "t":
                await guild.create_text_channel(name=channel[0], category=cat)
            elif channel[1] == "v":
                await guild.create_voice_channel(name=channel[0], category=cat)
            elif channel[1] == "ann":
                await guild.create_text_channel(name=channel[0], category=cat)
            else:
                await guild.create_voice_channel(name=channel[0], category=cat)

    await ctx.send("Done!")


def create_new_role(server, role: dict):
    role = server.create_role(
        name        = role["name"],
        colour      = discord.Colour(int(role["colour"], base=16)),
        permissions = discord.Permissions(role["perms"]),
        hoist       = role["hoist"],
        mentionable = role["mentionable"],
        reason      = role["reason"]
    )
    return role


client.run(settings["token"])