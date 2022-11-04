# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from config import settings
import asyncio
import os
import logging
import logging.handlers
from discord.ui import Select, View
import time
from time import strftime
from time import gmtime
import sqlite3

bot = commands.Bot(settings['prefix'], intents = discord.Intents.all())
bot.remove_command('help')
discord.utils.setup_logging(level = logging.INFO, root = False)

@bot.event
async def on_ready():
    print(f'{bot.user.name} підключився до Discord.')
    
    data = sqlite3.connect('data.sqlite')#connect to BD
    cur = data.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS stats_bot (
        'guilds' INT,
        'users' INT,
        'channels' INT,
        'commands' INT
        )""")
    data.commit()
    
    async def up_stats():
        """Оновлює статистику бота кожні 30 секунд
        """
        for row in cur.execute(f'SELECT guilds, users, channels, commands FROM stats_bot'):
            StBguilds = row[0]
            StBusers = row[1]
            StBchannels = row[2]
            StBcommands = row[3]
        guilds = bot.guilds
        users = len(bot.users)
        global channels
        channels = 0
        cur.execute(f'SELECT * FROM stats_bot')
        if cur.fetchone() == None:
            for guild in guilds:
                channels += len(guild.text_channels) + len(guild.voice_channels) + len(guild.stage_channels)
                cur.execute(f"INSERT INTO stats_bot VALUES ({int(len(guilds))}, {int(users)}, {int(channels)}, 0)")
                data.commit()
        else:
            for guild in bot.guilds:
                channels += len(guild.text_channels) + len(guild.voice_channels) + len(guild.stage_channels)
                cur.execute(f'UPDATE stats_bot SET guilds = {int(len(guilds))}, users = {int(users)}, channels = {int(channels)}, commands = {StBcommands}')
                data.commit()
    
    while True: # Status bots in his profile
        await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"{settings['prefix']}help | v{settings['version']}"))
        await up_stats()
        await asyncio.sleep(30)
        
        await up_stats()
        await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"за {len(bot.users)} користувачів"))
        await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = int(error.retry_after)
        cool = 0
        if cooldown < 60:
            cool = strftime('%S сек.', gmtime(cooldown))
        elif 60 < cooldown < 3600:
            cool = strftime('%M хв. %S сек.', gmtime(cooldown))
        elif 3600 < cooldown < 86400:
            cool = strftime('%H год. %M хв. %S сек.', gmtime(cooldown))
        elif 86400 < cooldown < 604800 or cooldown > 604800:
            cool = strftime('%d днів %H год. %M хв. %S сек.', gmtime(cooldown))
                    
        embed = discord.Embed(
            title='Помилка!',
            description=f'Ви ще не можете використовувати цю команду!\nСпробуйте через: **{cool}**',
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        print(error)
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title='Помилка!',
            description=f'Дану комнаду не знайдено!\nСкористайтесь: `{settings["prefix"]}help`',
            color=0xff0000
        )
        
        await ctx.reply(embed=embed)
        print(error)
        
async def load_extensions():
    """Load cogs for main file
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load_extensions()
    await bot.start(settings['token'])

if __name__ == '__main__':
    asyncio.run(main())