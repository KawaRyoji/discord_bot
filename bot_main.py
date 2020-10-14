import discord
from commands import Commands

TOKEN = "NzE1ODQ2NDA1OTMwODc2OTgw.XtDJ6g.xf98SLNgGXkhl7o-qobCHZkIuNw"

class Bot(discord.Client):
    async def on_ready(self):
        print("login as")
        print(self.user.name)
        print(self.user.id)
        print("-----------")

    async def on_message(self, message):
        ins = Commands(self)
        await ins.run_commands(message)

bot = Bot()
bot.run(TOKEN)