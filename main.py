"""
Project : Paint
paint : 선을 이용해 그림을 그리는 기능
paint_start : 왼쪽 마우스가 눌렸을때의 마우스 위치를 저장
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint_start(event):
    global x1, y1
    x1, y1 = event.x, event.y


def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    x1, y1 = x2, y2

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
