from ttkbootstrap import *
import os
import sys

# ############################ 設定工作目錄 ############################
# 將工作目錄切換到目前程式所在的資料夾，方便讀取相關檔案
os.chdir(sys.path[0])


# ############################ 定義函數 ############################
def on_switch_change():
    # 當 Checkbutton 狀態改變時，將目前布林值顯示在標籤上
    check_label.config(text=str(check_type.get()))


# ############################ 建立視窗 ############################
# 建立主視窗
window = Tk()

# 設定視窗標題
window.title("Checkbutton")

# ############################ 設定字型 ############################
# 設定全域預設字型大小
font_size = 20

# 設定所有元件的預設字型
window.option_add("*font", ("Helvetica", font_size))

# ############################ 設定主題 ############################
# 設定視窗主題樣式
style = Style(theme="minty")

# 設定按鈕與 Checkbutton 的字型樣式
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))

# ############################ 建立變數 ############################
# BooleanVar 是 tkinter / ttk 用來和元件同步的布林變數
check_type = BooleanVar()

# 預設為勾選狀態
check_type.set(True)

# ############################ 建立標籤 ############################
# 建立標籤，顯示目前 Checkbutton 對應的布林值
check_label = Label(window, text="True")

# 將標籤放到視窗中的指定位置
check_label.grid(row=1, column=2, padx=10, pady=10)

# ############################ 建立Checkbutton ############################
# Checkbutton 會和 check_type 綁在一起
# 勾選時存 True，取消勾選時存 False，並在狀態改變時呼叫 on_switch_change
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
)

# 將 Checkbutton 放到視窗中的指定位置
check.grid(row=1, column=1, padx=10, pady=10)

# ############################ 運行應用程式 ############################
# 開始執行主迴圈，等待使用者操作
window.mainloop()
