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

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageResizer:
    def __init__(self, master):
        self.master = master
        master.title("Image Resizer")

        # 파일 선택 버튼
        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)

        # 단위 선택 라디오 버튼
        self.unit_var = tk.StringVar()
        self.unit_var.set("inch")
        self.inch_radio = tk.Radiobutton(master, text="Inch", variable=self.unit_var, value="inch")
        self.cm_radio = tk.Radiobutton(master, text="Centimeter", variable=self.unit_var, value="cm")
        self.pixel_radio = tk.Radiobutton(master, text="Pixel", variable=self.unit_var, value="pixel")
        self.inch_radio.pack(pady=5)
        self.cm_radio.pack(pady=5)
        self.pixel_radio.pack(pady=5)

        # 크기 조절 입력 필드
        self.width_label = tk.Label(master, text="Width:")
        self.width_entry = tk.Entry(master)
        self.height_label = tk.Label(master, text="Height:")
        self.height_entry = tk.Entry(master)
        self.width_label.pack(pady=5)
        self.width_entry.pack(pady=5)
        self.height_label.pack(pady=5)
        self.height_entry.pack(pady=5)

        # 리사이즈 버튼
        self.resize_button = tk.Button(master, text="Resize", command=self.resize_image)
        self.resize_button.pack(pady=10)

        # 이미지 표시
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.gif")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)

    def resize_image(self):
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        unit = self.unit_var.get()

        if unit == "inch":
            dpi = 300
            new_size = (int(width * dpi), int(height * dpi))
        elif unit == "cm":
            dpi = 118  # 1인치 = 2.54cm
            new_size = (int(width * dpi / 2.54), int(height * dpi / 2.54))
        else:
            new_size = (width, height)

        resized_image = self.original_image.resize(new_size)
        self.display_image(resized_image)

    def display_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

root = tk.Tk()
app = ImageResizer(root)
root.mainloop()
