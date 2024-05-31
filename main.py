"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk, ImageOps

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()


def open_image():
    global image, tk_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        image = Image.open(file_path)
        tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image

def mirror_image():
    global image, tk_image
    if image:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image

def rotate_image():
    global image, tk_image
    if image:
        image = image.rotate(90)  # 90도씩 회전하도록 변경 가능
        tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image

def invert_colors():
    global image, tk_image
    if image:
        image = ImageOps.invert(image)
        tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image

root = tk.Tk()
root.title("이미지 불러오기")
root.geometry("800x600")

canvas = tk.Canvas(root, bg="white", width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

open_button = tk.Button(root, text="이미지 불러오기", command=open_image)
open_button.pack(side=tk.TOP)

mirror_button = tk.Button(root, text="대칭 이동", command=mirror_image)
mirror_button.pack(side=tk.LEFT)

rotate_button = tk.Button(root, text="회전", command=rotate_image)
rotate_button.pack(side=tk.LEFT)

invert_button = tk.Button(root, text="색 반전", command=invert_colors)
invert_button.pack(side=tk.LEFT)

root.mainloop()


