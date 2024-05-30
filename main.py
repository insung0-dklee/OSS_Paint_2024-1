"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

색상 선택 기능과 붓 크기 조절 기능 추가
"""

from tkinter import *
from tkinter.colorchooser import askcolor

current_color = "black"
brush_size = 2

def paint(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)

def clear_paint():
    canvas.delete("all")

def set_color():
    global current_color
    color = askcolor(color=current_color)[1]
    if color:
        current_color = color

def set_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

window = Tk()
window.title("Paint Program")

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_frame = Frame(window)
button_frame.pack(fill=X)

clear_button = Button(button_frame, text="Clear", command=clear_paint)
clear_button.pack(side=LEFT)

color_button = Button(button_frame, text="Color", command=set_color)
color_button.pack(side=LEFT)

brush_size_label = Label(button_frame, text="Brush Size:")
brush_size_label.pack(side=LEFT)

brush_size_slider = Scale(button_frame, from_=1, to=10, orient=HORIZONTAL, command=set_brush_size)
brush_size_slider.set(brush_size)
brush_size_slider.pack(side=LEFT)

window.mainloop()
