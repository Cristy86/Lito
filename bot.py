import discord
from discord.ext import commands

import asyncio
import os
import platform, pkg_resources, subprocess, pyfiglet, psutil
import codecs
import pathlib

from utils.settings import GREEN_EMBED, BOT_TOKEN, BOT_PREFIX
import utils.checks
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
description = "A android discord.py bot running on Termux."

bot = commands.Bot(description=description, command_prefix=commands.when_mentioned_or(BOT_PREFIX))
bot.launch_time = datetime.utcnow()
startup_extensions = ['cogs.owner','cogs.webhook','cogs.random','cogs.eh','jishaku']

@bot.event
async def on_ready():
    print(" ")
    print('Logged in as:')
    print('------')
    print(f'Username: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'Active on: {len(bot.guilds)} Servers.')
    print(f'Users: {len(bot.users)}')
    print(f'Cogs loaded: {len(bot.cogs)}')
    print('------')
    print(" ")
    subprocess.run(["pyfiglet","Lito"])
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {len(bot.users)} users."))

@bot.command(name='stats', aliases=["info"])
@commands.check(utils.checks.is_bot)
@commands.cooldown(1,5,BucketType.user) 
async def _stats(ctx):
    """Shows the stats about the bot. 5 second cooldown."""
    total = 0
    file_amount = 0
    for path, subdirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.py'):
                file_amount += 1
                with codecs.open('./' + str(pathlib.PurePath(path, name)), 'r', 'utf-8') as f:
                    for i, l in enumerate(f):
                        if l.strip().startswith('#') or len(l.strip()) == 0:
                            pass
                        else:
                            total += 1

    delta_uptime = datetime.utcnow() - bot.launch_time
    owner = bot.get_user(339752841612623872)
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=GREEN_EMBED)
    embed.title = "Stats"
    embed.add_field(name=f"Owned by {owner}", value=f"Status: {owner.status}\nUser ID: {owner.id}\nAccount created: {humanize.naturaldate(owner.created_at)}", inline=True)
    embed.description = f"\nPython Version: {platform.python_version()}\ndiscord.py version: {pkg_resources.get_distribution('discord.py').version}\nUsers: {len(bot.users)}\nPing latency: {round(bot.latency * 1000)}ms\nUptime: {days}d, {hours}h, {minutes}m, {seconds}s\nServers: {len(bot.guilds)}\nLine count: {total:,} lines and {file_amount:,} files.\nCPU Percent: {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}MiB"
    embed.set_footer(text=bot.user.name)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)                                                         
     
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(BOT_TOKEN)
