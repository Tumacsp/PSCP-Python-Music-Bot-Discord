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

# แจ้งเตือนที่แชทส่วนตัว เมื่อเข้าเซิฟเวอร์
@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.') 


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
    await ctx.send("คุณไม่ได้อยู่ในห้องเสียง❌") # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง555

@bot.command()
async def leave(ctx): # Leave ออกจากห้องคุยเสียง
  if ctx.voice_client:
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Bot ได้ออกจากห้องแล้ว👋")
  else:
    await ctx.send("Bot ไม่ได้อยู่ในห้องเสียง❌") # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง




# คำสั่งเปิดเพลง

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   
                            
@bot.command(pass_context=True)
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('you are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    voice_client = await channel.connect()

    guild = ctx.message.guild

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    await ctx.send(f'**Music: **{url}')

    while voice_client.is_playing():
        await asyncio.sleep(1)


bot.run(TOKEN)