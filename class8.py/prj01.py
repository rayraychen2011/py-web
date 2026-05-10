# 天氣應用程序
# 功能：根據使用者輸入的城市名稱，從OpenWeatherMap API獲取天氣資訊
# 並在GUI中顯示溫度、天氣描述和天氣圖標

from io import BytesIO  # 用於將下載的圖片轉換為字節流
import os  # 操作系統模塊
import sys  # 系統模塊
from tkinter import messagebox  # 用於顯示錯誤消息框

import requests  # 用於發送HTTP請求到天氣API
from PIL import Image, ImageTk  # 用於處理和顯示圖片
from ttkbootstrap import *  # 用於創建GUI界面

# 設定工作目錄為當前文件所在的目錄
os.chdir(sys.path[0])

# OpenWeatherMap API 設定
API_KEY = "de65126d13e1e81fca7d51f3563644df"  # API密鑰
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # 天氣數據API的基礎URL
ICON_BASE_URL = "https://openweathermap.org/img/wn/"  # 天氣圖標的基礎URL
LANG = "zh_tw"  # 語言設定：繁體中文


# 溫度轉換函數：將攝氏度轉換為華氏度
def c_to_f(celsius):
    """將攝氏度轉換為華氏度"""
    return celsius * 9 / 5 + 32


# 顯示錯誤消息
def show_error(message):
    """在狀態欄和消息框中顯示錯誤消息"""
    status_label.config(text=message)
    messagebox.showerror("錯誤", message)


# 下載並顯示天氣圖標
def show_weather_icon(icon_code):
    """根據圖標代碼下載天氣圖標並在GUI中顯示"""
    # 組合天氣圖標的完整URL
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    # 下載圖標
    icon_response = requests.get(icon_url, timeout=10)
    icon_response.raise_for_status()

    # 將圖片轉換為PIL Image對象，調整大小為90x90像素
    image = Image.open(BytesIO(icon_response.content)).resize((90, 90))
    # 轉換為tkinter可用的PhotoImage格式
    weather_photo = ImageTk.PhotoImage(image)
    # 在標籤中顯示圖片
    icon_label.config(image=weather_photo, text="")
    # 保持圖片引用，防止被垃圾回收
    icon_label.image = weather_photo


# 顯示天氣信息
def show_weather_info(info):
    """從API返回的信息中提取並顯示天氣數據"""
    # 從API響應中提取溫度、描述和圖標代碼
    current_temp = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]

    # 根據使用者選擇的溫度單位，顯示相應的溫度
    if temp_unit.get():
        temp_text = f"溫度: {current_temp:.1f}°C"
    else:
        temp_text = f"溫度: {c_to_f(current_temp):.1f}°F"

    # 更新GUI中各個標籤的內容
    temp_label.config(text=temp_text)
    desc_label.config(text=f"描述: {weather_description}")
    status_label.config(text="")  # 清除錯誤消息
    show_weather_icon(icon_code)  # 顯示天氣圖標


# 獲取天氣數據
def get_weather():
    """獲取輸入城市的天氣數據並顯示"""
    # 獲取並清理使用者輸入的城市名稱
    city_name = city_entry.get().strip()
    # 檢查是否有輸入城市名稱
    if city_name == "":
        show_error("請先輸入城市名稱")
        return

    # 設定API請求參數
    params = {
        "q": city_name,  # 城市名稱
        "appid": API_KEY,  # API密鑰
        "units": "metric",  # 使用公制單位（溫度單位為攝氏度）
        "lang": LANG,  # 語言設定
    }

    try:
        # 發送API請求
        response = requests.get(BASE_URL, params=params, timeout=10)
        info = response.json()

        # 檢查是否找到城市
        if response.status_code == 404 or str(info.get("cod")) == "404":
            show_error("找不到這個城市，請重新輸入，或改用英文城市名稱")
            return

        # 如果有其他HTTP錯誤，拋出異常
        response.raise_for_status()
        # 顯示獲取到的天氣信息
        show_weather_info(info)
    except requests.RequestException:
        # 處理網路連接錯誤
        show_error("無法取得天氣資料，請檢查網路連線或 API 設定")
    except (KeyError, IndexError, ValueError):
        # 處理數據解析錯誤
        show_error("天氣資料或語言設定錯誤，請稍後再試")


