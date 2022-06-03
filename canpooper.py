import discord
from discord.ext import commands

import io
import os
import sys
import time
from datetime import datetime
from dateutil import relativedelta
import math
import random
from string import ascii_uppercase, ascii_lowercase, digits

import re
from itertools import combinations, cycle
from contextlib import redirect_stdout
from googletrans import Translator
from textwrap import indent
from traceback import format_exception
from emoji import demojize
import asyncio

from src.brainfuck import BrainfuckInterpreter
from src.police import police as _police
from src.conversion import to_usd, to_jayd, USD_TO_JAYD_CONVERSION_RATE
from src.consts import LWORDS, CHECK_MARK_EMOJI, CROSS_MARK_EMOJI, \
    HOURGLASS_EMOJI, THUMBS_UP_EMOJI, CLOWN_EMOJI, FIRST_NAMES, \
    LAST_NAMES, STREET_NAME_ENDINGS, STREET_TYPES
from src.wikicrawler import Wikicrawler

primary_prefix = "!"
bot = commands.Bot(
    command_prefix = [primary_prefix, "lol "],
    intents = discord.Intents(guilds=True, members=True, bans=True, emojis=True, voice_states=True, messages=True, reactions=True), 
    allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True),
    help_command=None)
blList, snipelist_, sniper_, edit_, policing, tracking_channels, exempted = [], [], [], [], [], [], []
police, animation = False, False
t = 0

def product(s):
    res = 1
    for i in s:
        res *= i
    return res

def merge(a, b):
    a_slug_len = math.floor(len(a)/2)+1 if len(a) == 1 else math.floor(len(a)/2)
    b_slug_len = math.floor(len(b)/2)
    return a[:a_slug_len] + b[b_slug_len:]

def shipValue(a, b): 
    """return abs(math.ceil(100 * math.sin(product([ord(x) for x in a]) * product([ord(x) for x in b]))))"""
    
    """random.seed(product([ord(x) for x in a]) * product([ord(x) for x in b]))
    x = math.ceil(random.random()*100)
    random.seed(None)
    return x"""

    proda = product([ord(x) for x in a])
    prodb = product([ord(x) for x in b])
    return abs(math.ceil(100 * math.sin(proda * prodb)))

def round_to_5(s):
    return round(s/5) * 5

def nobl():
    def am(ctx):
        return (ctx.message.author.id not in blList)
    return commands.check(am)

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
    650439182204010496, # yue
    690265771955585029, # jay
    816692546272100442, # deshpande
    ]
    def am(ctx):
        return (ctx.message.author.id in staffs)
    return commands.check(am)

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
@nobl()
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

@bot.command(name="re")
@nobl()
async def _re(ctx, *s):
    s = ' '.join(s)
    await ctx.send(''.join(list(filter(lambda a: a != ":", list(demojize(s))))))

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

@bot.command(name="animation")
@dev()
async def _animation(ctx):
    global animation
    animation = (False if animation else True)
    frames = ["8D", "8=D", "8==D", "8===D", "8==D", "8=D"]
    _bot = ctx.guild.get_member(bot.user.id)
    for i in cycle(frames):
        if animation:
            await _bot.edit(nick=i)
            await asyncio.sleep(2)
        else:
            break

@bot.command()
@dev()
async def nickname(ctx, *args):
    await ctx.guild.get_member(bot.user.id).edit(nick=' '.join(args))
    await ctx.message.add_reaction(CHECK_MARK_EMOJI)

@bot.command()
@staff()
async def bl(ctx, user : discord.Member):
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

@bot.command()
@nobl()
async def translate(ctx, *args):
    translator = Translator()
    translateorigin = ''
    if not args:
        embed=discord.Embed(title="Bad translation machine")
        embed.add_field(name="Input", value="``` ```")
        embed.add_field(name="Output", value="```idiot you need to provide something for me to translate```")
        embed.set_footer(text=f'done in 69ms')
        await ctx.send(embed=embed)
        return
    for i in args:
        translateorigin = translateorigin + str(i) + ' '
    if len(translateorigin) > 1024:
        await ctx.send(f'Too many characters! ({len(translateorigin)} characters inputted)\nMust be 1024 or fewer in length.')
    else:
        t1 = time.time_ns()
        loadingsent = await ctx.send('Loading...')
        translation1 = translator.translate(translateorigin, dest='gu') # Gujarati
        translation2 = translator.translate(translation1.text, dest='so') # Somali
        translation3 = translator.translate(translation2.text, dest='ja') # Japanese
        translation4 = translator.translate(translation3.text, dest='xh') # Xhosa
        translation5 = translator.translate(translation4.text, dest='ko') # Korean
        translation6 = translator.translate(translation5.text, dest='mi') # Maori
        translation7 = translator.translate(translation6.text, dest='en') # English
        t2 = time.time_ns()
        t = (t2 - t1) / 1000
        if translateorigin == translation1.text and translation1.text == translation2.text and translation2.text == translation3.text and translation3.text == translation4.text and translation4.text == translation5.text and translation5.text == translation6.text:# and translation6.text == translation7.text and translation7.text == translation8.text
            await ctx.send('API limit reached. Maybe try again later?')
        embed = discord.Embed(title='Bad translation machine')
        embed.add_field(name='Input', value=f'```{translateorigin}```')
        embed.add_field(name='Output', value=f'```{translation7.text}```')
        embed.set_footer(text=f'done in {math.floor(t/1000)}ms')
        await loadingsent.edit(content='Done!',embed=embed)

