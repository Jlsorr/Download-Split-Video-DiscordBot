import discord
import os
import subprocess
import asyncio

# Remplacez TOKEN par votre token de bot Discord
TOKEN = "TOKEN"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Fonction pour exécuter des commandes shell de manière asynchrone
async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

# Fonction pour envoyer des messages longs en fragments tout en respectant la limite Discord
async def send_long_message(channel, message_content):
    # Discord a une limite de 2000 caractères, on doit prendre en compte les balises Markdown "```" qui prennent 6 caractères
    chunk_size = 1994  # 2000 - 6 (pour les balises ``` qui encadrent le code)
    
    if len(message_content) > chunk_size:
        for i in range(0, len(message_content), chunk_size):
            await channel.send(f"```{message_content[i:i+chunk_size]}```")
    else:
        await channel.send(f"```{message_content}```")

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Commande pour lister les formats vidéo disponibles
    if message.content.startswith('!formats'):
        url = message.content.split(" ")[1]
        command = f'yt-dlp -F "{url}"'
        embed = discord.Embed(
            title="Liste des formats",
            description=f"Récupération des formats pour {url}...",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

        stdout, stderr = await run_command(command)
        if stdout:
            # Envoie la sortie formatée (tableau) en fragments si nécessaire
            await send_long_message(message.channel, stdout)
        else:
            embed = discord.Embed(
                title="Erreur",
                description=f"```{stderr}```",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)

    # Commande pour télécharger une vidéo dans un format spécifique
    elif message.content.startswith('!download'):
        args = message.content.split(" ")
        url = args[1]
        format_code = args[2]
        output_file = args[3] if len(args) > 3 else "video_output.mp4"
        embed = discord.Embed(
            title="Téléchargement en cours",
            description=f"Téléchargement de la vidéo depuis {url}...",
            color=discord.Color.green()
        )
        await message.channel.send(embed=embed)

        command = f'yt-dlp -f {format_code} -o "{output_file}" "{url}"'
        stdout, stderr = await run_command(command)
        if stdout or stderr:
            embed = discord.Embed(
                title="Téléchargement terminé",
                description=f"Vidéo téléchargée sous le nom **{output_file}**",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)
        if stderr:
            embed = discord.Embed(
                title="Erreur",
                description=f"```{stderr}```",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)

    # Commande pour scinder la vidéo en segments
    elif message.content.startswith('!split'):
        args = message.content.split(" ")
        input_file = args[1]
        segment_time = args[2] if len(args) > 2 else "00:03:00"  # Durée par défaut de 3 minutes
        output_pattern = args[3] if len(args) > 3 else "output_segment%03d.mp4"
        command = f'ffmpeg -i {input_file} -c copy -map 0 -segment_time {segment_time} -reset_timestamps 1 -f segment {output_pattern}'

        embed = discord.Embed(
            title="Scission en cours",
            description=f"Scission de la vidéo **{input_file}** en segments de {segment_time}...",
            color=discord.Color.orange()
        )
        await message.channel.send(embed=embed)

        stdout, stderr = await run_command(command)
        if stdout or stderr:
            embed = discord.Embed(
                title="Scission terminée",
                description=f"Vidéo scindée en segments sous le format **{output_pattern}**",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)
        if stderr:
            embed = discord.Embed(
                title="Erreur",
                description=f"```{stderr}```",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)

client.run(TOKEN)