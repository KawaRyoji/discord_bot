import discord
from commands import Commands
import sys

class Bot(discord.Client):
    async def on_ready(self):
        print("login as")
        print(self.user.name)
        print(self.user.id)
        print("-----------")

    async def on_message(self, message):
        ins = Commands(self)
        await ins.run_commands(message)

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("Input your bot token to command line argument")
        exit()

    TOKEN = args[1]

    bot = Bot()
    bot.run(TOKEN)