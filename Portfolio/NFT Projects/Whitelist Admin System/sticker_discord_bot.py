import time
import MySQLdb
import discord
from discord.ext import commands, tasks
import asyncio
# from datetime import date, datetime, timedelta, timezone
import pandas as pd
import json
from pandas import json_normalize
import requests as r
import mysql.connector as mysql
import discord
from discord.ext import commands, tasks
import re
from discord.utils import get
from dotenv import load_dotenv
from pathlib import Path
import os
import datetime
from collections import Counter
import re
import pytz
import schedule
from discord.ui import Button, View, TextInput, Modal


solana_pattern = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['db_user']
db_passw = os.environ['db_pass']
db_host = os.environ['db_host']
db_db = os.environ['db']
discord_key = os.environ['discord_key']

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)


email_array = []


#DB Query
check_whitelist = 'select wallet_address, accessed, discord_id from whitelist'
insert_whitelist = "insert into nft_wallet_list (wallet_address, accessed, discord_id, discord_username) VALUES(%s, %s, %s, %s)"


def run_query(statement, args = None):
    cursor = zohoDB.cursor()
    cursor.execute(statement, args)

    if "select" == statement.split()[0]:
        result = cursor.fetchall()
        cursor.close()
        return result
    else:
        zohoDB.commit()
        cursor.close()


wallet_address = ""

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

# CREATE INSTANCE OF THE BOT
bot = PersistentViewBot()

# Bot introduction
@bot.event
async def on_ready():
    my_guild = bot.get_guild(123456789)
    my_task.start(my_guild, bot)
    sticker_stats.start(my_guild, bot)
    view = PersistentView()
    bot.add_view(view)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    print('We have logged in as {0.user}'.format(bot))
    await bot.wait_until_ready()
    bot_feed = bot.get_channel(123456789)

@bot.command()
@commands.has_permissions(administrator=False)
async def show_verify(ctx):
    view = PersistentView()
    embed = discord.Embed(title=f"Join Sticker Club", description="Sign up in just 2 easy steps:", color=0xFFD700)
    embed.set_thumbnail(url="https://cdn.glitch.global/f622098c-2262-4edf-9a71-9533179e8463/sticker_club.png?v=1684268936117")
    embed.add_field(name=f"", value="1) Click the button below OR type **/stickerclub** in any channel\n2) Drop in your SOL wallet address when prompted", inline=False)
    await bot.get_channel(VERIFY_CHANNEL).send(embed=embed, view=view)

# PERSISTENT VIEW SUBCLASS
class PersistentView(View):

    def __init__(self):
        super().__init__(timeout=None)
        #self.is_persistent = True
        self.timeout = None
        #self.ctx = ctx

    @discord.ui.button(
        label = "Join Sticker Club",
        style = discord.ButtonStyle.blurple,
        custom_id="verify",
        emoji="🍀",
        )
    async def button_callback(self, interaction, button):
        await interaction.response.send_modal(Questionnaire())

#UTC 4:20 is 21:20
# cdt = pytz.timezone('US/Central')
cdt = datetime.timezone.utc
# If no tzinfo is given then UTC is assumed.
times = [
    datetime.time(hour=21, minute=20, tzinfo=cdt),
]

times_stats = [
    datetime.time(hour=13, minute=00, tzinfo=cdt),
]

#This is the channel that the Wallet Submit Button will go to when the !show_verify command is triggered
#Join Channel
VERIFY_CHANNEL = 123456789

class Questionnaire(Modal, title='Sticker Club'):
    wallet_address = TextInput(label='Submit your SOL wallet')
    #answer = TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        #await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
        await verify(interaction, str(self.wallet_address))

