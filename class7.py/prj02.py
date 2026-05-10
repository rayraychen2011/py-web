###########################匯入模組###########################
# 匯入 ttkbootstrap 模組，這個美化版 tkinter 元件在 adv-02/prj-04-ttk_GUI.py 已經介紹過
from ttkbootstrap import *

# 匯入 sys、os 模組，用來設定工作目錄
import sys
import os

# 匯入 PIL 模組，用來讀取與顯示圖片
from PIL import Image, ImageTk

###########################設定工作目錄###########################
# 工作目錄的設定方式在 adv-01/prj-08-loadimage.py 已經介紹過
os.chdir(sys.path[0])

###########################建立視窗###########################
# 建立主視窗
window = Tk()

# 設定視窗標題
window.title("Label Image")

###########################讀取圖片###########################
# 這張 weather.png 可接續使用 adv-03/prj-04-get_icon.py 下載下來的圖片
image = Image.open("weather.png")

# tkinter 不能直接顯示 PIL 的圖片物件，所以要先轉成 PhotoImage
weather_photo = ImageTk.PhotoImage(image)

###########################建立標籤###########################
# Label 除了顯示文字，也可以用 image= 直接顯示圖片
weather_label = Label(window, image=weather_photo)
weather_label.pack(padx=20, pady=20)

# 這行要把圖片參照保留下來，否則圖片可能會被回收而消失
weather_label.image = weather_photo

###########################運行應用程式###########################
# 開始執行主迴圈，等待使用者操作
window.mainloop()
