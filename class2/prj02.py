##########################匯入模組############################
from tkinter import *  # 匯入tkinter模組
import random


##########################函數定義############################
def hi_fun():
    fg_color = "#" + "".join(
        [random.choice("0123456789ABCDEF") for j in range(6)]
    )  # 隨機生成顏色

    bg_color = "#" + "".join(
        [random.choice("0123456789ABCDEF") for j in range(6)]
    )  # 隨機生成顏色
    display.config(text="Hello, world!", fg=fg_color, bg=bg_color)


##########################建立視窗############################
windows = Tk()  # 建立視窗
windows.title("My first GUI")  # 設定視窗標題
windows.option_add("*Font", "Arial 20")  # 設定全局字體
btn1 = Button(
    windows, text="click me", command=hi_fun
)  # 建立按鈕,並指定按下按鈕後要執行的函數
btn1.pack()  # 將按鈕放入視窗中
display = Label(windows, text="Hello, world!", fg="red", bg="black")  # 建立標籤
display.pack()  # 將標籤放入視窗中
########################運行應用程式##########################
windows.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
