import discord
from discord.ext import commands
from discord.ext import tasks

import os
import sys
import time
from datetime import datetime, date
import math
import random
from string import ascii_uppercase, ascii_lowercase, digits
import io
import re
from itertools import combinations, cycle
from contextlib import redirect_stdout
from textwrap import indent
from traceback import format_exception
import asyncio

from src.translate import translate
from src.hangman import Hangman, WORD_CHOICES, FIGURES
from src.sokoban import Sokoban, SOKOBAN_GAMES
from src.dox import Doxxer
from src.data import update_data, load_data
from src.prompt import get_response
from src.consts import Users, Groups, Emojis, StEndings, StTypes, LWORDS
from src.methods import substring, product, round_to_5

primary_prefix = "!"
bot = commands.Bot(
    command_prefix = [primary_prefix, "lol ", "Lol "],
    intents = discord.Intents.all(),
    allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True),
    help_command=None)

PRINT_MESSAGES = False

# these 3 are permissions decorators
# for example, if you see @staff() in front of a command, it means only staff can run
def owner():
    group = (
        Users.progamrer,
    )
    def am(ctx):
        return ctx.message.author.id in group
    return commands.check(am)

def dev():
    group = (
        Users.progamrer,
        Users.hello,
    )
    def am(ctx):
        return ctx.message.author.id in group
    return commands.check(am)

def staff():
    group = (
        Users.progamrer,
        Users.hello,
        Users.jayd,
        Users.catvader,
        Users.fhd,
    )
    def am(ctx):
        return ctx.message.author.id in group
    return commands.check(am)

@bot.command(name="prompt")
async def _prompt(ctx, *args):
    msg = "Respond to the following message as the communist evil confident: " + " ".join(args)
    async with ctx.typing():
        response = get_response(msg)
    await ctx.reply(response.lower())

@bot.command(aliases=["pp"])
async def penis(ctx, user: discord.User = None):
    if not user:
        user = ctx.author
    nickname = user.display_name

    try: 
        random.seed(user.id)
    except AttributeError:
        user = ' '.join(user)
        random.seed(product([ord(x) for x in user]))
        username = user
    if user.id == 963533621812158474:
        embed = discord.Embed(title="pp size calculator", description=f"{username}'s penis size\nFATAL ERROR: No penis found. It could be too short (the bot can only detect min. 1cm penises)")
        await ctx.send(embed=embed)
        random.seed(None)
        return
    length = random.randrange(0, 21)
    random.seed(None)
    embed = discord.Embed(title="pp size calculator", description=f"{username}'s penis size\n8{'='*length}D")
    await ctx.send(embed=embed)
    
@bot.command()
@staff()
async def dm(ctx, user: discord.User, *message):
    try:
        await user.send(' '.join(message))
        await ctx.message.add_reaction(Emojis.check_mark)
    except:
        await ctx.message.add_reaction(Emojis.cross_mark)

@bot.command()
@staff()
async def nickname(ctx, *args):
    nickname = " ".join(args)
    await ctx.guild.get_member(bot.user.id).edit(nick=nickname)
    await ctx.message.add_reaction(Emojis.check_mark)

@bot.command(name="translate")
async def _translate(ctx, *args):
    await translate(ctx, " ".join(args))

@bot.command(name = "game", aliases = ["wordgame", "guess"])
async def _game(ctx):
    def check(msg):
        return (msg.channel == ctx.channel) and (not msg.author.bot)

    target_substring = substring(random.choice(LWORDS), random.choice([2,3]))
    await ctx.send(f"Please send a word containing \"{target_substring}\"!")
    while True:
        try:
            new_word = await bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.reply("You took too long, bye!")
            break
        if new_word.content.lower() == "`stop":
            await new_word.add_reaction(Emojis.check_mark)
            break
        if new_word.content.lower() not in LWORDS:
            continue
        if new_word.content == target_substring:
            await new_word.reply("dont be lazy choose a different word")
            continue
        if target_substring in new_word.content.lower():
            score = 1.9 ** len(new_word.content) * 9 * len(target_substring)
            await new_word.reply(f"Good job (you have been awarded with {math.ceil(score)} social credits)")
            user_data = load_data()
            user_data[str(new_word.author.id)]["score"] += math.ceil(score)
            update_data(user_data)
            break

