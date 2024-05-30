"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
rotation_angle : 현재 회전 각도를 저장
rotate_point : 포인트를 주어진 각도로 회전시키는 기능
rotate_canvas : 모든 그림을 주어진 각도로 회전시키는 기능
button_rotate : rotate_canvas의 버튼

"""

from tkinter import *
import math

rotation_angle = 0

def paint(event):
    x, y = rotate_point(event.x, event.y, canvas.winfo_width()/2, canvas.winfo_height()/2, rotation_angle)
    x1, y1 = (x - 1), (y - 1)
    x2, y2 = (x + 1), (y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def rotate_point(x, y, cx, cy, angle):
    radians = math.radians(angle)
    dx, dy = x - cx, y - cy
    new_x = cx + dx * math.cos(radians) - dy * math.sin(radians)
    new_y = cy + dx * math.sin(radians) + dy * math.cos(radians)
    return new_x, new_y

def rotate_canvas(angle):
    global rotation_angle
    rotation_angle += angle
    items = canvas.find_all()
    for item in items:
        coords = canvas.coords(item)
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            x1, y1 = rotate_point(x1, y1, canvas.winfo_width()/2, canvas.winfo_height()/2, angle)
            x2, y2 = rotate_point(x2, y2, canvas.winfo_width()/2, canvas.winfo_height()/2, angle)
            canvas.coords(item, x1, y1, x2, y2)

window = Tk()
canvas = Canvas(window, background="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_clear = Button(window, text="all clear", command=clear_paint)
button_clear.pack(side=LEFT)

button_rotate = Button(window, text="rotate 90°", command=lambda: rotate_canvas(90))
button_rotate.pack(side=LEFT)

window.mainloop()

