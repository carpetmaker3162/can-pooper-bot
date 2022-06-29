# if you try to run an instance of my bot, a lot of things will break
# since many features are dependant on files stored locally on my
# computer


# behold, all my imports :dyinginside:
# discord.py. Special thanks to its creators, hope they add support for buttons soon
import discord
from discord.ext import commands
from discord.ext import tasks

# standard stuff
import os
import sys
import time
from datetime import datetime, date
import math
import random
from string import ascii_uppercase, ascii_lowercase, digits

# other random stuff
import io
import re
from itertools import combinations, cycle
from contextlib import redirect_stdout
from textwrap import indent
from traceback import format_exception
import asyncio

# stuff i wrote myself that i just put in other files
from src.brainfuck import BrainfuckInterpreter
from src.police import police as _police
from src.conversion import to_usd, to_jayd, USD_TO_JAYD_CONVERSION_RATE
from src.philosophy import Wikicrawler
from src.wikicrawler import Crawler
from src.names import get_name
from src.translate import translate
from src.hangman import Hangman, WORD_CHOICES, FIGURES
from src.sokoban import Sokoban, SOKOBAN_GAMES
from src.dox import Doxxer
from src.data import update_data, load_data

# h
from src.consts import ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT, ARROW_UP, LWORDS, CHECK_MARK_EMOJI, CROSS_MARK_EMOJI, \
    HOURGLASS_EMOJI, THUMBS_UP_EMOJI, CLOWN_EMOJI, WARNING
from src.methods import substring, product, merge, shipValue, round_to_5

# setup
primary_prefix = "!"
bot = commands.Bot(
    command_prefix = [primary_prefix, "lol "],
    intents = discord.Intents(guilds=True, members=True, bans=True, emojis=True, voice_states=True, messages=True, reactions=True), 
    allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True),
    help_command=None)

# dont mind these extra globals im trying to get rid of them too
blList, snipelist_, sniper_, edit_, policing, tracking_channels, exempted = [], [], [], [], [], [], []
police, animation = False, False
t = 0
val = 0
user_data = load_data()


# blacklist filter, probably will remove since blacklist system is never used anyway
def nobl():
    def am(ctx):
        return (ctx.message.author.id not in blList)
    return commands.check(am)

# these 3 are permissions decorators
# for example, if you see @staff() in front of a command, it means only staff can run
# yeah i know imagine having """staff""" for such a shitty bot so cringe ong
def owner():
    def am(ctx):
        return ctx.message.author.id == 672892838995820553
    return commands.check(am)

def dev():
    poopers = [650439182204010496, 672892838995820553]
    def am(ctx):
        return ctx.author.id in poopers
    return commands.check(am)

def staff():
    staffs = [672892838995820553, # me
    650439182204010496, # hello
    690265771955585029, # jayd
    816692546272100442, # catvader
    628672513345454122, # fhd
    ]
    def am(ctx):
        return (ctx.message.author.id in staffs)
    return commands.check(am)

# message event handler. Here is also where I store edited messages (ikr so bad)
# Maybe ill move this and all the other globals into a cache file or something idk
@bot.event
async def on_message_edit(before,after):
    global edit_
    match len(edit_):
        case 0:
            edit_.append(before.content)
            edit_.append(after.content)
            edit_.append(before.channel.id)
            edit_.append(before.author.id)
        case _:
            edit_ = []
            edit_.append(before.content)
            edit_.append(after.content)
            edit_.append(before.channel.id)
            edit_.append(before.author.id)