# 刷新溫度單位
def refresh_temperature_unit():
    """當使用者改變溫度單位時，重新獲取並顯示天氣數據"""
    temp_text = temp_label.cget("text")
    # 只有當已經顯示了有效的溫度數據時，才重新獲取天氣
    if temp_text.startswith("溫度: ") and temp_text != "溫度: ?°C":
        get_weather()


# ====== GUI 初始化部分 ======
# 創建主窗口
window = Tk()
window.title("Weather App")
window.geometry("1000x230")  # 設定窗口大小為1000x230像素
window.resizable(False, False)  # 禁用窗口調整大小

# 設定字體大小
font_size = 24
window.option_add("*Font", ("Microsoft JhengHei UI", font_size))

# 設定主題和組件樣式
style = Style(theme="minty")  # 使用minty主題
style.configure("success.TButton", font=("Microsoft JhengHei UI", 24))  # 設定按鈕字體
style.configure("my.TCheckbutton", font=("Microsoft JhengHei UI", 24))  # 設定複選框字體

# ====== 創建 GUI 組件 ======
# 溫度單位切換變數（True=攝氏度，False=華氏度）
temp_unit = BooleanVar(value=True)

# 第一行：標題標籤、城市輸入框、搜尋按鈕
title_label = Label(window, text="請輸入想搜尋的城市:")
title_label.grid(row=0, column=0, padx=(15, 0), pady=(35, 0), sticky="w")

# 城市名稱輸入框
city_entry = Entry(window, width=25)
city_entry.grid(row=0, column=1, padx=5, pady=(35, 0), sticky="ew")
city_entry.focus()  # 設定焦點到輸入框
city_entry.bind("<Return>", lambda event: get_weather())  # 按Enter鍵時獲取天氣

# 獲取天氣按鈕
search_button = Button(
    window,
    text="獲得天氣資訊",
    command=get_weather,
    bootstyle="success",
    style="success.TButton",
)
search_button.grid(row=0, column=2, padx=(0, 15), pady=(35, 0), sticky="ew")

# 第二行：天氣圖標、溫度、天氣描述
icon_title_label = Label(window, text="天氣圖標")
icon_title_label.grid(row=1, column=0, padx=15, pady=(10, 0))

# 溫度顯示標籤
temp_label = Label(window, text="溫度: ?°C")
temp_label.grid(row=1, column=1, padx=15, pady=(10, 0))

# 天氣描述顯示標籤
desc_label = Label(window, text="描述: ?")
desc_label.grid(row=1, column=2, padx=15, pady=(10, 0))

# 第三行：天氣圖標、溫度單位複選框、狀態/錯誤消息
icon_label = Label(window, text="")  # 用於顯示天氣圖標的標籤
icon_label.grid(row=2, column=0, padx=15, pady=(0, 0))

# 溫度單位切換複選框
unit_check = Checkbutton(
    window,
    text="溫度單位(°C/°F)",
    variable=temp_unit,
    onvalue=True,  # 選中時為True（攝氏度）
    offvalue=False,  # 未選中時為False（華氏度）
    command=refresh_temperature_unit,  # 切換時刷新溫度
    style="my.TCheckbutton",
)
unit_check.grid(row=2, column=1, padx=15, pady=(0, 0))

# 狀態/錯誤消息標籤
status_label = Label(window, text="", bootstyle="danger")
status_label.grid(row=2, column=2, padx=15, pady=(0, 0))

# 設定列權重，讓城市輸入框能夠自動展開
window.columnconfigure(1, weight=1)

# 進入事件循環，顯示窗口
window.mainloop()
