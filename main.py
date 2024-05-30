"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter import simpledialog

# 기본 선 두께 설정
default_width = 2

# 그리기 함수
def paint(event):
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", width=current_width)

# 선 두께 선택 함수
def select_width():
    global current_width
    current_width = simpledialog.askinteger("선 두께 선택", "선 두께를 입력하세요:", initialvalue=default_width)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# Tkinter 창 생성
window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# 선 두께 선택 버튼
button_width = Button(window, text="선 두께 선택", command=select_width)
button_width.pack(side=LEFT)  # 왼쪽에 배치

# 모두 지우기 버튼
button_clear = Button(window, text="모두 지우기", command=clear_paint)
button_clear.pack(side=TOP)  # 상단에 배치

# 현재 선 두께 설정
current_width = default_width

window.mainloop()