@bot.command(name = "hangman")
async def _hangman(ctx, *_category):
    if not _category:
        category = random.choice(list(WORD_CHOICES.keys()))
    else:
        category = " ".join(_category)
    target = random.choice(WORD_CHOICES[category])
    h = Hangman(target)
    def check(msg):
        return (msg.channel == ctx.channel) and (msg.author.id == ctx.author.id) and (not msg.author.bot)
    embed = discord.Embed(title="Hangman")
    embed.set_footer(text=f"{ctx.author} | say 'EXIT' to run away like a coward")
    while True:
        #embed.description = f"```\n{FIGURES[h.life]}\n\nCategory: {category}\nWord: {' '.join(h.configuration)}\nWrong guesses: {', '.join(h.wrong_guesses)}```"
        embed.description = f"```Category: {category}\nWord: {' '.join(h.configuration)}\nWrong guesses: {', '.join(h.wrong_guesses)}```"
        embed.title = f"Hangman (Lives left: {6-h.life})"
        await ctx.send(content=f"{ctx.author.mention}", embed=embed)
        try:
            msg = await bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.reply("You took too long, bye!")
            break
        if (msg.content.upper() == msg.content) and (msg.content.upper() == 'EXIT'):
            await ctx.send(f"{ctx.author.mention} you ran away from the game, thinking you will finally wake up from the nightmare. But in reality, you are ever closer to the all-consuming void. This time, you have escaped your fate by sacrificing hangman, by killing him to spare yourself. Be sure that the gods are aware of your cowardliness and treachery, and will make your life even more difficult before your very being gets consumed by the beast. Now you will never find out what the correct word was.")
            break
        match h.guess(msg.content.lower()):
            case 0:
                await ctx.send(f"{ctx.author.mention} congratulations you have won, i guess you are mildly intelligent (word was: {h.target})")
                break
            case -1:
                await ctx.send(f"{ctx.author.mention} '{msg.content}' is not in the word idiot! (Life -1)")
            case -2:
                await ctx.send(f"{ctx.author.mention} '{msg.content}' is not the correct word idiot! lol! lmao! (Life -1)")
            case -999:
                await ctx.send(f"{ctx.author.mention} HANGMAN DIED RIP (the word was: {h.target})")
                return

# very useful command
@bot.command()
async def whoasked(ctx):
    msg = await ctx.send('[▖] Looking for who asked...')
    await asyncio.sleep(0.2)
    await msg.edit(content='[▘] Looking for who asked...')
    await asyncio.sleep(0.2)
    await msg.edit(content='[▝] Looking for who asked...')
    await asyncio.sleep(0.2)
    await msg.edit(content='[▗] Looking for who asked...')
    await asyncio.sleep(0.2)
    await msg.edit(content='[▖] Looking for who asked...')
    await asyncio.sleep(0.2)
    if random.random() > 0.33:
        await msg.edit(content='ERROR: Failed to find who asked')
    else:
        await msg.edit(content=f'Found! **{random.choice(ctx.guild.members)}** asked.')

@bot.command(name = "commands")
async def _commands(ctx):
    await ctx.reply(f"```py\n{[str(x) for x in bot.commands]} ```")

@bot.command(name = "restart", aliases = ["r"])
@dev()
async def restart(ctx):
    await ctx.message.add_reaction(Emojis.hourglass)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
async def ping(ctx):
    await ctx.reply("Ping: `" + str(round(bot.latency * 1000)) + "` ms")

