"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
askcolor: 사용자가 색상을 선택하는 기능
choose_color: 사용자가 선택한 색상을 current_color 변수에 저장하는 기능
color_button: choose_color의 버튼

"""

from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill=current_color.get(), outline=current_color.get())  

def clear_paint():
    canvas.delete("all")

def choose_color(): 
    color = askcolor()[1] 
    if color:  
        current_color.set(color) 

window = Tk()
current_color = StringVar() 
current_color.set("black") 

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True) 
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

color_button = Button(window, text="색 선택", command=choose_color)
color_button.pack(side=BOTTOM)
window.mainloop()