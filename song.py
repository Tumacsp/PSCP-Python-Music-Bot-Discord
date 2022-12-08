import discord
from discord.ext import commands
import youtube_dl

bot = commands.Bot(command_prefix="/", intents= discord.Intents.all())

# คำสั่งเปิดเพลง

ydl_opts = {'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',}],}  

@bot.command(pass_context=True)
async def play(ctx, url):
    if not ctx.message.author.voice: # ถ้าผู้ใช้ไม่ได้อยู่ในห้อง เล่นเพลงไม่ได้
        await ctx.send('คุณไม่ได้อยู่ในห้อง❌')
        return
    else:
        voice = ctx.voice_client

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=False) # ไม่ได้ download
        url1 = file['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(url1))
    voice.is_playing()

    voice.source = discord.PCMVolumeTransformer(voice.source, 1)

    await ctx.send('')
    await ctx.send(f'**Music: **{url}')

#หยุดเพลง
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused ⏸")
    else:
        await ctx.send("ขณะนี้ไม่มีเพลงเล่นในห้องเสียง!❗")

@bot.command()
async def resume(ctx): #เล่นต่อ
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resume ⏯")
    else:
        await ctx.send("ขณะนี้ไม่มีเพลงที่กำลังหยุดชั่วคราว❗")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.send("Stop ⛔")