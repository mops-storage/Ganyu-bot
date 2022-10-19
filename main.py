# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from config import settings
import asyncio
import os
import logging
import logging.handlers
from discord.ui import Select, View

bot = commands.Bot(settings['prefix'], intents = discord.Intents.all())
#bot.remove_command('help')
discord.utils.setup_logging(level = logging.INFO, root = False)

@bot.event
async def on_ready():
    print(f'{bot.user.name} підключився до Discord.')
    for guild in bot.guilds:
        print(guild.id)
        members_count = 0
        members_count += len(guild.members)
            
        while True: # Status bots in his profile
            await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"{settings['prefix']}help | v{settings['version']}"))
            await asyncio.sleep(30)
            await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = f"за {members_count} користувачів"))
            await asyncio.sleep(30)

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