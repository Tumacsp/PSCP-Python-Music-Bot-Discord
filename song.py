import discord
from discord.ext import commands
import youtube_dl
from discord import Embed



bot = commands.Bot(command_prefix="/", intents= discord.Intents.all())

# ////////////// เล่นเพลง //////////////////////

ydl_opts = {'format': 'bestaudio'}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
# แก้บอทเล่นเพลงไม่จบ
class Songapi:
    async def play(ctx, url):
        # ถ้าผู้ใช้ไม่ได้อยู่ในห้อง จะเล่นเพลงไม่ได้
        voice = ctx.voice_client # การเชื่อมต่อเสียงผู้ใช้
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=False) # ไม่ได้ download
            url = file['formats'][0]['url'] #ลิ้งเพลง
        voice.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
        voice.is_playing() # เล่นเพลง
            
        thumb = file['thumbnail'] # รูปเพลง
        title = file['title'] #ชื่อเพลง
        view = file['view_count'] # ยอดวิว
        date = file['upload_date'] # วันเวลา
        time = file['duration'] #เวลาเพลง
        # คำนวณเวลาเพลง
        minute= int(time/60)
        second = int(time%60)

        # Embed เล่นเพลง
        embed = Embed(title="🎶Now Playing🎶", color=0xFF0046)
        embed.add_field(name=f"Music: {title}", value="—————————————————————————————", inline=False)
        embed.add_field(name="🕘| Duration", value=f"```0{minute}:{second} ```", inline=True)
        embed.add_field(name="👀| Views", value=f"```ดู {view} ครั้ง```", inline=True)
        embed.add_field(name="📅| Date", value=f"```เมื่อ {date}```", inline=True)
        embed.set_thumbnail(url=thumb) # รูปเล็ก
        embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
        await ctx.channel.send(embed=embed)



    # หยุดเพลง
    async def pause(ctx):  # หยุดเพลงไว้ก่อนเดี๋ยวฟังต่อนะ
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            # Embed หยุดเพลง
            embed = Embed(title="🎶Now Pause🎶", color=0xFF0046)
            embed.add_field(name='⏸️| Pause', value='type /resume to resume')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1039567269992341554/1051727418353778748/pause.png')
            embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send("ขณะนี้ไม่มีเพลงเล่นในห้องเสียง!❗")

    # เล่นต่อหลังหยุดเพลง
    async def resume(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            #embed เล่นต่อ
            embed = Embed(title="🎶Now Resume🎶", color=0xFF0046)
            embed.add_field(name='▶️| Resume', value='type /pause to pause')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1039567269992341554/1051727415153541180/play.png')
            embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send("ขณะนี้ไม่มีเพลงที่กำลังหยุดชั่วคราว❗")

    # ปิดเพลงเลย แบบปิดไม่ฟังต่อแล้ว
    async def stop(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        #embed เล่นต่อ
        embed = Embed(title="🎶Now Stop🎶", color=0xFF0046)
        embed.add_field(name='⏹️| Stop', value='type /play to play')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1039567269992341554/1051727414604070952/stop.png')
        embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
        await ctx.channel.send(embed=embed)
