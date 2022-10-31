from tkinter.tix import Select
from discord.ext import commands
from discord.ui import Select, View
import discord
from config import settings
from asyncio import sleep

class Information(commands.Cog, name='Інформативні команди'):
    async def setup(bot):
        await bot.add_cog(Information(bot))
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Information commands - Ready!')

    @commands.command(name='help', invoke_without_command=True)
    async def help(self, ctx):
        menu = Select(
            placeholder='Виберіть категорію...',
            options=[
                discord.SelectOption(
                    label='Інформація',
                    value='1',
                    emoji='📃'
                ),
                discord.SelectOption(
                    label='Економіка',
                    value='2',
                    emoji='💰'
                )
            ]
        )
        
        async def callback(interaction:discord.Integration):
            if menu.values[0] == '1':
                embed = discord.Embed(
                    title='Доступні команди категорії 📃Інформація',
                    description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {settings["prefix"]}help `<назва команди>`',
                    color=settings['color']
                )
                embed.set_thumbnail(
                    url=settings['avatar']
                )
                embed.set_footer(
                    text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                    icon_url=settings['avatar']
                )
                embed.add_field(
                    name=f'{settings["prefix"]}help',
                    value='Список всі доступних команд та категорій',
                    inline=False
                )
                embed.add_field(
                    name=f'{settings["prefix"]}info',
                    value=f'Корисна інформація про {settings["name"]}',
                    inline=False
                )
                embed.add_field(
                    name=f'{settings["prefix"]}stats',
                    value=f'Статистика використання {settings["name"]}',
                    inline=False
                )
                embed.add_field(
                    name=f'{settings["prefix"]}server',
                    value='Інформація про поточний сервер',
                    inline=False
                )
                embed.add_field(
                    name=f'{settings["prefix"]}user',
                    value='Інформація про учасника',
                    inline=False
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
            if menu.values[0] == '2':
                embed = discord.Embed(
                    title='Доступні команди категорії 💰Економіка',
                    description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {settings["prefix"]}help `<назва команди>`',
                    color=settings['color']
                )
                embed.set_thumbnail(
                    url=settings['avatar']
                )
                embed.set_footer(
                    text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                    icon_url=settings['avatar']
                )
                embed.add_field(
                    name=f'{settings["prefix"]}card `<користувач>`',
                    value='Виводить інформацію про рівень користувача',
                    inline=False
                )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
        menu.callback = callback
        view = View()
        view.add_item(menu)
        
        embed=discord.Embed(
            title='Доступні команди:',
            description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {settings["prefix"]}help `<назва команди>`',
            color=settings['color']
            )
        embed.set_thumbnail(url=settings['avatar'])
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=settings['avatar']
            )
        embed.add_field(
            name=f'📃Information ({settings["prefix"]}help information)',
            value=f'`{settings["prefix"]}help` `{settings["prefix"]}info` `{settings["prefix"]}info` `{settings["prefix"]}stats` `{settings["prefix"]}serv`er `{settings["prefix"]}user`',
            inline=False
            )
        embed.add_field(
            name=f'💰Економіка ({settings["prefix"]}help economy)',
            value=f'`{settings["prefix"]}card`',
            inline=False
            )
        
        await ctx.defer(ephemeral=True)
        await ctx.reply(embed=embed, view=view)
        
    @commands.command()
    @commands.cooldown(1, 604700, commands.BucketType.user)
    async def cool(self, ctx):
        await ctx.send("Work!")
        
async def setup(bot):
    await bot.add_cog(Information(bot))