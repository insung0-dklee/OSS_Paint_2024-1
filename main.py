"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

"""
 fill = 'black' 에서 sel_color 로 변경
"""
def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=sel_color, outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

"""
 펜의 색을 변경하는 함수
 
 @매개변수
    color : 변경하고 싶은 펜의 색상
 
 @변수
    sel_color : 선택된 색상으로 변경
"""
def change_color(color):
    global sel_color
    sel_color = color

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

"""
 color : 기본 색상, 검정색
 
 color_frame : 색상을 변경하기 위한 버튼 구성
 
 colors : 총 7가지 색 구현
 btn : 색상 변경 버튼, 왼쪽부터 차례대로 배치

"""
color = "black"

color_frame = Frame(window)
color_frame.pack()

colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple', 'orange']
for color in colors:
    btn = Button(color_frame, text=color, bg=color, width=2, height=1, command=lambda col=color: change_color(col))
    btn.pack(side=LEFT)

window.mainloop()
