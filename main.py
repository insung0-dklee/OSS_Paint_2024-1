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

#(100,100)좌표에 원을 그리는 함수
#radius가 98을 넘을시 원이 canvas의 크기를 넘게 된다.
def circle_radius():
    def draw_circle():
        radius = int(radius_Entry.get())
        Draw_Circle(canvas, 100, 100, radius)
    lab_Circle = Label(window, text="Radius(0<radius<98) = "
    lab_Circle.grid(row=1, column=2)
    radius_Entry = Entry(bg='white', width=8)
    radius_Entry.grid(row=1, column=3)
    button_confirm = Button(window, text="Confirm", command=draw_circle)
    button_confirm.grid(row=1, column=4)

def Draw_Circle(canvas, x, y, r):
    canvas.create_oval(x-r, y-r, x+r, y+r)

window = Tk()
canvas = Canvas(window)
canvas.grid(row=2, column=0)
canvas.bind("<B1-Motion>", paint)
button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.grid(row=0, column=1)
button_oval = Button(window, text="Draw Oval", command=circle_radius)
button_oval.grid(row=1, column=1)

window.mainloop()