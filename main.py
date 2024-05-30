from tkinter import *

def paint(event):
    x1, y1 = (event.x - brush_size.get() // 2), (event.y - brush_size.get() // 2)
    x2, y2 = (event.x + brush_size.get() // 2), (event.y + brush_size.get() // 2)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

window = Tk()

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)

#브러쉬 사이즈 조절 기능 추가
'''

brush_size.set     : 기본값
size.pack           : 툴바
Scale	         : 크기를 결정짓는 변수

'''

brush_size = Scale(window, from_=1, to=20, orient=HORIZONTAL, label="Brush Size") 
brush_size.set(5)  
brush_size.pack() 

#all clear 기능 추가
"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

def clear_paint():
    canvas.delete("all")

canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()