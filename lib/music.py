from discord.ext import commands


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


    @commands.command(
        brief = "Leaves the current voice channel.",
        description = '''
            Command to leave the current voice channel if in one at all.
        '''
    )
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()


    @commands.command(
        brief="Plays song in voice channel.",
        description='''
            Command to join the message author's voice channel
            and play a desired link/song.
        '''
    )
    async def play(self, ctx):
        await self.join()