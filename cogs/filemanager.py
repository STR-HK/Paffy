from discord.ext import commands
from modules import jsonreader as jsr
import os

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"
traffic_s_folder = "traffic_s"
SvI = ["ServerIcon", "TimeStamp", "Title", "Text"]


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

        if not os.path.isdir(f"{path}{serverid}/{traffic_s_folder}"):
            os.mkdir(f"{path}{serverid}/{traffic_s_folder}")
            for i in range(0, 2):
                f = open(f"{path}{serverid}/{traffic_s_folder}/{SvI[i]}.txt", 'w')
                f.write("1")
                f.close()
            f = open(f"{path}{serverid}/{traffic_s_folder}/{SvI[2]}.txt", 'w')
            f.write("{{GuildName}}에 오신 것을 환영합니다!")
            f.close()
            f = open(f"{path}{serverid}/{traffic_s_folder}/{SvI[3]}.txt", 'w')
            f.write("{{UserName}} 은/는 {{GuildName}}의 {{Counts}}번째 손님입니다!")
            f.close()


def setup(bot):
    bot.add_cog(Filemanager(bot))
