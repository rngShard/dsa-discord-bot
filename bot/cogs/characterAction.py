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

        msg, prevent_result = "", False
        if rolls.count(1) == 2:
            msg = "Critical success! (thanks to 2x1)"
            prevent_result = True
        elif rolls.count(1) == 3:
            msg = "Whaaaaaaaaaaaaaaaaat?!?!? (thanks to 3x1)"
            prevent_result = True
        elif rolls.count(20) == 2:
            msg = "Epic failure ... (due to 2x20)"
            prevent_result = True
        elif rolls.count(20) == 3:
            msg = "You dead son. (due to 3x20)"
            prevent_result = True
        
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

        return rolls, min(e_value, skill_value), msg, prevent_result

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
    async def c(self, ctx, check: str, difficulty=0):
        await self.check(ctx, check, difficulty, 'CTX_AUTHOR_DISPLAY_NAME')

    @commands.command(pass_contect=True)
    async def check(self, ctx, check: str, difficulty=0, char='CTX_AUTHOR_DISPLAY_NAME'):
        """Check Kopfwert / Talent for character"""
        char_obj = None

        if char == 'CTX_AUTHOR_DISPLAY_NAME':
            char = ctx.author.display_name

        # adding embed for beautiful text visualization
        embed = discord.embeds.Embed(
            colour=discord.colour.Colour.orange()
        )
        author = f'{char}'
        embed.set_author(name=f'{check.upper()} ({author})')
        # - for special icon needed: user_id of author of message --> find profilpic through user_id
        # embed.set_thumbnail(url='')
        # embed.set_image(url='')
        # embed.set_footer(text='TESTING',icon_url='')

        char_files = os.listdir(CHAR_DIR)
        if f'{char}.yaml' not in char_files:
            embed.add_field(name=f'Error',
                            value=f'No character-file found for character "{char}". Did you provide a "{char}.yaml" file?')
            await ctx.send(embed=embed)
            return
        else:
            char_obj = yaml.full_load(open(os.path.join(CHAR_DIR, f'{char}.yaml')))
            logging.info(f'.check check={check} difficulty={difficulty} char={char}')

        if check.upper() in CHECKS['ATTRIBUTES']:
            attr_value = char_obj[check.upper()]
            roll = Dice.roll_dX(20)
            res = attr_value + difficulty - roll
            msg = "Success!" if res >= 0 else "Failure..."
            embed.add_field(name=f'{check.upper()}', value=f'{attr_value}', inline=True)
            embed.add_field(name=f'Modifier', value=f'{difficulty}', inline=True)
            embed.add_field(name='Roll:', value=f'{roll}', inline=False)
            embed.add_field(name='Result:', value=f'**{res} >> {msg}**', inline=False)
            await ctx.send(embed=embed)

        elif check.lower() in CHECKS['SKILLS'].keys():
            comment, true_BE = "", None
            skill = CHECKS['SKILLS'][check.lower()]
            attrs = [char_obj[attr] for attr in skill['attrs']]
            try:
                skill_value = char_obj[check.lower()]
            except KeyError:
                embed.add_field(name=f'Error', value=f'Cannot check {check}, because you do not know that skill.')
                await ctx.send(embed=embed)
                return

            try:
                eBE = skill['eBE']
                BE = char_obj['BE']
                true_BE = SkillCheck.getTrueBE(BE, eBE)
                old_difficulty = difficulty
                difficulty -= true_BE
                comment = f'(info) BE-relevant skill, difficulty adjusted for BE={BE} & eBE={eBE}, {self.pre(old_difficulty)}{old_difficulty} >> {self.pre(difficulty)}{difficulty}\n'
            except KeyError:
                pass  # no BE to be accounted for

            rolls, res, msg, prevent_result = SkillCheck.checkSkill(attrs, skill_value, difficulty)

            embed.add_field(name=f'Value:', value=f'{skill_value}', inline=True, )
            embed.add_field(name=f'Modifier:', value=f'{difficulty}\n{comment}', inline=True)
            embed.add_field(name=f'Properties', value=f'{skill["attrs"]}', inline=False)
            embed.add_field(name=f'Properties', value=f'{attrs}', inline=True)
            embed.add_field(name='Rolls:', value=f'{rolls}', inline=True)
            if not prevent_result:
                embed.add_field(name='Result:', value=f'**{res} >> {msg}**', inline=False)

            await ctx.send(embed=embed)

        elif check.lower() in CHECKS['SPELLS'].keys():
            skill = CHECKS['SPELLS'][check.lower()]
            attrs = [char_obj[attr] for attr in skill['attrs']]
            try:
                skill_value = char_obj[check.lower()]
            except KeyError:
                embed.add_field(name=f'Error', value=f'Cannot check {check}, because you do not know that spell.')
                await ctx.send(embed=embed)
                return

            rolls, res, msg, prevent_result = SkillCheck.checkSkill(attrs, skill_value, difficulty)

            embed.add_field(name=f'Value:', value=f'{skill_value}', inline=True, )
            embed.add_field(name=f'Modifier:', value=f'{difficulty}', inline=True)
            embed.add_field(name=f'Properties', value=f'{skill["attrs"]}', inline=False)
            embed.add_field(name=f'Properties', value=f'{attrs}', inline=True)
            embed.add_field(name='Rolls:', value=f'{rolls}', inline=True)
            embed.add_field(name='Result:', value=f'**{res} >> {msg}**', inline=False)
            await ctx.send(embed=embed)

        else:
            logging.warning(f'Invalid .check command, args: {check}, {char}')
            embed.add_field(name='Error:', value=f'"{check}" is not a valid check.', inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def reg(self, ctx):
        await self.regenerate(ctx, 'CTX_AUTHOR_DISPLAY_NAME')

    @commands.command(pass_context=True)
    async def regenerate(self, ctx, char='CTX_AUTHOR_DISPLAY_NAME'):
        """Check Regeneration for character"""
        char_obj = None
        if char == 'CTX_AUTHOR_DISPLAY_NAME':
            char = ctx.author.display_name
        char_files = os.listdir(CHAR_DIR)
        if f'{char}.yaml' not in char_files:
            await ctx.send(
                f'Errors: No character-file found for character "{char}". Did you provide a "{char}.yaml" file?')
            return
        else:
            char_obj = yaml.full_load(open(os.path.join(CHAR_DIR, f'{char}.yaml')))

        reg_asp = 0
        reg_le = 0
        reg_kap = 0  # change to 1 if priest

        # additional regeneration rules: WdS 161

        # lifereg
        reg_le += Dice.roll_dX(6)  # regularreg
        if Dice.roll_dX(20) <= char_obj['KO']:  # check if KO-check is succesful
            reg_le += 1
        # add character SF's (healing I/II/III - bad_healing I/II/III)

        # asp-reg
        # if not masterreg:
        reg_asp += Dice.roll_dX(6)
        if Dice.roll_dX(20) <= char_obj['IN']:  # check if IN-check is succesful
            reg_asp += 1
        # add character SF's (reg I, reg II, masterreg, astral_reg I/II/III)
        # regreg + adv - disadv + SF_reg
        # else: change with masterregrules

        # ka-reg
        reg_kap += 1  # if priest

        author = char
        embed = discord.embeds.Embed(
            colour=discord.colour.Colour.orange()
        )

        embed.set_author(name=f'regeneration')
        embed.add_field(name=f'LE', value=f'{reg_le}')
        embed.add_field(name=f'AsP', value=f'{reg_asp}')
        embed.add_field(name=f'KaP', value=f'{reg_kap}')
        await ctx.send(author, embed=embed)
        # plain-text without embed:
        # await ctx.send(f'<{char}>\nregenerated:\n-**LE: {reg_le}**\n-**AsP: {reg_asp}** (if mage)\n-**KaP: {reg_kap}** (if priest)\nREMEMBER: regeneration modifiers not implemented yet!')
