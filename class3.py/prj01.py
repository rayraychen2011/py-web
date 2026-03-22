##########################匯入模組############################
from tkinter import *  # 匯入tkinter模組
from PIL import Image, ImageTk
import sys
import os

########################新增工作目錄##########################
os.chdir(sys.path[0])


##########################函數定義############################
def move_circle(event):
    key = event.keysym
    print(key)
    if key == "Right":
        canvas.move(circle, 10, 0)
    elif key == "Left":
        canvas.move(circle, -10, 0)
    elif key == "Up":
        canvas.move(circle, 0, -10)
    elif key == "Down":
        canvas.move(circle, 0, 10)


##########################建立視窗############################
windows = Tk()  # 建立視窗
windows.title("My first GUI")  # 設定視窗標題
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()
#######################建立視窗圖片##########################

windows.iconbitmap("crocodile2.ico")
#####################載入圖片#############################
image = Image.open("crocodile2.png")
img = ImageTk.PhotoImage(image)
#####################顯示圖片#############################
my_img = canvas.create_image(300, 300, image=img)

#######################畫圖形#################################
circle = canvas.create_oval(250, 150, 300, 200, fill="red")
rect = canvas.create_rectangle(220, 400, 340, 430, fill="blue")
msg = canvas.create_text(300, 100, text="crocodile", fill="black", font=("Arial", 30))
canvas.bind_all("<Key>", move_circle)

########################運行應用程式##########################
windows.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
