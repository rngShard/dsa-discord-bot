import discord
from discord.ext import commands
import random
import re

class SkillCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_roll = None
    
    def roll_dX(self, sides: int):
        return random.randint(0, sides)


    @commands.command()
    async def roll(self, ctx, roll: str):
        """Translate str into rolls"""
        r = re.compile(r'\d*[dw]\d*')

        if r.match(roll) is None:
            await ctx.send(f'"{roll}" is not a valid input, please use e.g. 1d20 / 3d6 or 1w20 / 3w6')
        else:
            self._last_roll = roll
            await ctx.send(f'rolling {roll}')

    # async def reroll(self, ctx):
    #     if self._last_roll is not None:
    #         await