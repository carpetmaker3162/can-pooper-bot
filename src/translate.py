import math
import discord
from googletrans import Translator
import time

async def translate(ctx, args):
    path = ["gu", "so", "ja", "xh", "ko", "af", "az", "sw", "mi", "en"]
    arguments = list(args.split())
    if "path=" in arguments:
        new_arguments = arguments[:arguments.index("path=")]
        path = arguments[arguments.index("path=")+1:]
        arguments = new_arguments
    translator = Translator()
    if not arguments:
        embed=discord.Embed(title="Bad translation machine")
        embed.add_field(name="Input", value="``` ```")
        embed.add_field(name="Output", value="```idiot you need to provide something for me to translate```")
        embed.set_footer(text=f'done in 69ms')
        await ctx.send(embed=embed)
        return
    txt = " ".join(list(arguments))
    if len(txt) > 1024:
        await ctx.send(f'Too many characters! ({len(txt)} characters inputted)\nMust be 1024 or fewer in length.')
    else:
        t1 = time.time_ns()
        loadingsent = await ctx.send('Loading...')
        for i in path:
            txt = translator.translate(txt, dest=i).text
        t2 = time.time_ns()
        t = (t2 - t1) / 1000
        embed = discord.Embed(title='Bad translation machine')
        embed.add_field(name='Input', value=f'```{" ".join(arguments)}```')
        embed.add_field(name='Output', value=f'```{txt}```')
        embed.set_footer(text=f'done in {math.floor(t/1000)}ms')
        await loadingsent.edit(content='Done!',embed=embed)