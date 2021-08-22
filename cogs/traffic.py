import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from modules import jsonreader as jsr
import os

import datetime

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"
traffic_s_folder = "traffic_s"
SvI = ["ServerIcon", "TimeStamp", "Title", "Text"]


class Traffic(commands.Cog):
    def __init__(self, bot):
        """실행하며 필요한 파일들은 paffy_lib로."""
        self.bot = bot
        self.config = jsr.get("config.json")

    # lib 폴더에 길드생성 -> traffic채널 id 저장
    @commands.command(aliases=["트래픽", "joinmessage"])
    @has_permissions(manage_guild=True)
    async def traffic(self, ctx, channelid: str):
        if channelid[:2] == "<#":
            channelid = channelid[2:][:-1]
            if os.path.isfile(f"{path}{ctx.guild.id}/{traffic_file_nm}"):
                f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'r')
                contents = f.read()
                f.close()
                if contents == "0":
                    f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'w')
                    f.write(channelid)
                    f.close()
                    await ctx.reply("설정되었습니다.", mention_author=False)

                else:
                    if contents == channelid:
                        await ctx.reply("기존의 채널과 겹칩니다.", mention_author=False)

                    else:
                        f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'r')
                        msg = await ctx.reply(f"기존에 설정된 채널은 <#{f.read()}>입니다. 바꾸시겠습니까?", mention_author=False)

                        def reaction_check(m):
                            if m.message_id == msg.id and m.user_id == ctx.author.id and str(m.emoji) == "✅":
                                return True
                            return False

                        try:
                            await msg.add_reaction("✅")
                            await self.bot.wait_for('raw_reaction_add', timeout=10.0, check=reaction_check)
                            await ctx.reply("ss", mention_author=False)

                        except asyncio.TimeoutError:
                            await msg.delete()
                            await ctx.reply("시간초과입니다.", mention_author=False)

            else:
                await ctx.reply("필요한 파일이 아직 생성되지 않았습니다. 다시 시도해주세요.", mention_author=False)

        else:
            await ctx.reply("대상이 채널이 아닙니다.", mention_author=False)

    @traffic.error
    async def traffic_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("**Manage Server** 권한이 필요합니다.", mention_author=False)

    @commands.command(aliases=["트래픽세팅", "트래픽설정"])
    @has_permissions(manage_guild=True)
    async def traffic_set(self, ctx):
        if os.path.isfile(f"{path}{ctx.guild.id}/{traffic_file_nm}"):
            array = []
            for i in range(0, 4):
                f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[i]}.txt", 'r')
                array.append(f.read())
                f.close()
                if i < 2:
                    if array[i] == "1":
                        array[i] = "✅"
                    else:
                        array[i] = "❌"
            liww = "\n\n"
            embed = discord.Embed(
                title="무엇을 수정하시겠습니까?",
                description=f"1. ServerIcon: {array[0]}{liww}2. TimeStamp: {array[1]}{liww}"
                            f"3. Title: {array[2]}{liww}4. Text: {array[3]}",
                timestamp=datetime.datetime.utcnow(),
                color=0xFA747D
            )
            embed.set_thumbnail(
                url=ctx.guild.icon_url
            )
            msg = await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msgt = await self.bot.wait_for("message", timeout=10.0, check=check)
                if msgt.content == "1":
                    await ctx.send("수정되었습니다.")
                    await msg.delete()
                    f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[0]}.txt", 'r')
                    if f.read() == "1":
                        f.close()
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[0]}.txt", 'w')
                        f.write("0")
                        f.close()
                    else:
                        f.close()
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[0]}.txt", 'w')
                        f.write("1")
                        f.close()
                elif msgt.content == "2":
                    f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[1]}.txt", 'r')
                    if f.read() == "1":
                        f.close()
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[1]}.txt", 'w')
                        f.write("0")
                        f.close()
                    else:
                        f.close()
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[1]}.txt", 'w')
                        f.write("1")
                        f.close()
                elif msgt.content == "3":
                    try:
                        await ctx.send("입력해주세요. ")
                        msge = await self.bot.wait_for("message", timeout=40.0, check=check)
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[2]}.txt", 'w')
                        f.write(msge.content)
                        f.close()
                    except asyncio.TimeoutError:
                        await ctx.reply("시간초과입니다.", mention_author=False)
                else:
                    try:
                        await ctx.send("입력해주세요.")
                        msge = await self.bot.wait_for("message", timeout=40.0, check=check)
                        f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[3]}.txt", 'w')
                        f.write(msge.content)
                        f.close()
                    except asyncio.TimeoutError:
                        await ctx.reply("시간초과입니다.", mention_author=False)

                array = []
                for i in range(0, 4):
                    f = open(f"{path}{ctx.guild.id}/{traffic_s_folder}/{SvI[i]}.txt", 'r')
                    array.append(f.read())
                    f.close()
                    if i < 2:
                        if array[i] == "1":
                            array[i] = "✅"
                        else:
                            array[i] = "❌"
                liww = "\n\n"
                embed = discord.Embed(
                    title="무엇을 수정하시겠습니까?",
                    description=f"1. ServerIcon: {array[0]}{liww}2. TimeStamp: {array[1]}{liww}"
                                f"3. Title: {array[2]}{liww}4. Text: {array[3]}",
                    timestamp=datetime.datetime.utcnow(),
                    color=0xFA747D
                )
                embed.set_thumbnail(
                    url=ctx.guild.icon_url
                )
                msg = await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.reply("시간초과입니다.", mention_author=False)

        else:
            await ctx.reply("필요한 파일이 아직 생성되지 않았습니다. 다시 시도해주세요.", mention_author=False)

    @traffic_set.error
    async def traffic_s_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("**Manage Server** 권한이 필요합니다.", mention_author=False)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if os.path.isfile(f"{path}{member.guild.id}/{traffic_file_nm}"):
            f = open(f"{path}{member.guild.id}/{traffic_file_nm}", 'r')
            contents = f.read()
            f.close()
            if contents != "0":
                channel = discord.utils.get(member.guild.channels, id=int(contents))

                servericon = open(f"{path}{member.guild.id}/{traffic_s_folder}/{SvI[0]}.txt", 'r')
                timestamp = open(f"{path}{member.guild.id}/{traffic_s_folder}/{SvI[1]}.txt", 'r')
                title = open(f"{path}{member.guild.id}/{traffic_s_folder}/{SvI[2]}.txt", 'r')
                text = open(f"{path}{member.guild.id}/{traffic_s_folder}/{SvI[3]}.txt", 'r')

                embed = discord.Embed(
                    title=f"{title.read()}",
                    description=f"{text.read()}",
                    color=0xFA747D
                )
                if servericon == "1":
                    embed.set_thumbnail(
                        url=member.guild.icon_url
                    )
                if timestamp == "1":
                    embed.timestamp = datetime.datetime.utcnow()

                embed.set_author(
                    name=member,
                    icon_url=member.avatar_url
                )
                servericon.close()
                timestamp.close()
                title.close()
                text.close()

                await channel.send(embed=embed)

        else:
            print(f"no lib yet {member.guild.id}")


def setup(bot):
    bot.add_cog(Traffic(bot))
