import discord.ext.commands

TOKEN           = open("token.txt", "r").readline()
DEFAULT_ROLE    = "Newcomers"
DEFAULT_MSG     = "Welcome to the server! Hope you enjoy your stay :D"

client = discord.ext.commands.Bot(command_prefix="a!")

@client.event
async def on_ready():
    print(f"{client.user} connected...")

@client.event
async def on_member_join(member):
    await member.send(DEFAULT_MSG)

    # Checks if default role is present
    for role in member.guild.roles:
        if role.name == DEFAULT_ROLE:
            role = discord.utils.get(member.server.roles, name=DEFAULT_ROLE)
            await member.add_roles(role)
            break
    else:
        role = await member.guild.create_role(name=DEFAULT_ROLE,
                                              colour=discord.Colour(0xf8f8f8))
        await member.add_roles(role)

client.run(TOKEN)