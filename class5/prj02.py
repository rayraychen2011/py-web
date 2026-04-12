from ttkbootstrap import *
import sys
import os


def show_result():
    entry_text = entry.get()
    try:
        result = eval(entry_text)
    except:
        result = "輸入錯誤"
    label.config(text=result)


os.chdir(sys.path[0])
Windows = Tk()  # 建立視窗
Windows.title("My first GUI")  # 設定視窗標題
label = Label(Windows, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
button = Button(Windows, text="顯示計算結果", command=show_result, style="my.TButton")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
entry = Entry(Windows, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
font_size = 20
Windows.option_add("*Font", ("Helvetica", font_size))

Style = Style(theme="minty")  # 設定主題
Style.configure("my.TButton", font=("Helvetica", font_size))  # 設定按鈕字型

window.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
