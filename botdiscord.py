import discord
import os
import random
from discord.ext import commands

TOKEN = 'ํOUR TOKEN HERE BUT CANT PASTE IT HERE FOR NOW'

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())

@bot.event
async def on_ready():
    print("I'm ONLINE But Discord")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello", description="Replies with Hello")
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello It's me BUT DISCORD")

@bot.tree.command(name="bot", description="SAID SOMETHING")
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Yes, the bot is cool. BUT DISCORD")

bot.run(TOKEN)