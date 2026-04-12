##########################匯入模組############################
from tkinter import *  # 匯入tkinter模組


##########################函數定義############################
def clear_fun():
    bg_color = display.cget("bg")  # 使用cget獲取背景色
    print(f"背景色: {bg_color}")  # 偵測並顯示背景色
    display.config(text="")  # 清除文字


show_fun = lambda: display.config(text="Hello, world!")


##########################建立視窗############################
windows = Tk()  # 建立視窗
windows.title("My first GUI")  # 設定視窗標題
btn1 = Button(
    windows, text="show screen", command=show_fun
)  # 建立按鈕,並指定按下按鈕後要執行的函數
btn1.pack()  # 將按鈕放入視窗中
btn2 = Button(
    windows, text="clear screen", command=clear_fun
)  # 建立按鈕,並指定按下按鈕後要
btn2.pack()  # 將按鈕放入視窗中
display = Label(windows, text="")
display.pack()  # 將標籤放入視窗中
########################運行應用程式##########################
windows.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
