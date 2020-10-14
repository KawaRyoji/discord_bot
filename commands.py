from scraping import scraping
import discord
import random

class Commands:
    class Command:
        def __init__(self, com: str, *args):
            self.command = com
            self.args = args

        def get_command(self):
            return self.command
        
        def get_args(self):
            return self.args

    def __init__(self, client: discord.Client):
        self.client = client
        self.prefix = "!"

        self.commands = [
            {
                "name"          : "commands",
                "function"      : self.commands,
                "args"          : False,
                "description"   : "コマンドの一覧を取得します。"
            },
            {
                "name"          : "omikuzi",
                "function"      : self.omikuzi,
                "args"          : False,
                "description"   : "今日の運勢を占います。"
            },
            {
                "name"          : "dice",
                "function"      : self.dice,
                "args"          : True,
                "description"   : "(回数)d(面数)を引数とし, サイコロを振ります。"
            },
            {
                "name"          : "clear",
                "function"      : self.clear,
                "args"          : False,
                "description"   : "自分に宛てられたbotのメッセージを削除します。"
            },
            {
                "name"          : "clearall",
                "function"      : self.clearAll,
                "args"          : False,
                "description"   : "全てのbotのメッセージを削除します。(要管理者権限)"
            },
            {
                "name"          : "tenki",
                "function"      : self.tenki,
                "args"          : False,
                "description"   : "名古屋と横浜の今日明日の天気を表示します。"
            }
        ]

    # コマンドを実行
    async def run_commands(self, message : discord.message):
        # メッセージがbotであれば無視する
        if message.author.bot:
            return

        if not message.content.startswith(self.prefix):
            return

        c = await self.command_format(message.content)

        for command in self.commands:
            if c.get_command() == self.prefix + command["name"]:
                func = command["function"]
                if command["args"]:
                    await func(message, c.get_args())
                else:
                    await func(message)
                
                await message.delete()
                return

        await self.send_message(message, "「" + c.get_command() + "」はコマンドに登録されていません")
        await message.delete()
    
    # メッセージをコマンドと引数に分ける
    async def command_format(self, message: str):
        s = message.split(" ")
        if len(s) == 1:
            return Commands.Command(s[0])
        else:
            args = s[1:]
            return Commands.Command(s[0], *args)

    # これでメッセージを送信する
    async def send_message(self, message: discord.message, s_message: str):
        await message.channel.send("{}\n{}".format(message.author.mention, s_message))

    # ----------------コマンドの実装部分----------------

    # コマンド一覧を取得
    async def commands(self, message: discord.message):
        res = "{}\nコマンド一覧:\n".format(message.author.mention)
        for command in self.commands:
            res += "\t{0}:\n\t\t{1}\n".format(command["name"], command["description"])
        
        await message.channel.send(res)

    # おみくじ(やるたびに結果が違う)
    async def omikuzi(self, message: discord.message):
        yaku = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶"]
        res = random.choice(yaku)
        await self.send_message(message, "今日の運勢は「"+ res +"」です！")

    # ndmでサイコロを振る
    async def dice(self, message: discord.message, *args):
        """ フォーマットは ndm """
        if len(args) == 0:
            await self.send_message(message, "コマンドの後に空白を開けて必要な情報を入れてね")
            return

        try:
            times, sides = map(int, args[0][0].split('d'))
        except Exception:
            await self.send_message(message, "何回(数字)d何面(数字) と指定してね\n例: 10d6")
            return

        if times <= 0 or sides <= 0:
            await self.send_message(message, "数字は1以上の整数で入力してね")
            return

        result = args[0][0] + "の結果:\n"
        for i in range(1, times+1):
            result += "{:2d}".format(random.randint(1, sides))
            if i != times:
                result += ","
            if i % 10 == 0:
                result += "\n"

        await self.send_message(message, result)

    # コマンド実行者へのメンションをしているbotのメッセージを全部消す
    async def clear(self, message: discord.message):
        author = message.author
        async for msg in message.channel.history(limit=100):
            mentions = msg.mentions
            
            if not mentions:
                continue

            if len(mentions) == 1 and author.mention == mentions[0].mention and msg.author.bot:
                await msg.delete()

    # botのメッセージ全部消す
    async def clearAll(self, message: discord.message):
        if not message.author.guild_permissions.administrator:
            await self.send_message(message, "コマンド実行権限がありません")
            return
        
        async for msg in message.channel.history(limit=100):
            if msg.author.bot:
                await msg.delete()

    # 今日明日の天気を表示する
    async def tenki(self, message: discord.message):
        sc = scraping()
        whether = sc.forecast("名古屋", "横浜")

        await self.send_message(message, whether)
