from dataclasses import replace
from tkinter.tix import Select
from turtle import colormode
from discord.ext import commands
from discord.ui import Select, View
import discord
from config import settings
import sqlite3
import time

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()

class Information(commands.Cog, name='Інформативні команди'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Information commands - Ready!')
        global start_time
        start_time = int(time.time())
        
    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx, command = None):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]

        if command == None:
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
                        value='Перелік всіх команд та категорій',
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
                value=f'`{settings["prefix"]}help` `{settings["prefix"]}info` `{settings["prefix"]}stats` `{settings["prefix"]}server` `{settings["prefix"]}user`',
                inline=False
                )
            embed.add_field(
                name=f'💰Економіка ({settings["prefix"]}help economy)',
                value=f'`{settings["prefix"]}card` `{settings["prefix"]}set_xp` `{settings["prefix"]}set_lvl`',
                inline=False
                )
            
            await ctx.defer(ephemeral=True)
            await ctx.reply(embed=embed, view=view)
        elif command == 'help':
            embed = discord.Embed(
                title='Перелік всіх команд та категорій',
                description='Показує всі доступні команди та категорії бота',
                color=settings['color']
            )
            
            embed.set_author(
                name=f'Команда "{settings["prefix"]}help"'
            )
            embed.add_field(
                name='Використання',
                value=f'{settings["prefix"]}help `<назва команди чи категорії>`',
                inline=False
            )
            embed.add_field(
                name='Приклад 1',
                value=f'{settings["prefix"]}help\n┗Показує весь список команд',
                inline=False
            )
            embed.add_field(
                name='Приклад 2',
                value=f'{settings["prefix"]}help information\n┗Показує всі доступні команди категорії **📃Інформація**',
                inline=False
            )
            embed.add_field(
                name='Приклад 3',
                value=f'{settings["prefix"]}help help\n┗Показує детальну інформацію про команду **{settings["prefix"]}help** (!Ви зараз переглядаєте її!)'
            )
            
            embed.set_thumbnail(url=settings['avatar'])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=settings['avatar']
            )
            
            await ctx.reply(embed=embed)
        elif command == 'info':
            embed = discord.Embed(
                title=f'Корисна інформація про {settings["name"]}',
                description=f'Показує корисну інформацію про {settings["name"]} (версія, автор, посилання на ресурси і т.д.)',
                color=settings['color']
            )
            
            embed.set_author(
                name=f'Команда "{settings["prefix"]}info"'
            )
            embed.add_field(
                name='Використання',
                value=f'{settings["prefix"]}info',
                inline=False
            )
            
            embed.set_thumbnail(url=settings['avatar'])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=settings['avatar']
            )
            
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(embed=discord.Embed(title='Помилка', description=f'Такої команди чи категорії немає!\nПерегляньте команди за допомгою: {settings["prefix"]}help', color=0xff0000))
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @help.command(name='information')
    async def information(self, ctx):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
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
        
        await ctx.reply(embed=embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @commands.command(name='info')
    async def info(self, ctx):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
            
        embed = discord.Embed(
            title=settings['name'],
            description=f'Привіт, я Ґанью секретарка Цісін в Ліюе. Моє завдання допомагати мандрівникам освоюватися з дивовижним світом Тейват\n\nМій префікс `{settings["prefix"]}`. Якщо ти хочеш дізнатися всі мої команди тоді можеш скористатися **{settings["prefix"]}help**. Або скористайся **{settings["prefix"]}starjour**, щоб розпочати свою подорож<a:ganyuroll:1037043774850867241>',
            color=settings['color']
        )
        
        embed.set_thumbnail(url=settings['avatar'])
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=settings['avatar']
        )
        
        embed.add_field(
            name='Збірка:',
            value=f'{settings["version"]} (<t:1666194420:d>)'
        )
        embed.add_field(
            name='Мій розробник:',
            value='<:dev:1037048854190772295> [Indi Mops#0424](https://discord.com/users/734082410504781854)'
        )
        embed.add_field(
            name='⠀',
            value='⠀'
        )
        embed.add_field(
            name='Корисні посилання:',
            value=f'[Веб-сайт]({settings["site"]})\n[Сервер підтримки]({settings["support_server"]})'
        )
        embed.add_field(
            name='⠀',
            value=f'[GitHub репозиторій]({settings["github_repo"]})\n[top.gg]({settings["top.gg"]})'
        )
        embed.add_field(
            name='⠀',
            value=f'[Patreon]({settings["patreon"]})\n[Diaka]({settings["diaka"]})'
        )
        
        await ctx.reply(embed=embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @commands.command()
    async def stats(self, ctx):
        """Перевіряє чи працює Cog система"""
        ping = self.bot.latency
        for row in cur.execute(f'SELECT guilds, users, channels, commands FROM stats_bot'):
            StBguilds = row[0]
            StBusers = row[1]
            StBchannels = row[2]
            StBcommands = row[3]
          
        embed = discord.Embed(
            title=f'Статистика {settings["name"]}',
            color=settings['color']
            )
        embed.set_thumbnail(url=settings['avatar'])
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=settings['avatar']
        )
        
        embed.add_field(
            name='Основна',
            value=f'Сервери: {"{0:,}".format(StBguilds).replace(",", " ")}\nКористувачів: {"{0:,}".format(StBusers).replace(",", " ")}\nКаналів: {"{0:,}".format(StBchannels).replace(",", " ")}'
        )
        embed.add_field( 
            name='Платформена',
            value=f'Команд використано: {"{0:,}".format(StBcommands + 1).replace(",", " ")}\nЗатримка: {round(ping, 2)} мс.\nЗапущений: <t:{start_time}:R>'
        )
        
        await ctx.reply(embed=embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @commands.command()
    @commands.cooldown(1, 604700, commands.BucketType.user)
    async def cool(self, ctx):
        await ctx.reply(content = f'<t:{int(time.time()) + 30}:R>', delete_after = 30)
        
async def setup(bot):
    await bot.add_cog(Information(bot))