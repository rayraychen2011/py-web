import requests
import openai


class WeatherAPI:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.lang = lang
        self.units = "metric"  # 使用公制单位
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.icon_url = "http://openweathermap.org/img/wn/"
        self.api_key = api_key
        self.units = "metric"
        self.lang = lang
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.icon_base_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city):
        send_url = f"{self.base_url}q={city}&appid={self.api_key}&lang={self.lang}&units={self.units}"
        print(f"Sending request to: {send_url}")  # 調試輸出
        response = requests.get(send_url)
        return response.json()

    def get_weather_icon_url(self, icon_code):
        return f"{self.icon_url}{icon_code}@2x.png"

    def get_weather_summary(self, city_name):
        info = self.get_current_weather(city_name)
        if "weather" in info and "main" in info:
            return {
                "city_name": info.get("name", city_name),
                "temperature_c": round(info["main"]["temp"], 2),
                "description": info["weather"][0]["description"],
                "icon_code": info["weather"][0]["icon"],
            }
        return None

    def get_icon(self, icon_code):
        icon_url = self.get_weather_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content
        return None

    def get_forecast(self, city):
        send_url = f"{self.forecast_url}q={city}&appid={self.api_key}&lang={self.lang}&units={self.units}"
        print(f"Sending request to: {send_url}")  # 調試輸出

        response = requests.get(send_url)
        response.raise_for_status()  # 確保請求成功
        return response.json()

    def get_forecast_summary(self, city_name, count=10):
        forecast_count = max(0, count)
        try:
            info = self.get_forecast(city_name)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None
            raise
        if "city" not in info or "list" not in info:
            return None

        city_label = info["city"].get("name", city_name)
        forecast_summary = []

        for forecast in info["list"][:forecast_count]:
            forecast_summary.append(
                {
                    "city_name": city_label,
                    "datetime": forecast.get("dt_txt"),
                    "temperature_c": round(forecast["main"]["temp"], 2),
                    "description": forecast["weather"][0]["description"],
                    "icon_code": forecast["weather"][0]["icon"],
                }
            )
        return forecast_summary


class AIAssistant:
    """把 OpenAI 的對話功能整理成可重複使用的工具類別。"""

    def __init__(self, api_key):
        # __init__() 負責準備 OpenAI 的設定。
        # 把 API 金鑰存起來，之後呼叫 AI 分析時才能通過驗證。
        self.api_key = api_key
        openai.api_key = api_key  # 設定 OpenAI 的全域金鑰

    def ask(
        self,
        system_prompt,
        user_message,
        history_messages=None,
        temperature=0.2,
        model="gpt-4o",
    ):
        """進行一次 AI 對話，也可以帶入整理好的對話歷史。"""
        # 這個方法讓我們可以問 AI 一個問題，並得到一次性的回答。
        # system_prompt 是給 AI 的角色設定，例如「你是氣象分析師」。
        # user_message 是我們要問的具體問題，例如「請分析這份天氣預報」。
        # history_messages 是已經整理好的舊對話；沒有需要上下文時可以不傳。

        # 如果沒有設定金鑰，直接回傳錯誤訊息
        if not self.api_key:
            return None, "尚未設定 OPENAI_API_KEY，請先在 .env 檔案中完成設定。"

        if history_messages is None:
            history_messages = []

        # messages 的順序很重要：
        # 1. system：先告訴 AI 要扮演什麼角色
        # 2. history：放入已經整理好的舊對話
        # 3. user：最後放這次真正要問的新問題
        messages = (
            [{"role": "system", "content": system_prompt}]
            + history_messages
            + [{"role": "user", "content": user_message}]
        )

        print("=== 傳給 OpenAI 的訊息 ===")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")
        print("===========================")

        try:
            # 向 OpenAI 送出請求
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            # 取出 AI 的回答
            assistant_message = response.choices[0].message.content

            return assistant_message, None  # 成功時回傳回答，錯誤訊息為 None

        except Exception as e:
            # 如果 OpenAI 呼叫失敗，回傳錯誤訊息
            return None, f"發生錯誤：{e}"