@bot.command()
@nobl()
async def test(ctx, *args):
    translator = Translator()
    translateorigin = ''
    if not args:
        embed=discord.Embed(title="Bad translation machine")
        embed.add_field(name="Input", value="``` ```")
        embed.add_field(name="Output", value="```idiot you need to provide something for me to translate```")
        embed.set_footer(text=f'done in 69ms')
        await ctx.send(embed=embed)
        return
    for i in args:
        translateorigin = translateorigin + str(i) + ' '
    if len(translateorigin) > 1024:
        await ctx.send(f'Too many characters! ({len(translateorigin)} characters inputted)\nMust be 1024 or fewer in length.')
    else:
        t1 = time.time_ns()
        loadingsent = await ctx.send('Loading...')
        translation1 = translator.translate(translateorigin, dest='en') # Gujarati
        t2 = time.time_ns()
        t = (t2 - t1) / 1000
        #if translateorigin == translation1.text and translation1.text == translation2.text and translation2.text == translation3.text and translation3.text == translation4.text and translation4.text == translation5.text and translation5.text == translation6.text:# and translation6.text == translation7.text and translation7.text == translation8.text
        #    await ctx.send('API limit reached. Maybe try again later?')
        embed = discord.Embed(title='Good translation machine')
        embed.add_field(name='Input', value=f'```{translateorigin}```')
        embed.add_field(name='Output', value=f'```{translation1.text}```')
        embed.set_footer(text=f'done in {math.floor(t/1000)}ms')
        await loadingsent.edit(content='Done!',embed=embed)


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

@bot.command()
@dev()
async def restart(ctx):
    await ctx.message.add_reaction(HOURGLASS_EMOJI)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
@nobl()
async def unix(ctx):
    await ctx.reply(math.floor(time.time()))

@bot.command()
@nobl()
async def ping(ctx):
    await ctx.reply("Ping: `" + str(round(bot.latency * 1000)) + "` ms")

@bot.command(name="death",aliases = ["deathdate","whenwillidie","dead"])
@nobl()
async def _death(ctx, *person : discord.Member):
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
    print('[' + str(time.strftime("%H:%M:%S", time.localtime())) + "] can pooper is now running")
    
    t = math.floor(time.time()) # record time at which bot started running
    
    #channel = bot.get_channel(967137143208161301) # automatically join vc
    #await channel.connect()

    #_guild = bot.get_guild(966819556016418856) # start tracking g9ds channels
    #for idx in _guild.text_channels:
    #    tracking_channels.append(idx.id)

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
        "neng": 'cool',
        "exempted": exempted,
        "guild": ctx.guild,
        "dox": dox_command,
        "ghostping": _ghost_ping,
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
        def ballsacks(txt):
            return txt.replace("neng","n") # for hiding my name ong
        embed=discord.Embed(title='')
        embed.add_field(name='imagine getting an error',value = ballsacks((f'```py\n{result}```')))
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
        "neng": 'cool',
        "exempted": exempted,
        "guild": ctx.guild,
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

@bot.command()
@staff()
async def police(ctx):
    global police
    police = not police
    await ctx.send(f"police mode is now `{police}`")

@bot.command()
async def send_news(ctx: commands.Context, channel: int):
    channel = bot.get_channel(channel)
    # Check if the person is permitted to publish news articles
    if not ctx.author.id in [650439182204010496, 672892838995820553]:
        await ctx.reply("ur not permitted to publish articles bozo :joy_cat: :joy_cat: :joy_cat:")
        return
    
    news_file = open("news.txt")
    news_message = news_file.read()
    news_paragraphs = news_message.split("\n\n")
    
    for paragraph in news_paragraphs:
        await channel.send(paragraph + "\n​")
        await asyncio.sleep(1)

