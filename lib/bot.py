import json
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self, roles_file: str, presets_file: str, prefix: str):
        super().__init__(
            command_prefix=commands.when_mentioned_or(prefix)
        )

        with open(roles_file, "r") as roles:
            self.roles = json.load(roles)

        with open(presets_file, "r") as presets:
            self.presets = json.load(presets)


    async def on_ready(self):
        print(f"{self.user} connected...")