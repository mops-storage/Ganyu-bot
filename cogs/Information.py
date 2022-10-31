from discord.ext import commands
import discord
from config import settings
from asyncio import sleep

class Information(commands.Cog, name='Інформативні команди'):
    async def setup(bot):
        await bot.add_cog(Information(bot))
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Information commands - Ready!')
        
    @commands.command()
    @commands.cooldown(1, 604700, commands.BucketType.user)
    async def cool(self, ctx):
        await ctx.send("Work!")
        
async def setup(bot):
    await bot.add_cog(Information(bot))