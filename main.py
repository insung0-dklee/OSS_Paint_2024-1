"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
button_circle : 마우스로 드래그하여 동그라미를 그리는 버튼

"""

from tkinter import *

drawing_mode = None
start_x, start_y = None, None

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")
    
    
def draw_circle():
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x1, y1 = (width // 2 - 50), (height // 2 - 50)
    x2, y2 = (width // 2 + 50), (height // 2 + 50)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")


# 마우스로 드래그하여 동그라미 그리기 기능
def start_circle(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw_circle(event):
    canvas.delete("preview_circle")
    x1, y1 = start_x, start_y
    x2, y2 = event.x, event.y
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black", tags="preview_circle")

def end_circle(event):
    x1, y1 = start_x, start_y
    x2, y2 = event.x, event.y
    canvas.delete("preview_circle")
    canvas.create_oval(x1, y1, x2, y2, outline="black")

# 동그라미 그리기 모드 활성화
def activate_circle_mode():
    global drawing_mode
    drawing_mode = "circle"
    canvas.bind("<Button-1>", start_circle)
    canvas.bind("<B1-Motion>", draw_circle)
    canvas.bind("<ButtonRelease-1>", end_circle)
  


window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# 버튼 프레임 추가
button_frame = Frame(window)
button_frame.pack(side=TOP, fill=X)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_circle = Button(button_frame, text="draw circle", command=activate_circle_mode)
button_circle.pack()    

window.mainloop()
