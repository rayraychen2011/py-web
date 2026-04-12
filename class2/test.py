##########################匯入模組############################
from tkinter import *  # 匯入tkinter模組


##########################函數定義############################
def hi_fun():
    if display.cget("bg") == "red":
        display.config(text="green", fg="black", bg="green")
    elif display.cget("bg") == "green":
        display.config(text="red", fg="black", bg="red")


##########################建立視窗############################
windows = Tk()  # 建立視窗
windows.title("My first GUI")  # 設定視窗標題
btn1 = Button(
    windows, text="click me", command=hi_fun
)  # 建立按鈕,並指定按下按鈕後要執行的函數
btn1.pack()  # 將按鈕放入視窗中
display = Label(windows, text="red", fg="black", bg="red")  # 建立標籤
display.pack()  # 將標籤放入視窗中
########################運行應用程式##########################
windows.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