@bot.command()
@nobl()
async def editsnipe(ctx):
    color = discord.Colour.from_rgb(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    global edit_
    match len(edit_):
        case 0:
            await ctx.reply('are you stupid or something theres nothing to snipe')
        case _: 
            embed = discord.Embed(title = 'Edited message', description = f'Before: "{edit_[0]}"\nAfter: "{edit_[1]}"\nUser: <@{edit_[3]}>\nChannel: <#{edit_[2]}>',color=color)
            embed.set_footer(text = 'lol sniped')
            await ctx.send(embed=embed)

@bot.command(aliases=["pp"])
async def penis(ctx, *user):
    if not user:
        user = ctx.author
        username = user.display_name
    else:
        if re.findall("<@(\d{18})>", user[0]):
            user = bot.get_user(int(re.findall("<@(\d{18})>", user[0])[0]))
            username = user.display_name
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
@dev()
async def dm(ctx, user: discord.User, *message):
    try:
        await user.send(' '.join(message))
        await ctx.message.add_reaction(CHECK_MARK_EMOJI)
    except:
        await ctx.message.add_reaction(CROSS_MARK_EMOJI)

@bot.command()
@staff()
async def report(ctx):
    msg = await ctx.send("Checking report logs...")
    
    with open("report_logs.txt", "r") as file:
        reports = file.read().split("\n")
        if reports:
            last_report = reports[-1]
        else:
            last_report = None
        file.close()

    time_elapsed = (time.time() - int(last_report)) / 60

    await msg.edit("Counting messages...")

    with open("msg_count.txt", "r") as file:
        data = {}
        for i in tracking_channels:
            data[str(i)] = 0
        
        for i in file.read().split("\n"):
            if i:
                data[i] += 1
        file.close()
    
    await msg.edit("Organizing data...")
    
    stats = ""
    total = 0
    for channel, count in data.items():
        if count:
            stats += f"{bot.get_channel(int(channel))}: {count}\n"
            total += count
    
    embed = discord.Embed(title="Activity Report")
    embed.add_field(name="Stats",value=f"```{stats} ```", inline=False)
    embed.add_field(name="Extra Info",value=f"Total messages sent (since last reset): {total}\nCurrent time: <t:{math.floor(time.time())}>\nLast resetted: <t:{last_report}> (<t:{last_report}:R>)\nMessage rate: {total / time_elapsed:.3f} messages/minute\nMinutes passed since last reset: {math.floor(time_elapsed)}", inline=False)
    await msg.edit(embed=embed)

@bot.command()
@dev()
async def reset(ctx):
    msg = await ctx.send("Resetting message data...")
    
    f = open("msg_count.txt", "w")
    f.close()

    await msg.edit("Recording current reset time...")
    
    with open("report_logs.txt", "a") as file:
        file.write("\n")
        file.write(str(math.floor(time.time())))
        file.close()
    
    with open("report_logs.txt", "r") as file:
        times = file.read().split("\n")
        file.close()
        lasttime = times[-2]

    await msg.edit(f"Resetted\nCurrent time: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\nLast reset: {datetime.fromtimestamp(int(lasttime)).strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
@dev()
async def lastreset(ctx, *new):
    with open("report_logs.txt", "r") as file:
        times = file.read().split("\n")
        file.close()
    if not new:
        await ctx.send(f"Last resetted: <t:{times[-1]}>")
    else:
        with open("report_logs.txt", "a") as file:
            file.write("\n")
            file.write(str(new[0]))
        await ctx.send(f"Last reset time manually set to <t:{str(new[0])}>")

@bot.event
async def on_message_delete(msg):
    global snipelist_
    snipelist_.append([msg.content, msg.author.id, msg.channel.id])
    global sniper_
    if len(sniper_) != 0:
        sniper_ = []
        sniper_.append([msg.content, msg.author.id, msg.channel.id])
    else:
        sniper_.append([msg.content, msg.author.id, msg.channel.id])

@bot.command()
@nobl()
async def ship(ctx, *people):
    h = True
    try:
        b = people[1]
    except IndexError:
        a = ctx.author.display_name
        h = False
        try:
            b = people[0]
        except IndexError:
            a, b = random.sample(set([x.display_name for x in ctx.guild.members]), 2)
            h = False
    if h:
        a = people[0]
    if re.findall("<@(\d{18})>", a):
        a = bot.get_user(int(re.findall("<@(\d{18})>", a)[0])).display_name
    if re.findall("<@(\d{18})>", b):
        b = bot.get_user(int(re.findall("<@(\d{18})>", b)[0])).display_name

    val = shipValue(a, b)
    if (a.lower() == "shiva" and b.lower() == "lal") or (b.lower() == "shiva" and a.lower() == "lal"):
        val = 69
    if val in range(0,11):
        msg = f"Awful :face_vomiting:"
    elif val == 69:
        msg = f":flushed:"
    elif val in range(11,31):
        msg = f"Meh :neutral_face:"
    elif val in range(31,51):
        msg = f"Almost good :face_with_raised_eyebrow:"
    elif val in range(51,71):
        msg = f"Pretty good :blush:"
    elif val in range(71,91):
        msg = f"Great :heart_eyes:"
    elif val in range(91, 100):
        msg = f"Almost perfect :sparkling_heart:"
    elif val == 100:
        msg = f"PERFECT :sparkles:"
    fullc = math.floor(round_to_5(val) / 10)
    emptc = 10 - fullc
    full = "<:f:971070032241127536>"
    half = "<:h:971070061139877939>"
    empty = "<:e:971070086360215572>"
    bar = ""
    for i in range(fullc):
        bar += full
    if str(round_to_5(val))[-1] == "5":
        bar += half
        emptc -= 1
    for i in range(emptc):
        bar += empty
    embed = discord.Embed(title="")
    embed.add_field(name=f":twisted_rightwards_arrows: `{merge(a, b)}`", value=f"**{val}%** {bar} {msg}")
    await ctx.send(content=f":two_hearts: `{a}`\n:two_hearts: `{b}`", embed=embed)

@bot.command(name = "sniper", aliases = ["snipe"])
@nobl()
async def sniper(ctx):
    color = discord.Colour.from_rgb(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    global sniper_
    match len(sniper_):
        case 0:
            await ctx.reply('are you stupid or something theres nothing to snipe')
        case _:
            embed = discord.Embed(title="Deleted message", description=f'Message content: "{sniper_[0][0]}"\nUser: <@{sniper_[0][1]}>\nChannel: <#{sniper_[0][2]}>', color=color)
            embed.set_footer(text='lol sniped')
            await ctx.send(embed=embed)

@bot.command()
@nobl()
async def snipelist(ctx):
    color = discord.Colour.from_rgb(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    global snipelist_
    embed = discord.Embed(title="Snipe list (most recent at top)", description='', color=color)
    match len(snipelist_):
        case 0:
            embed.add_field(name = 'No items!', value = 'If there was anything to snipe, it would show up here.')
        case 1:
            embed.add_field(name = 'Item 1', value = f'Content: "{snipelist_[0][0]}"\nUser: <@{snipelist_[0][1]}>\nChannel: <#{snipelist_[0][2]}>', inline = False)
            embed.set_footer(text='Snipelist can store at most 5 messages')
        case 2:
            embed.add_field(name = 'Item 1', value = f'Content: "{snipelist_[1][0]}"\nUser: <@{snipelist_[1][1]}>\nChannel: <#{snipelist_[1][2]}>', inline = False)
            embed.add_field(name = 'Item 2', value = f'Content: "{snipelist_[0][0]}"\nUser: <@{snipelist_[0][1]}>\nChannel: <#{snipelist_[0][2]}>', inline = False)
            embed.set_footer(text='Snipelist can store at most 5 messages')
        case 3:
            embed.add_field(name = 'Item 1', value = f'Content: "{snipelist_[2][0]}"\nUser: <@{snipelist_[2][1]}>\nChannel: <#{snipelist_[2][2]}>', inline = False)
            embed.add_field(name = 'Item 2', value = f'Content: "{snipelist_[1][0]}"\nUser: <@{snipelist_[1][1]}>\nChannel: <#{snipelist_[1][2]}>', inline = False)
            embed.add_field(name = 'Item 3', value = f'Content: "{snipelist_[0][0]}"\nUser: <@{snipelist_[0][1]}>\nChannel: <#{snipelist_[0][2]}>', inline = False)
            embed.set_footer(text='Snipelist can store at most 5 messages')
        case 4:
            embed.add_field(name = 'Item 1', value = f'Content: "{snipelist_[3][0]}"\nUser: <@{snipelist_[3][1]}>\nChannel: <#{snipelist_[3][2]}>', inline = False)
            embed.add_field(name = 'Item 2', value = f'Content: "{snipelist_[2][0]}"\nUser: <@{snipelist_[2][1]}>\nChannel: <#{snipelist_[2][2]}>', inline = False)
            embed.add_field(name = 'Item 3', value = f'Content: "{snipelist_[1][0]}"\nUser: <@{snipelist_[1][1]}>\nChannel: <#{snipelist_[1][2]}>', inline = False)
            embed.add_field(name = 'Item 4', value = f'Content: "{snipelist_[0][0]}"\nUser: <@{snipelist_[0][1]}>\nChannel: <#{snipelist_[0][2]}>', inline = False)
            embed.set_footer(text='Snipelist can store at most 5 messages')
        case 5:
            embed.add_field(name = 'Item 1', value = f'Content: "{snipelist_[4][0]}"\nUser: <@{snipelist_[4][1]}>\nChannel: <#{snipelist_[4][2]}>', inline = False)
            embed.add_field(name = 'Item 2', value = f'Content: "{snipelist_[3][0]}"\nUser: <@{snipelist_[3][1]}>\nChannel: <#{snipelist_[3][2]}>', inline = False)
            embed.add_field(name = 'Item 3', value = f'Content: "{snipelist_[2][0]}"\nUser: <@{snipelist_[2][1]}>\nChannel: <#{snipelist_[2][2]}>', inline = False)
            embed.add_field(name = 'Item 4', value = f'Content: "{snipelist_[1][0]}"\nUser: <@{snipelist_[1][1]}>\nChannel: <#{snipelist_[1][2]}>', inline = False)
            embed.add_field(name = 'Item 5', value = f'Content: "{snipelist_[0][0]}"\nUser: <@{snipelist_[0][1]}>\nChannel: <#{snipelist_[0][2]}>', inline = False)
            embed.set_footer(text='Snipelist can store at most 5 messages')
    await ctx.send(embed=embed)

@bot.command()
@nobl()
async def brainfuck(ctx, *code):
    code = ''.join(code)
    t = time.time()
    output = BrainfuckInterpreter(code, verbose=False).output
    embed = discord.Embed(title="")
    embed.add_field(name="Input", value=f"```{code}```", inline=False)
    embed.add_field(name="Output", value=f"```{output}```", inline=False)
    embed.set_footer(text=f"done in {math.floor((time.time()-t)*1000)}ms")
    await ctx.send(embed=embed)

@bot.command()
@staff()
async def exempt(ctx, *user: discord.Member):
    if not user:
        user = (ctx.author,)

    for u in user:
        if u.id in exempted:
            exempted.remove(u.id)
            await ctx.send(f"{u} is no longer exempted from police")
            return
        exempted.append(u.id)
        await ctx.send(f"{u} is now exempted from police")

@bot.command()
@staff()
async def nickname(ctx, *args):
    await ctx.guild.get_member(bot.user.id).edit(nick=' '.join(args))
    await ctx.message.add_reaction(CHECK_MARK_EMOJI)

@bot.command()
@staff()
async def bl(ctx, user: discord.Member):
    global blList
    if user in blList:
        blList.remove(user.id)
        removedtxt = '**' + str(user) + '** removed from blacklist.'
        await ctx.reply(removedtxt)
    elif user.id not in blList:
        blList.append(user.id)
        addedtxt = '**' + str(user) + '** added to blacklist.'
        await ctx.reply(addedtxt)

@bot.command()
@nobl()
async def about(ctx):
    color = discord.Colour.from_rgb(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    embed=discord.Embed(title="About can pooper",url='https://www.google.com/', description="", color=color)
    embed.add_field(name="Extra",value=f"There is literlaly b o info about this bot like idc kys bro\nBot has been running since <t:{t}:R>",inline=False)
    embed.set_footer(text="a creative footer because im out of ideas")
    await ctx.send(embed=embed)

@bot.command(name="translate")
@nobl()
async def _translate(ctx, *args):
    await translate(ctx, " ".join(args))

@bot.command(name = "game", aliases = ["wordgame", "guess"])
@nobl()
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
            await new_word.add_reaction(CHECK_MARK_EMOJI)
            break
        if new_word.content.lower() not in LWORDS:
            continue
        if new_word.content == target_substring:
            await new_word.reply("dont be lazy choose a different word")
            continue
        if target_substring in new_word.content.lower():
            score = 2.7 ** len(new_word.content.lower()) * 17
            await new_word.reply(f"Good job (you have been awarded with {math.ceil(score)} social credits)")
            user_data[str(ctx.author.id)]["score"] += math.ceil(score)
            update_data(user_data)
            break

@bot.command(name = "hangman")
@nobl()
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
            msg = await bot.wait_for("message", check=check, timeout=10)
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

# for maz
@bot.command(name = "countries", aliases = ["country", "countryguess"])
@nobl()
async def _countries(ctx):
    await _hangman(ctx, "countries")

# RATIO COMMAND!!!!
@bot.command(name = "ratio")
@nobl()
async def _ratio(ctx, user: discord.Member):
    msgs = await ctx.channel.history(limit=20).flatten()
    for msg in msgs:
        if msg.author.id == user.id:
            reply = await msg.reply(random.choice(["ratio", "ratio bozo", "take this ratio"]))
            await msg.add_reaction(THUMBS_UP_EMOJI)
            await reply.add_reaction(THUMBS_UP_EMOJI)
            return
    await ctx.message.add_reaction(CROSS_MARK_EMOJI)

# very useful command
@bot.command()
@nobl()
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

# outdated and im too lazy to update
@bot.command(name="help", aliases=["Help"])
@nobl()
async def help(ctx):
    color = discord.Colour.from_rgb(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
    embed=discord.Embed(title="Commands", description="", color=color)
    embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/282/face-with-spiral-eyes_1f635-200d-1f4ab.png")
    embed.add_field(name=f"{primary_prefix}ping", value="See the latency of the bot in ms.", inline=False)
    embed.add_field(name=f"{primary_prefix}penis", value="How big is yours?\n`.penis @user`", inline=False)
    embed.add_field(name=f"{primary_prefix}whoasked", value="A command to find who asked.", inline=False)
    embed.add_field(name=f"{primary_prefix}sniper", value="Shows the most recent deleted message, so you can hold what people say against them even after they delete it.", inline=False)
    embed.add_field(name=f"{primary_prefix}snipelist", value="Shows the 5 most recent deleted messages. Most recent on top", inline=False)
    embed.add_field(name=f"{primary_prefix}editsnipe", value="Shows the most recent edited message.", inline=False)
    embed.add_field(name=f"{primary_prefix}translate", value="Translates whatever text you input into bad english.\n`.translate <insert text here>`", inline=False)
    embed.add_field(name=f"{primary_prefix}about", value="Shows some information about the bot :man_shrugging:", inline=False)
    embed.set_footer(text="nghfnhghnghfnghf")
    await ctx.send(embed=embed)

@bot.command(name = "commands")
@nobl()
async def _commands(ctx):
    await ctx.reply(f"```py\n{[str(x) for x in bot.commands]} ```")

@bot.command()
@dev()
async def restart(ctx):
    await ctx.message.add_reaction(HOURGLASS_EMOJI)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command(name = "time", aliases = ["unix"])
@nobl()
async def _time(ctx):
    await ctx.reply(math.floor(time.time()))

@bot.command()
@nobl()
async def ping(ctx):
    await ctx.reply("Ping: `" + str(round(bot.latency * 1000)) + "` ms")

@bot.command(name="death", aliases = ["deathdate","whenwillidie","dead"])
@nobl()
async def _death(ctx, *person: discord.Member):
    if not person:
        person = ctx.author
        other = False
    else:
        person = person[0]
        other = True
    msg = await ctx.reply("Calculating...")
    current_time = math.floor(time.time())
    random.seed(person.id / 18) # 13
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
        await ctx.message.add_reaction(CHECK_MARK_EMOJI)
    except:
        await ctx.message.add_reaction(CROSS_MARK_EMOJI)

@bot.command()
@nobl()
async def echo(ctx, *msg):
    if ctx.author.id in [672892838995820553, 650439182204010496]:
        try: 
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
    await ctx.send(" ".join(msg))

@bot.event
async def on_ready():
    global t, police
    police = False

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    print('[' + str(time.strftime("%H:%M:%S", time.localtime())) + "] bot is now running")
    
    t = math.floor(time.time()) # record time at which bot started running
    
    channel = bot.get_channel(967896902823718932) # automatically join vc
    await channel.connect()
    
    """
    _guild = bot.get_guild(966819556016418856) # start tracking channels
    for idx in _guild.text_channels:
        tracking_channels.append(idx.id)
    """

    # await check_for_dead_channel()

@bot.command(name="eval", aliases=["exec", "lol"])
@owner()
async def lol(ctx, *, code):
    _globals = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "blList": blList,
        "owner": owner,
        "math": math,
        "random": random,
        "time": time,
        "exempted": exempted,
        "guild": ctx.guild,
        "dox": dox_command,
        "ghostping": _ghost_ping,
        "sys": sys,
        "snipelist": snipelist_,
        "user_data": user_data,
    }
    
    buffer = io.StringIO()

    try:
        with redirect_stdout(buffer):
            exec(f"async def func():\n{indent(code, '    ')}", _globals)
            func = await _globals["func"]()
            result = f"{buffer.getvalue()}\n-- {func}\n"
            try:
                await ctx.message.add_reaction(CHECK_MARK_EMOJI)
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
        "blList": blList,
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

@bot.command(name = "police")
@staff()
async def _police(ctx):
    global police
    police = not police
    await ctx.send(f"police mode is now `{police}`")

@bot.command()
@dev()
async def send_news(ctx: commands.Context, channel: int):
    channel = bot.get_channel(channel)
    
    news_file = open("news.txt")
    news_message = news_file.read()
    news_paragraphs = news_message.split("\n\n")
    
    for paragraph in news_paragraphs:
        await channel.send(paragraph + "\n​")
        await asyncio.sleep(1)

"""
# @tasks.loop(seconds=10)
async def check_for_dead_channel():
    while True:
        for id in open("tracking_channels.txt", "r").read().split("\n"):
            if not id.strip():
                continue
            channel = await bot.fetch_channel(int(id))
            last_msg = [ch async for ch in channel.history(limit=1)]
            if not last_msg:
                await channel.send("first")
            
            elif last_msg[0].author.id == 895318267151929405 and last_msg[0].content.startswith("dead chat X"):
                break

            if (datetime.now().replace(tzinfo=None) - last_msg[0].created_at.replace(tzinfo=None)).seconds >= 10:
                await channel.send(f"dead chat X{'D' * random.randrange(0,10)}")
        await asyncio.sleep(10)
"""

"""
@bot.command(name = "track", aliases = ["deadchattrack", "deadchat"])
@dev()
async def _track(ctx, channel: discord.TextChannel = None):
    try:
        with open("tracking_channels.txt", "a") as file:
            file.write("\n")
            if not channel:
                ch = ctx.channel.id
            else:
                ch = channel.id
            file.write(str(ch))
            file.close()
        await ctx.message.add_reaction(CHECK_MARK_EMOJI)
    except:
        await ctx.message.add_reaction(CROSS_MARK_EMOJI)
"""

# handler for when a message is sent
@bot.event
async def on_message(message):
    print(f'--------\n{message.author}: {message.content}\nChannel: ', end='')
    try: print(f'{message.channel} ({message.channel.id})\nGuild: {message.guild.name}\n')
    except: print("possibly a dm\n")


    if message.author.bot:
        return
    
    if message.content.removeprefix(primary_prefix).strip().lower().split()[0] in [str(cmnd) for cmnd in bot.commands]:
        if str(message.author.id) not in user_data.keys():
            print(user_data)
            user_data[str(message.author.id)] = {
                "id": message.author.id,
                "score": 0,
            }
            update_data(user_data)

    if message.channel.id in tracking_channels:
        with open("msg_count.txt", "a") as file:
            file.write("\n")
            file.write(str(message.channel.id))
            file.close()

    if len(snipelist_) > 5:
        snipelist_.remove(snipelist_[0])
    
    await bot.process_commands(message)
    
    global police
    if police or message.author.id in policing:
        await _police(message, exempted)
    
    if "ratio" in message.content.lower():
        if message.reference is not None:
            await message.add_reaction(THUMBS_UP_EMOJI)
            original_msg = await message.channel.fetch_message(message.reference.message_id)
            await original_msg.add_reaction(THUMBS_UP_EMOJI)
    
    if random.random() < val:
        responses = ["ratio", "take this ratio", "ratio bozo"]
        ratio = await message.reply(random.choice(responses))
        await ratio.add_reaction(THUMBS_UP_EMOJI)
        original_msg = await message.channel.fetch_message(ratio.reference.message_id)
        await original_msg.add_reaction(THUMBS_UP_EMOJI)

@bot.command(name = "val")
@dev()
async def _val(ctx, value: float):
    global val
    val = value
    await ctx.message.add_reaction(CHECK_MARK_EMOJI)

@bot.command(name = "dox", aliases = ["doxx"])
async def dox_command(ctx, user: discord.User):
    msg: discord.Message = await ctx.send("Waiting...")
    await asyncio.sleep(2)
    doxxer = Doxxer(user.id / 13)

    # insert stuff here

    embed = discord.Embed(
        title = "Private Information Extractor v1.0.4",
        description = f"{user.mention}'s info:"
    )
    embed.add_field(name = "FULL NAME", value = doxxer.full_name, inline = False)
    embed.add_field(name = "AGE", value = f"{doxxer.age} years", inline = False)
    embed.add_field(name = "GENDER", value = doxxer.gender, inline = False)
    embed.add_field(name = "ADDRESS", value = doxxer.address, inline = False)
    embed.add_field(name = "IP ADDRESS", value = doxxer.ip, inline = False)
    embed.add_field(name = "DISCORD AUTH TOKEN", value = doxxer.token, inline = False)

    embed.set_footer(text = "for legal reasons this is a joke (but is it really?)")

    await msg.edit(content="", embed=embed)

@bot.command()
@nobl()
async def convert(ctx, value: float, currency = None):
    if not currency:
        embed = discord.Embed(title = "JAYD-USD Converter", description = f"${value:,.2f} USD ≈ 😹{to_jayd(value):,.2f} Jayd Dollar\n😹{value:,.2f} Jayd Dollar ≈ ${to_usd(value):,.2f} USD")
        embed.set_footer(text = f"Conversion rate: 1 Jayd Dollar = ${USD_TO_JAYD_CONVERSION_RATE:,.3f} USD")
        await ctx.reply(embed = embed)
        return
    elif currency.lower() in ("jayd", "jay", "j", "jayd dollar", "😹", ":joy_cat:"):
        embed = discord.Embed(title = "Jayd Dollar to USD", description = f"😹{value:,.2f} Jayd Dollar ≈ ${to_usd(value):,.2f} USD")
    elif currency.lower() in ("usd", "us", "us dollar", "$", "dollar"):
        embed = discord.Embed(title = "USD to Jayd Dollar", description = f"${value:,.2f} USD ≈ 😹{to_jayd(value):,.2f} Jayd Dollar")
    else:
        await ctx.reply(f"idiot, re-do this command but this time do it like this:\n```{primary_prefix}convert 250 Jayd```\n```{primary_prefix}convert 1500 USD```")
        return
    embed.set_footer(text = f"Conversion rate: 1 Jayd Dollar = ${USD_TO_JAYD_CONVERSION_RATE:,.3f} USD")
    await ctx.reply(embed = embed)

@bot.command()
@dev()
async def test(ctx, *args):
    await translate(ctx, " ".join(args))

@bot.command()
@nobl()
async def nitro(ctx, user: discord.User = None):
    code = ''.join([random.choice(ascii_lowercase + ascii_uppercase + digits) for i in range(24)])
    if not user:
        user = ctx.author
        await ctx.reply("Check your DMs for free nitro!")
        await user.send(f"https://discord.gift/{code}")
        await asyncio.sleep(1)
        await user.send("Nitro sent to you by: yourself\nNote: this has an approximately 0.0000000000000000000000000000000000000000096% chance of being a real nitro link")
    else:
        await ctx.message.add_reaction(CHECK_MARK_EMOJI)
        await user.send(f"https://discord.gift/{code}")
        await asyncio.sleep(1)
        await user.send(f"Nitro sent to you by: {ctx.author}\nNote: this has an approximately 0.0000000000000000000000000000000000000000096% chance of being a real nitro link")

@bot.command(name = "ghostping", aliases = ["ghost_ping"])
@nobl()
async def _ghost_ping(ctx, user: discord.User):
    try:
        await ctx.message.delete()
    except (discord.errors.Forbidden, discord.errors.NotFound):
        pass
    msg = await ctx.send(user.mention)
    await msg.delete()

@bot.command(name = "change_name_of_everybody_in_the_server")
@dev()
async def name(ctx):
    if not ctx.guild.me.guild_permissions.manage_nicknames:
        await ctx.message.add_reaction(CROSS_MARK_EMOJI)
        return
    await ctx.message.add_reaction(HOURGLASS_EMOJI)
    for member in ctx.guild.members:
        try:
            await member.edit(nick = get_name())
        except discord.errors.Forbidden:
            await ctx.message.add_reaction(WARNING)
        except discord.errors.HTTPException:
            pass
    await ctx.message.add_reaction(CHECK_MARK_EMOJI)
    await asyncio.sleep(1)
    await ctx.message.clear_reactions()

@bot.command(name = "crawl")
@dev()
async def _crawl(ctx, *url):
    if not url:
        url = None
    else:
        url = " ".join(url)

    await ctx.message.add_reaction(HOURGLASS_EMOJI)

    w = Wikicrawler(url)

    history = await w.crawl()

    if w.exit_code == 0:
        if len(history) == 1:
            path = "Philosophy"
        else:
            path = ' → '.join(history)
        embed = discord.Embed(title = "Wikipedia Crawler", description = f"```{path}```")
        embed.set_footer(text = f"If you go to a Wikipedia article, click on the first link in the page, and repeatedly click the first links in subsequent pages, you will (mostly) reach the page for Philosophy. Here, it took {w.steps} redirects to get to Philosophy")
        await ctx.reply(embed=embed)
    else:
        match w.exit_code:
            case 1:
                await ctx.reply(f"It seems that <{w.entry}> is not a valid Wikipedia page.")
            case 2:
                await ctx.reply(f"It seems that following the first URL of every page starting from <{w.entry}> results in a loop.")
            case 3:
                await ctx.reply(f"It seems that <{w.entry}> leads to a disambiguation page.\nA disambiguation Wikipedia page is a page with multiple different articles with similar titles.")
            case 4:
                await ctx.reply(f"It seems that following the first URL of every page starting from <{w.entry}> results in a dead end.")

@bot.command(name = "search", aliases = ["google", "wikipedia"])
@nobl()
async def _search(ctx, *url):
    url = ' '.join(url)
    url = url.replace(" ", "_").capitalize()
    if not url.startswith("https://en.wikipedia.org/wiki/"):
        url = "https://en.wikipedia.org/wiki/" + url
    await ctx.reply("Warning: This command is in beta. Please expect it to be extremely broken")
    crawler = Crawler(url)
    crawler.search_paragraphs()
    try:
        if crawler.disambiguation:
            name = url.replace("https://en.wikipedia.org/wiki/", "")
            
            formatted = '\n- '.join(crawler.results)
            await ctx.reply(f"{name} may refer to the following:\n- {formatted}\n\n")
        else:
            formatted = '\n\n'.join(crawler.results)
            await ctx.reply(f"{formatted[:500]}\n\n")
    except discord.errors.HTTPException:
        await ctx.reply("you are such a bozo, the link you sent was invalid")

@bot.command(name = "score", aliases = ["bal", "balance"])
@nobl()
async def _score(ctx, user: discord.User = None):
    if not user:
        user = ctx.author
    await asyncio.sleep(0.1)
    await ctx.reply(f"Your social credit score: {load_data()[str(user.id)]['score']}")

@bot.command(name = "sokoban", aliases = ["soko", "blockpush"])
@nobl()
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
    await msg.add_reaction(ARROW_UP)
    await msg.add_reaction(ARROW_DOWN)
    await msg.add_reaction(ARROW_LEFT)
    await msg.add_reaction(ARROW_RIGHT)
    await msg.add_reaction(CROSS_MARK_EMOJI)

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
                user_data[str(ctx.author.id)]["score"] += score
                update_data(user_data)
                break

        await msg.remove_reaction(reaction[0], reaction[1])
        rows = "\n".join([''.join([s.icons[x] for x in a]) for a in s.grid])
        embed.description = rows
        await msg.edit(embed = embed)

if __name__ == "__main__":
    token = open("token.txt","r").read()
    bot.run(token)