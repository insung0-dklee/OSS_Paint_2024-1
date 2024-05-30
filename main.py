from tkinter import *

def paint(event):
    x1, y1 = (event.x - brush_size.get() // 2), (event.y - brush_size.get() // 2)
    x2, y2 = (event.x + brush_size.get() // 2), (event.y + brush_size.get() // 2)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

window = Tk()

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)

brush_size = Scale(window, from_=1, to=20, orient=HORIZONTAL, label="Brush Size") 
brush_size.set(5)  
brush_size.pack() 

'''
scale      : 변수 1~20까지 조정
set         : 기본값
pack        : 크기를 조정하는 툴바

'''