"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
change_line_width : 선의 굵기를 조절하는 기능
button_width_ : change_line_width의 버튼

"""

from tkinter import *



def paint(event):
    x1, y1 = (event.x - line_width/2), (event.y - line_width/2)
    x2, y2 = (event.x + line_width/2), (event.y + line_width/2)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 선 굵기를 조절하는 기능 추가
def change_line_width(delta):
    global line_width
    line_width += delta
    # 선의 굵기가 음수가 되지 않도록 보정
    if line_width < 1:
        line_width = 1

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

line_width = 1  # 초기 선 굵기
button_width_increase = Button(window, text="+", command=lambda: change_line_width(1))
button_width_increase.pack(side=LEFT)
button_width_decrease = Button(window, text="-", command=lambda: change_line_width(-1))
button_width_decrease.pack(side=LEFT)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()



window.mainloop()