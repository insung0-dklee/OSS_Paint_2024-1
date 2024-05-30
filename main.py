"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 수평으로 그림 뒤집기 함수
def flip_horizontal():
    # 캔버스에 그려진 모든 아이템 가져오기
    items = canvas.find_all()
    # 각 아이템을 순회하며 좌표를 조정하여 수평으로 뒤집기
    for item in items:
        coords = canvas.coords(item)
        new_coords = [coords[0], coords[1], coords[2], coords[3]]
        new_coords[0] = canvas.winfo_reqwidth() - coords[2]
        new_coords[2] = canvas.winfo_reqwidth() - coords[0]
        canvas.coords(item, *new_coords)

# 수직으로 그림 뒤집기 함수
def flip_vertical():
    # 캔버스에 그려진 모든 아이템 가져오기
    items = canvas.find_all()
    # 각 아이템을 순회하며 좌표를 조정하여 수직으로 뒤집기
    for item in items:
        coords = canvas.coords(item)
        new_coords = [coords[0], coords[1], coords[2], coords[3]]
        new_coords[1] = canvas.winfo_reqheight() - coords[3]
        new_coords[3] = canvas.winfo_reqheight() - coords[1]
        canvas.coords(item, *new_coords)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# Clear 버튼 생성
button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

# Flip Horizontal 버튼 생성(좌측에 생성)
button_flip_horizontal = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip_horizontal.pack(side=LEFT)

# Flip Vertical 버튼 생성(우측에 생성)
button_flip_vertical = Button(window, text="Flip Vertical", command=flip_vertical)
button_flip_vertical.pack(side=RIGHT)

window.mainloop()
