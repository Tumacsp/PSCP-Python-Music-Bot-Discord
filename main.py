import discord
from discord.ext import commands
from discord import Embed
import youtube_dl
import datetime
import random
import requests

# token bot
TOKEN = ''


# กำหนดเครื่องหมายในการพิมพ์คำสั่งเรียก  bot
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

txtquiz = []
txtquizhint = []
txtcheck = []

# คำสั่งที่บอกว่า bot พร้อมใช้งานแล้ว
@bot.event
async def on_ready():
    print("I'm ONLINE But Discord")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")



# แจ้งเตือนที่แชทส่วนตัว เมื่อเข้าเซิฟเวอร์
@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.') # แจ้งไปที่แชท สต.
    channel = bot.get_channel(721276405480030321) # ส่งที่ห้องไอดีนี้
    embed = discord.Embed(title=f"👋 Hi {member}  \n🎊 Welcome To My Server!", description=f"Welcome {member.mention}! Enjoy your stay here.", color=0xFF0046)
    embed.add_field(name="หากสนใจเรื่องอะไร ❓", value="พิมพ์ตามนี้เลย👇", inline=False)
    embed.add_field(name="Help Music", value="```/helpmusic```", inline=True)
    embed.add_field(name="Help Python", value="```/helppython```", inline=True)
    embed.add_field(name="Help News", value="```/newstech```", inline=True)
    embed.set_image(url='https://media.tenor.com/LDuF2jVabwoAAAAC/banner-welcome.gif') # รูป welcome
    await channel.send(embed=embed)


#แจ้งคนออกเซิฟ
@bot.event
async def on_member_remove(member): 
    channel = bot.get_channel(721276405480030321) # ส่งที่ห้องไอดีนี้
    embed = discord.Embed(title=f"👋 Bye Bye {member}", description="Thank you for joining in the fun on our server.😭", color=0xFF0046)
    embed.set_image(url='https://j.gifs.com/98OvjJ.gif')
    await channel.send(embed=embed)



#แจ้งคนเข้า- ออก วอย แชท
@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(1039567376162750475)
    tmp1 = datetime.datetime.now()
    txtsend = tmp1.strftime(" %d %B %Y %H:%M:%S")
    if before.channel != after.channel:
        if after.channel is not None and after.channel.id == int(721276405480030322):
            embed = discord.Embed(title=f"👋 {member.name} Join \n  {txtsend}", color=0x99FF99)
            await channel.send(embed=embed)
    if before.channel != after.channel:
        if before.channel is not None and before.channel.id == int(721276405480030322):
            embed = discord.Embed(title=f"👋 {member.name} Leave \n  {txtsend}", color=0xFF0046)
            await channel.send(embed=embed)

#เกมท้ายคำ
@bot.tree.command(name="game", description="เกมทายคำ")
async def gamecommand(ctx, txt:str):
    txt = txt.lower()
    txtcheck.append(txt)
    for i in txt:
        txtquiz.append(i)
        txtquizhint.append(i)
    for i in range(len(txtquiz)//2):
        ran = random.randint(0, len(txtquiz)-1)
        txtquizhint.pop(ran)
        txtquizhint.insert(ran, '#')
    print(txtcheck)
    embed = discord.Embed(title=f"GAME", description=f"ท้ายคำใน List.", color=0xFF0046)
    embed.add_field(name="HINT", value=txtquizhint, inline=False)
    embed.add_field(name="เล่นได้ที่ละครั้ง เกมจะรีเซ็ตเมื่อตอบถูกนะ", value="ถ้ามยอมไม่ไหวให้ใช้ /reset นะครับ", inline=True)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="reset", description="reset") #รีเซ็ตเกม
async def resetgame(ctx):
    txtquiz.clear()
    txtquizhint.clear()
    txtcheck.clear()
    print(txtquiz)
    await ctx.response.send_message("gamereset")

def check(mes_user:str): #คืนค่าคำตอบเกม
    tempthai = "อยู่ตำแหน่งที่"
    temp = ""
    if mes_user in txtquiz and txtquiz.count(mes_user) == 1:
        return "%s %s %s"%(mes_user, tempthai, txtquiz.index(mes_user))
    if txtquiz.count(mes_user) > 1 and mes_user in txtquiz:
        for i in range(0,len(txtquiz)):
            if txtquiz[i] == mes_user:
                temp += "%s "%str(i)
        return "%s %s %s"%(mes_user, tempthai, temp)


