"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = ( event.x - brush_size // 2 ), ( event.y - brush_size // 2 )
    x2, y2 = ( event.x + brush_size // 2 ), ( event.y + brush_size // 2 )
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 색상 선택 함수
def choose_color():
    global color
    # 색상 선택 대화 상자를 띄우기
    color = askcolor(color=color)[1]

# 메인 윈도우 생성
window = Tk()
window.title("그림판")

# 기본 색상과 브러시 크기 설정
color = "black"
brush_size = 5

# 캔버스 생성
canvas = Canvas(window, bg="white", width=800, height=600)
canvas.pack()

# 그리기 함수 바인딩
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 색상 선택 버튼 추가
color_button = Button(window, text="색상 선택", command=choose_color)
color_button.pack(side=LEFT)

# 메인 루프 실행
window.mainloop()
