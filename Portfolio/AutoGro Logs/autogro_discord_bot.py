import time
import MySQLdb
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import date, datetime, timedelta, timezone
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
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests
import tweepy
from PIL import Image
import os
import ssl
from io import BytesIO
from PIL import Image
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter
import re
import glob
import matplotlib.ticker as ticker



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


data_array = []


#DB Shit
db_query = "select accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left from autogro_calibration_logs"

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

db_records = run_query(db_query)
for (accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left) in db_records:
    print(f"Saturation: {saturation_data} | Dry Data: {dry_time} | Dry Target: {dry_target} | Moisture Status: {moisture_status} | Dry delta data left: {dry_time_left}")
    data_array.append(rotations)
# print('Email Array', email_array)


# bot = commands.Bot(command_prefix="", case_insensitive=False, help_command=None)
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)


# Bot introduction
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    print('We have logged in as {0.user}'.format(bot))
    await bot.wait_until_ready()
    bot_feed = bot.get_channel(1090495308741484614)
def is_in_channel(ctx):
     return ctx.channel.id == 1090495308741484614


@bot.command()
@commands.check(is_in_channel)
async def chart(ctx):
    channel = bot.get_channel(1090495308741484614)
    api_url = ""
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        recent_data = data[:5]  # This reverses the list and takes the first 10 items
        recent_data.reverse()  # This reverses the order so the most recent is last

        for item in recent_data:
            soil_1_wet = item.get('soil_1_wet', 'N/A')
            soil_2_wet = item.get('soil_2_wet', 'N/A')
            soil_3_wet = item.get('soil_3_wet', 'N/A')
            soil_4_wet = item.get('soil_4_wet', 'N/A')
            soil_5_wet = item.get('soil_5_wet', 'N/A')
            tds = item.get('tds', 'N/A')
            ph = item.get('ph', 'N/A')
            accessed = item.get('accessed_str', 'N/A')

    time_format = "%Y-%m-%dT%H:%M:%SZ"


    time1 = "Time:", accessed
    print(time1)
    soil_1_data = [float(item["soil_1_wet"]) for item in data if item.get("soil_1_wet") is not None]
    soil_2_data = [float(item["soil_2_wet"]) for item in data if item.get("soil_2_wet") is not None]
    tds = [float(item["tds"]) for item in data if item.get("tds") is not None]
    ph = [float(item["ph"]) for item in data if item.get("ph") is not None]
    print('Soil 2 Data: ', soil_2_data)

    # Code block to save the image so we can upload to twitter
    # Convert a Matplotlib figure to a PIL Image and return it
    def fig2img(fig):
        buf = BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        # img.show()

        return {"buffer": buf, "img": img}
    plt.style.use('dark_background')

    # Graph Config
    fig = plt.figure()

    # Convert the accessed datetime string to a datetime object
    accessed_datetime = datetime.strptime(accessed, "%Y-%m-%d %H:%M:%S")

    # Create a list of datetime objects for the x-axis
    timestamps = [accessed_datetime - timedelta(seconds=i) for i in range(len(soil_1_data))]

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(timestamps, soil_1_data, label='Soil 1')
    ax.plot(timestamps, soil_2_data, label='Soil 2')
    ax.plot(timestamps, tds, label='TDS')
    ax.plot(timestamps, ph, label='PH')

    # Customize the plot
    ax.set_xlabel('Time')
    ax.set_ylabel('Sensor Data')
    ax.set_title('AutoGro Logs')
    ax.legend()

    # Save the figure as an image
    fig.savefig('soil_moisture.png')

    # Display the image
    plt.imshow(plt.imread('soil_moisture.png'))

    plt.axis('off')
    plt.show()
    with open('soil_moisture.png', 'rb') as file:
        image = discord.File(file)

    # Send the image to the channel
    await channel.send(file=image)
    # await ctx.channel.send("Sam the Man")

# test_email = "sam@yahoo.com"
# @bot.command()
# @commands.check(is_in_channel)
# async def test_email(ctx):
#     await ctx.channel.send("Sam the Man")



# # @bot.application_command(name="verify", description="Verify email address", hidden=True)
# @bot.command(hidden=True)
# async def verify(ctx, email):
#     # Define the regular expression pattern to match the email
#     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#     # Check if the given argument matches the email pattern
#     if re.match(email_pattern, email):
#         # Check if the given email is "christian.goff@xprize.org"
#         matched = False
#         for e in email_array:
#             if email.strip().lower() == e.strip().lower():
#                 matched = True
#                 # await ctx.author.send("Valid email address!")
#                 # await interaction.response.send_message(f"Valid email address and matches the DB records!", ephemeral=True)
#                 role = discord.utils.get(ctx.guild.roles, name="Team")

#                 # Add the role to the user
#                 await ctx.author.add_roles(role)

#                 # Send a message confirming that the role has been added
#                 await ctx.author.send(f"Hey {ctx.author.name}, you have been issued the '{role.name}' role. You can now access the team channels!!")
#                 return
#                 break

#         # Check if a match was not found in the email_array
#         if not matched:
#             await ctx.author.send("Valid email address, but does not match the DB records.")
#     else:
#         await ctx.author.send("Invalid email address.")

#interaction.response.send_message
@bot.command()
@commands.check(is_in_channel)
async def data(ctx):
    db_query = "SELECT accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left FROM autogro_calibration_logs"

    def run_queryCommand(statement, args=None):
        cursor = zohoDB.cursor()
        cursor.execute(statement, args)

        if "SELECT" in statement.upper():
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            zohoDB.commit()
            cursor.close()

    db_records = run_queryCommand(db_query)
    for (accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left) in db_records:
        await ctx.channel.send(f"```Saturation: {saturation_data} | Dry Data: {dry_time} | Dry Target: {dry_target} | Moisture Status: {moisture_status} | Dry delta data left: {dry_time_left}```")


@bot.command()
@commands.check(is_in_channel)
async def recent(ctx):
    api_url = ""
    response = r.get(api_url)

    if response.status_code == 200:
        data = response.json()
        recent_data = data[:5]  # This reverses the list and takes the first 10 items
        recent_data.reverse()  # This reverses the order so the most recent is last

        for item in recent_data:
            soil_1_wet = item.get('soil_1_wet', 'N/A')
            soil_2_wet = item.get('soil_2_wet', 'N/A')
            soil_3_wet = item.get('soil_3_wet', 'N/A')
            soil_4_wet = item.get('soil_4_wet', 'N/A')
            soil_5_wet = item.get('soil_5_wet', 'N/A')
            tds = item.get('tds', 'N/A')
            ph = item.get('ph', 'N/A')
            accessed = item.get('accessed_str', 'N/A')
            await ctx.channel.send(f"```S1: {soil_1_wet} | S2: {soil_2_wet} | S3: {soil_3_wet} | S4: {soil_4_wet} | S5: {soil_5_wet}\nPH: {ph}\nTDS: {tds}\nTimestamp: {accessed}```")
    else:
        await ctx.channel.send("Failed to retrieve data from the API.")

# dailyreport.start()
bot.run(discord_key)

