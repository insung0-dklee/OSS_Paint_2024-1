import time
from tkinter.colorchooser import askcolor

def initialize_globals(main_globals):
    """
    initialize_globals: 전역 변수를 초기화하는 함수
    매개변수: main_globals - 초기값을 포함하는 딕셔너리
    """
    global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, start_time
    brush_size = main_globals.get('brush_size', 5)
    brush_color = main_globals.get('brush_color', 'black')
    brush_mode = main_globals.get('brush_mode', 'solid')
    last_x = main_globals.get('last_x', None)
    last_y = main_globals.get('last_y', None)
    x1 = main_globals.get('x1', None)
    y1 = main_globals.get('y1', None)
    start_time = None

def change_brush_size(new_size):
    """
    change_brush_size: 슬라이더를 통해 펜 굵기를 변경하는 함수
    매개변수: new_size - 새로운 브러쉬 크기
    """
    global brush_size
    brush_size = int(new_size)

def change_bg_color(canvas):
    """
    change_bg_color: 배경색을 변경하는 함수
    매개변수: canvas - 색상을 변경할 캔버스 객체
    """
    bg_color = askcolor()
    if bg_color[1]:  # 색상이 선택된 경우에만 변경
        canvas.config(bg=bg_color[1])

def change_brush_color():
    """
    change_brush_color: 브러쉬 색상을 변경하는 함수
    """
    global brush_color
    color = askcolor()[1]
    if color:  # 색상이 선택된 경우에만 변경
        brush_color = color

def set_brush_mode(canvas, mode):
    """
    set_brush_mode: 브러쉬 모드를 변경하는 함수
    실선 브러쉬와 점선 브러쉬로 전환한다.
    매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
    """
    global brush_mode
    brush_mode = mode
    canvas.unbind("<B1-Motion>")
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))
        canvas.bind("<ButtonRelease-1>", reset_last_position)

def set_paint_mode_normal(canvas):
    """
    set_paint_mode_normal: 마우스 움직임에 따라 도형을 그리는 함수 (기본 모드)
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))

def set_paint_mode_pressure(canvas):
    """
    set_paint_mode_pressure: 압력을 감지하여 도형을 그리는 모드 설정 함수
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
    canvas.unbind("<B1-Motion>")
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event):
    """
    start_paint_pressure: 압력 감지 페인트 모드를 시작하는 함수
    매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
    """
    global start_time
    start_time = time.time()

def paint_pressure(event, canvas):
    """
    paint_pressure: 압력을 감지하여 도형을 그리는 함수
    매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event, canvas):
    """
    paint_start: 페인트 시작 지점을 설정하는 함수
    매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
    global x1, y1, brush_size
    x1, y1 = (event.x, event.y)

def paint(event, canvas):
    """
    paint: 마우스 움직임에 따라 선을 그리는 함수
    매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
    global x1, y1, brush_size, brush_color
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    x1, y1 = x2, y2

def dotted_paint(event, canvas):
    """
    dotted_paint: 점선 브러쉬 함수
    이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
    매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
    매개변수: canvas - 도형을 그릴 캔버스 객체
    """
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

def reset_last_position(event):
    """
    reset_last_position: 마우스를 떼었을 때 점선 브러쉬의 마지막 위치를 초기화하는 함수
    매개변수: event - 마우스 이벤트 객체
    """
    global last_x, last_y
    last_x, last_y = None, None
