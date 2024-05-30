"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter import simpledialog # 사용자로부터 입력을 받아오기 위해 simpledialog 모듈을 가져옴

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

"""

좌상단 점의 좌표와 우하단 점의 좌표를 기준으로 직사각형을 그렸을 때 그 사각형 안에 들어갈 원을 그리는 함수
사용자로부터 x1, y1, x2, y2, color를 입력받아 그림
x1 : 좌상단 점의 x의 좌표
y1 : 좌상단 점의 y의 좌표
x2 : 우하단 점의 x의 좌표
y2 : 우하단 점의 y의 좌표
fill=color : 원의 색 지정, 별도의 지정이 없을 시 투명

"""
def draw_circle(x1, y1, x2, y2, color):
    canvas.create_oval(x1, y1, x2, y2,fill=color)

"""
사용자에게 도형의 위치, 크기를 정하는 점의 좌표를 묻고 그에 따라 원을 생성하는 함수
simpledialog.askinteger : 사용자에게 int형 값을 묻는 대화 상자를 생성
if ~ is None : 사용자가 입력을 그만 둘 경우 대화 상자 중지 
"""


def user_input_circle():
    x1 = simpledialog.askinteger("크기 및 위치", "도형의 왼쪽 상단 x좌표를 입력하세요:")
    if x1 is None:
        return
    y1 = simpledialog.askinteger("크기 및 위치", "도형의 왼쪽 상단 y좌표를 입력하세요:")
    if y1 is None:
        return
    x2 = simpledialog.askinteger("크기 및 위치", "도형의 오른쪽 하단 x좌표를 입력하세요:")
    if x2 is None:
        return
    y2 = simpledialog.askinteger("크기 및 위치", "도형의 오른쪽 하단 y좌표를 입력하세요:")
    if y2 is None:
        return
    color = simpledialog.askstring("색 선택", "도형의 색을 입력하세요:")
    if color is None:
        return
    draw_circle(x1,y1,x2,y2,color)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_draw_circle = Button(window, text="circle", command=user_input_circle)
button_draw_circle.pack(side="left")


window.mainloop()
