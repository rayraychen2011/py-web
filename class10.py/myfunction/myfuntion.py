import requests

class WeatherAPI:
    def __init__(self, api_key, lang="zh_tw"):
        self.api_key = api_key
        self.lang = lang
        self.units = "metric"  # 使用公制单位
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.icon_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city):
        send_url=(f"{self.base_url}?q={city}&appid={self.api_key}&lang={self.lang}&units={self.units}")
        response = requests.get(send_url)
        return response.json()
    def get_weather_icon_url(self, icon_code):
        return f"{self.icon_base_url}{icon_code}@2x.png"
