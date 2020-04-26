import discord
from discord.ext import commands
import random
import re

MAX_RESULT_LEN = 2000

class DiceRoller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_roll = None
    
    def rollStringToValues(self, rollString):
        roll_times, roll_sides = None, None
        for split_char in ['D','d','W','w']:
            roll_split = rollString.split(split_char)
            if roll_split[0] != rollString:
                roll_times, roll_sides = int(roll_split[0]), int(roll_split[1])
                break
        return roll_times, roll_sides

    def roll_XdY(self, times, sides: int):
        # print(f'Rolling {times} x {sides}')
        rolls = []
        for _ in range(times):
            roll = random.randint(1, sides)
            rolls.append(roll)
        return rolls

    async def send(self, ctx, msg):
        if len(msg) >= MAX_RESULT_LEN:
            await ctx.send(f'Result is a too-long respone (Discord-limit is {MAX_RESULT_LEN} characters)')
        else:
            await ctx.send(msg)

    @commands.command()
    async def roll(self, ctx, roll: str):
        """Translate str into rolls"""
        r = re.compile(r'\d*[DdWw]\d*')

        if r.match(roll) is None:
            await ctx.send(f'"{roll}" is not a valid input, please use e.g. 1d20 / 3d6 or 1w20 / 3w6')
        else:
            roll_times, roll_sides = self.rollStringToValues(roll)
            roll_values = self.roll_XdY(roll_times, roll_sides)
            self._last_roll = roll
            await self.send(ctx, f'Rolling {roll}:\t{roll_values}')

    @commands.command()
    async def reroll(self, ctx):
        if self._last_roll is None:
            await ctx.send('No rolls happened yet; cannot re-roll.')
        else:            
            roll_times, roll_sides = self.rollStringToValues(self._last_roll)
            roll_values = self.roll_XdY(roll_times, roll_sides)
            await self.send(ctx, f'Re-rolling {self._last_roll}:\t{roll_values}')