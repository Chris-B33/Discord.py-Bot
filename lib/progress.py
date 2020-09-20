class ProgressBar:

    def __init__(self, ctx):
        self.progress = 0
        self.ctx = ctx

        self.bar = None
        self.message = None


    async def start(self, ctx):
        self.message = await ctx.send("Loading...")
        self.bar = await ctx.send("**[" + "-" * 51 + "]**")


    async def update(self, progress: int, message: str):
        # Update Progress
        if progress > self.progress:
            self.progress = progress
        else:
            return "Invalid"

        content = self.bar.content
        load = round(25*progress/100)

        current = "".join([
             content[:3:],
             "#"*load,
             "-"*(50-(load*2)),
             content[len(content)-3::]
        ])

        await self.bar.edit(content=current)
        await self.message.edit(content=message)