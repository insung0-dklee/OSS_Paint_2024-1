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


#도형 이동 기능 추가
import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.current_shape = None
        self.start_x = None
        self.start_y = None

        self.create_sample_shapes()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

    def create_sample_shapes(self):
        self.canvas.create_rectangle(100, 100, 300, 200, outline="black", fill="red", tags="movable")
        self.canvas.create_oval(400, 100, 500, 200, outline="black", fill="blue", tags="movable")

    def on_canvas_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_shape = self.canvas.find_closest(event.x, event.y)

    def on_canvas_drag(self, event):
        if self.current_shape:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.current_shape, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

