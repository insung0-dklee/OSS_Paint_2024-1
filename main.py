"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def draw_line(event):
    if not hasattr(draw_line, 'prev_x') or not hasattr(draw_line, 'prev_y'):
        draw_line.prev_x, draw_line.prev_y = event.x, event.y
        return
    canvas.create_line(draw_line.prev_x, draw_line.prev_y, event.x, event.y, fill="black", width=2)
    draw_line.prev_x, draw_line.prev_y = event.x, event.y

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-3>", draw_line) 

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()

