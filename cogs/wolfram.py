from discord.ext import commands
from modules import jsonreader as jsr
from wolframalpha import *


class Wolframalpha(commands.Cog):
    def __init__(self, bot):
        """config읽어오기"""
        self.bot = bot
        self.config = jsr.get("config.json")

    @commands.command(aliases=["풀기", "풀어"])
    async def solve(self, ctx, *, ask: str):
        app_id = self.config.wolframapi
        client = Client(app_id)
        try:
            res = client.query(ask)
            resarray = []
            for pod in res.pods:
                for sub in pod.subpods:
                    resarray.append(str(sub.img)[10:str(sub.img).find("'", 11)])

        except Exception as e:
            await ctx.reply(f"에러가 발생했어요. {e}", mention_author=False)
            return

        for i in range(1, len(resarray)):
            await ctx.send(resarray[i])


def setup(bot):
    bot.add_cog(Wolframalpha(bot))
