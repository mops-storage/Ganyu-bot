import discord
from discord.ext import commands
from config import settings
import asyncio
import os
import logging

bot = commands.Bot(settings['prefix'], intents = discord.Intents.all())
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

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