# คำสั่ง chatbot เมื่อพิมพ์อะไรบางอย่างแล้ว bot จะตอบกลับมา
@bot.event
async def on_message(message):
    mes_user = message.content # กำหนดเป็นตัวพิมเล็ก
    tmp1 = datetime.datetime.now()
    txtsend = tmp1.strftime(" %d %B %Y %H:%M:%S")
    if mes_user == "hello":
        await message.channel.send('สวัสดี')
    elif 'กี่โมง' in mes_user:
        await message.channel.send(txtsend)
    elif mes_user == 'hi bot':
        await message.channel.send('Hello, ' + str(message.author.name)) # เรียกชื่อผู้ใช้ + hello
    elif mes_user in txtquiz: #เช็คค่าถ้าพิมถูก
        test = check(mes_user)
        embed = discord.Embed(title=f"Yes", description="", color=0xCCFF00)
        embed.add_field(name="อยู่ตำแหน่งที่", value=test, inline=False)
        await message.channel.send(embed=embed)
    elif mes_user in txtcheck:#ถ้าตอบถูก
        embed = discord.Embed(title=f"GAME WIN", description=f"!!!======!!!", color=0x99FF99)
        embed.add_field(name="คำนั้นคือ", value=txtcheck[0], inline=False)
        await message.channel.send(embed=embed)
        txtquiz.clear()
        txtquizhint.clear()
        txtcheck.clear()
    await bot.process_commands(message) # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ


@bot.tree.command(name="hello", description="Replies with Hello")
async def hellocommand(ctx):
    await ctx.response.send_message("Hello It's me BUT DISCORD")



# เรียกบอทเข้าห้องคุย ถ้าผู้ใช้ไม่ได้อยู่ในห้อง จะเล่นเพลงไม่ได้
@bot.command()
async def join(ctx):  # Join เออกจากห้องคุยเสียงของคนที่อยู่ใช้คำสั่ง
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("--- พร้อมเปิดเพลงให้คุณแล้ว ---")
    else:
        # กรณีคนใช้คำสั่งไม่อยู่ในห้องเสียง
        await ctx.send("คุณไม่ได้อยู่ในห้องเสียง❌")

# เรียกบอทออกห้องคุย
@bot.command()
async def leave(ctx):  # Leave ออกจากห้องคุยเสียง
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
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
    embed = Embed(title="🎶Now Playing🎶", color=0xFF0046)
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
        # Embed หยุดเพลง
        embed = Embed(title="🎶Now Pause🎶", color=0xFF0046)
        embed.add_field(name='⏸️| Pause', value='type /resume to resume')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1039567269992341554/1051727418353778748/pause.png')
        embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
        await ctx.channel.send(embed=embed)
    else:
        await ctx.send("ขณะนี้ไม่มีเพลงเล่นในห้องเสียง!❗")

