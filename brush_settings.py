import time
from tkinter.colorchooser import askcolor

# 초기화 함수: 전역 변수를 설정한다.
# main_globals: 초기값을 포함하는 딕셔너리
def initialize_globals(main_globals):
    global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1
    brush_size = main_globals['brush_size']  # 브러쉬 크기
    brush_color = main_globals['brush_color']  # 브러쉬 색상
    brush_mode = main_globals['brush_mode']  # 브러쉬 모드 (실선, 점선 등)
    last_x = main_globals['last_x']  # 마지막 마우스 X 좌표
    last_y = main_globals['last_y']  # 마지막 마우스 Y 좌표
    x1 = main_globals['x1']  # 시작 X 좌표
    y1 = main_globals['y1']  # 시작 Y 좌표

# 슬라이더를 통해 펜 굵기를 변경하는 함수
# new_size: 새로운 펜 굵기 값
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)  # 새로운 펜 굵기를 정수로 변환하여 저장

# 배경 색상을 변경하는 함수
# canvas: 색상을 변경할 캔버스 객체
def change_bg_color(canvas):
    bg_color = askcolor()  # 색상 선택 대화상자를 열어 색상 선택
    if bg_color[1]:  # 색상이 선택된 경우에만 변경
        canvas.config(bg=bg_color[1])  # 캔버스 배경 색상 설정

# 브러쉬 색상을 변경하는 함수
def change_brush_color():
    global brush_color
    color = askcolor()[1]  # 색상 선택 대화상자를 열어 색상 선택
    if color:  # 색상이 선택된 경우에만 변경
        brush_color = color  # 브러쉬 색상 설정

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
canvas: 브러쉬 모드를 설정할 캔버스 객체
"""
def set_brush_mode(canvas, mode):
    global brush_mode
    brush_mode = mode  # 브러쉬 모드 설정
    if brush_mode == "solid":
        # 실선 브러쉬 모드: 마우스 이동 시 paint 함수 호출
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        # 점선 브러쉬 모드: 마우스 이동 시 dotted_paint 함수 호출
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))

# 일반 페인트 모드 설정 함수
# canvas: 페인트 모드를 설정할 캔버스 객체
def set_paint_mode_normal(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))  # 마우스 이동 시 paint 함수 호출

# 압력 기반 페인트 모드 설정 함수
# canvas: 페인트 모드를 설정할 캔버스 객체
def set_paint_mode_pressure(canvas):
    # 마우스 버튼 클릭 시 start_paint_pressure 함수 호출
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event))
    # 마우스 이동 시 paint_pressure 함수 호출
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

# 압력 기반 페인트 시작 함수
# event: 마우스 이벤트 객체
def start_paint_pressure(event):
    global start_time
    start_time = time.time()  # 현재 시간 저장 (페인트 시작 시간)

# 압력 기반 페인트 함수
# event: 마우스 이벤트 객체
# canvas: 페인트할 캔버스 객체
def paint_pressure(event, canvas):
    global start_time, brush_color
    elapsed_time = time.time() - start_time  # 페인트 시작 후 경과 시간 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 경과 시간에 따라 원의 반지름 결정
    x1, y1 = (event.x - radius), (event.y - radius)  # 원의 좌상단 좌표
    x2, y2 = (event.x + radius), (event.y + radius)  # 원의 우하단 좌표
    # 캔버스에 원 그리기
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

# 마우스 눌림 시작 시 좌표 설정 함수
# event: 마우스 이벤트 객체
# canvas: 페인트할 캔버스 객체
def paint_start(event, canvas):
    global x1, y1, brush_size
    x1, y1 = (event.x, event.y)  # 시작 좌표 설정

# 일반 페인트 함수
# event: 마우스 이벤트 객체
# canvas: 페인트할 캔버스 객체
def paint(event, canvas):
    global x1, y1, brush_size, brush_color
    x2, y2 = event.x, event.y  # 현재 좌표
    # 시작 좌표와 현재 좌표를 연결하는 선 그리기
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    x1, y1 = x2, y2  # 현재 좌표를 다음 시작 좌표로 설정

"""
dotted_paint: 점선 브러쉬 함수
이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
canvas: 점선 브러쉬로 페인트할 캔버스 객체
"""
def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = 10  # 점선 간격
    if last_x is not None and last_y is not None:
        dx = event.x - last_x  # X 좌표 차이
        dy = event.y - last_y  # Y 좌표 차이
        distance = (dx ** 2 + dy ** 2) ** 0.5  # 두 점 사이의 거리 계산
        if distance >= spacing:
            # 현재 좌표에 작은 원 그리기
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
            last_x, last_y = event.x, event.y  # 현재 좌표를 마지막 좌표로 설정
    else:
        last_x, last_y = event.x, event.y  # 첫 번째 점 설정
