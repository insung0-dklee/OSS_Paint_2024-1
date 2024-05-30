"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

"""
 @변수추가
    last_x : 이전에 그렸던 선의 끝점, x좌표
    last_y : 이전에 그렸던 선의 끝점, y좌표
    x : 이벤트(마우스 클릭)이 일어난 위치, x좌표
    y : 이벤트(마우스 클릭)이 일어난 위치, y좌표

 @수정사항
    원을 그리는 create_oval() 메소드에서 선을 그리는 create_line() 메소드로 변경
    create_oval()에서 create_line()으로 변경함에 따라, 매개 변수 변경
    기존 원의 바깥선에 해당하는 매개변수 outline 제거
    선의 두께를 설정하는 매개변수 width 추가

 @함수추가
    reset : 그림을 그리는 동안 마지막으로 사용된 좌표값을 초기화하는 함수
    last_x, last_y에 None을 할당하여 클릭이 끝나면 새로운 선을 그리기 위해 이전 좌표값을 초기화
"""
def paint(event):
    global last_x, last_y
    x, y = event.x, event.y
    if last_x is not None and last_y is not None:
        canvas.create_line(last_x, last_y, x, y, fill="black", width=2)
    last_x, last_y = x, y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
"""
 bg : 그림판은 배경 색 추가
 width : 그림판 윈도우의 넓이 추가
 height : 그림판 윈도우의 높이 추가
"""
canvas = Canvas(window, bg="white", width=800, height=600)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset)


button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 마우스 좌표 값을 초기화
last_x, last_y = None, None

window.mainloop()
