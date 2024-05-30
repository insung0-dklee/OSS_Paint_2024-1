"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
color_buttons : 펜의 색상을 결정하는 버튼들 색상 리스트 크기만큼 버튼이 추가됨.
colors: 펜 색상 리스트. 여기서 색상을 추가하면 버튼으로 반영됨.
"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

colors = ["red", "green", "blue", "black", "orange", "pink"]

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

def change_color(select):
    global color
    color = select

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

color_buttons = []
for color in colors:
    color_buttons.append(Button(window, text=color.capitalize(), bg=color, command=lambda c=color: change_color(c)))
    color_buttons[-1].pack(side=LEFT)

window.mainloop()
