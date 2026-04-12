from ttkbootstrap import *
import sys
import os
from tkinter import filedialog
from PIL import Image, ImageTk


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])
    label2.config(text=file_path)


def show_image():
    global file_path
    image = Image.open(file_path)
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo  # 防止圖片被垃圾回收機制回收


window = Tk()  # 建立視窗
window.title("My first GUI")  # 設定視窗標題
label = Label(window, text="選擇檔案:")
label.grid(row=0, column=0, sticky="E")
label2 = Label(window, text="無")
label2.grid(row=0, column=1, sticky="E")

button = Button(window, text="瀏覽", command=open_file, style="my.TButton")
button.grid(row=0, column=2, sticky="W")
button2 = Button(window, text="顯示", command=show_image, style="my.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")

canvas = Canvas(window, width=600, height=600)
canvas.grid(row=2, column=0, columnspan=3)

window.mainloop()  # 開始執行主迴圈,讓視窗保持顯示狀態
