from discord.ext import commands
import sys
import asyncio
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Ready!\n\nUsage:\nSwitch channel:      .channel <channel id>\nType then send msg:  .type <seconds> <msg>\nStop program:        .exit\n\n##########################################')
    try:
        channel = int(sys.argv[1])
    except IndexError:
        print("Please specify a channel on command line!\nex: python3 talking.py 978304385895522324")
        await bot.close()
    ch = bot.get_channel(channel)
    while True:
        msg = input('msg: ')
        if msg == ".exit":
            await bot.close()
        elif msg.startswith('.channel '):
            ch = bot.get_channel(int(msg.split()[1].strip()))
            print(f"Channel is now {ch}")
            continue
        elif msg.startswith(".type "):
            secs = float(msg.split()[1].strip())
            async with ch.typing():
                await asyncio.sleep(secs)
            msg = ' '.join(msg.split()[2:])
        await ch.send(msg)

if __name__ == "__main__":
    bot.run(open("token.txt","r").read())