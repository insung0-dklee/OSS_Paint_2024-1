"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
# 색상 선택 대화 상자를 사용하기 위해 tkinter 모듈에서 colorchooser 모듈을 가져옴
from tkinter import colorchooser

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    # 사용자가 선택한 색상으로 선 색상 변경
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 선의 색상을 선택하는 기능 구현
def choose_color():
    color = colorchooser.askcolor()[1]  # askcolor() 함수로 색상 선택 대화상자를 열어 선택한 색상을 가져옴
    return color

# 선택한 색깔로 선의 색상을 설정함
def set_color():
    global current_color
    current_color = choose_color()

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# 기본 색상을 검은색으로 설정
current_color = "black"

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 색을 선택할 수 있도록 하는 버튼 생성 
button_color = Button(window, text="Choose Color", command=set_color)
button_color.pack()

window.mainloop()