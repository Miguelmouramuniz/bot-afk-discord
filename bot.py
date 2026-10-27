import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            if not discord.utils.get(bot.voice_clients, guild=channel.guild):
                await channel.connect()
                print(f"Conectado ao canal de voz: {channel.name}")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel is None:
        print("Bot desconectado. A reconectar...")
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect()
            except Exception as e:
                print(f"Erro ao reconectar: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
