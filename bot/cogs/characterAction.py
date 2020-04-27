import discord
from discord.ext import commands
import logging
import os
import yaml
from .diceRoller import Dice

DIR_NAME = os.path.dirname(__file__)
CHAR_DIR = os.path.join(DIR_NAME, '../../chars')
ASSETS_DIR = os.path.join(DIR_NAME, '../../assets')

CHECKS = {
    'ATTRIBUTES': yaml.full_load(open(os.path.join(ASSETS_DIR, 'attributes.yaml'))),
    'SKILLS': yaml.full_load(open(os.path.join(ASSETS_DIR, 'skills.yaml')))
}

class CharacterAction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    @commands.command()
    async def check(self, ctx, check: str, char='CTX_AUTHOR_DISPLAY_NAME'):
        """Check Kopfwert / Talent for character"""
        check = check.upper()

        char_obj = None
        if char == 'CTX_AUTHOR_DISPLAY_NAME':
            char = ctx.author.display_name
        char_files = os.listdir(CHAR_DIR)
        if f'{char}.yaml' not in char_files:
            await ctx.send(f'Errors: No character-file found for character "{char}". Did you provide a "{char}.yaml" file?')
            return
        else:
            char_obj = yaml.full_load(open(os.path.join(CHAR_DIR, f'{char}.yaml')))
            logging.info(f'.check {check} {char}')

        if check in CHECKS['ATTRIBUTES']:
            eig_value = char_obj[check]
            roll = Dice.roll_dX(20)
            await ctx.send(f'<{char}> Checking {check} ({eig_value}): {roll}. {"Success!" if roll <= eig_value else "Failure..."}')
        elif check in CHECKS['SKILLS'].keys():
            # TODO: implement 
            await ctx.send(f'<{char}> Checking {check}: Todo')
        else:
            logging.warning(f'Invalid .check command, args: {check}, {char}')
            await ctx.send(f'Error: "{check}" is not a valid check.')