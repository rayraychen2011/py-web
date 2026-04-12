from ttkbootstrap import *
import sys
import os


def test():
    print("test")


windows = Tk()  # 建立視窗
windows.title("My first GUI")  # 設定視窗標題

font_size = 20
windows.option_add("*Font", ("Arial", font_size))  # 設定全域字型

style = Style(theme="darkly")  # 設定主題
style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型

Label = Label(windows, text="Hello, world!")
Label.grid(row=0, column=0, sticky="E")

button = Button(windows, text="瀏覽", command=test, style="my.TButton")
button.grid(row=0, column=1, sticky="W")
button2 = Button(windows, text="顯示", command=test, style="my.TButton")
button2.grid(row=1, column=0, columnspan=2, sticky="EW")


windows.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
