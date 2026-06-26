import asyncio
import discord
import os
from dotenv import load_dotenv
import requests
from myfunction.myfuntion import WeatherAPI, AIAssistant
import openai

load_dotenv()
asyncio.set_event_loop(asyncio.new_event_loop())  # 解決 Windows 上的事件循環問題

intents = discord.Intents.default()
intents.message_content = True  # 啟用 message_content intent

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))
ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))
# 限制讀取的歷史訊息數量，避免一次把整個頻道都交給 AI。
CHANNEL_HISTORY_LIMIT = 15

# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣自然、簡短、適合國小學生閱讀。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

# 允許 AI 回覆中提到「使用者或 bot」，但不要讓 AI 觸發 @everyone、@here 或角色標記。
# bot 在 Discord 裡也屬於 user，所以 users=True 就可以提到其他 bot。
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False,
    users=True,
    roles=False,
    replied_user=True,
)


def build_weather_embed(weather_summary):
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


async def get_channel_history(channel, bot_user, limit=15, before=None):
    """讀取 Discord 頻道中的舊訊息，整理成 OpenAI 可以使用的 messages。"""
    old_messages = []
    history_messages = []
    # Discord API 讀頻道訊息時，預設會先拿較新的訊息。
    # 這裡先明確抓「最近的幾則」，把「抓資料」和「排成對話順序」分成兩步。
    # oldest_first=False 代表先拿最接近 before 的新訊息。
    # 下面再反轉成「舊到新」交給 AI，比較像大家平常閱讀對話的順序。
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)

    # Discord 抓回來的是「新到舊」，但 AI 閱讀對話時需要「舊到新」。
    for old_message in reversed(old_messages):
        # 這裡使用 message.content，而不是 clean_content。
        # message.content 會保留 <@使用者ID> 這種真正的 mention 格式。
        content = old_message.content.strip()
        if not content:
            continue  # 空白訊息不用交給 AI，避免浪費上下文空間

        if old_message.author.id == bot_user.id:
            # 機器人自己以前說過的話，用 assistant 角色放回歷史中。
            history_messages.append({"role": "assistant", "content": content})
        else:
            # 其他同學和其他 bot 都標上名字，AI 才知道是誰說的。
            speaker_type = "機器人" if old_message.author.bot else "同學"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"（{speaker_type}，mention：{speaker_mention}）說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages


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
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    await interaction.response.defer()  # 延遲回應，表示正在處理
    city = city.strip()
    if not weather_api.api_key:
        await interaction.followup.send("天氣 API 金鑰未設定，無法查詢天氣資訊。")
        return

    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(
                    f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。"
                )
                return
            embed = build_weather_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return
        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(
                    f"無法取得 {city} 的天氣預報資訊，請確認城市名稱是否正確。"
                )
                return
            embeds = build_forecast_embed(forecast_summary)

            await interaction.followup.send(embeds=embeds[:10])
            return

        raw_forecast = weather_api.get_forecast(city)

    except Exception as e:
        await interaction.followup.send(f"查詢天氣資訊時發生錯誤: {str(e)}")
        return

    analysis, error = ai_assistant.ask(
        system_prompt="你是一個天氣分析師，請根據以下天氣預報資訊提供分析和建議。",
        user_message=f"請分析以下天氣預報資訊並提供建議:\n{raw_forecast}",
    )
    if error:
        await interaction.followup.send(f"AI 分析時發生錯誤: {error}")
    else:
        await interaction.followup.send(f"AI 分析結果: {analysis}")


def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
