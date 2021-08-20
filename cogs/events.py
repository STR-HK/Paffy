import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from modules import jsonreader as jsr


class Events(commands.Cog):
    def __init__(self, bot):
        """
        봇의 초기상태를 설정하는 모듈.
        """
        self.bot = bot
        self.config = jsr.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_ready(self):
        """ The function that actiavtes when boot was completed """
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        # Indicate that the bot has successfully booted up
        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)}')

        # Check if user desires to have something other than online
        if self.config.status_type == "idle":
            status_type = discord.Status.idle
        elif self.config.status_type == "dnd":
            status_type = discord.Status.dnd
        else:
            status_type = discord.Status.online

        # Check if user desires to have a different type of playing status
        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=discord.Activity(type=playing_type, name=self.config.playing),
            status=status_type
        )


def setup(bot):
    bot.add_cog(Events(bot))
