"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

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

#도형회전기능 추가

def rotate_shapes():
    angle = math.radians(45)  # 45도 회전
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    objects = canvas.find_all()
    for obj in objects:
        coords = canvas.coords(obj)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            # 원점 기준 회전
            new_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
            new_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
            new_coords.extend([new_x, new_y])
        canvas.coords(obj, *new_coords)


# 도형크기조절(1.5배 증가) 기능 추가
import tkinter as tk
import math

def resize_shapes(scale=1.5):
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    objects = canvas.find_all()
    for obj in objects:
        coords = canvas.coords(obj)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            # 원점 기준 크기 조절
            new_x = center_x + (x - center_x) * scale
            new_y = center_y + (y - center_y) * scale
            new_coords.extend([new_x, new_y])
        canvas.coords(obj, *new_coords)

def initialize_paint_app():
    root = tk.Tk()
    root.title("그림판")
    root.geometry("800x600")
    return root

def create_canvas(root):
    canvas = tk.Canvas(root, bg="white", width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    return canvas

def create_sample_shapes(canvas):
    canvas.create_rectangle(100, 100, 300, 200, outline="black", fill="red", tags="movable")
    canvas.create_oval(400, 100, 500, 200, outline="black", fill="blue", tags="movable")

def run_paint_app():
    global canvas
    root = initialize_paint_app()
    canvas = create_canvas(root)
    create_sample_shapes(canvas)
    
    # 버튼으로 크기 조절 기능 실행
    resize_button = tk.Button(root, text="크기 조절", command=resize_shapes)
    resize_button.pack()
    
    root.mainloop()

if __name__ == "__main__":
    run_paint_app()


# 색상추출 기능
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        show_image(image)

def show_image(image):
    # 이미지 크기 조정
    image.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.image = photo  # 이미지가 garbage-collected 되는 것을 방지하기 위해 저장
    return image

def extract_color(event):
    x, y = event.x, event.y
    rgb_color = current_image.getpixel((x, y))
    hex_color = '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])
    color_label.config(text=f"Color: {hex_color}")

root = tk.Tk()
root.title("Color Extractor")

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

color_label = tk.Label(root, text="Color: ")
color_label.pack()

current_image = None  # 현재 이미지를 저장할 변수

canvas.bind("<Button-1>", extract_color)

root.mainloop()
