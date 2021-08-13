import discord
from discord.ext import commands
from modules import jsonreader as jsr


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = jsr.get("config.json")

    # Commands
    @commands.command(name="say")
    async def _say(self, ctx, *, content: str):
        async with ctx.typing():
            await ctx.message.delete()
        if "@everyone" in content:
            embed = discord.Embed(title="NO", description='You cannot do that', color=0xeff0f1)
            await ctx.send(embed=embed)
        else:
            await ctx.send(content)


def setup(bot):
    bot.add_cog(Say(bot))