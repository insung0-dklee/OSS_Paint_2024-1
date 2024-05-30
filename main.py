"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

"""
Project : erase
erase : 배경의 색에 맞춰 펜 기능 = 지우기 기능
BackGround : 그림판 배경의 색깔 변수 (초기 배경색 흰색으로 지정)
canvas.config(bg=BackGround) : 그림판 배경의 색깔을 Background 변수에 따라 변경
canvas.bind("<B3-Motion>", erase) : B3-Motion 에 해당된 마우스 우클릭 클릭시 erase 함수를 발동시키는 이밴트 함수
"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#지우기 기능 추가
def erase(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1-5, y1+5, x2+5, y2-5, fill=BackGround, outline=BackGround)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
BackGround="white"
canvas = Canvas(window)
canvas.config(bg=BackGround)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<B3-Motion>", erase)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
