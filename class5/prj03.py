import requests

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"

city_name = input("請輸入城市名稱: ")
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的URL: {send_url}")
response = requests.get(send_url)
info = response.json()
