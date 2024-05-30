"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    # draw_stack(그린 선들을 저장하는 스택)을 전역 변수로 선연
    global draw_stack
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    oval = canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    # 그린 선의 객체를 스택에 추가.
    draw_stack.append(oval)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 마지막으로 그린 부분 삭제
def undo_action():
    if draw_stack:
        canvas.delete(draw_stack.pop()) # 스택에서 마지막으로 그린 부분을 꺼내어 삭제함

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# 그린 선들을 저장할 스택
draw_stack = []

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# 마지막으로 그린 부분을 삭제해주는 버튼 생성
button_undo = Button(window, text="Undo", command=undo_action)
button_undo.pack()

window.mainloop()
