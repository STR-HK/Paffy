import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from modules import jsonreader as jsr
import os

import datetime
import json
import sys

path = "./paffy_lib/"
traffic_file_nm = "trafficch.txt"
traffic_cus_nm = 'trafficcus.txt'

default = {
    'AuthorText' : 'Member',
    'AuthorIcon' : 'Avatar',
    'Title' : "GuildName에 떨어진 것을 환영합니다",
    'Description' : "DisplayName이(가) GuildName에 MemberCount번째로 떨어졌습니다.",
    'Thumbnail' : 'GuildIcon',
}

class Traffic(commands.Cog):
    def __init__(self, bot):
        """실행하며 필요한 파일들은 paffy_lib로."""
        self.bot = bot
        self.config = jsr.get("config.json")

    # lib 폴더에 길드생성 -> traffic채널 id 저장
    @commands.command(aliases=["트래픽", "joinmessage"])
    @has_permissions(manage_guild=True)
    async def traffic(self, ctx, channelid: str):
        # 채널명인지 아닌지 판별
        if channelid[:2] == "<#":
            channelid = channelid[2:][:-1]
            # 트래픽 파일 없다면 생성
            if not os.path.isfile(f"{path}{ctx.guild.id}/{traffic_file_nm}"):
                f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'w')
                f.write("0")
                f.close()
                
            # 트래픽 파일 읽어옴
            f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'r')
            contents = f.read()
            f.close()

            # 비어있으면 적기
            if contents == "0":
                f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'w')
                f.write(channelid)
                f.close()
                await ctx.reply("설정되었습니다.", mention_author=False)

            # 기존과 동일하면 중복메시지
            else:
                if contents == channelid:
                    await ctx.reply("기존의 채널과 겹칩니다.", mention_author=False)

                # 기존과 다르면 물어보기
                else:
                    f = open(f"{path}{ctx.guild.id}/{traffic_file_nm}", 'r')
                    msg = await ctx.reply(f"기존에 설정된 채널은 <#{f.read()}>입니다. 바꾸시겠습니까?", mention_author=False)

                    def reaction_check(m):
                        if m.message_id == msg.id and m.user_id == ctx.author.id and str(m.emoji) == "✅":
                            return True
                        return False

                    # 여기에 설정하는 기능 넣으세요
                    try:
                        await msg.add_reaction("✅")
                        await self.bot.wait_for('raw_reaction_add', timeout=10.0, check=reaction_check)
                        await ctx.reply("설정되는 기능은 구현하지 않았어요 ( 전시현 바보 )", mention_author=False)

                    except Exception as e:
                        print(f'Error: {e}')
                        await msg.delete()
                        await ctx.reply("시간초과입니다.", mention_author=False)

        else:
            await ctx.reply("대상이 채널이 아닙니다.", mention_author=False)

    def read_custom(self, ctx):
        f = open(f"{path}{ctx.guild.id}/{traffic_cus_nm}", 'r')
        custom = f.read()
        f.close()
        custom = json.loads(custom)
        return custom

    @commands.command(aliases=["트래픽설정", "trafficsetting"])
    @has_permissions(manage_guild=True)
    async def traffic_s(self, ctx):
        # 어느 부분을 손볼지 물어봅니다

        if os.path.isfile(f"{path}{ctx.guild.id}/{traffic_cus_nm}"):
            custom = self.read_custom(ctx)
        else:
            custom = {}

        view = default

        for cus in custom:
            view[cus] = custom[cus]

        embed = discord.Embed(
            title = "무엇을 수정하실지 입력해주세요.",
            description = f" 1 - AuthorText : {view['AuthorText']} \n 2 - AuthorIcon : {view['AuthorIcon']} \n 3 - Title : {view['Title']} \n 4 - Description : {view['Description']} \n 5 - Thumbnail : {view['Thumbnail']} ",
            color = 0xFA747D
        )
        msg = await ctx.reply(embed=embed, mention_author=False)

        # 메시지로 입력받으므로 author만 체크해도 됨
        def message_check(message):
            if message.author == ctx.author:
                return True
            else:
                return False

        try:
            ret = await self.bot.wait_for('message', timeout=20.0, check=message_check)

            if not ret.content.isnumeric():
                await ret.reply("잘못된 입력입니다.", mention_author=False)

            if os.path.isfile(f"{path}{ctx.guild.id}/{traffic_cus_nm}"):
                custom = self.read_custom(ctx)
            else:
                f = open(f"{path}{ctx.guild.id}/{traffic_cus_nm}", 'w')
                f.write(json.dumps({}))
                f.close()
                custom = {}

            self.arguments = {
                'AuthorText' : ['Member', 'GuildName'],
                'AuthorIcon' : ['Avatar', 'GuildIcon'],
                'Title' : ["GuildName", 'DisplayName', 'Member', 'MemberCount'],
                'Description' : ["GuildName", 'DisplayName', 'Member', 'MemberCount'],
                'Thumbnail' : ['Avatar', 'GuildIcon'],
            }

            async def changecustom(name):
                if name in custom:
                    view = custom[name]
                else:
                    view = default[name]

                await ctx.send(f'```{view}```\n사용 가능 인자 : {", ".join(self.arguments[name])}\n\n위의 내용을 대체할 것을 입력하세요.')
                change = await self.bot.wait_for('message', timeout=20.0, check=message_check)

                if change.content != view:
                    if name in ['AuthorIcon', 'Thumbnail'] and change.content in ['AuthorIcon', 'Thumbnail']:
                        await change.add_reaction("✅")
                        custom[name] = change.content

                        f = open(f"{path}{ctx.guild.id}/{traffic_cus_nm}", 'w')
                        f.write(json.dumps(custom))
                        f.close()
                    else:
                        await ctx.reply("잘못된 입력입니다.", mention_author=False)
                
                else:
                    await ctx.reply("기존과 동일합니다.", mention_author=False)

            try:
                key = list(default)[int(ret.content) - 1]
                await changecustom(key)

            except IndexError:
                await ret.reply("잘못된 입력입니다.", mention_author=False)

        except Exception as e:
            print(f'Error: {e}')
            await ctx.reply("시간초과입니다.", mention_author=False)

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

                if os.path.isfile(f"{path}{member.guild.id}/{traffic_cus_nm}"):
                    custom = self.read_custom(member)
                else:
                    custom = {}

                sett = default

                for cus in custom:
                    sett[cus] = custom[cus]

                def replacer(give):
                    give = give.replace('GuildName', member.guild.name).replace('DisplayName', member.display_name)
                    give = give.replace('Member', str(member)).replace('MemberCount', str(len(member.guild.members)))
                    give = give.replace('Avatar', str(member.avatar_url)).replace('GuildIcon', str(member.guild.icon_url))
                    return give

                embed = discord.Embed(
                    title=replacer(sett['Title']),
                    description=replacer(sett['Description']),
                    timestamp=datetime.datetime.utcnow(),
                    color=0x53DC98
                )
                embed.set_author(
                    name=replacer(sett['AuthorText']),
                    icon_url=replacer(sett['AuthorIcon'])
                )
                embed.set_thumbnail(
                    url=replacer(sett['Thumbnail'])
                )
                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Traffic(bot))
