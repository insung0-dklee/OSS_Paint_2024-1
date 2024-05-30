"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
erase: 배경색과 같은 원을 이용해 그림을 지우는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
change_bg_color : 배경 색을 변경하는 기능
change_brush_color : 브러쉬 색을 변경하는 기능
button_delete : clear_paint의 버튼
button_bg_color : change_bg_color의 버튼
button_brush_color : change_brush_color의 버튼

"""

from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def erase(event):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    
def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<B3-Motion>", erase)

brush_color = "black"

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack()

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack()

window.mainloop()
