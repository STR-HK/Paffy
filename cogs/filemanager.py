from discord.ext import commands
from modules import jsonreader as jsr
import os

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"

class Filemanager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = jsr.get("config.json")

    # Commands
    @commands.Cog.listener()
    async def on_message(self, message):
        serverid = message.guild.id
        if not os.path.isdir(f"{path}{serverid}"):
            os.mkdir(f"{path}{serverid}")
        if not os.path.isfile(f"{path}{traffic_file_nm}"):
            f = open(f"{path}{serverid}/{traffic_file_nm}", 'w')
            f.close()


def setup(bot):
    bot.add_cog(Filemanager(bot))