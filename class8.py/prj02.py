#######################匯入模組#######################
# 輸入 tkinter 模組
from ttkbootstrap import *
import sys
import os
import requests
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

#######################設定工作目錄########################
os.chdir(sys.path[0])


#######################定義函式########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"  # 請求天氣資料的URL
UNITS = "metric"  # 攝氏溫度
LANG = "zh_tw"  # 中文顯示
ICON_URL = "http://openweathermap.org/img/wn/"  # 請求天氣圖示的URL

# 存儲最新的天氣數據
weather_data = {"temp_celsius": None, "weather_desc": None, "icon": None}

# 溫度單位選擇（暫時存放，在 window 建立後才能用 StringVar）
temp_unit_choice = "metric"


def update_temperature_display():
    """根據新選擇的區間更新溫度顯示"""
    if weather_data["temp_celsius"] is None:
        return

    unit_choice = temp_unit_var.get()
    if unit_choice == "metric":
        temp_display = f"溫度: {weather_data['temp_celsius']}°C"
    else:  # imperial
        temp_fahrenheit = (weather_data["temp_celsius"] * 9 / 5) + 32
        temp_display = f"溫度: {temp_fahrenheit:.1f}°F"

    temp_label.config(text=temp_display)


def get_weather():
    """獲取輸入城市的天氣資訊"""
    city = entry.get().strip()
    if not city:
        messagebox.showwarning(
            "警告", "你是傻b嗎？好像是耶! 大家都說了要輸入城市了，你還不輸入？"
        )
        return

    try:
        # 構建請求URL（統一使用攝氏溫度購取，然後根據選擇轉換）
        url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric&lang={LANG}"
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()

        # 提取並存儲天氣資訊
        weather_data["temp_celsius"] = data["main"]["temp"]
        weather_data["weather_desc"] = data["weather"][0]["description"]
        weather_data["icon"] = data["weather"][0]["icon"]

        # 更新溫度顯示（根據當前選擇）
        update_temperature_display()
        # 更新描述標籤
        desc_label.config(text=f"描述: {weather_data['weather_desc']}")

        # 下載並顯示天氣圖示
        icon_url = f"{ICON_URL}{weather_data['icon']}@2x.png"
        img_response = requests.get(icon_url)
        img_response.raise_for_status()
        from io import BytesIO

        img = Image.open(BytesIO(img_response.content))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo  # 保持參照，防止垃圆回收

    except requests.exceptions.RequestException as e:
        # messagebox.showerror("錯誤", f"無法連接到天氣API: {str(e)}")
        messagebox.showerror("錯誤", f"無法連接到天氣API: 大傻b，你的有問題嗎？")
    except KeyError:
        messagebox.showerror("錯誤", "城市未找到，請檢查城市名稱")
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")


#######################建立視窗########################
# 建立主視窗
window = Tk()
# 設定視窗標題
window.title("Weather App")
#######################設定字形########################
font_size = 20
window.option_add("*Font", ("新細明體", font_size))
#######################設定主題########################
style = Style(theme="vapor")
style.configure("my.TButton", font=("新細明體", font_size))
#######################建立標籤########################
label = Label(window, text="請輸入想搜尋的城市:")
label.grid(row=0, column=0, columnspan=1, sticky="EW")
#######################建立輸入框########################
entry = Entry(window, font=("新細明體", font_size))
entry.grid(row=0, column=1, columnspan=1, sticky="EW", padx=5)
#######################建立按鈕########################
btn_search = Button(window, text="搜尋天氣", command=get_weather, style="my.TButton")
btn_search.grid(row=0, column=2, columnspan=1, sticky="EW", padx=5)

#######################建立結果顯示標籤########################
# 左側：天氣圖標
image_label = Label(window, relief="sunken", anchor="center")
image_label.grid(row=1, column=0, columnspan=1, sticky="NSEW", padx=10, pady=10)

# 中間：溫度
temp_label = Label(
    window, text="溫度: ?°C", justify="center", relief="sunken", anchor="center"
)
temp_label.grid(row=1, column=1, columnspan=1, sticky="NSEW", padx=10, pady=10)

# 右側：天氣描述
desc_label = Label(
    window, text="描述: ?", justify="center", relief="sunken", anchor="center"
)
desc_label.grid(row=1, column=2, columnspan=1, sticky="NSEW", padx=10, pady=10)

#######################建立溫度區間選擇########################
# 創建一個框架來容納複選框
button_frame = Frame(window)
button_frame.grid(row=2, column=1, columnspan=1, sticky="EW", padx=10, pady=5)

# 溫度區間複選框
temp_unit_var = StringVar(value="metric")
celsius_btn = Checkbutton(
    button_frame,
    text="溫度區間(°C/°F)",
    variable=temp_unit_var,
    onvalue="metric",
    offvalue="imperial",
    command=update_temperature_display,
)
celsius_btn.pack(side="left")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(1, weight=1)
window.mainloop()
