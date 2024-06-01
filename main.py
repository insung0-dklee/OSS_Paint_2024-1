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