async def verify(interaction: discord.Interaction , wallet_address: str):
    user_id = interaction.user.id
    page = 1
    items_per_page = 100
    waitlist_data = []

    while True:
        response = r.get(f'https://portfolio.portfolio.com/check_waitlist?page={page}&items_per_page={items_per_page}')
        if response.status_code == 200:
            page_data = response.json()
            waitlist_data.extend(page_data)
            if len(page_data) < items_per_page:
                break
            page += 1
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("We are currently having some server issues. WTF. Reach out to one of the Mycelium Staff for further assistance.", ephemeral=True)
            return

    if solana_pattern.match(wallet_address):
        if any(entry['discord_id'] == str(user_id) for entry in waitlist_data):
            existing_entry = next((entry for entry in reversed(waitlist_data) if entry['discord_id'] == str(user_id)), None)
            if existing_entry['wallet_address'] != wallet_address:
                user = await bot.fetch_usfer(user_id)
                username = f"{user.name}#{user.discriminator}"
                ip_address = ""
                await interaction.response.defer(ephemeral=True)
                await interaction.followup.send(f"You've updated your Sticker Club wallet to **{wallet_address[:4]}...{wallet_address[-4:]}**.", ephemeral=True)
                url = "https://portfilio.portfolio.com/submit_stickerclub"
                data = {
                    "wallet_address": wallet_address,
                    "accessed": datetime.datetime.now(),
                    "discord_id": user_id,
                    "discord_username": username,
                    "ip_address": ip_address
                }
                response = r.post(url, data=data)
                if response.status_code == 200:
                    print("Data inserted successfully")
                return
    # check if the user_id matches any discord_id in the waitlist
    if any(entry['wallet_address'] == str(wallet_address) for entry in waitlist_data):

        #Check Spot on Wait/White list
        response = r.get('https://portfilio.portfolio.com/sticker_whitelist')
        if response.status_code == 200:
            json_data = response.json()

            for index, entry in enumerate(json_data):
                discord_id = entry['discord_id']
                if discord_id == str(user_id):
                    # print(f"You are number {index + 1} on the whitelist!")
                    break

        if index != -1:  # Check if a valid index was found
            channel = discord.utils.get(interaction.guild.channels, name="🎽｜club")
            channel_link = f"https://discord.com/channels/{interaction.guild.id}/"
            embed = discord.Embed(title="Sticker Club", description="You're already in the club!", color=0xFFD700)
            embed.add_field(name=f"You're currently #{index + 1} on the drop list!", value=channel_link, inline=False)
            # await interaction.response.defer(embed=embed, ephemeral=True)
            await interaction.response.defer(ephemeral=True)
            # Perform time-consuming operations here
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        else:
            channel = discord.utils.get(interaction.guild.channels, name="🚦｜wait-list")
            channel_link = f"https://discord.com/channels/{interaction.guild.id}/portfolio"
            # await interaction.response.send_message("You're already on the waitlist. In the meantime, come hang out in **#wait-list.**", ephemeral=True)
            embed = discord.Embed(title="Sticker Club Waitlist", description="You're already on the waitlist.", color=0xFFD700)
            embed.add_field(name=f"You're already on the waitlist. In the meantime, come hang out in **#wait-list.**", value=channel_link, inline=False)
            # await interaction.response.defer(embed=embed, ephemeral=True)
            await interaction.response.defer(ephemeral=True)
            # Perform time-consuming operations here
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
    last_address[user_id] = wallet_address  # store the current address for future comparison
    user = await bot.fetch_user(user_id)
    username = f"{user.name}#{user.discriminator}"
    ip_address = ""
    if solana_pattern.match(wallet_address):
        role = discord.utils.get(interaction.guild.roles, name="Sticker Waitlist")
        await interaction.user.add_roles(role)
        channel = discord.utils.get(interaction.guild.channels, name="🚦｜wait-list")

        channel_link = f"https://discord.com/channels/{interaction.guild.id}/1098245458159206540"
        embed = discord.Embed(title=f"Sticker Club Waitlist", description="Congrats! You've been added to the official Waitlist.", color=0xFFD700)
        embed.add_field(name="You've been granted access to the Waitlist channel:", value=channel_link, inline=False)
        # await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(embed=embed, ephemeral=True)

        url = "https://portfolio.portfolio.com/submit_stickerclub"
        data = {
            "wallet_address": wallet_address,
            "accessed": datetime.datetime.now(),
            "discord_id": user_id,
            "discord_username": username,
            "ip_address": ip_address
        }
        response = r.post(url, data=data)
        if response.status_code == 200:
            print("Data inserted successfully")

    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Please try again with a valid SOL address.", ephemeral=True)


@tasks.loop(time=times_stats)

