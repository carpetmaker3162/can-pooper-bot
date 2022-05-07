import discord
from discord.ext import commands

import io
import os
import sys
import time
import math
import random

import re
import itertools
import contextlib
from datetime import datetime
from googletrans import Translator
import textwrap
from traceback import format_exception
from emoji import demojize

import _brainfuck
from police import police as _police

primary_prefix = "!"
bot = commands.Bot(
    command_prefix = [primary_prefix, "lol ", "$", "%", "^", "&", "*", "-", "--", ", ", "/", ";;", ";", "?", "—"],
    intents = discord.Intents(guilds=True, members=True, bans=True, emojis=True, voice_states=True, messages=True, reactions=True), 
    allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True),
    help_command=None)
checkreaction, crossreaction, hourglass = '\N{WHITE HEAVY CHECK MARK}', '\N{CROSS MARK}', '\N{HOURGLASS}'
blList, snipelist_, sniper_, edit_, policing, tracking_channels, exempted = [], [], [], [], [], [], []
police, animation = False, False
lwords = tuple(open("/Users/neng/desktop/nengstuff/code/algorithm/words.txt", "r").read().split("\n"))
t = 0

POOPER_TIMES_PUBLISHERS = [
    672892838995820553, # Neng
    650439182204010496 # Yue
]

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
    return abs(math.ceil(100 * math.sin(product([ord(x) for x in a]) * product([ord(x) for x in b]))))
    """random.seed(product([ord(x) for x in a]) * product([ord(x) for x in b]))
    x = math.ceil(random.random()*100)
    random.seed(None)
    return x"""

def round_to_5(s):
    return round(s/5) * 5

def round_to_10(s):
    return round(s/10) * 10

def nobl():
    def am(ctx):
        return (ctx.message.author.id not in blList)
    return commands.check(am)

def botowner():
    def am(ctx):
        return (ctx.message.author.id == 672892838995820553)
    return commands.check(am)

def staff():
    staffs = [672892838995820553, # me
    650439182204010496, # yue
    690265771955585029] # jay
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
        return
    length = random.randrange(0, 21)
    random.seed(None)
    embed = discord.Embed(title="pp size calculator", description=f"{username}'s penis size\n8{'='*length}D")
    await ctx.send(embed=embed)
    
@bot.command()
@nobl()
async def dm(ctx, user: discord.Member, *message):
    try:
        await user.send(' '.join(message))
        await ctx.message.add_reaction(checkreaction)
    except:
        await ctx.message.add_reaction(crossreaction)

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
@botowner()
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
            h=False
    if h:
        a = people[0]
    if re.findall("<@(\d{18})>", a):
        a = bot.get_user(int(re.findall("<@(\d{18})>", a)[0])).display_name
    if re.findall("<@(\d{18})>", b):
        b = bot.get_user(int(re.findall("<@(\d{18})>", b)[0])).display_name

            
    val = shipValue(a, b)
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
    if str(val)[-1] == "5":
        bar += half
        emptc -= 1
    for i in range(emptc):
        bar += empty
    embed = discord.Embed(title="")
    embed.add_field(name=f":twisted_rightwards_arrows: `{merge(a, b)}`", value=f"**{val}%** {bar} {msg}")
    await ctx.send(content=f":two_hearts: `{a}`\n:two_hearts: `{b}`", embed=embed)

@bot.command()
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
    output = _brainfuck.BrainfuckInterpreter(code, verbose=False).output
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
@botowner()
async def _animation(ctx):
    global animation
    animation = (False if animation else True)
    frames = ["8D", "8=D", "8==D", "8===D", "8==D", "8=D"]
    _bot = ctx.guild.get_member(bot.user.id)
    for i in itertools.cycle(frames):
        if animation:
            await _bot.edit(nick=i)
            time.sleep(2)
        else:
            break

