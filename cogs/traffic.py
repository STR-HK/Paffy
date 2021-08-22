import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from modules import jsonreader as jsr
import os

import datetime

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"


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

                        except Exception as e:
                            print(f'Error: {e}')
                            await msg.delete()
                            await ctx.reply("시간초과입니다.", mention_author=False)

            else:
                await ctx.reply("필요한 파일이 아직 생성되지 않았습니다.", mention_author=False)

        else:
            await ctx.reply("대상이 채널이 아닙니다.", mention_author=False)

    @traffic.error
    async def traffic_error(self, ctx, error):
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
                embed = discord.Embed(
                    title=f"{member.guild.name}에 온 것을 환영합니다",
                    description=f"{member.display_name}이(가) {member.guild.name}에 떨어졌습니다.",
                    timestamp=datetime.datetime.utcnow(),
                    color=0xFA747D
                )
                embed.set_author(
                    name=member,
                    icon_url=member.avatar_url
                )
                embed.set_thumbnail(
                    url=member.guild.icon_url
                )
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Traffic(bot))
