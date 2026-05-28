import requests


class WeatherAPI:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.lang = lang
        self.units = "metric"  # 使用公制单位
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.icon_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city):
        send_url = f"{self.base_url}?q={city}&appid={self.api_key}&lang={self.lang}&units={self.units}"
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
