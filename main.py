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

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()

#도형회전기능 추가

def rotate_shapes():
    angle = math.radians(45)  # 45도 회전
    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    objects = canvas.find_all()
    for obj in objects:
        coords = canvas.coords(obj)
        new_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            # 원점 기준 회전
            new_x = center_x + (x - center_x) * math.cos(angle) - (y - center_y) * math.sin(angle)
            new_y = center_y + (x - center_x) * math.sin(angle) + (y - center_y) * math.cos(angle)
            new_coords.extend([new_x, new_y])
        canvas.coords(obj, *new_coords)
