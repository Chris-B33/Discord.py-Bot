import discord, json, youtube_dl
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
        await member.send(WELCOME)

        # Checks if default role is present
        for role in member.guild.roles:
            name = self.roles["default"]["name"]
            if role.name == name:
                role = discord.utils.get(member.guild.roles, name=name)
                await member.add_roles(role)
                break
        else:
            default = self.create_role_from_file(member.guild, self.roles["default"])
            for member in member.guild.members:
                await member.add_roles(default)

    async def on_member_leave(self, member):
        await member.send(LEAVE)

    async def on_guild_remove(self, guild):
        owner = guild.owner
        await owner.send(REMOVED)

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
    async def create_server(self, ctx, num):
        guild = ctx.guild

        # Load matching preset
        await ctx.send("Loading preset...")
        with open("presets.json", "r") as server:
            sets = json.load(server)
            preset = sets["presets"][num - 1]

        # Create and Add roles
        await ctx.send("Creating roles...")
        admin = await self.create_role_from_file(guild, self.roles["admin"])
        bots = await self.create_role_from_file(guild, self.roles["bots"])
        default = await self.create_role_from_file(guild, self.roles["default"])

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
                else:
                    await guild.create_voice_channel(name=channel[0], category=cat)

        await ctx.send("Done!")


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
        # Joins channel
        try:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await channel.connect()
            else:
                # If already in the same chat
                await ctx.send("I'm already in the same chat :/")
        except:
            # If message author not in a chat
            await ctx.send("You are not currently in a channel...")

    @commands.command(
        brief = "Leaves the current voice channel.",
        description = '''
            Command to leave the current voice channel if in one at all.
        '''
    )
    async def leave(self, ctx):
        try:
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
            else:
                raise Exception
        except:
            # Not in a channel
            await ctx.send("I am not currently in a channel...")


if __name__ == "__main__":
    bot = Bot("a!")
    bot.add_cog(Music(bot))
    bot.add_cog(Server(bot))

    with open("token.txt", "r") as token:
        bot.run(token)