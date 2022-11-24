import discord
from discord.ext import commands
from discord import Embed
import youtube_dl

TOKEN = 'Token'

bot = commands.Bot(command_prefix="/", intents= discord.Intents.all())

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

@bot.command()
async def join(ctx): # Join เออกจากห้องคุยเสียงของคนที่อยู่ใช้คำสั่ง
  if ctx.author.voice:
    channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("Bot เข้าร่วมแล้ว👍")
  else:
    await ctx.send("คุณไม่ได้อยู่ในห้องเสียง❌❌") # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง

@bot.command()
async def leave(ctx): # Leave ออกจากห้องคุยเสียง
  if ctx.voice_client:
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Bot ได้ออกจากห้องแล้ว👋")
  else:
    await ctx.send("Bot ไม่ได้อยู่ในห้องเสียง❌") # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง

bot.run(TOKEN)