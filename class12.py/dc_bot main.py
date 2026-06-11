import asyncio
import discord
import os
from dotenv import load_dotenv
import requests
from myfunction.myfuntion import WeatherAPI

load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())  # 解決 Windows 上的事件循環問題

intents = discord.Intents.default()
intents.message_content = True  # 啟用 message_content intent

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))


def build_eather_embed(weather_summary):
    embed = discord.Embed(
        title=f"{weather_summary['city_name']} 的天氣",
        description=f"描述:{weather_summary["description"]}",
        color=discord.Colour.from_str("#205386"),
    )
    icon_url = weather_api.get_weather_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)
    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_c']}°C", inline=False
    )
    return embed


def build_forecast_embed(forecast_summary):
    embeds = []
    for forecast in forecast_summary:
        embed = discord.Embed(
            title=f"{forecast['city_name']} 的天氣預報",
            description=f"描述:{forecast['description']}",
            color=discord.Colour.from_str("#205386"),
        )
        icon_url = weather_api.get_weather_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度", value=f"{forecast['temperature_c']}°C", inline=False
        )
        embeds.append(embed)

    return embeds


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await tree.sync()  # 同步命令到 Discord


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "hello":
        await message.channel.send("Hey!")


@tree.command(name="hello", description="Say hello to the bot")
async def hello_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@tree.command(name="weather", description="查詢城市天氣")
async def weather(interaction: discord.Interaction, city: str):
    await interaction.response.defer()  # 延遲回應，表示正在處理
    city = city.strip()
    if not weather_api.api_key:
        await interaction.followup.send("天氣 API 金鑰未設定，無法查詢天氣資訊。")
        return

    try:
        weather_summary = weather_api.get_weather_summary(city)
    except Exception as e:
        await interaction.followup.send(f"查詢天氣資訊時發生錯誤: {str(e)}")
        return
    if weather_summary is None:
        await interaction.followup.send(
            f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。"
        )
        return


@tree.command(name="forecast", description="查詢城市天氣預報")
async def forecast(interaction: discord.Interaction, city: str, forecast: bool = False):
    await interaction.response.defer()  # 延遲回應，表示正在處理
    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(
                    f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。"
                )
                return
            embed = build_eather_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return
    except Exception as e:
        await interaction.followup.send(f"查詢天氣資訊時發生錯誤: {str(e)}")
        return


def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
