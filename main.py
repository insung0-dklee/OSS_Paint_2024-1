"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
set_color_blue: 그림을 파란색으로 그리게하는 기능
set_color_black: 그림을 검은색으로 그리게하는 기능
button_blue : set_color_blue의 버튼
button_black : set_color_black()의 버튼

"""

from tkinter import *

current_color = "black"

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

def set_color_blue():
    global current_color
    current_color = "blue"

def set_color_black():
    global current_color
    current_color = "black"

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_blue = Button(window, text="Blue", command=set_color_blue)
button_blue.pack()

button_black = Button(window, text="Black", command=set_color_black)
button_black.pack()

window.mainloop()
