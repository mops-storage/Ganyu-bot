# -*- coding: utf-8 -*-import discord
import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands
from dislash import slash_command


class Test_Commands(commands.Cog, name='Команди розробника'):
    """Команди для перевірки різних функцій, подій і т.д.
    
    Виокристовується лиша для тесту і не більше!
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Test commands - Ready!')# Виводить, коли гвинтик готовий до роботи

    @commands.command()
    async def ping(self, ctx):
        """Перевіряє чи працює Cog система"""
        ping = self.bot.latency
        guilds = self.bot.guilds
        for guild in guilds:
            print(guild)
            print(f'Канали: {len(guild.text_channels) + len(guild.voice_channels) + len(ctx.guild.stage_channels)}')
        embed = discord.Embed(
            title=f'Пінг - {round(ping, 2)}\nСервери: {len(guilds)}\nУччасники: {len(self.bot.users)}'
        )
        await ctx.send(embed=embed)  

    @commands.command()
    async def create_invite(self, ctx, server_id: int):
        guild = self.bot.get_guild(server_id)
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
        await ctx.send(invite)


    
    @commands.command()
    async def select_menu(self, ctx):
        select = Select(
            placeholder='Вибери дію...',
            options=[
                discord.SelectOption(
                    label='Padoru',
                    value='1',
                    emoji='<a:SoraoDev:931927261731516477>',
                    description='Час настав...'
                    ),
                discord.SelectOption(
                    label='Що?',
                    value='2',
                    emoji='<a:SoraSquints:931922199403696188>',
                    description='Сорова мружиться'
                    ),
                discord.SelectOption(
                    label='Хе-хе, не хе-хе',
                    value='3',
                    emoji='<a:HuTaoRock:1030925213522727122>',
                    description='Ху Тао-Скала'
                    )
                ]
            )
        
        async def my_callback(interaction:discord.Interaction):
            if select.values[0] == '1':
                await interaction.response.send_message(f'Ти вибрав {select.values[0]}')
                await ctx.send(select.values[0])
            if select.values[0] == '2':
                await interaction.response.send_message(f'Ти вибрав {select.values[0]}')
            if select.values[0] == '3':
                await interaction.response.edit_message(content=f'Ти вибрав {select.values[0]}')
        
        select.callback = my_callback
        view = View()
        view.add_item(select)
    
        await ctx.defer(ephemeral=True)
        await ctx.send('Menu', view=view)

async def setup(bot):
    await bot.add_cog(Test_Commands(bot))