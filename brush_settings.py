from tkinter.colorchooser import askcolor
import time
import random
import math

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y
brush_size = 1
brush_color = "black"
brush_mode = "solid"
last_x, last_y = None, None

# 브러시 크기 변경
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# 배경 색상 변경
def change_bg_color(canvas):
    bg_color = askcolor()
    if bg_color[1]:
        canvas.config(bg=bg_color[1])

# 브러시 색상 변경
def change_brush_color():
    global brush_color
    color = askcolor()
    if color[1]:
        brush_color = color[1]

# 브러시 모드 설정
def set_brush_mode(canvas, mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))

# 일반 그리기 모드 설정
def set_paint_mode_normal(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))

# 압력 그리기 모드 설정
def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

# 압력 페인팅 시작
def start_paint_pressure(event, canvas):
    global start_time
    start_time = time.time()

# 압력 페인팅
def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

# 페인팅 시작
def paint_start(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

# 페인팅
def paint(event, canvas):
    global last_x, last_y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, event.x, event.y, fill=brush_color, width=brush_size, capstyle=ROUND, smooth=TRUE)
    last_x, last_y = event.x, event.y

# 점선 페인팅
def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = brush_size
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill=brush_color, outline=brush_color)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y
        canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)
