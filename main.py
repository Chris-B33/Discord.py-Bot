phrases = [
    "Welcome to the server! Hope you enjoy your stay :D",
    "Aww, sad to see you leave ;(",
    "Alright then, I see how it is ;("
]


from lib.server import Server
from lib.music  import Music
from lib.bot    import Bot


bot = Bot("roles.json", "presets.json", "a!")

bot.add_cog(Music(bot))
bot.add_cog(Server(bot, phrases))

token = open("token.txt", "r").read()
bot.run(token)