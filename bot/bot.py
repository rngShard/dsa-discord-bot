import os
import yaml
import discord
from discord.ext import commands

DIR_NAME = os.path.dirname(__file__)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        # don't respond to ourselves
        if message.author == self.user:
            return
        if message.content == 'ping':
            await message.channel.send('pong')

config_file_path = os.path.join(DIR_NAME, '../config.yaml')
with open(config_file_path) as config_file:
    config = yaml.full_load(config_file)

    client = MyClient()
    client.run(config['DISCORD_BOT_TOKEN'])