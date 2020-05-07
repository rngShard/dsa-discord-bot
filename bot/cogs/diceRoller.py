import discord
from discord.ext import commands
import random
import re
import logging

MAX_RESULT_LEN = 2000


class Dice:
    @staticmethod
    def roll_dX(sides: int):
        logging.info(f'Rolling D{sides}')
        return random.randint(1, sides)

    @staticmethod
    def roll_XdY(times, sides: int):
        logging.info(f'Rolling {times}D{sides}')
        rolls = []
        for _ in range(times):
            roll = random.randint(1, sides)
            rolls.append(roll)
        return rolls


class DiceRoller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_roll = None

    def rollStringToValues(self, rollString):
        roll_times, roll_sides = None, None
        for split_char in ['D', 'd', 'W', 'w']:
            roll_split = rollString.split(split_char)
            if roll_split[0] != rollString:
                roll_times, roll_sides = int(roll_split[0]), int(roll_split[1])
                break
        return roll_times, roll_sides

    async def overlength_check(self, ctx, msg):
        passed = False
        if len(msg) >= MAX_RESULT_LEN:
            await ctx.send(f'Result is a too-long respone (Discord-limit is {MAX_RESULT_LEN} characters)')
        else:
            passed = True
        return passed

    async def send_embed_roll(self, ctx, roll: str, roll_values, author='ROLLING'):
        if len(f'{roll_values}') <= 1000:
            # adding embed for beautiful text visualization
            embed = discord.embeds.Embed(
                colour=discord.colour.Colour.orange()
            )
            embed.set_author(name=f'{author}')
            # - for special icon needed: user_id of author of message --> find profilpic through user_id
            # embed.set_thumbnail(url='')
            # embed.set_image(url='')
            # embed.set_footer(text='TESTING',icon_url='')
            embed.add_field(name=f'{roll}', value=f'{roll_values}')
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Output too long for embed-output - using standard-chat instead!\nRolling {roll}:\t{roll_values}')

    @commands.command()
    async def r(self, ctx, roll: str):
        await self.roll(ctx, roll)

    @commands.command()
    async def roll(self, ctx, roll: str):
        """Translate str into rolls"""
        r = re.compile(r'\d+[DdWw]\d+')

        if r.match(roll) is None:
            await ctx.send(f'"{roll}" is not a valid input, please use e.g. 1d20 / 3d6 or 1w20 / 3w6')
        else:
            roll_times, roll_sides = self.rollStringToValues(roll)
            roll_values = Dice.roll_XdY(roll_times, roll_sides)
            self._last_roll = roll
            if await self.overlength_check(ctx, f'{roll_values}'):
                await self.send_embed_roll(ctx, roll, roll_values)

    @commands.command()
    async def reroll(self, ctx):
        if self._last_roll is None:
            await ctx.send('No rolls happened yet; cannot re-roll.')
        else:
            roll_times, roll_sides = self.rollStringToValues(self._last_roll)
            roll_values = Dice.roll_XdY(roll_times, roll_sides)
            if await self.overlength_check(ctx, f'{roll_values}'):
                await self.send_embed_roll(ctx, self._last_roll, roll_values, author='RE-ROLLING')
