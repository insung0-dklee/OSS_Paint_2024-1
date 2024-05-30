"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 그림을 확대하는 함수
def zoom(event):
    scale_factor = 1.1  # 확대 비율
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.scale("all", x, y, scale_factor, scale_factor)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 마우스 휠 이벤트에 확대 함수 바인딩
canvas.bind("<MouseWheel>", zoom)

window.mainloop()