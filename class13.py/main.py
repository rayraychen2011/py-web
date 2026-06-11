import requests

API_KEY = "de65126d13e1e81fca7d51f3563644df"
Base_URL = "http://api.openweathermap.org/data/2.5/forecast?"
UNITS = "metric"  # 使用公制单位
LANG = "zh_tw"  # 使用中文

city_name = "Taipei"
send_url = f"{Base_URL}q={city_name}&appid={API_KEY}&lang={LANG}&units={UNITS}"
print(f"Sending request to: {send_url}")  # 調試輸出

response = requests.get(send_url)
response.raise_for_status()  # 確保請求成功
info = response.json()

if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        wather_description = forecast["weather"][0]["description"]
        print(dt_txt, temp, wather_description)
else:
    print("無法取得天氣資訊，請確認城市名稱是否正確。")
