import discord, json
from discord.ext import commands


WELCOME = "Welcome to the server! Hope you enjoy your stay :D"
LEAVE   = "Aww, sad to see you leave ;("
REMOVED = "Alright then, I see how it is ;("


class Bot(commands.Bot):

    def __init__(self, prefix):
        super().__init__(
            command_prefix=commands.when_mentioned_or(prefix)
        )
        with open("roles.json", "r") as data:
            self.roles = json.load(data)


    async def on_ready(self):
        print(f"{bot.user} connected...")


    async def on_member_join(self, member):
        if not member.bot:
            await member.send(WELCOME)

        # Add default role if present
        bots = discord.utils.get(member.guild.roles, name=self.roles["bots"]["name"])
        default = discord.utils.get(member.guild.roles, name=self.roles["default"]["name"])

        if member.bot:
            await member.add_roles(bots)
        else:
            await member.add_roles(default)
        '''for role in member.guild.roles:
            name = self.roles["default"]["name"]
            if role.name == name:
                role = discord.utils.get(member.guild.roles, name=name)
                await member.add_roles(role)
                break'''


    async def on_member_leave(self, member):
        await member.send(LEAVE)


    async def on_guild_remove(self, guild):
        owner = guild.owner
        await owner.send(REMOVED)


class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        brief="Creates categories and channels from an existing preset (1-3)",
        description='''
            Creates categories with channels inside from an existing preset specified (1-3).
            1: Small
            2: Medium
            3: Large
        '''
    )
    @commands.has_permissions(administrator=True)
    async def create_server(self, ctx, num: int):
        guild = ctx.guild

        await ctx.send("Loading preset...")
        with open("presets.json", "r") as server:
            sets = json.load(server)
            preset = sets["presets"][num-1]

        await ctx.send("Creating roles...")
        admin   = await self.create_role_from_file(guild, bot.roles["admin"])
        bots    = await self.create_role_from_file(guild, bot.roles["bots"])
        default = await self.create_role_from_file(guild, bot.roles["default"])

        await guild.owner.add_roles(admin)
        for member in guild.members:
            if member.bot:
                await member.add_roles(bots)
            else:
                await member.add_roles(default)

        await ctx.send("Adding categories and channels...")
        for category in preset["categories"]:
            cat = await guild.create_category(category["name"])
            for channel in category["channels"]:
                if channel[1] == "t":
                    await guild.create_text_channel(name=channel[0], category=cat)
                else:
                    await guild.create_voice_channel(name=channel[0], category=cat)

        await ctx.send("Done!")


    def create_role_from_file(self, server, role):
        role = server.create_role(
            name        = role["name"],
            colour      = discord.Colour(int(role["colour"], base=16)),
            permissions = discord.Permissions(role["perms"]),
            hoist       = role["hoist"],
            mentionable = role["mentionable"],
            reason      = role["reason"]
        )
        return role


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        brief = "Joins the message author's voice channel.",
        description = '''
            Command to join the current voice channel of the message author,
            if in one at all.
        '''
    )
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        else:
            await ctx.send("I'm already in the same chat :/")


    @commands.command(
        brief = "Leaves the current voice channel.",
        description = '''
            Command to leave the current voice channel if in one at all.
        '''
    )
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Bitch fuck off")


if __name__ == "__main__":
    bot = Bot("a!")
    bot.add_cog(Music(bot))
    bot.add_cog(Server(bot))

    token = open("token.txt", "r").read()
    bot.run(token)