# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
from config import settings
from asyncio import sleep
import sqlite3
import random
import easy_pil
import datetime
from discord.utils import get


data = sqlite3.connect('data.sqlite')# connected to BD
cur = data.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (
        'id' INT,
        'name' TEXT,
        'mention' TEXT,
        'avatar' TEXT,
        'reg' TEXT,
        'join' TEXT,
        'cash' INT,
        'money' INT,
        'xp' INT,
        'lvl' INT,
        'bot' TEXT,
        'server_id' INT
        )""")

data.commit()

class Economy(commands.Cog, name='Економічні команди'):
    def __init__(self, bot):
        self.bot=bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy commands - Ready!')# Виводить, коли гвинтик готовий до роботи
        for guild in self.bot.guilds:
            print(f'Свервер {guild.name} під  id {guild.id} - знайдено')
            for member in guild.members:
                cur.execute(f"SELECT id FROM users where id={member.id}")
                if cur.fetchone() == None:
                    cur.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', '{member.avatar}', '{member.created_at}', '{member.joined_at}', 200, 0, 0, 1, '{member.bot}', {guild.id})")
                else:
                    pass
                data.commit()

    @commands.Cog.listener()
    async def on_memmber_join(self, member):
        """Додання користувача до БД, який зашов на сервер
        ---
        Args:
            member (dist): Спиок, в якому міститься дані користувача, котрі пізніше будуть додані до БД
        """
        cur.execute(f'SELECT id FROM users WHERE id = {member.id}')
        if cur.fetchone() == None:
            cur.execute(f"INSERT INTO users VALUES (?, '{member.name}', '<@{member.id}>', '{member.avatar}', '{member.create_at}', '{member.joined_at}', 200, 0, 0, 1, '{member.bot}', {member.guild.id})",({member.id}, '{member.name}', '<@{member.id}>', '{member.avatar}', '{member.create_at}', '{member.joined_at}', 200, 0, 0, 1, '{member.bot}', {member.guild.id}))
            data.commit()
        else:
            pass
        
        channel = self.bot.get_channel(930193655183056939)
        await channel.send(f'Привіт {member.name}, ти попав на сервер {member.guild.name}')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.content) > 10:
            for row in cur.execute(f'SELECT xp, lvl, mention, cash FROM users WHERE id = {message.author.id}'):
                global xp, lvl, mention, cash
                xp = row[0]
                lvl = row[1]
                mention = row[2]
                cash = row[3]

            if message.author.bot == False:
                xp += random.randint(0, 2) # add exp for message, default from 0 to 2
                nexp = int(5 * (lvl ** 2) + (50 * lvl) + 100) # Formula to calculate the next level
                print(f'Xp користувача {message.author.name} змінено на {xp}. До натсупного рівня {nexp}')
                cur.execute(f'UPDATE users SET xp = {xp} WHERE id = {message.author.id}')
                if xp >= nexp:
                    nlvl = lvl + 1
                    await message.channel.send(f'Агов {mention}, ти підняв свій рівень на {nlvl}')
                    if nlvl == 5:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 10:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 20:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 30:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 40:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 50:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 60:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 70:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 80:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 90:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    elif nlvl == 100:
                        gift = nlvl * 100
                        await message.channel.send(f'Також в подарок ти торимуєш {gift} грошей! Вітаю!')
                    else:
                        gift = row[3]
                    cur.execute(f'UPDATE users SET xp = 0, lvl = {nlvl}, cash = {cash + gift} WHERE id = {message.author.id}')
            #await self.bot.process_commands(message)
            data.commit()
            
    @commands.command(name='card')
    async def card(self, ctx, user: discord.Member = None):
        """
        Повертає картку, на якій зазанчена інформація про рівень користувача, або автора команди.\n
        ---\n
        >> .card `<none or user mention>`
        """
        if user is None:
            user = ctx.author
            for row in cur.execute(f'SELECT name, cash, money, xp, lvl FROM users WHERE id = {user.id}'):
                name = row[0]
                cash = row[1]
                money = row[2]
                xp = row[3]
                lvl = row[4]
                procent = int(5 * (lvl ** 2) + (50 * lvl) + 100)
                req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
                banner_id = req["banner"]
                if banner_id is None:
                    bbackground = easy_pil.utils.load_image("https://media.discordapp.net/attachments/939569454390603837/1030821644597473431/bg_no_banner.jpg").resize((932, 282))
                else:
                    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=2048"    
                    bbackground = easy_pil.utils.load_image(str(banner_url))
                    bbackground = easy_pil.Editor(bbackground).resize((932, 282), crop = True)
                # draw card🔽
                background = easy_pil.Editor(easy_pil.Canvas((932, 282)))
                rec = easy_pil.utils.load_image("https://cdn.discordapp.com/attachments/939569454390603837/1029807764211511316/rec_blask.png").resize((894, 242))
                background.paste(bbackground, (0, 0))
                profile_image = easy_pil.utils.load_image(str(user.avatar))
                profile = easy_pil.Editor(profile_image).resize((190, 190)).circle_image()
                poppins = easy_pil.Font.montserrat(size = 30)
                background.paste(rec, (20, 20))
                background.paste(profile, (50, 50))
                if str(user.status) == "online":
                    global color
                    color = "#43b581"
                elif str(user.status) == "offline" or user.status == "invisible":\
                    color = "#747f8d"
                elif str(user.status) == "idle":
                    color = "#faa51b"
                elif str(user.status) == "dnd" or user.status == "do_not_disturb":
                    color = "#f04848"
                else:
                    await ctx.send("Status don't work")
                background.ellipse((42, 42), width=206, height=206, outline=f"{color}", stroke_width=10)
                background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
                step = int((xp / int(5 * (lvl ** 2) + (50 * lvl) + 100))*100)
                if xp < 10 and xp > 0:
                    background.bar(
                        (260, 180),
                        max_width = 630,
                        height = 40,
                        percentage = 6,
                        fill = "#00fa81",
                        radius = 20
                    )
                else:
                    background.bar(
                        (260, 180),
                        max_width = 630,
                        height = 40,
                        percentage = step,
                        fill = "#00fa81",
                        radius = 20
                    )
                    print(step)
                background.text((270, 120), f"{user.name}#{user.discriminator}", font = poppins, color = "#00fa81")
                background.text(
                    (870, 125),
                    f"{xp} / {procent}",
                    font = poppins,
                    color = "#00fa81",
                    align = "right",
                    )

                rank_level_texts = [
                    easy_pil.Text("Rep ", color = "#00fa81", font = poppins),
                    easy_pil.Text(f"A+", color = "#1EAAFF", font = poppins),
                    easy_pil.Text("   Рівень ", color = "#00fa81", font = poppins),
                    easy_pil.Text(f"{lvl}", color = "#1EAAFF", font = poppins),
                ]
                background.multicolor_text((850, 30), texts = rank_level_texts, align = "right")
                background.save("card.png")
                await ctx.send(file = discord.File(fp = "card.png"))
        else:
            for row in cur.execute(f'SELECT name, cash, money, xp, lvl FROM users WHERE id = {user.id}'):
                name = row[0]
                cash = row[1]
                money = row[2]
                xp = row[3]
                lvl = row[4]
                procent = int(5 * (lvl ** 2) + (50 * lvl) + 100)
                print(f'Користувач {name}, досвіду {xp}')
                req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
                banner_id = req["banner"]
                if banner_id is None:
                    bbackground = easy_pil.utils.load_image("https://media.discordapp.net/attachments/939569454390603837/1030821644597473431/bg_no_banner.jpg").resize((932, 282))
                    background = easy_pil.Editor(easy_pil.Canvas((932, 282)))
                    background.paste(bbackground, (0, 0))
                    profile_image = easy_pil.utils.load_image(str(user.avatar))
                    profile = easy_pil.Editor(profile_image).resize((190, 190)).circle_image()
                    poppins = easy_pil.Font.montserrat(size = 30)
                    background.paste(profile, (50, 50))   
                else:
                    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=2048"    
                    bbackground = easy_pil.utils.load_image(str(banner_url))
                    bbackground = easy_pil.Editor(bbackground).resize((932, 282), crop = True)
                    
                # draw card🔽
                background = easy_pil.Editor(easy_pil.Canvas((932, 282)))
                rec = easy_pil.utils.load_image("https://cdn.discordapp.com/attachments/939569454390603837/1029807764211511316/rec_blask.png").resize((894, 242))
                background.paste(bbackground, (0, 0))
                profile_image = easy_pil.utils.load_image(str(user.avatar))
                profile = easy_pil.Editor(profile_image).resize((190, 190)).circle_image()
                poppins = easy_pil.Font.montserrat(size = 30)
                background.paste(rec, (20, 20))
                background.paste(profile, (50, 50))
                if str(user.status) == "online":
                    color = "#43b581"
                elif str(user.status) == "offline" or user.status == "invisible":\
                    color = "#747f8d"
                elif str(user.status) == "idle":
                    color = "#faa51b"
                elif str(user.status) == "dnd" or user.status == "do_not_disturb":
                    color = "#f04848"
                else:
                    await ctx.send("Status don't work")
                background.ellipse((42, 42), width=206, height=206, outline=f"{color}", stroke_width=10)
                background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
                step = int((xp / int(5 * (lvl ** 2) + (50 * lvl) + 100))*100)
                if xp < 10 and xp > 0:
                    background.bar(
                        (260, 180),
                        max_width = 630,
                        height = 40,
                        percentage = 6,
                        fill = "#00fa81",
                        radius = 20
                    )
                else:
                    background.bar(
                        (260, 180),
                        max_width = 630,
                        height = 40,
                        percentage = step,
                        fill = "#00fa81",
                        radius = 20
                    )
                background.text((270, 120), f"{user.name}#{user.discriminator}", font = poppins, color = "#00fa81")
                background.text(
                    (870, 125),
                    f"{xp} / {procent}",
                    font = poppins,
                    color = "#00fa81",
                    align = "right",
                )

                rank_level_texts = [
                    easy_pil.Text("Rep ", color = "#00fa81", font = poppins),
                    easy_pil.Text(f"A+", color = "#1EAAFF", font = poppins),
                    easy_pil.Text("   Рівень ", color = "#00fa81", font = poppins),
                    easy_pil.Text(f"{lvl}", color = "#1EAAFF", font = poppins),
                ]
                background.multicolor_text((850, 30), texts = rank_level_texts, align = "right")
                background.save("card.png")
                await ctx.send(file = discord.File(fp = "card.png"))
        
    @commands.command(name='set_exp')
    async def set_xp(self, ctx, count:int, user: discord.Member = None):
        """Встановлює досвід користувачу

        Args:
            `count` (int): Кількість досвіду
            `user` (discord.Member, optional): Користувач, якому змінюється досвід. Якщщо це параметр пустий(`None`), тоді досвід присвоюється автору. 
        Example:
        >> .set_exp `<count>` `<user:optional>`\n
        >> .set_exp `40`\n
        >> .set_exp `40` `@Indi Mops`
        """
        await ctx.channel.purge(limit=1)
        if user is None:
            user=ctx.author
            cur.execute(f'UPDATE users SET xp = {count} WHERE id = {user.id}')
            emb = discord.Embed(title = 'Досвід успішно змінено', description=f'Досвід користувача **<@{user.id}>** упішно змінено на **{count}**', color = 0x46eb34)
            await ctx.send(embed = emb)
            data.commit()
        else:
            cur.execute(f'UPDATE users SET xp = {count} WHERE id = {user.id}')
            emb = discord.Embed(title = 'Досвід успішно змінено', description=f'Досвід користувача **<@{user.id}>** упішно змінено на **{count}**', color = 0x46eb34)
            await ctx.send(embed = emb)
            data.commit()
    
    @commands.command(name='set_lvl')
    async def set_xp(self, ctx, count:int, user: discord.Member = None):
        """Встановлює рівень користувачу

        Args:
            `count` (int): Кількість досвіду
            `user` (discord.Member, optional): Користувач, якому змінюється досвід. Якщщо це параметр пустий(`None`), тоді досвід присвоюється автору. 
        Example:
        >> .set_lvl `<count>` `<user:optional>`\n
        >> .set_lvl `40`\n
        >> .set_lvl `40` `@Indi Mops`
        """
        await ctx.channel.purge(limit=1)
        if user is None:
            user=ctx.author
            cur.execute(f'UPDATE users SET lvl = {count} WHERE id = {user.id}')
            emb = discord.Embed(title = 'Рівень успішно змінено', description=f'Рівень користувача **<@{user.id}>** упішно змінено на **{count}**', color = 0x46eb34)
            await ctx.send(embed = emb)
            data.commit()
        else:
            cur.execute(f'UPDATE users SET xp = {count} WHERE id = {user.id}')
            emb = discord.Embed(title = 'Рівень успішно змінено', description=f'Рівень користувача **<@{user.id}>** упішно змінено на **{count}**', color = 0x46eb34)
            await ctx.send(embed = emb)
            data.commit()
    
    
    @commands.command(alias='ld')
    async def leaderboard(self, ctx):
        count = 0
        count_member = 0
        for i in cur.execute(f'SELECT id FROM users WHERE server_id = {ctx.author.guild.id}'):
            count_member+=1
        embed = discord.Embed(title=f'Свього окристувачів: {count_member}', color=0x46eb34)
        for row in cur.execute(f'SELECT name, lvl, xp FROM users WHERE server_id = {ctx.author.guild.id} ORDER BY lvl DESC, xp DESC, name ASC LIMIT 10'):
            count+=1
            embed.add_field(
                name=f'# {count} - {row[0]}',
                value=f'**Рівень:** {row[1]} | **Досвід:** {row[2]}',
                inline=False
            )
            embed.set_thumbnail(url=ctx.author.guild.icon)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
