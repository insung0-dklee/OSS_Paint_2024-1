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
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        self.canvas_width = 400
        self.canvas_height = 400

        self.img = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.photo = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.photo, state="normal")

        # 그리기 모드 활성화
        self.drawing = False
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # 대칭 버튼 추가
        self.flip_h_button = tk.Button(root, text="가로 대칭", command=self.flip_horizontal)
        self.flip_h_button.pack(side=tk.LEFT)

        self.flip_v_button = tk.Button(root, text="세로 대칭", command=self.flip_vertical)
        self.flip_v_button.pack(side=tk.RIGHT)

    def paint(self, event):
        if not self.drawing:
            self.drawing = True
            self.start_x = event.x
            self.start_y = event.y
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, fill="black", width=2)
        self.start_x = self.end_x
        self.start_y = self.end_y

    def reset(self, event):
        self.drawing = False
        self.update_image()

    def update_image(self):
        self.img = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.img)
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if len(coords) == 4:
                self.draw.line([coords[0], coords[1], coords[2], coords[3]], fill="black", width=2)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.photo, state="normal")

    def flip_horizontal(self):
        self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.photo, state="normal")

    def flip_vertical(self):
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.photo, state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
