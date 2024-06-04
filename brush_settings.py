import time
from tkinter.colorchooser import askcolor

def initialize_globals(main_globals):
    global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1
    brush_size = main_globals['brush_size']
    brush_color = main_globals['brush_color']
    brush_mode = main_globals['brush_mode']
    last_x = main_globals['last_x']
    last_y = main_globals['last_y']
    x1 = main_globals['x1']
    y1 = main_globals['y1']

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def change_bg_color(canvas):
    bg_color = askcolor()
    if bg_color[1]:  # 색상이 선택된 경우에만 변경
        canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    color = askcolor()[1]
    if color:  # 색상이 선택된 경우에만 변경
        brush_color = color

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(canvas, mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))

def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event):
    global start_time
    start_time = time.time()

def paint_pressure(event, canvas):
    global start_time, brush_color
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event, canvas):
    global x1, y1, brush_size
    x1, y1 = (event.x, event.y)

def paint(event, canvas):
    global x1, y1, brush_size, brush_color
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    x1, y1 = x2, y2

"""
dotted_paint: 점선 브러쉬 함수
이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
"""
def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = 10
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y


