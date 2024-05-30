"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
change_bg_color : 캔버스의 배경색을 바꿔주는 기능
button_bg_color : 캔버스의 배경색을 바꿔주게 해주는 버튼

"""


from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def change_bg_color():
    color = askcolor()[1]
    if color:
        canvas.config(bg=color)

window = Tk()
canvas = Canvas(window, bg="white")
canvas.pack(expand=True, fill=BOTH)
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="All Clear", command=clear_paint)
button_delete.pack()

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack()

window.mainloop()
