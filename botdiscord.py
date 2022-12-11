import discord
from discord.ext import commands
from discord import Embed
import youtube_dl
import datetime
from song import*

TOKEN = 'MTAzOTU2NzgzMzUxMzg1NzA4NQ.GGbOS0.5ZIYK1KSP3g8NEwBkdLyCqKX1-3wsqPBQ_9k1I'

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


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
    await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.') # แจ้งไปที่แชท สต.
    channel = bot.get_channel(721276405480030321) # ส่งที่ห้องไอดีนี้
    # await channel.send()
    embed = discord.Embed(title=f"👋 Hi {member}  \n🎊 Welcome To My Server!", description=f"Welcome {member.mention}! Enjoy your stay here.", color=0xFF0046)
    embed.add_field(name="หากสนใจเรื่องอะไร ❓", value="👉  ```พิมพ์ '...py' หรือ '/help```' ", inline=False)
    embed.set_image(url='https://media.tenor.com/LDuF2jVabwoAAAAC/banner-welcome.gif') # รูป welcome
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member): #แจ้งคนออกเซิฟ
    channel = bot.get_channel(721276405480030321) # ส่งที่ห้องไอดีนี้
    # await channel.send()
    embed = discord.Embed(title=f"👋 Bye Bye {member}  \n🎊 Bye", description=f"Bye {member.mention}! Enjoy your stay here.", color=0xFF0046)
    await channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after): #แจ้งคนเข้า- ออก วอย แชท
    channel = bot.get_channel(1039567269992341554)
    tmp1 = datetime.datetime.now()
    txtsend = tmp1.strftime(" %d %B %Y %H:%M:%S")
    if before.channel != after.channel:
        if after.channel is not None and after.channel.id == int(721276405480030322):
            embed = discord.Embed(title=f"👋 {member} Join \n  {txtsend}", color=0xFF0046)
            await channel.send(embed=embed)
    if before.channel != after.channel:
        if before.channel is not None and before.channel.id == int(721276405480030322):
            embed = discord.Embed(title=f"👋 {member} Leave \n  {txtsend}", color=0x99FF99)
            await channel.send(embed=embed)


@bot.tree.command(name="hello", description="Replies with Hello")
async def hellocommand(ctx):
    await ctx.response.send_message("Hello It's me BUT DISCORD")





# เรียกบอทเข้าห้องคุย ถ้าผู้ใช้ไม่ได้อยู่ในห้อง จะเล่นเพลงไม่ได้
@bot.command()
async def join(ctx):  # Join เออกจากห้องคุยเสียงของคนที่อยู่ใช้คำสั่ง
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Bot เข้าร่วมห้องเสียงแล้ว 😎")
        await ctx.send("--- พร้อมเปิดเพลงให้คุณแล้ว ---")
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

ydl_opts = {'format': 'bestaudio'}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
# แก้บอทเล่นเพลงไม่จบ

@bot.command(pass_context=True)
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
    embed = Embed(title="🎶Now playing🎶", color=0xFF0046)
    embed.add_field(name=f"Music: {title}", value="—————————————————————————————", inline=False)
    embed.add_field(name="🕘| Duration", value=f"```0{minute}:{second} ```", inline=True)
    embed.add_field(name="👀| Views", value=f"```ดู {view} ครั้ง```", inline=True)
    embed.add_field(name="📅| Date", value=f"```เมื่อ {date}```", inline=True)
    embed.set_thumbnail(url=thumb) # รูปเล็ก
    embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
    await ctx.channel.send(embed=embed)



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


@bot.event
async def on_message(message):
    mes_user = message.content # กำหนดเป็นตัวพิมเล็ก
    tmp1 = datetime.datetime.now()
    txtsend = tmp1.strftime(" %d %B %Y %H:%M:%S")
    if mes_user == "hello":
        await message.channel.send('สวัสดี')
    elif mes_user[0:] == "กี่โมง":
        await message.channel.send(txtsend)
    await bot.process_commands(message) # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ



# /////////////// คำสั่ง python //////////////////

