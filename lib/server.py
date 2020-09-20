import discord
from discord.ext import commands
from .progress import ProgressBar


class Server(commands.Cog):

    def __init__(self, bot, phrases):
        self.bot = bot
        self.welcome = phrases[0]
        self.leave = phrases[1]
        self.removed = phrases[2]


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

        if not member.bot:
            await member.send(self.welcome)

        bots = discord.utils.get(member.guild.roles, name=self.roles["bots"]["name"])
        default = discord.utils.get(member.guild.roles, name=self.roles["default"]["name"])

        if member.bot:
            await member.add_roles(bots)
        else:
            await member.add_roles(default)


    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.member):
        await member.send(self.leave)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.guild):
        owner = guild.owner
        await owner.send(self.removed)


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

        progress = ProgressBar(ctx)
        await progress.start(ctx)

        guild = ctx.guild
        preset = self.presets["presets"][num-1]

        admin   = await self.create_role_from_file(guild, self.roles["admin"])
        bots    = await self.create_role_from_file(guild, self.roles["bots"])
        default = await self.create_role_from_file(guild, self.roles["default"])

        await progress.update(33, "Creating Roles...")

        await guild.owner.add_roles(admin)
        for member in guild.members:
            if member.bot:
                await member.add_roles(bots)
            else:
                await member.add_roles(default)

        await progress.update(66, "Creating Categories and Channels...")

        for category in preset["categories"]:
            cat = await guild.create_category(category["name"])
            for channel in category["channels"]:
                if channel[1] == "t":
                    await guild.create_text_channel(name=channel[0], category=cat)
                else:
                    await guild.create_voice_channel(name=channel[0], category=cat)

        await progress.update(100, "Done! :D")


    def create_role_from_file(self, server: discord.Guild, role: discord.Role):
        role = server.create_role(
            name        = role["name"],
            colour      = discord.Colour(int(role["colour"], base=16)),
            permissions = discord.Permissions(role["perms"]),
            hoist       = role["hoist"],
            mentionable = role["mentionable"],
            reason      = role["reason"]
        )
        return role