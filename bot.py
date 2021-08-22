import os
import discord

from modules import jsonreader as jsr
from modules.bot import Bot

config = jsr.get("config.json")
print("Logging in...")

intents = discord.Intents.all()

bot = Bot(
    command_prefix=config.prefix,
    prefix=config.prefix,
    command_attrs=dict(hidden=True),
    help_command=None,
    intents=intents
)

#needs
path = "./paffy_lib"
if not os.path.isdir(path):
    os.mkdir(path)


for name in ['cogs.'+file[:-3] for file in os.listdir("cogs") if file.endswith('.py')]:
    bot.load_extension(name)
    print(f"{name} Loaded.")

try:
    bot.run(config.token)
except Exception as e:
    print(f'Error when logging in: {e}')