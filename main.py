"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

set_paint_mode_airbrush : 에어브러쉬 그리기 모드로 전환하는 기능
paint_airbrush : 마우스를 누르고 있는 만큼 점이 점점 굵어지는 원을 이용해 그림을 그리는 기능
dot_count : 에어브러쉬의 원의 개수를 저장하기 위한 변수
dot_size : 에어브러쉬의 원의 크기를 저장하기 위한 변수
dot_distance : 에어브러쉬의 원들 간의 거리를 저장하기 위한 변수
"""

from tkinter import *
import time #시간 계산을 위한 모듈
import random #random 모듈
import math #math 모듈

def paint_airbrush(event):
    for _ in range(dot_count.get()):  # 에어브러쉬 효과를 위해 여러 개의 작은 점을 그림
        radius = random.randint(1, dot_size.get())  # 점의 크기를 무작위로 선택
        angle = random.uniform(0, 2 * math.pi)  # 점의 방향을 무작위로 선택
        distance = random.uniform(0, dot_distance.get())  # 점의 거리를 무작위로 선택
        x = event.x + distance * math.cos(angle)
        y = event.y + distance * math.sin(angle)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black", outline="black")

# 에어브러쉬 속성을 조정하는 함수
def increase_dot_count():
    dot_count.set(dot_count.get() + 1)

def decrease_dot_count():
    dot_count.set(max(dot_count.get() - 1, 1))  # 최소값 1 설정

def increase_dot_size():
    dot_size.set(dot_size.get() + 1)

def decrease_dot_size():
    dot_size.set(max(dot_size.get() - 1, 1))  # 최소값 1 설정

def increase_dot_distance():
    dot_distance.set(dot_distance.get() + 1)

def decrease_dot_distance():
    dot_distance.set(max(dot_distance.get() - 1, 0))  # 최소값 0 설정

def set_paint_mode_normal(): #기본 그리기 모드로 전환하는 기능 
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_airbrush(): #에어브러쉬 그리기 모드로 전환하는 기능
    canvas.bind("<B1-Motion>", paint_airbrush)

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

button_paint = Button(window, text="airbrush", command=set_paint_mode_airbrush) #에어브러쉬 그리기 모드로 전환하는 기능
button_paint.pack()

# 에어브러쉬 속성 변수 생성
dot_count = IntVar()
dot_count.set(10)

dot_size = IntVar()
dot_size.set(2)

dot_distance = IntVar()
dot_distance.set(10)

# 버튼 프레임 생성
frame_size = Frame(window)
frame_size.pack()

frame_distance = Frame(window)
frame_distance.pack()

frame_count = Frame(window)
frame_count.pack()

# 에어브러쉬 속성 조절 버튼 추가
Button(frame_size, text="+", command=increase_dot_size).pack(side=LEFT)
Label(frame_size, text="Size").pack(side=LEFT)
Label(frame_size, textvariable=dot_size).pack(side=LEFT)  # 사이즈 표시
Button(frame_size, text="-", command=decrease_dot_size).pack(side=LEFT)

Button(frame_distance, text="+", command=increase_dot_distance).pack(side=LEFT)
Label(frame_distance, text="Distance").pack(side=LEFT)
Label(frame_distance, textvariable=dot_distance).pack(side=LEFT)  # 거리 표시
Button(frame_distance, text="-", command=decrease_dot_distance).pack(side=LEFT)

Button(frame_count, text="+", command=increase_dot_count).pack(side=LEFT)
Label(frame_count, text="Count").pack(side=LEFT)
Label(frame_count, textvariable=dot_count).pack(side=LEFT)  # 개수 표시
Button(frame_count, text="-", command=decrease_dot_count).pack(side=LEFT)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

set_paint_mode_normal() # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
