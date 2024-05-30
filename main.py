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
    if drawing_mode == "draw":
        x1, y1 = ( event.x-1 ), ( event.y-1 )
        x2, y2 = ( event.x+1 ), ( event.y+1 )
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    if drawing_mode == "erase":
        x1, y1 = ( event.x-8 ), ( event.y-8 )
        x2, y2 = ( event.x+8 ), ( event.y+8 )
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 지우개 모드 활성화
def activate_erase_mode():
    global drawing_mode
    drawing_mode = "erase"

# 기본 그리기 모드 활성화
def activate_draw_mode():
    global drawing_mode
    drawing_mode = "draw"

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

# all clear 버튼 추가
button_delete = Button(button_frame, text="all clear", command=clear_paint)
button_delete.pack(side=LEFT, padx=5, pady=5)

# 그리기 모드 버튼 추가
button_draw = Button(button_frame, text="draw", command=activate_draw_mode)
button_draw.pack(side=LEFT, padx=5, pady=5)

# 지우개 모드 버튼 추가
button_erase = Button(button_frame, text="erase", command=activate_erase_mode)
button_erase.pack(side=LEFT, padx=5, pady=5)

# 동그라미 그리기 모드 추가
button_circle = Button(button_frame, text="draw circle", command=activate_circle_mode)
button_circle.pack()    

window.mainloop()


