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

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await tree.sync()  # 同步命令到 Discord

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content=="hello":
        await message.channel.send("Hey!")

@tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))

if __name__ == "__main__":
    main()