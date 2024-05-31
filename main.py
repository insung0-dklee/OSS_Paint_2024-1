"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time  # 시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
brush_size = 1  # 초기 브러시 크기
brush_color = "black"  # 초기 브러시 색상

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal(canvas):
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭시작시
    canvas.bind("<B1-Motion>", paint_pressure) #마우스를 클릭중일시 -> 그림을 그리고 있을시

def start_paint_pressure(event):
    global start_time
    start_time = time.time() #마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵기는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    event.widget.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    event.widget.create_line(x1, y1, x2, y2, fill=brush_color, width=2)
    x1, y1 = x2, y2

"""
dotted_paint: 점선 브러쉬 함수
이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
"""
def dotted_paint(event): # 점선 브러쉬 함수
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            event.widget.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(mode, canvas): # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid": # 브러쉬 모드가 solid면 
        canvas.bind("<B1-Motion>", paint) # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted": # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", dotted_paint) # 점선 브러쉬로 변경

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

#all clear 기능 추가
def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None # 마지막 좌표 초기화

def add_text(event):# 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.
    text = event.widget.text_box.get()
    event.widget.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

def toggle_fullscreen(event):
    window = event.widget.winfo_toplevel()
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

# 좌우 반전 기능 추가
def flip_horizontal(canvas):
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
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

# 새 창 열기 생성
def create_new_window():
    new_window = Toplevel(window)  # 새 창을 생성
    setup_canvas(new_window)  # 새 창에 그림판 설정


"""
setup_canvas : 주 윈도우 및 새 창의 캔버스를 설정하는 함수
 새 창 열기 시 아무 기능도 사용할 수 없었던 문제 해결
"""
def setup_canvas(parent):
    global canvas;
    canvas = Canvas(parent, bg="white")  # 캔버스를 생성하여 주 윈도우 또는 새 창에 추가
    canvas.pack(fill="both", expand=True)
    
    button_frame = Frame(parent)  # 버튼 프레임을 생성하여 주 윈도우 또는 새 창에 추가
    button_frame.pack(fill=X)

    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.pack(side=LEFT)

    # 펜 굵기를 조절할 수 있는 슬라이더 추가
    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)  # 슬라이더 초기값 설정
    brush_size_slider.pack(side=LEFT)

    button_solid = Button(parent, text="Solid Brush", command=lambda: set_brush_mode("solid", canvas))  # 버튼을 누르면 실선 모드로 변경
    button_solid.pack()  # 실선 브러쉬 버튼을 주 윈도우 또는 새 창에 배치

    button_dotted = Button(parent, text="Dotted Brush", command=lambda: set_brush_mode("dotted", canvas))  # 버튼을 누르면 점선 모드로 변경
    button_dotted.pack()  # 점선 브러쉬 버튼을 주 윈도우 또는 새 창에 배치

    button_paint_normal = Button(parent, text="normal", command=lambda: set_paint_mode_normal(canvas))  # 기본 그리기 모드로 전환하는 기능
    button_paint_normal.pack(side=RIGHT)

    button_paint_pressure = Button(parent, text="pressure", command=lambda: set_paint_mode_pressure(canvas))  # 감압 브러시 그리기 모드로 전환하는 기능
    button_paint_pressure.pack(side=RIGHT)

    text_box = Entry(parent)  # 텍스트를 입력할 공간을 생성합니다.
    text_box.pack(side=LEFT)
    canvas.text_box = text_box  # 캔버스에 텍스트 박스 참조 추가

    button_new_window = Button(parent, text="새 창 열기", command=create_new_window)  # "새 창 열기" 버튼 생성
    button_new_window.pack(side=LEFT)  # "새 창 열기" 버튼을 주 윈도우 또는 새 창에 배치

    button_flip = Button(parent, text="Flip Horizontal", command=lambda: flip_horizontal(canvas))  # 좌우 반전 버튼 생성
    button_flip.pack(side=LEFT)

    button_bg_color = Button(parent, text="Change Background Color", command=lambda: change_bg_color(canvas))  # 배경색 변경 버튼 생성
    button_bg_color.pack(side=LEFT)

    button_brush_color = Button(parent, text="Change Brush Color", command=change_brush_color)  # 브러시 색상 변경 버튼 생성
    button_brush_color.pack(side=LEFT)

    # 마우스 이벤트 바인딩
    canvas.bind("<Button-1>", paint_start)  # 왼쪽 버튼 클릭 시 그림 시작 위치 저장
    canvas.bind("<B1-Motion>", paint)  # 왼쪽 버튼 드래그 시 그림 그리기
    canvas.bind("<Button-3>", add_text)  # 오른쪽 버튼 클릭 시 텍스트 추가
    canvas.bind("<B3-Motion>", erase)  # 오른쪽 버튼 드래그 시 지우개 기능
    parent.bind("<F11>", toggle_fullscreen)  # F11 키를 누르면 전체 화면 토글

    set_paint_mode_normal(canvas)  # 기본적으로 normal 모드로 설정

window = Tk()
window.title("그림판")
window.geometry("640x400+200+200")
window.resizable(True, True)

setup_canvas(window)  # 주 윈도우에 그림판 설정

window.mainloop()
