"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

set_paint_mode_normal : 기본 그리기 모드로 전환하는 기능
set_paint_mode_pressure : 감압 브러시 그리기 모드로 전환하는 기능
start_paint_pressure : 감압 브러시 그리기를 시작할 시, 마우스 버튼을 누르기 시작할 때의 시간을 저장하는 기능
paint_pressure : 마우스를 누르고 있는 만큼 점이 점점 굵어지는 원을 이용해 그림을 그리는 기능
start_time : 마우스 버튼을 누르기 시작할 때의 시간을 저장하기 위한 변수
radius : 감압 브러시 모드일때의 원의 반지름
"""

from tkinter import *
import time #시간 계산을 위한 모듈

def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭시작시
    canvas.bind("<B1-Motion>", paint_pressure) #마우스를 클릭중일시 -> 그림을 그리고 있을시

def start_paint_pressure(event):
    global start_time
    start_time = time.time() #마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵가는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def paint(event):
    x1, y1 = ( event.x - 1 ), ( event.y - 1 )
    x2, y2 = ( event.x + 1 ), ( event.y + 1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()

button_paint = Button(window, text="normal", command=set_paint_mode_normal) #기본 그리기 모드로 전환하는 기능
button_paint.pack()

button_paint = Button(window, text="pressure", command=set_paint_mode_pressure) #감압 브러시 그리기 모드로 전환하는 기능
button_paint.pack()

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

set_paint_mode_normal() # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