# Python Lists
@bot.tree.command(name="lstpy", description="Bot commands")
async def lstcommand(ctx):
    embed = Embed(title="Python List []", description="เป็นข้อมูลแบบมีลำดับรวมข้อมูลได้หลายประเภท", color=0xFF0046)
    embed.add_field(name='mylist = ["coconut", 1, 1.26]', value="List เก็บข้อมูลเป็น index ไอเทมแรกเริ่มที่ 0 ", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่ ", value="👉https://www.w3schools.com/python/python_lists.asp", inline=False)
    embed.add_field(name='List Methods', value="List มี built-in ให้ใช้ ", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่ ", value="👉 https://www.w3schools.com/python/python_lists_methods.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="strmeth_py", description="Bot commands")
async def lstcommand(ctx):
    embed = Embed(title="Python String Methods", description="เป็นคำสั่ง built-in ที่สามารถนำมาใช้กับ String ได้", color=0xFF0046)
    embed.add_field(name='.capitalize()', value="จะเปลี่ยนแค่ตัวอักษรตัวแรกเป็นตัวใหญ่", inline=False)
    embed.add_field(name='.swapcase()', value="จะเปลี่ยนทุกตัวอักษรที่เป็นตัวใหญ่เป็นเล็ก และเล็กเป็นใหญ่ \nเช่น ABcd ---> abCD", inline=False)
    embed.add_field(name=".upper() ", value="จะเปลี่ยนทุกตัวเป็นตัวใหญ่ เช่น abcd ---> ABCD", inline=False)
    embed.add_field(name=".lower() ", value="จะเปลี่ยนทุกตัวอักษรเป็นตัวเล็ก เช่น ABCD ---> abcd", inline=False)
    embed.add_field(name=".casefold()", value="จะเปลี่ยนทุกตัวอักษรเป็นตัวเล็กเหมือนกับ .lower() \nแต่จะเปลี่ยนตัวอักษรประเภทอื่นด้วย", inline=False)
    embed.add_field(name=".split() ", value="คำสั่งนี้จะแยกตัวคั่นที่ระบุไว้ และส่งกลับเป็น List", inline=False)
    embed.add_field(name=".isnumeric() ", value="จะเช็คว่าทุกตัว input ที่ใส่ไปนั้นเป็นเลขทั้งหมดหรือไม่ \nเช่น ถ้าใช้จะ return True ถ้าไม่จะ return False", inline=False)
    embed.add_field(name="อยากรู้คำสั่ง String Methods เพิ่มเติมคลิกดูได้ที่นี่ ", value="👉 https://www.w3schools.com/python/python_ref_string.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)



#//////////////// เมนู Help ///////////////////

@bot.tree.command(name="helpmusic", description="Bot commands")
async def musiccommand(ctx):
    embed = Embed(title="Help me! - Help Music", color=0xff2450)
    embed.add_field(name="Bot commands", value="```/help```", inline=True)
    embed.add_field(name="Hello", value="```/hello```", inline=True)
    embed.add_field(name="Bot is cool.", value="```/bot```", inline=True)
    embed.add_field(name="play music", value="```/play```", inline=True)
    embed.add_field(name="stop music", value="```/stop```", inline=True)
    embed.add_field(name="pause music", value="```/pause```", inline=True)
    embed.add_field(name="Bot leave", value="```/leave```", inline=True)
    embed.add_field(name="Bot join", value="```/join```", inline=True)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png')
    await ctx.response.send_message(embed=embed)



@bot.tree.command(name="helppython", description="Bot commands")
async def pythoncommand(ctx):
    embed = Embed(title="Help me! - Help Python Function", color=0xff2450)
    embed.add_field(name="Bot commands", value="```/helppy```", inline=True)
    embed.add_field(name="Python Lists", value="```/listpy```", inline=True)
    embed.add_field(name="Python Dictionaries", value="```/dictpy```", inline=True)
    embed.add_field(name="Python Sets", value="```/setpy```", inline=True)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png')
    await ctx.response.send_message(embed=embed)

bot.run(TOKEN)
