"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

def clear_paint():
    canvas.delete("all")

def choose_color():
    global color
    color = askcolor(color=color)[1]

window = Tk()

color = "black"

canvas = Canvas(window)
canvas.pack()

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_color = Button(window, text="Choose Color", command=choose_color)
button_color.pack()

canvas.bind("<B1-Motion>", paint)

window.mainloop()