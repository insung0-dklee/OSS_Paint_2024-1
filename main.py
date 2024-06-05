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

import pyautogui
from PIL import Image, ImageDraw

pyautogui.press('win')
pyautogui.write('그림판')
pyautogui.press('enter')

pyautogui.sleep(1)

pyautogui.alert("도형을 그린 후 확인 버튼을 눌러주세요.")
screenshot = pyautogui.screenshot()

screenshot.save("screenshot.png")

image = Image.open("screenshot.png")

selected_shape = (100, 100, 200, 200)

draw = ImageDraw.Draw(image)
draw.rectangle(selected_shape, fill="white")  

image.save("filled_screenshot.png")

image.show()

from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=line_width.get())

def clear_paint():
    canvas.delete("all")

def choose_color():
    global color
    color = askcolor(color=color)[1]

def draw_rectangle():
    global start_x, start_y, rectangle
    start_x, start_y = None, None
    rectangle = None

    def on_button_press(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y

    def on_move_press(event):
        global rectangle
        if rectangle:
            canvas.delete(rectangle)
        end_x, end_y = event.x, event.y
        rectangle = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=color, width=line_width.get())

    def on_button_release(event):
        global rectangle
        rectangle = None

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

def clear_inside_rectangle():
    global start_x, start_y, fill_rect
    start_x, start_y = None, None
    fill_rect = None

    def on_button_press(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y

    def on_move_press(event):
        global fill_rect
        if fill_rect:
            canvas.delete(fill_rect)
        end_x, end_y = event.x, event.y
        fill_rect = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="", fill="white")

    def on_button_release(event):
        global fill_rect
        fill_rect = None
        clear_area(start_x, start_y, event.x, event.y)

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

def clear_area(x1, y1, x2, y2):
    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="white")

color = "black"

window = Tk()
canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)

canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="All Clear", command=clear_paint)
button_delete.pack()

button_color = Button(window, text="Choose Color", command=choose_color)
button_color.pack()

line_width = Scale(window, from_=1, to=10, orient=HORIZONTAL)
line_width.pack()

button_rectangle = Button(window, text="Draw Rectangle", command=draw_rectangle)
button_rectangle.pack()

button_clear_inside = Button(window, text="Clear Inside Rectangle", command=clear_inside_rectangle)
button_clear_inside.pack()

window.mainloop()