@bot.command(name="death", aliases = ["deathdate","whenwillidie","dead"])
async def _death(ctx, *person: discord.Member):
    if not person:
        person = ctx.author
        other = False
    else:
        person = person[0]
        other = True
    msg = await ctx.reply("Calculating...")
    current_time = math.floor(time.time())
    random.seed(person.id / 7) # 13
    val = random.random()
    if val < 0.01:
        add_years = random.randrange(1200, 604800)
    elif 0.01 < val < 0.05:
        add_years = random.randrange(31556926, 157680000)
    elif 0.05 < val < 0.1:
        add_years = random.randrange(3784320000, 5045760000)
    elif 0.1 < val < 0.2:
        add_years = random.randrange(946080000, 1261440000)
    else:
        add_years = random.randrange(1576800000, 2444040000)
    random.seed(None)
    await asyncio.sleep(0.1)
    if not other:
        embed = discord.Embed(title="", description=f"**You** will die <t:{current_time + add_years}:R>")
    else:
        embed = discord.Embed(title="", description=f"**{person}** will die <t:{current_time + add_years}:R>")
    embed.set_footer(text="note that can pooper is just a badly written discord bot so dont take this seriously lol")
    await msg.edit(embed=embed)

@bot.command()
@dev()
async def say(ctx, channelid, *msg):
    try:
        channel_ = bot.get_channel(int(channelid))
        await channel_.send(' '.join(msg))
        print(f'Message \'{msg}\' sent. ')
        await ctx.message.add_reaction(Emojis.check_mark)
    except:
        await ctx.message.add_reaction(Emojis.cross_mark)

@bot.command()
async def echo(ctx, *msg):
    if ctx.author.id in [672892838995820553, 650439182204010496]:
        try: 
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
    await ctx.send(" ".join(msg))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    print('[' + str(time.strftime("%H:%M:%S", time.localtime())) + "] bot is now running")
    
    channel = bot.get_channel(1118259599393443942) # automatically join vc
    _channel = await channel.connect()
    _channel.play(discord.FFmpegPCMAudio('./res/rick_roll.mp3'))

@bot.command(name="eval", aliases=["exec", "lol"])
@owner()
async def lol(ctx, *, code):
    _globals = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "owner": owner,
        "math": math,
        "random": random,
        "time": time,
        "exempted": exempted,
        "guild": ctx.guild,
        "dox": dox_command,
        "ghostping": _ghost_ping,
        "sys": sys,
        "Emojis": Emojis,
        "asyncio": asyncio,
    }
    
    buffer = io.StringIO()

    try:
        with redirect_stdout(buffer):
            exec(f"async def func():\n{indent(code, '    ')}", _globals)
            func = await _globals["func"]()
            result = f"{buffer.getvalue()}\n-- {func}\n"
            try:
                await ctx.message.add_reaction(Emojis.check_mark)
            except discord.errors.NotFound:
                pass
    except Exception as e:
        tbegin = time.time()
        result = "".join(format_exception(e, e, e.__traceback__))
        embed=discord.Embed(title='')
        embed.add_field(name='imagine getting an error', value = (f'```py\n{result}```'))
        embed.set_footer(text=f'evaluated in {math.floor((time.time()-tbegin)*1000)} ms')
        await ctx.send(embed=embed)

@bot.command()
@owner()
async def e(ctx, *expression):
    _globals = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "owner": owner,
        "math": math,
        "random": random,
        "time": time,
        "exempted": exempted,
        "guild": ctx.guild,
        "sys": sys,
    }
    expression = ' '.join(expression)
    try:
        tbegin = time.time()
        output = eval(expression, _globals)
        color = discord.Colour.from_rgb(0x56, 0x18, 0x90)
    except Exception as e:
        tbegin = time.time()
        output = e
        color = discord.Colour.from_rgb(0xff, 0x00, 0x00)
    embed = discord.Embed(title = '',color=color)
    embed.add_field(name='Input',value=f'```py\n{expression}```',inline=False)
    embed.add_field(name='Output',value=f'```py\n{output} ```',inline=False)
    embed.set_footer(text=f'evaluated in {math.floor((time.time() - tbegin) * 1000)} ms')
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if PRINT_MESSAGES:
        print(f'--------\n{message.author}: {message.content}\nChannel: ', end='')
        try: print(f'{message.channel} ({message.channel.id})\nGuild: {message.guild.name}\n')
        except: print("possibly a dm\n")

    if message.author.bot:
        return
 
    if message.content.removeprefix(primary_prefix).strip().lower().split()[0] in [str(cmnd) for cmnd in bot.commands]:
        user_data = load_data()
        if str(message.author.id) not in user_data.keys():
            user_data[str(message.author.id)] = {
                "id": message.author.id,
                "score": 0,
            }
            update_data(user_data)
    
    await bot.process_commands(message)

