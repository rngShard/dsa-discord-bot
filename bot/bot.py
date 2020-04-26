import os
import yaml
import discord
from discord.ext import commands
from cogs.diceroller import DiceRoller
import logging

DIR_NAME = os.path.dirname(__file__)
LOG_FILE = os.path.join(DIR_NAME, '../log.txt')
CONFIG_FILE = os.path.join(DIR_NAME, '../config.yaml')

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
logging.basicConfig(
    filename = LOG_FILE,
    filemode = 'w',
    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level = logging.INFO)


bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    rdy_msg = 'DSA Discord Bot, at your service'
    logging.info(rdy_msg)
    print(rdy_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


with open(CONFIG_FILE) as cfg_file:
    config = yaml.full_load(cfg_file)

    bot.add_cog(DiceRoller(bot))
    bot.run(config['DISCORD_BOT_TOKEN'])