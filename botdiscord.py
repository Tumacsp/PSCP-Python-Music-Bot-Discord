import discord
from discord.ext import commands
from discord import Embed
import youtube_dl
from song import*


# token bot
TOKEN = ''

# กำหนดเครื่องหมายในการพิมพ์คำสั่งเรียก  bot 
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


# คำสั่งที่บอกว่า bot พร้อมใช้งานแล้ว
@bot.event
async def on_ready(): # ถ้า bot พร้อมเมื่อไหร่จะทำฟังก์ชันนี้ ครั้งเดียวเท่านั้น
    print("The bot is now ready for use!")
    print("------------------------------")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)") # แสดงคำสั่งทั้งหมดของ bot ตัวนี้
    except Exception as e:
        print(e)


# แจ้งเตือนที่แชทส่วนตัว เมื่อเข้าเซิฟเวอร์

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.')


@bot.tree.command(name="hello", description="Replies with Hello")
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message("Hello It's me BUT DISCORD")

# เรียกบอทเข้าห้องคุย
@bot.command()
async def join(ctx):  # Join เออกจากห้องคุยเสียงของคนที่อยู่ใช้คำสั่ง
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Bot เข้าร่วมแล้ว�")
    else:
        # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง555
        await ctx.send("คุณไม่ได้อยู่ในห้องเสียง❌")

# เรียกบอทออกห้องคุย
@bot.command()
async def leave(ctx):  # Leave ออกจากห้องคุยเสียง
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Bot ได้ออกจากห้องแล้ว👋")
    else:
        # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง
        await ctx.send("Bot ไม่ได้อยู่ในห้องเสียง❌")

# ////////////// เล่นเพลง //////////////////////


ydl_opts = {'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192', }], }

@bot.command(pass_context=True)
async def play(ctx, url):
    if (ctx.author.voice): # ถ้าผู้ใช้ไม่ได้อยู่ในห้อง จะเล่นเพลงไม่ได้
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Bot เข้าร่วมห้องเสียงแล้ว 😎")
        await ctx.send("--- พร้อมเปิดเพลงให้คุณแล้ว ---")
    else:
        await ctx.send("คุณไม่ได้อยู่ในห้องเสียง❗")

    voice = ctx.voice_client # การเชื่อมต่อเสียงผู้ใช้
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=False)  # ไม่ได้ download
        
    url = file['formats'][0]['url'] #ลิ้งเพลง
    thumb = file['thumbnails'][0]['url'] # รูปเพลง
    title = file['title'] #ชื่อเพลง

    voice.play(discord.FFmpegPCMAudio(url))
    voice.is_playing()

    voice.source = discord.PCMVolumeTransformer(voice.source, 1)

    await ctx.send(f'**Music: **{title}') # ชื่อเพลง
    await ctx.send(thumb) # รูปเพลง



# หยุดเพลง
@bot.command()
async def pause(ctx):  # หยุดเพลงไว้ก่อนเดี๋ยวฟังต่อนะ
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused ⏸")
    else:
        await ctx.send("ขณะนี้ไม่มีเพลงเล่นในห้องเสียง!❗")

# เล่นต่อหลังหยุดเพลง
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resume ⏯")
    else:
        await ctx.send("ขณะนี้ไม่มีเพลงที่กำลังหยุดชั่วคราว❗")

# ปิดเพลงเลย แบบปิดไม่ฟังต่อแล้ว
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Stop ⛔")


#//////////////// แมนู Help ///////////////////

@bot.tree.command(name="help", description="Bot commands")
async def hellocommand(ctx):
    embed = Embed(title="Help me!", color=0xff2450)
    embed.add_field(name="/help", value="Bot commands", inline=False)
    embed.add_field(name="/hello", value="Hello It's me", inline=False)
    embed.add_field(name="/bot", value="Yes, the bot is cool.", inline=False)
    embed.add_field(name="/play", value="play music", inline=False)
    embed.add_field(name="/stop", value="stop music", inline=False)
    embed.add_field(name="/pause", value="pause music", inline=False)
    embed.add_field(name="/leave", value="Bot leave", inline=False)
    embed.add_field(name="/join", value="Bot join", inline=False)
    await ctx.response.send_message(embed=embed)


bot.run(TOKEN)
