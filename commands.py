# -*- coding: utf-8 -*-
from discord.ext import commands
import discord
from config import settings
from asyncio import sleep
import sqlite3
import random
import easy_pil
import os

bot = commands.Bot(settings['prefix'], intents = discord.Intents.all())
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
        'bot' TEXT
        )""")

data.commit()
@bot.event
async def on_ready():
    print('Бот готовий')# When ready
    for guild in bot.guilds:
        print(guild.id)
        for member in guild.members:
            global members_count
            members_count = 0
            members_count += len(guild.members) 

            cur.execute(f"SELECT id FROM users where id={member.id}")
                    if cur.fetchone() == None:
                        cur.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', '{member.avatar_url}', '{member.created_at}', '{member.joined_at}', 200, 0, 0, 1, '{member.bot}')")
                    else:
                        pass
                    data.commit()
            while True: # Status bots in his profile
                await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"{settings['prefix']}help | v{settings['version']}"))
                await sleep(35)
                await bot.change_presence(status = discord.Status.online, activity=discord.Game(f"Дивиться за {members_count} користувачів"))
                await sleep(35)

    @bot.event
    async def on_memmber_join(member):
            cur.execute(f'SELECT id FROM users WHERE id = {member.id}')
            if cur.fetchone() == None:
                cur.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', '{member.avatar_url}', '{member.create_at}', '{member.joined_at}', 200, 0, 0, 1, '{member.bot}')")
            else:
                pass
            data.commit()

    @bot.event
    async def on_message(message):
            if len(message.content) > 10:
                for row in cur.execute(f'SELECT xp, lvl, mention, cash FROM users WHERE id = {message.author.id}'):
                    global xp, lvl, mention, cash
                    xp = row[0]
                    lvl = row[1]
                    mention = row[2]
                    cash = row[3]

                if message.author.bot == False:
                    xp += random.randint(0, 2) # add exp for message, default from 0 to 2
                    print(f'Xp користувача {message.author.name} змінено на {xp}')
                    cur.execute(f'UPDATE users SET xp = {xp} WHERE id = {message.author.id}')
                    nexp = int(5 * (lvl ** 2) + (50 * lvl) + 100) # Formula to calculate the next level
                    print(xp)
                    print(int(nexp))
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
            await bot.process_commands(message)
            data.commit()

    @bot.command()
    async def card(ctx, user: discord.Member = None):
            """
            Повертає картку, на якій зазанчена інформація про рівень користувача, або автора команди.\n
            ---\n
            >> .card <none or user mention>
            """
            if user is None:
                user = ctx.author
                for row in cur.execute(f'SELECT name, cash, money, xp, lvl FROM users WHERE id = {user.id}'):
                    global uid, name, cash, money, xp, lvl
                    name = row[0]
                    cash = row[1]
                    money = row[2]
                    xp = row[3]
                    lvl = row[4]
                procent = int(5 * (lvl ** 2) + (50 * lvl) + 100)
                req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
                banner_id = req["banner"]
                if banner_id is None:
                    bbackground = easy_pil.untils.load_image("https://media.discordapp.net/attachments/939569454390603837/1030821644597473431/bg_no_banner.jpg").resize((894, 242))
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
                if xp < 10:
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
                req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
                banner_id = req["banner"]
                if banner_id is None:
                    bbackground = easy_pil.utils.load_image("https://media.discordapp.net/attachments/939569454390603837/1030821644597473431/bg_no_banner.jpg").resize((894, 242))
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
                if xp < 10:
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
                        radius = 20,
                        outline = "#ffffff", stroke_width = 3
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

    @bot.command()
    async def test(ctx, user: discord.Member = None):
            #user = ctx.author
            req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
            banner_id = req["banner"]
            print(banner_id)
            if banner_id is None:
                banner_url = "https://cdn.discordapp.com/attachments/939569454390603837/1029805586096852992/rank_card.png"
            else:
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=2048"
            emb = discord.Embed(title = 'Banner')
            emb.set_image(url = banner_url)
            await ctx.send(embed = emb)

    @bot.command()
    async def add_exp(ctx, count, user: discord.Member = None):
            await ctx.channel.purge(limit = 1)
            if user is None:
                user = ctx.author
                cur.execute(f'UPDATE users SET xp = {count} WHERE id = {user.id}')
                emb = discord.Embed(title = 'Досвід успішно змінено', description = f'Досвід користувача **<@{user.name}>** упішно змінено на **{count}**', color = 0x46eb34)
                await ctx.send(embed = emb)
                print('None')
                data.commit()
            else:
                cur.execute(f'UPDATE users SET xp = {count} WHERE id = {user.id}')
                emb = discord.Embed(title = 'Досвід успішно змінено', decription = f'Досвід користувача **<@{user.name}>** упішно змінено на **{count}**', color = 0x46eb34)
                await ctx.send(embed = emb)
                print('Mem')
                data.commit()










if select.values[0] == '1':
                    emb = discord.embed(
                        title = 'Padoru',
                        description = 'It\' time to...',
                        color = 0x0013FA
                    )
                    emb.set_image(url = 'https://media.tenor.com/ddSa-psbO3sAAAAC/fate-padoru-christmas.gif')
                    await interaction.response.send_message(embed = emb)
                elif select.values[0] == '2':
                    emb = discord.embed(
                        title = 'What\'s?',
                        description = 'Sorawo squints',
                        color = 0x67d4a7
                    )
                    emb.set_image(url = 'https://im2.ezgif.com/tmp/ezgif-2-1a4f4f4f55.gif')
                    await interaction.response.send_message(embed = emb)
                elif select.values[0] == '3':
                    emb = discord.embed(
                        title = 'For real?',
                        description = 'Hehe, not hee!',
                        color = 0x67d4a7
                    )
                    emb.set_image(url = 'https://media.tenor.com/Bt2rs4I7uMcAAAAC/hu-tao.gif')
                    await interaction.response.send_message(embed = emb)