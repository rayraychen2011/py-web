import asyncio
import discord
import os
from dotenv import load_dotenv


load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())  # 解決 Windows 上的事件循環問題

intents = discord.Intents.default()
intents.message_content = True  # 啟用 message_content intent

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


@bot.event
async def on_ready():