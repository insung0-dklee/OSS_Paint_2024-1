"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
"""

from tkinter import *
from zoom import zoom

def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 확대 축소 기능
def zoom_in(event=None):
    zoom(canvas, 1)

def zoom_out(event=None):
    zoom(canvas, -1)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 확대 Button : event->zoom_in
btn_zoom_in = Button(window, text="확대", command=zoom_in)
btn_zoom_in.pack(side=LEFT)

# 축소 버튼 : event->zoom_out
btn_zoom_out = Button(window, text="축소", command=zoom_out)
btn_zoom_out.pack(side=LEFT)



window.mainloop()
