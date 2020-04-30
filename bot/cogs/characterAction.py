import discord
from discord.ext import commands
import logging
import os
import yaml
from .diceRoller import Dice
import re

DIR_NAME = os.path.dirname(__file__)
CHAR_DIR = os.path.join(DIR_NAME, '../../chars')
ASSETS_DIR = os.path.join(DIR_NAME, '../../assets')

CHECKS = {
    'ATTRIBUTES': yaml.full_load(open(os.path.join(ASSETS_DIR, 'attributes.yaml'))),
    'SKILLS': yaml.full_load(open(os.path.join(ASSETS_DIR, 'skills.yaml'))),
    'SPELLS': yaml.full_load(open(os.path.join(ASSETS_DIR, 'spells.yaml')))
}

class SkillCheck:
    @staticmethod
    def checkSkill(attrs: [int, int, int], skill_value: int, difficulty=0):
        e_value = skill_value + difficulty
        if e_value < 0:
            attrs = [attrs[i] - abs(e_value) for i in range(3)]
            e_value = 0

        rolls = []
        for _ in range(3):
            rolls.append(Dice.roll_dX(20))
        
        msg = ""
        if rolls.count(1) == 2:
            msg = "Critical success!"
        elif rolls.count(1) == 3:
            msg = "Whaaaaaaaaaaaaaaaaat?!?!?"
        elif rolls.count(20) == 2:
            msg = "Epic failure ..."
        elif rolls.count(20) == 3:
            msg = "You dead son."
        else:
            for i in range(3):
                if rolls[i] > attrs[i]:
                    e_value -= rolls[i] - attrs[i]
            if e_value < 0:
                msg = "Failure..."
            elif e_value == 0:
                msg = "Success! (Close one...)"
            else:
                msg = "Success!"
        return rolls, min(e_value, skill_value), msg
    @staticmethod
    def getTrueBE(BE: int, eBE: str):
        if re.compile(r'x\d').match(eBE):
            times = int(eBE[1])
            return BE * times
        elif re.compile(r'-\d').match(eBE):
            minus = int(eBE[1])
            return BE - minus

class CharacterAction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def pre(self, num: int):
        return "+" if num >= 0 else ""
  
    @commands.command()
    async def c(self, ctx, check: str, difficulty = 0):
        await self.check(ctx, check, difficulty, 'CTX_AUTHOR_DISPLAY_NAME')

    @commands.command()
    async def check(self, ctx, check: str, difficulty = 0, char = 'CTX_AUTHOR_DISPLAY_NAME'):
        """Check Kopfwert / Talent for character"""
        char_obj = None
        if char == 'CTX_AUTHOR_DISPLAY_NAME':
            char = ctx.author.display_name
        char_files = os.listdir(CHAR_DIR)
        if f'{char}.yaml' not in char_files:
            await ctx.send(f'Errors: No character-file found for character "{char}". Did you provide a "{char}.yaml" file?')
            return
        else:
            char_obj = yaml.full_load(open(os.path.join(CHAR_DIR, f'{char}.yaml')))
            logging.info(f'.check check={check} difficulty={difficulty} char={char}')

        if check.upper() in CHECKS['ATTRIBUTES']:
            attr_value = char_obj[check.upper()]
            roll = Dice.roll_dX(20)
            res = attr_value + difficulty - roll
            msg = "Success!" if res >= 0 else "Failure..."
            await ctx.send(f'<{char}> Checking {check.upper()} ({attr_value}) {self.pre(difficulty)}{difficulty}:\nRolling {roll} >> {msg}\nResult = {self.pre(res)}{res}')
        
        elif check.lower() in CHECKS['SKILLS'].keys():
            comment, true_BE = "", None
            skill = CHECKS['SKILLS'][check.lower()]
            attrs = [char_obj[attr] for attr in skill['attrs']]
            try:
                skill_value = char_obj[check.lower()]
            except KeyError:
                await ctx.send(f'<{char}> Cannot check {check}, because you do not know that skill.')
                return
                
            try:
                eBE = skill['eBE']
                BE = char_obj['BE']
                true_BE = SkillCheck.getTrueBE(BE, eBE)
                old_difficulty = difficulty
                difficulty -= true_BE
                comment = f'(info) BE-relevant skill, difficulty adjusted for BE={BE} & eBE={eBE}, {self.pre(old_difficulty)}{old_difficulty} >> {self.pre(difficulty)}{difficulty}\n'
            except KeyError:
                pass    # no BE to be accounted for
            
            rolls, res, msg = SkillCheck.checkSkill(attrs, skill_value, difficulty)

            await ctx.send(f'<{char}> Checking {check} {skill["attrs"]}={attrs} ({skill_value}) {self.pre(difficulty)}{difficulty}:\n{comment}Rolling {rolls} >> {msg}\nResult = {self.pre(res)}{res}')
        
        elif check.lower() in CHECKS['SPELLS'].keys():
            skill = CHECKS['SPELLS'][check.lower()]
            attrs = [char_obj[attr] for attr in skill['attrs']]
            try:
                skill_value = char_obj[check.lower()]
            except KeyError:
                await ctx.send(f'<{char}> Cannot check {check}, because you do not know that spell.')
                return

            rolls, res, msg = SkillCheck.checkSkill(attrs, skill_value, difficulty)

            await ctx.send(f'<{char}> Checking {check} {skill["attrs"]}={attrs} ({skill_value}) {self.pre(difficulty)}{difficulty}:\nRolling {rolls} >> {msg}\nResult = {self.pre(res)}{res}')

        else:
            logging.warning(f'Invalid .check command, args: {check}, {char}')
            await ctx.send(f'Error: "{check}" is not a valid check.')