@bot.command(name="school", aliases=["schoolend","whendoesschoolend","endofschool"])
async def school(ctx):
    current_time = math.floor(time.time())
    school_end_unix = 1656442200
    seconds = school_end_unix - current_time
    minutes = math.floor(seconds / 60)
    hours = math.floor(minutes / 60)
    days = math.ceil(hours / 24)
    embed = discord.Embed(title="Time until end of school", description=f"Days: {days}\nHours: {hours}\nMinutes: {minutes}\nSeconds: {seconds}\n\nSchool ends <t:{school_end_unix}>")
    embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/141/alarm-clock_23f0.png")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """
    print(f'---New Message---\nContent: "{message.content}"\nUser: {message.author}\nChannel: ',end='')
    try: print(f'{message.channel} ({message.channel.id})\nGuild: {message.guild.name}\n')
    except: print("possibly a dm\n")
    """
    
    if message.author.bot:
        return
    
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
    
    if random.random() < 0.02:
        responses = ["ratio", "take this ratio", "ratio bozo"]
        ratio = await message.reply(random.choice(responses))
        await ratio.add_reaction(THUMBS_UP_EMOJI)
        original_msg = await message.channel.fetch_message(ratio.reference.message_id)
        await original_msg.add_reaction(THUMBS_UP_EMOJI)

@bot.command(name = "dox", aliases = ["doxx"])
async def dox_command(ctx, user: discord.User):
    random.seed(user.id / 13)

    msg: discord.Message = await ctx.send("Waiting...")
    await asyncio.sleep(5)

    # insert stuff here

    embed = discord.Embed(
        title = "Private Information Extractor v1.0.4",
        description = f"{user.mention}'s info:",
    )

    embed.add_field(
        name = "FULL NAME",
        value = random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
        inline = False
    )

    embed.add_field(
        name = "AGE",
        value = f"{random.randrange(2,150)} years",
        inline = False
    )

    embed.add_field(
        name = "GENDER",
        value = random.choice(("Male", "Male", "Male", "Female", "Female", "Female", "Non-binary")),
        inline = False
    )
    
    embed.add_field(
        name = "ADDRESS",
        value = str(random.randrange(1, 2500)) + " " + random.choice(LWORDS).title() + random.choice(STREET_NAME_ENDINGS) + " " + random.choice(STREET_TYPES),
        inline = False
    )

    embed.add_field(
        name = "IP ADDRESS",
        value = str(random.randrange(0, 256)) + "." + str(random.randrange(0, 256)) + "." + str(random.randrange(0, 256)) + "." + str(random.randrange(0, 256)),
        inline = False
    )

    t1 = ''.join([random.choice(ascii_uppercase + ascii_uppercase + ascii_uppercase + ascii_lowercase + digits) for i in range(24)])
    t2 = ''.join([random.choice(ascii_uppercase + ascii_uppercase + digits) for i in range(6)])
    t3 = ''.join([random.choice(ascii_uppercase + ascii_lowercase + digits) for i in range(11)])
    t4 = ''.join([random.choice(ascii_uppercase + digits) for i in range(5)])
    
    embed.add_field(
        name = "DISCORD AUTH TOKEN",
        value = t1 + "." + t2 + "." + t3 + "-" + t4,
        inline = False
    )

    random.seed(None)
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
@nobl()
async def nitro(ctx, user: discord.User = None):
    code = ''.join([random.choice(ascii_lowercase + ascii_uppercase + digits) for i in range(24)])
    if not user:
        user = ctx.author
        await ctx.reply("Check your DMs for free nitro!")
        await user.send(f"https://discord.gift/{code}")
        await asyncio.sleep(1)
        await user.send("Nitro sent to you by: yourself\n||Note: this has an approximately 0.0000000000000000000000000000000000000000096% chance of being a real nitro link||")
    else:
        await ctx.message.add_reaction(CHECK_MARK_EMOJI)
        await user.send(f"https://discord.gift/{code}")
        await asyncio.sleep(1)
        await user.send(f"Nitro sent to you by: {ctx.author}\n||Note: this has an approximately 0.0000000000000000000000000000000000000000096% chance of being a real nitro link||")

@bot.command(name = "ghostping", aliases = ["ghost_ping"])
@nobl()
async def _ghost_ping(ctx, user: discord.User):
    try:
        await ctx.message.delete()
    except (discord.errors.Forbidden, discord.errors.NotFound):
        pass
    msg = await ctx.send(user.mention)
    await msg.delete()

@bot.command(name = "crawl", aliases = ["wikicrawl", "wikipedia", "crawler", "wikicrawler", "philosophy"])
@nobl()
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

if __name__ == "__main__":
    token = open("token.txt","r").read()
    bot.run(token)