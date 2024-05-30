"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from PIL import ImageGrab #pip install Pillow필요

def paint(event):
    global selected_color
    x1, y1 = (event.x-1), (event.y-1)
    x2, y2 = (event.x+1), (event.y+1)
    canvas.create_oval(x1, y1, x2, y2, fill=selected_color, outline=selected_color)#원본 검정에서 선택된 색으로 칠하도록 변경

def clear_paint():
    canvas.delete("all")

def activate_dropper():
    canvas.bind("<Button-1>", get_pixel_color)

def get_pixel_color(event):
    global selected_color
    x, y = canvas.winfo_rootx() + event.x, canvas.winfo_rooty() + event.y
    image = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    selected_color = "#" + "".join([f"{i:02x}" for i in image.getpixel((0, 0))])  # RGB를 hex 코드로 변환
    canvas.bind("<Button-1>", lambda event: None)  # 스포이드 모드 비활성화
    canvas.bind("<B1-Motion>", paint)  # 다시 그리기 모드로 전환

window = Tk()
selected_color = "#000000" # 초기 색상은 검정색

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack(side=LEFT)

dropper_button = Button(window, text="dropper", command=activate_dropper)
dropper_button.pack(side=RIGHT)

window.mainloop()
