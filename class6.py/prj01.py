import requests
import os
import sys

API_KEY = "de65126d13e1e81fca7d51f3563644df"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "http://openweathermap.org/img/wn/"

city_name = input("請輸入城市名稱: ")
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的URL: {send_url}")
response = requests.get(send_url)
info = response.json()
os.chdir(sys.path[0])  # 切換到當前腳本所在的目錄
if not (info.get("cod") == 404):
    currnt_temp = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]
    print(f"城市: {city_name}")
    print(f"溫度: {currnt_temp}°C")
    print(f"天氣描述: {weather_description}")
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    print(f"天氣圖示URL: {icon_url}")
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open(f"{icon_code}.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
        print(f"天氣圖示已下載並保存為 {icon_code}.png")
    else:
        print("無法下載天氣圖示。")
else:
    print("城市名稱錯誤，請重新輸入。")