@bot.command(name = "dox", aliases = ["doxx"])
async def dox_command(ctx, user: discord.User):
    msg: discord.Message = await ctx.send("Waiting...")
    await asyncio.sleep(2)
    doxxer = Doxxer(user.id / 3)

    embed = discord.Embed(
        title = "Private Information Extractor v1.0.4",
        description = f"{user.mention}'s info:"
    )
    embed.add_field(name = "FULL NAME", value = doxxer.full_name, inline = False)
    embed.add_field(name = "AGE", value = f"{doxxer.age} years", inline = False)
    embed.add_field(name = "GENDER", value = doxxer.gender, inline = False)
    embed.add_field(name = "ADDRESS", value = doxxer.address, inline = False)
    embed.add_field(name = "IP ADDRESS", value = doxxer.ip, inline = False)

    embed.set_footer(text = "for legal reasons this is a joke (but is it really?)")

    await msg.edit(content="", embed=embed)

@bot.command(name = "sokoban", aliases = ["soko", "blockpush"])
async def _sokoban(ctx):
    game = random.choice(SOKOBAN_GAMES)
    s = Sokoban(
        game,
        floor = ":black_large_square:",
        wall = ":blue_square:",
        crate = "<:nc:988933443306008636>",
        gcrate = "<:gc:988933466156568647>",
        player = ":smiley_cat:",
        goal = ":x:",
        gplayer = ":smiley_cat:",
    )

    score = game.score

    valid_moves = {
        "⬆️": "UP",
        "⬇️": "DOWN",
        "⬅️": "LEFT",
        "➡️": "RIGHT",
    }
    
    embed = discord.Embed(title="Sokoban (pc is reocmmended)", description="\n".join([''.join([s.icons[x] for x in a]) for a in s.grid]))
    embed.set_footer(text="If the bot is not responding, it's probably being rate limited. Just wait a sec, don't spam reactions")
    msg = await ctx.reply(embed=embed)
    await msg.add_reaction(Emojis.arrow_up)
    await msg.add_reaction(Emojis.arrow_down)
    await msg.add_reaction(Emojis.arrow_left)
    await msg.add_reaction(Emojis.arrow_right)
    await msg.add_reaction(Emojis.cross_mark)

    def check(reaction, user):
        return (user == ctx.author) and (reaction.message == msg)

    while True:
        try:
            reaction = await bot.wait_for('reaction_add', timeout=20, check=check)
        except asyncio.TimeoutError:
            await ctx.reply("You took too long, bye!")
            await msg.clear_reactions()
            break
        if reaction[0].emoji == "\N{CROSS MARK}":
            await msg.clear_reactions()
            break
        else:
            if s.move(valid_moves[reaction[0].emoji]) == 2147483647:
                rows = "\n".join([''.join([s.icons[x] for x in a]) for a in s.grid])
                embed.description = rows
                await msg.edit(embed = embed)
                await msg.clear_reactions()
                await ctx.reply(f"Congrats you solved it (you have been awarded with {score} social credits)")
                user_data = load_data()
                user_data[str(ctx.author.id)]["score"] += score
                update_data(user_data)
                break

        try:
            await msg.remove_reaction(reaction[0], reaction[1])
        except discord.errors.Forbidden:
            pass
        rows = "\n".join([''.join([s.icons[x] for x in a]) for a in s.grid])
        embed.description = rows
        await msg.edit(embed = embed)

if __name__ == "__main__":
    token = open("token.txt", "r").read()
    bot.run(token)
