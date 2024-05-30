"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능. 대칭 모드가 활성화되면 사용자가 한쪽에 그린 것이 자동으로 다른 쪽에 대칭되어 그립니다.
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
symmetry_mode : 대칭 모드의 활성화/비활성화를 제어하는 체크 버튼
"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

    # 대칭 모드 기능 추가 시작
    if symmetry_mode.get():
        canvas_width = canvas.winfo_width()
        sym_x1, sym_y1 = (canvas_width - event.x - 1), (event.y - 1)
        sym_x2, sym_y2 = (canvas_width - event.x + 1), (event.y + 1)
        canvas.create_oval(sym_x1, sym_y1, sym_x2, sym_y2, fill="black", outline="black")
    # 대칭 모드 기능 추가 끝

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# 대칭 모드 체크 버튼 추가 시작
symmetry_mode = BooleanVar()
symmetry_checkbutton = Checkbutton(window, text="Symmetry Mode", variable=symmetry_mode)
symmetry_checkbutton.pack()
# 대칭 모드 체크 버튼 추가 끝

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