import tkinter as tk
from tkinter.colorchooser import askcolor

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        
        self.pen_color = 'black'
        self.eraser_on = False
        
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)
        
        self.color_button = tk.Button(self.button_frame, text='색 변경', command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        
        self.eraser_button = tk.Button(self.button_frame, text='지우개', command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)
        
        self.pen_button = tk.Button(self.button_frame, text='펜', command=self.use_pen)
        self.pen_button.pack(side=tk.LEFT)
        
        self.canvas.bind('<B1-Motion>', self.paint)
        self.root.bind('<z>', self.undo)
        
        self.undo_stack = []

    def choose_color(self):
        color = askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.eraser_on = False
    
    def use_eraser(self):
        self.eraser_on = True
    
    def use_pen(self):
        self.eraser_on = False
    
    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.pen_color
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        item = self.canvas.create_oval(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
        self.undo_stack.append(item)
    
    def undo(self, event=None):
        if self.undo_stack:
            last_item = self.undo_stack.pop()
            self.canvas.delete(last_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

import tkinter as tk
from tkinter.colorchooser import askcolor

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        
        self.pen_color = 'black'
        self.eraser_on = False
        self.shape_mode = None
        
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill=tk.X)
        
        self.color_button = tk.Button(self.button_frame, text='색 변경', command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        
        self.eraser_button = tk.Button(self.button_frame, text='지우개', command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)
        
        self.pen_button = tk.Button(self.button_frame, text='펜', command=self.use_pen)
        self.pen_button.pack(side=tk.LEFT)
        
        self.clear_button = tk.Button(self.button_frame, text='All Clear', command=self.clear_paint)
        self.clear_button.pack(side=tk.LEFT)
        
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-1>', self.start_draw_shape)
        self.root.bind('<Key>', self.set_shape_mode)
        self.root.bind('<z>', self.undo)
        
        self.undo_stack = []
        self.start_x, self.start_y = None, None

    def choose_color(self):
        color = askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.eraser_on = False
    
    def use_eraser(self):
        self.eraser_on = True
        self.shape_mode = None
    
    def use_pen(self):
        self.eraser_on = False
        self.shape_mode = None
    
    def paint(self, event):
        if self.shape_mode:
            return
        
        paint_color = 'white' if self.eraser_on else self.pen_color
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        item = self.canvas.create_oval(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
        self.undo_stack.append(item)
    
    def start_draw_shape(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.canvas.bind('<ButtonRelease-1>', self.draw_shape)
    
    def draw_shape(self, event):
        if not self.shape_mode:
            return
        
        end_x, end_y = event.x, event.y
        paint_color = self.pen_color
        if self.shape_mode == 'rectangle':
            item = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline=paint_color)
        elif self.shape_mode == 'circle':
            x1, y1 = self.start_x, self.start_y
            x2, y2 = end_x, end_y
            r = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            item = self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, outline=paint_color)
        
        self.undo_stack.append(item)
        self.canvas.unbind('<ButtonRelease-1>')
    
    def set_shape_mode(self, event):
        if event.char.lower() == 's':
            self.shape_mode = 'rectangle'
        elif event.char.lower() == 'c':
            self.shape_mode = 'circle'
        else:
            self.shape_mode = None
    
    def clear_paint(self):
        self.canvas.delete("all")
    
    def undo(self, event=None):
        if self.undo_stack:
            last_item = self.undo_stack.pop()
            self.canvas.delete(last_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

import subprocess
import time

def run_ms_paint():
    try:
        subprocess.Popen(['mspaint'])
    except FileNotFoundError:
        print("그림판이 설치되어 있지 않습니다.")

if __name__ == "__main__":
    start_time = time.time()
    
    # 그림판 실행
    run_ms_paint()
    
    input("그림판을 종료하고 Enter를 누르세요.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("그림판 사용 시간:", elapsed_time, "초")

import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")

        self.canvas_width = 800
        self.canvas_height = 600
        self.default_color = "black"
        self.default_thickness = 5

        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.color = self.default_color
        self.thickness = self.default_thickness
        self.old_x, self.old_y = None, None

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Button-3>", self.erase)

        self.choose_color_button = tk.Button(root, text="색상 선택", command=self.choose_color)
        self.choose_color_button.pack(side=tk.LEFT)

        self.thickness_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="선 굵기", command=self.change_thickness)
        self.thickness_scale.pack(side=tk.LEFT)
        self.thickness_scale.set(self.default_thickness)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="색상 선택")
        if color_code[1] is not None:
            self.color = color_code[1]

    def change_thickness(self, value):
        self.thickness = int(value)

    def paint(self, event):
        if self.old_x and self.old_y:
            overlapping_items = self.canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
            if not overlapping_items:
                self.canvas.create_line(
                    self.old_x, self.old_y, event.x, event.y,
                    width=self.thickness, fill=self.color, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=100  # 여기서 splinesteps 값을 늘립니다.
                )
        self.old_x, self.old_y = event.x, event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def erase(self, event):
        overlapping_items = self.canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
        for item in overlapping_items:
            self.canvas.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import Canvas

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        self.canvas = Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.shape_type = "line"  # Default shape type

        self.shapes = []  # List to store shapes

        # Bind events
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Shape selection buttons
        self.btn_line = tk.Button(root, text="Line", command=self.select_line)
        self.btn_line.pack(side="left")
        self.btn_rect = tk.Button(root, text="Rectangle", command=self.select_rect)
        self.btn_rect.pack(side="left")
        self.btn_oval = tk.Button(root, text="Oval", command=self.select_oval)
        self.btn_oval.pack(side="left")

    def select_line(self):
        self.shape_type = "line"

    def select_rect(self):
        self.shape_type = "rectangle"

    def select_oval(self):
        self.shape_type = "oval"

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.shape_type == "line":
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="black")
        elif self.shape_type == "rectangle":
            self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black")
        elif self.shape_type == "oval":
            self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline="black")

    def on_mouse_drag(self, event):
        if self.current_shape:
            if self.shape_type == "line":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.shape_type == "rectangle":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.shape_type == "oval":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.current_shape:
            x1, y1, x2, y2 = self.canvas.coords(self.current_shape)
            for shape in self.shapes:
                if self.check_intersection(x1, y1, x2, y2, shape):
                    self.canvas.delete(self.current_shape)
                    break
            else:
                self.shapes.append(self.canvas.coords(self.current_shape))  # Save the final shape
            self.current_shape = None

    def check_intersection(self, x1, y1, x2, y2, shape_coords):
        # Implement line intersection logic here
        # For simplicity, let's assume shape_coords are in the form of [x3, y3, x4, y4] representing a line
        x3, y3, x4, y4 = shape_coords

        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        A = (x1, y1)
        B = (x2, y2)
        C = (x3, y3)
        D = (x4, y4)
        
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()