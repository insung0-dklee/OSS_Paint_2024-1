"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time  # 시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화

ruler_visible = False  # 눈금자 초기 상태 (보이지 않음)

# 눈금자를 그리는 함수
def draw_ruler():
    global ruler_visible
    if ruler_visible:
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        for i in range(0, canvas_width, 10):
            canvas.create_line(i, 0, i, 5, fill="gray", tags="ruler")
            if i % 50 == 0:
                canvas.create_line(i, 0, i, 10, fill="gray", tags="ruler")
                canvas.create_text(i + 2, 12, text=str(i), anchor="nw", fill="gray", font=('Arial', 6), tags="ruler")
        for j in range(0, canvas_height, 10):
            canvas.create_line(0, j, 5, j, fill="gray", tags="ruler")
            if j % 50 == 0:
                canvas.create_line(0, j, 10, j, fill="gray", tags="ruler")
                canvas.create_text(12, j + 2, text=str(j), anchor="nw", fill="gray", font=('Arial', 6), tags="ruler")

# 눈금자를 토글하는 함수
def toggle_ruler():
    global ruler_visible
    ruler_visible = not ruler_visible
    canvas.delete("ruler")
    if ruler_visible:
        draw_ruler()
    else:
        ruler_visible = False

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭시작시
    canvas.bind("<B1-Motion>", paint_pressure)  # 마우스를 클릭중일시 -> 그림을 그리고 있을시

def start_paint_pressure(event):
    global start_time
    start_time = time.time()  # 마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵기는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=2)
    x1, y1 = x2, y2

"""
dotted_paint: 점선 브러쉬 함수
이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
"""
def dotted_paint(event):  # 점선 브러쉬 함수
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(mode):  # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":  # 브러쉬 모드가 solid면
        canvas.bind("<B1-Motion>", paint)  # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted":  # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", dotted_paint)  # 점선 브러쉬로 변경

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화
    if ruler_visible:
        draw_ruler()  # 캔버스를 지운 후 다시 눈금자 그리기

def add_text(event):  # 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.
    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

def toggle_fullscreen(event):
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

# 좌우 반전 기능 추가
def flip_horizontal():
    objects = canvas.find_all()
    canvas.update()
    canvas_width = canvas.winfo_width()
    for obj in objects:
        coords = canvas.coords(obj)
        for i in range(len(coords)):
            if i % 2 == 0:  # x 좌표를 반전시킵니다.
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)

def erase(event):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

# 새 창 열기 생성
def create_new_window():
    new_window = Tk()  # 새로운 Tk 인스턴스 생성
    new_canvas = Canvas(new_window)  # 새로운 창에 캔버스 추가
    new_canvas.pack()  # 캔버스가 새로운 창에 배치
    new_window.mainloop()

window = Tk()
# Tk 객체를 생성하여 주 윈도우를 만들기
window.title("그림판")

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")
# Canvas 위젯을 생성하여 주 윈도우에 추가
window.geometry("640x400+200+200")
# 윈도우이름.geometry("너비x높이+x좌표+y좌표")를 이용하여
# 윈도우 창의 너비와 높이, 초기 화면 위치의 x좌표와 y좌표를 설정
window.resizable(True, True)
# 윈도우이름.resizeable(상하, 좌우)을 이용하여
# 윈도우 창의 창 크기 조절 가능 여부를 설정
canvas.pack(fill="both", expand=True)
# 캔버스를 창 너비에 맞춰 동적으로 크기 조절

last_x, last_y = None, None  # 마지막 좌표 초기화
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)
# 캔버스에 마우스 왼쪽 버튼을 누르고 움직일 때마다 paint 함수를 호출하도록 바인딩

button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

# 펜 굵기를 조절할 수 있는 슬라이더 추가
brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
brush_size_slider.set(brush_size)  # 슬라이더 초기값 설정
brush_size_slider.pack(side=LEFT)

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode("solid"))  # 버튼을 누르면 실선 모드로 바꾼다
button_solid.pack()  # 실선 브러쉬 버튼을 윈도우에 배치

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))  # 버튼을 누르면 점선 모드로 바꾼다
button_dotted.pack()  # 점선 브러쉬 버튼을 윈도우에 배치

button_paint = Button(window, text="normal", command=set_paint_mode_normal)  # 기본 그리기 모드로 전환하는 기능
button_paint.pack(side=RIGHT)

button_paint = Button(window, text="pressure", command=set_paint_mode_pressure)  # 감압 브러시 그리기 모드로 전환하는 기능
button_paint.pack(side=RIGHT)

text_box = Entry(window)  # 텍스트를 입력할 공간을 생성합니다.
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", add_text)  # 입력한 텍스트를 오른쪽 클릭으로 텍스트를 찍어냅니다.
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window)  # "새 창 열기"라는 버튼 생성 command: 버튼 클릭 시 create_new_window: 새로운 창을 만듦
button_new_window.pack(side=LEFT)  # "새 창 열기"버튼을 윈도우에 배치

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", erase)

brush_color = "black"

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

# 눈금자 토글 버튼 추가
button_toggle_ruler = Button(window, text="Toggle Ruler", command=toggle_ruler)
button_toggle_ruler.pack(side=LEFT)

set_paint_mode_normal()  # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()

