from discord.ext import commands
from modules import jsonreader as jsr
import os

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"

class Filemanager(commands.Cog):
    def __init__(self, bot):
        """실행하며 필요한 파일들은 paffy_lib로."""
        self.bot = bot
        self.config = jsr.get("config.json")

    # lib 폴더에 길드생성 -> traffic채널 id 저장
    @commands.Cog.listener()
    async def on_message(self, message):
        serverid = message.guild.id
        if not os.path.isdir(f"{path}{serverid}"):
            os.mkdir(f"{path}{serverid}")
        if not os.path.isfile(f"{path}{serverid}/{traffic_file_nm}"):
            f = open(f"{path}{serverid}/{traffic_file_nm}", 'w')
            f.write("0")
            f.close()


def setup(bot):
    bot.add_cog(Filemanager(bot))
