"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
current_color : 현재 선택된 색깔
change_color : 색상을 바꾸는 기능
button_colorchange : change_color의 버튼

"""

from tkinter import *

current_color = "black"

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

def change_color(new_color):
    global current_color
    current_color = new_color

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

colors = ["black", "red", "green", "blue", "yellow", "purple", "orange"]

for color in colors:
    button_colorchange = Button(window, bg=color, width=10, command=lambda c=color: change_color(c))
    button_colorchange.pack(side=LEFT)

window.mainloop()