@bot.command()
@botowner()
async def nickname(ctx, *args):
    await ctx.guild.get_member(bot.user.id).edit(nick=' '.join(args))
    await ctx.message.add_reaction(checkreaction)

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
        translation1 = translator.translate(translateorigin, dest='hy')
        translation2 = translator.translate(translation1.text, dest='ht')
        translation3 = translator.translate(translation2.text, dest='ka')
        translation4 = translator.translate(translation3.text, dest='af')
        translation5 = translator.translate(translation4.text, dest='so')
        translation6 = translator.translate(translation5.text, dest='en')
        t2 = time.time_ns()
        t = (t2 - t1) / 1000
        if translateorigin == translation1.text and translation1.text == translation2.text and translation2.text == translation3.text and translation3.text == translation4.text and translation4.text == translation5.text and translation5.text == translation6.text:# and translation6.text == translation7.text and translation7.text == translation8.text
            await ctx.send('API limit reached. Maybe try again later?')
        embed = discord.Embed(title='Bad translation machine')
        embed.add_field(name='Input', value=f'```{translateorigin}```')
        embed.add_field(name='Output', value=f'```{translation6.text}```')
        embed.set_footer(text=f'done in {math.floor(t/1000)}ms')
        await loadingsent.edit(content='Done!',embed=embed)


@bot.command()
@nobl()
async def whoasked(ctx):
    msg = await ctx.send('[▖] Looking for who asked...')
    time.sleep(0.2)
    await msg.edit(content='[▘] Looking for who asked...')
    time.sleep(0.2)
    await msg.edit(content='[▝] Looking for who asked...')
    time.sleep(0.2)
    await msg.edit(content='[▗] Looking for who asked...')
    time.sleep(0.2)
    await msg.edit(content='[▖] Looking for who asked...')
    time.sleep(0.2)
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
    embed.set_footer(text="fhdfnsdhfndhgbsdf")
    await ctx.send(embed=embed)

@bot.command()
@botowner()
async def restart(ctx):
    await ctx.message.add_reaction(hourglass)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
@nobl()
async def unix(ctx):
    await ctx.reply(math.floor(time.time()))

@bot.command()
@nobl()
async def ping(ctx):
    await ctx.reply("Ping: `" + str(round(bot.latency * 1000)) + "` ms")

@bot.command()
@botowner()
async def say(ctx, channelid, *msg):
    try:
        channel_ = bot.get_channel(int(channelid))
        await channel_.send(' '.join(msg))
        print(f'Message \'{msg}\' sent. ')
        await ctx.message.add_reaction(checkreaction)
    except:
        await ctx.message.add_reaction(crossreaction)

@bot.command()
@nobl()
async def echo(ctx, *msg):
    await ctx.send(' '.join(msg))

@bot.event
async def on_ready():
    global t, police
    police = False
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="FHDbot bend over"))
    print('[' + str(time.strftime("%H:%M:%S", time.localtime())) + "] can pooper is now running")
    
    t = math.floor(time.time()) # record time at which bot started running
    
    channel = bot.get_channel(967137143208161301) # automatically join vc
    await channel.connect()

    _guild = bot.get_guild(966819556016418856) # start tracking g9ds channels
    for idx in _guild.text_channels:
        tracking_channels.append(idx.id)

@bot.command(name="eval", aliases=["exec", "lol"])
@botowner()
async def lol(ctx, *, code):
    _globals = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "blList": blList,
        "botowner": botowner,
        "math": math,
        "random": random,
        "time": time,
        "neng": 'cool',
        "exempted": exempted,
        "guild": ctx.guild,
    }

    buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(buffer):
            exec(f"async def func():\n{textwrap.indent(code, '    ')}", _globals)
            func = await _globals["func"]()
            result = f"{buffer.getvalue()}\n-- {func}\n"
            await ctx.message.add_reaction(checkreaction)
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
@botowner()
async def e(ctx, *expression):
    _globals = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "blList": blList,
        "botowner": botowner,
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
async def send_news(ctx: commands.Context, channel: discord.TextChannel):
    # Check if the person is permitted to publish news articles
    if not ctx.author.id in POOPER_TIMES_PUBLISHERS:
        await ctx.reply("ur not permitted to publish articles bozo :joy_cat: :joy_cat: :joy_cat:")
        return
    
    news_file = open("news.txt")
    news_message = news_file.read()
    news_paragraphs = news_message.split("\n\n")
    
    for paragraph in news_paragraphs:
        channel.send(paragraph)
        channel.send("​")

@bot.event
async def on_message(message):
    print(f'---New Message---\nContent: "{message.content}"\nUser: {message.author}\nChannel: ',end='')
    try: print(f'{message.channel} ({message.channel.id})\nGuild: {message.guild.name}\n')
    except: print("possibly a dm\n")

    
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


if __name__ == "__main__":
    token = open("token.txt","r").read()
    bot.run(token)