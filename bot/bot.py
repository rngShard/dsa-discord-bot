import os
import yaml
import discord
from discord.ext import commands
from cogs.skillchecks import SkillCheck

DIR_NAME = os.path.dirname(__file__)


bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('(info) Bot ready')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


config_file_path = os.path.join(DIR_NAME, '../config.yaml')
with open(config_file_path) as config_file:
    config = yaml.full_load(config_file)

    bot.add_cog(SkillCheck(bot))
    bot.run(config['DISCORD_BOT_TOKEN'])