# เล่นต่อหลังหยุดเพลง
@bot.command()
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
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    #embed เล่นต่อ
    embed = Embed(title="🎶Now Stop🎶", color=0xFF0046)
    embed.add_field(name='⏹️| Stop', value='type /play to play')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1039567269992341554/1051727414604070952/stop.png')
    embed.set_footer(text='Bot Music Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
    await ctx.channel.send(embed=embed)





# /////////////// คำสั่ง python //////////////////


# เรียกหนังสือ Think Python
@bot.tree.command(name="bookpy", description="หนังสือ Think Python") 
async def bookcommand(ctx):
    embed = Embed(title="แนะนำหนังสือ Python 🐍", description="แนะนำการเขียนโปรแกรม Python สำหรับผู้เริ่มต้น", color=0xFF0046)
    embed.add_field(name="Think Python", value="How to Think Like a Computer Scientist", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่", value="👉  https://greenteapress.com/thinkpython2/thinkpython2.pdf", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    embed.set_image(url='https://i.imgur.com/qYPNY8d.png')
    await ctx.response.send_message(embed=embed)
    # embed คือป้าย ทำให้การเรียกใช้งานดูสวย ดูดีมากขึ้น
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# ขั้นตอนการเขียนโปรแกรม Python
@bot.tree.command(name="startpy", description="ขั้นตอนการเขียนโปรแกรม Python") 
async def startcommand(ctx):
    await ctx.channel.send('คุณจะเริ่มเขียน Python ยังไงหน่ะหรอ? ลองดูนี่สิ!! 👇')
    embed = Embed(title="Python Getting Started", description="ขั้นตอนการเขียนโปรแกรม Python", color=0xFF0046)
    embed.add_field(name="Python Install", value="👉  https://www.python.org/downloads/", inline=False)
    embed.add_field(name="Let's write our first Python", value="ค้นหา python idle และพิมพ์คำสั่งแรก \n - print('Hello, World!')", inline=False)
    embed.add_field(name="ศึกษาเพิ่มเติมที่นี่!!", value="👉 https://www.w3schools.com/python/default.asp", inline=False)
    embed.set_thumbnail(url='https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png')
    embed.set_image(url='https://files.realpython.com/media/hello_idle.294af1398cd8.png')
    await ctx.channel.send(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# StackOverFlow
@bot.tree.command(name="stack_of", description="เว็บไซต์ StackOverFlow") 
async def lstcommand(ctx):
    embed = Embed(title="StackOverFlow", description="เว็บไซต์ Stack OverFlow เหมาะสำหรับนักเขียนโปรแกรมทุกคน", color=0xFF0046)
    embed.add_field(name='Stack OverFlow คือเว็บอะไร', value="เว็บ ถาม - ตอบ เกี่ยวกับปัญหาการเขียนโปรแกรมทุกภาษา ที่ใหญ่ที่สุดในโลก", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่👇", value="https://stackoverflow.com/", inline=False)
    embed.set_thumbnail(url='https://i1.sndcdn.com/avatars-000708374642-k6d7gm-t500x500.jpg')
    embed.set_image(url='https://techcrunch.com/wp-content/uploads/2021/03/stack-overflow-for-teams.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# Python Lists
@bot.tree.command(name="lstpy", description="Bot commands")
async def lstcommand(ctx):
    embed = Embed(title="Python List []", description="เป็นข้อมูลแบบมีลำดับรวมข้อมูลได้หลายประเภท", color=0xFF0046)
    embed.add_field(name='mylist = ["coconut", 1, 1.26]', value="List เก็บข้อมูลเป็น index ไอเทมแรกเริ่มที่ 0 ", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่ ", value="👉https://www.w3schools.com/python/python_lists.asp", inline=False)
    embed.add_field(name='List Methods', value="List มี built-in ให้ใช้ ", inline=False)
    embed.add_field(name='.append()', value="เพิ่มข้อมูลไปยังตำแหน่งสุดท้ายของ list ", inline=False)
    embed.add_field(name='.count()', value="คืนค่าจำนวนที่ระบุไว้", inline=False)
    embed.add_field(name='.pop()', value="ลบข้อมูลตามตำแหน่งที่ระบุไว้ ", inline=False)
    embed.add_field(name='.remove()', value="ลบข้อมูลตามสิ่งที่ระบุไว้ ", inline=False)
    embed.add_field(name='.sort()', value="จัดเรียงข้อมูลใน list ", inline=False)
    embed.add_field(name="คลิกดูได้ที่นี่เพิ่มเติมที่ ", value="👉 https://www.w3schools.com/python/python_lists_methods.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# Python String Methods
@bot.tree.command(name="strmeth_py", description="Bot commands")
async def lstcommand(ctx):
    embed = Embed(title="Python String Methods", description="เป็นคำสั่ง built-in ที่สามารถนำมาใช้กับ String ได้", color=0xFF0046)
    embed.add_field(name='.capitalize()', value="จะเปลี่ยนแค่ตัวอักษรตัวแรกเป็นตัวใหญ่", inline=False)
    embed.add_field(name='.swapcase()', value="จะเปลี่ยนทุกตัวอักษรที่เป็นตัวใหญ่เป็นเล็ก และเล็กเป็นใหญ่ \nเช่น ABcd ---> abCD", inline=False)
    embed.add_field(name=".upper() ", value="จะเปลี่ยนทุกตัวเป็นตัวใหญ่ เช่น abcd ---> ABCD", inline=False)
    embed.add_field(name=".lower() ", value="จะเปลี่ยนทุกตัวอักษรเป็นตัวเล็ก เช่น ABCD ---> abcd", inline=False)
    embed.add_field(name=".casefold()", value="จะเปลี่ยนทุกตัวอักษรเป็นตัวเล็กเหมือนกับ .lower() \nแต่จะเปลี่ยนตัวอักษรประเภทอื่นด้วย", inline=False)
    embed.add_field(name=".split() ", value="คำสั่งนี้จะแยกตัวคั่นที่ระบุไว้ และ return ค่าเป็น List", inline=False)
    embed.add_field(name=".isnumeric() ", value="จะเช็คว่าทุกตัว input ที่ใส่ไปนั้นเป็นเลขทั้งหมดหรือไม่ \nเช่น ถ้าใช้จะ return True ถ้าไม่จะ return False", inline=False)
    embed.add_field(name="อยากรู้คำสั่ง String Methods เพิ่มเติมคลิกดูได้ที่นี่ ", value="👉 https://www.w3schools.com/python/python_ref_string.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# Python Set Methods
@bot.tree.command(name="setmeth_py", description="Bot commands")
async def lstcommand(ctx):
    embed = Embed(title="Python Set Methods", description="เป็นคำสั่ง built-in ที่สามารถนำมาใช้กับ Set เท่านั้น", color=0xFF0046)
    embed.add_field(name='.add()', value="เพิ่มค่าเข้าไปในตัว Set ที่เราจะใช้", inline=False)
    embed.add_field(name='intersection()', value="จะดึงค่าที่เหมือนกันออกมา", inline=False)
    embed.add_field(name=".union() ", value="จะดึงค่าที่ต่างกันออกมา", inline=False)
    embed.add_field(name=".update() ", value="จะเพิ่มตัว Set ที่เลือกเข้าไปใน Set ที่เรากำหนดไว้", inline=False)
    embed.add_field(name="อยากรู้คำสั่ง Set Methods เพิ่มเติมคลิกดูได้ที่นี่ 👇", value="https://www.w3schools.com/python/python_sets_methods.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# Python Math Methods
@bot.tree.command(name="math_py", description="Bot commands")
async def mathcommand(ctx):
    embed = Embed(title="Math", description="เป็น built-in เกี่ยวกับคณิตศาสตร์", color=0xFF0046)
    embed.add_field(name='min()', value="คืนค่าค่าต่ำสุดในข้อมูลนั้น \n min(6, 4, 7) ---> 4", inline=False)
    embed.add_field(name='max()', value="คืนค่าค่ามากสุดในข้อมูลนั้น \n min(6, 4, 7) ---> 7", inline=False)
    embed.add_field(name="abs() ", value="คืนค่าข้อมูลเป็นจำนวนเต็มบวก \n abs(-5.5) ---> 5.5", inline=False)
    embed.add_field(name="pow(x, y) ", value="คืนค่า x ยกกำลัง y \n pow(2, 3) ---> 8\n------------------------------", inline=False)
    embed.add_field(name="Math module", value="เป็นโมดูลที่ต้อง import math เข้ามา", inline=False)
    embed.add_field(name="math.ceil() ", value="คืนค่าโดยการปัดเลขขึ้น \n math.celi(5.6) ---> 6", inline=False)
    embed.add_field(name="math.floor() ", value="คืนค่าโดยการปัดเลขลง \n math.celi(5.6) ---> 5", inline=False)
    embed.add_field(name=" math.sqrt() ", value="คืนค่ารากที่สอง \n math.sqrt(64) ---> 8.00", inline=False)
    embed.add_field(name="อยากรู้คำสั่ง Math เพิ่มเติมคลิกดูได้ที่นี่ ", value="👉 https://www.w3schools.com/python/python_math.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')


# Python Dictionary
@bot.tree.command(name="dictpy", description="Bot commands")
async def mathcommand(ctx):
    embed = Embed(title="Dictionaries", description="ประเภทข้อมูลที่เก็บข้อมูลในรูปแบบคู่ของ Key และ Value", color=0xFF0046)
    embed.add_field(name='.clear()', value="ลบองค์ประกอบทั้งหมดออกจาก dict ", inline=False)
    embed.add_field(name='.items()', value="ส่งกลับคู่key-value ของdict เป็น tuples", inline=False)
    embed.add_field(name='.keys()', value="ส่งกลับ key ของdict", inline=False)
    embed.add_field(name='.pop()', value="ลบข้อมูลตามตำแหน่งที่ระบุไว้", inline=False)
    embed.add_field(name='.update()', value="อัปเดต dict ด้วยคู่key-value ที่ระบุไว้", inline=False)
    embed.add_field(name='.values()', value="ส่งกลับ values ของdict", inline=False)
    embed.add_field(name="อยากรู้คำสั่ง Dictionary Methods เพิ่มเติมคลิกดูได้ที่นี่ ", value="👉 https://www.w3schools.com/python/python_dictionaries_methods.asp", inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/Yn64sH9.png')
    await ctx.response.send_message(embed=embed)
    await ctx.channel.send('❓สนใจเรื่องอะไรอีก พิมพ์ /helppython')



#//////////////// เมนู Help ///////////////////

@bot.tree.command(name="helpmusic", description="Bot commands")
async def musiccommand(ctx):
    embed = Embed(title="Help me! - Help Music", color=0xff2450)
    embed.add_field(name="play music", value="```/play```", inline=True)
    embed.add_field(name="stop music", value="```/stop```", inline=True)
    embed.add_field(name="pause music", value="```/pause```", inline=True)
    embed.add_field(name="resume music", value="```/resume```", inline=True)
    embed.add_field(name="Bot leave", value="```/leave```", inline=True)
    embed.add_field(name="Bot join", value="```/join```", inline=True)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png')
    await ctx.response.send_message(embed=embed)


@bot.tree.command(name="helppython", description="Bot commands")
async def pythoncommand(ctx):
    embed = Embed(title="Help me! - Help Python Function", color=0xff2450)
    embed.add_field(name="Think Python book", value="```/bookpy```", inline=True)
    embed.add_field(name="Start Python", value="```/startpy```", inline=True)
    embed.add_field(name="StackOverFlow web", value="```/stack_of```", inline=True)
    embed.add_field(name="Python Lists commands", value="```/lstpy```", inline=True)
    embed.add_field(name="Python Strings commands", value="```/strmeth_py```", inline=True)
    embed.add_field(name="Python Set commands", value="```/setmeth_py```", inline=True)
    embed.add_field(name="Python Math commands", value="```/math_py```", inline=True)
    embed.add_field(name="Python Dict commands", value="```/dictpy```", inline=True)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png')
    await ctx.response.send_message(embed=embed)


#//////////////// ข่าว Technology ///////////////////

@bot.tree.command(name="newstech", description="Technology News")
async def newscommand(ctx):
    # ข่าวรายวัน
    url = "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=2557d02b638e4052abb76a63b4c02843"

    response = requests.get(url) #ดึงข้อมูลจาก API
    news = response.json()  # อ่านไฟล์ JSON

    for i in range(3,6):
        title = news['articles'][i]['title'] #หัวข่าว
        des = news['articles'][i]['description'] #รายละเอียด
        url2 = news['articles'][i]['url'] # ลิ้งข่าว
        img1 = news['articles'][i]['urlToImage'] # รูปประกอบข่าว
        time2 = news['articles'][i]['publishedAt'] # เวลา
        embed = Embed(title="ข่าวรายวัน", color=0xFF0046)
        embed.add_field(name="Technology News", value="—————————————————————————————", inline=False)
        embed.add_field(name="| Title", value=f"```{title}```", inline=False)
        embed.add_field(name="| Description", value=f"```{des}```", inline=False)
        embed.add_field(name="| Date", value=f"```เมื่อ {time2}```", inline=False)
        embed.add_field(name="| Read More", value=url2, inline=False)
        embed.set_image(url=img1)
        embed.set_footer(text='Bot News Mode',icon_url='https://media.discordapp.net/attachments/1039567269992341554/1051132242577084516/1.1.png') # footer
        await ctx.channel.send(embed=embed)


bot.run(TOKEN)