async def sticker_stats(guild, bot):
    test_channel = bot.get_channel() #Test Channel
    sticker_club_channel = bot.get_channel() #Sticker Club Channel
    page = 1
    items_per_page = 100
    waitlist_count = 0
    while True:
        response = r.get(f'https://portfilio.pythonanywhere.com/sticker_waitlist?page={page}&items_per_page={items_per_page}')
        if response.status_code == 200:
            json_data = response.json()
            if len(json_data) == 0:
                break
            waitlist_count += len(json_data)
            page += 1
        else:
            break
    response = r.get('https://portfolio.pythonanywhere.com/sticker_whitelist')
    if response.status_code == 200:
        json_data = response.json()
        whitelist_count = len(json_data)

        embed = discord.Embed(title="Sticker Club Stats", description="", color=0xFFD700)
        embed.set_thumbnail(url="https://cdn.glitch.global/f622098c-2262-4edf-9a71-9533179e8463/sticker_club.png?v=1684268936117")
        embed.add_field(name="", value=f"Members: {whitelist_count}\n Waitlist: {waitlist_count-whitelist_count}\nCollections Dropped: 0", inline=False)
        await test_channel.send(embed = embed)


@tasks.loop(time=times)
# @tasks.loop(hours=24)
# @tasks.loop(minutes=1)
async def my_task(guild, bot):
    channel = bot.get_channel()
    sticker_club_channel = bot.get_channel() #Sticker Club Channel
    response = r.get('https://portfolio.pythonanywhere.com/sticker_whitelist')
    if response.status_code == 200:
        json_data = response.json()
        mentions = []
        for item in json_data:
            discord_id = item['discord_id']
            # print(discord_id)
            user = guild.get_member(discord_id)
            wl_role = discord.utils.get(guild.roles, name="Sticker Waitlist")
            role = discord.utils.get(guild.roles, name="Sticker Club")
            if discord_id is not None and discord_id.isdigit():
                user = guild.get_member(int(discord_id))
                if user is not None:
                    channel_id = 1098245554284281856
                    channel = guild.get_channel(channel_id)
                    await user.remove_roles(wl_role)
                    await user.add_roles(role)
                    mentions.append(user.mention)
                    welcome_message = f"Welcoming new Sticker Club member {user.mention}"
                    # await channel.send(welcome_message)
            else:
                print(f"Skipping invalid discord_id {discord_id}")

    response_welcome = r.get('https://portfolio.pythonanywhere.com/sticker_whitelist_welcome')
    if response_welcome.status_code == 200:
        json_data_welcome = response_welcome.json()
        for item in json_data_welcome:
            discord_id = item['discord_id']
            user = guild.get_member(discord_id)
            wl_role = discord.utils.get(guild.roles, name="Sticker Waitlist")
            role = discord.utils.get(guild.roles, name="Sticker Club")
            if discord_id is not None and discord_id.isdigit():
                user = guild.get_member(int(discord_id))
                if user is not None:
                    mentions.append(user.mention)
                    welcome_message = f"Welcoming new Sticker Club member {user.mention}"
                    await channel.send(welcome_message)
            else:
                print(f"Skipping invalid discord_id {discord_id}")


target_channel_id = 1083786228022915102
last_address = {}  # dictionary to store last entered wallet_address for each user


#Channel Specific Commands
def is_in_channel(ctx):
     return ctx.channel.id == 1083786228022915102

@bot.command()
@commands.check(is_in_channel)
async def abuse(ctx):
    response = r.get('https://portfolio.pythonanywhere.com/sticker_whitelist')
    if response.status_code == 200:
        json_data = response.json()
        discord_ids = [item['discord_id'] for item in json_data if item['discord_id'] is not None]
        ip_address = [item['ip_address'] for item in json_data if item['ip_address'] != ""]
        counts_ip = Counter(ip_address)
        repeat_ips = [ip_address for ip_address, count in counts_ip.items() if count >= 2]

        counts = Counter(discord_ids)
        repeat_ids = [discord_id for discord_id, count in counts.items() if count >= 2]
        if repeat_ids:
            print("The following discord_id(s) appear more than once:")
            await ctx.channel.send("The following users are abusing the whitelist:")
            for discord_id in repeat_ids:
                member = ctx.guild.get_member(int(discord_id))
                if member is not None:
                    username = member.display_name
                    # print(username)
                    await ctx.channel.send(username)

        if repeat_ips:
            await ctx.channel.send(repeat_ips)
        else:
            await ctx.channel.send("No one is currently abusing the drop list")


bot.run(discord_key)

