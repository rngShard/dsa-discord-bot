import discord
from discord.ext import commands
import logging
import os
import yaml

EIGENSCHAFTEN = ['MU', 'KL', 'IN', 'CH', 'FF', 'GE', 'KO', 'KK']
DIR_NAME = os.path.dirname(__file__)
CHAR_DIR = os.path.join(DIR_NAME, '../../chars')

class CharacterAction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    async def check(self, ctx, check: str, char: str):
        """Check Kopfwert / Talent for character"""
        check = check.upper()
        char = char.lower()

        errors = []
        if not check in EIGENSCHAFTEN:
            errors.append(f'"{check}" is not a valid EIGENSCHAFT to check for.\nPlease use one of {EIGENSCHAFTEN} instead.')
        char_files = os.listdir(CHAR_DIR)
        if f'{char}.yaml' not in char_files:
            errors.append(f'No character-file found for character "{char}". Did you provide a "{char}.yaml" file?')
        if len(errors) > 0:
            logging.warning(f'Invalid .check command, args: {check}, {char}')
            await ctx.send(f'Errors: {errors}')
        else:
            with open(os.path.join(CHAR_DIR, f'{char}.yaml')) as char_file:
                char_obj = yaml.full_load(char_file)
                eig_value = char_obj[check]
                # TODO: implement
                await ctx.send(f'<{char}> Checking {check} ({eig_value}): 42. Check successful / unsuccessful...')