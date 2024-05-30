"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time #시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
selected_area = None  # 선택된 영역을 저장할 변수
selected_coords = [] # 선택된 객체의 좌표를 저장할 리스트

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭시작시
    canvas.bind("<B1-Motion>", paint_pressure) #마우스를 클릭중일시 -> 그림을 그리고 있을시

def start_paint_pressure(event):
    global start_time
    start_time = time.time() #마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵가는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
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
def dotted_paint(event): # 점선 브러쉬 함수
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(mode): # 브러쉬 모드를 변경하는 함수
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
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None # 마지막 좌표 초기화

def add_text(event):# 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.

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
    new_window = Tk()  #새로운 Tk 인스턴스 생성
    new_canvas = Canvas(new_window) # 새로운 창에 캔버스 추가
    new_canvas.pack() #캔버스가 새로운 창에 배치
    new_window.mainloop()

def start_select(event):
    """
    선택 영역을 시작하는 함수
    마우스 클릭 위치를 기준으로 선택 영역을 초기화하고, 
    마우스 드래그 시 영역이 확장되도록 이벤트를 바인딩한다
    """
    global start_x, start_y, selected_area
    start_x, start_y = event.x, event.y
    selected_area = canvas.create_rectangle(start_x, start_y, start_x, start_y, dash=(2, 2), outline="blue") # 선택 영역을 표시하기 위해 점선 사각형 그리기
    canvas.bind("<B1-Motion>", update_select) # 마우스 왼쪽 버튼으로 드래그 시 update_select 함수 호출
    canvas.bind("<ButtonRelease-1>", end_select) # 마우스 왼쪽 버튼 떼면 end_select 함수 호출

def update_select(event):
    """
    선택 영역을 업데이트하는 함수
    마우스 드래그에 따라 선택 영역의 크기와 위치를 조정한다
    """
    global selected_area
    canvas.coords(selected_area, start_x, start_y, event.x, event.y) # 선택 영역을 현재 마우스 위치까지 확장

def end_select(event):
    """
    선택 영역을 종료하는 함수
    선택된 영역 내의 객체들을 찾고, 해당 객체들의 좌표를 저장한다
    """
    global selected_area, selected_objects, selected_coords
    x1, y1, x2, y2 = canvas.coords(selected_area)
    selected_objects = canvas.find_enclosed(x1, y1, x2, y2) # 선택된 영역 내의 객체들을 찾음
    selected_coords = [(canvas.coords(obj), obj) for obj in selected_objects]  # 선택된 객체들의 좌표를 저장
    canvas.delete(selected_area) # 선택 영역 표시 지움
    # 언바인딩 
    canvas.unbind("<B1-Motion>")  
    canvas.unbind("<ButtonRelease-1>")

def start_drag(event):
    """
    선택된 객체들을 드래그 시작하는 함수
    마우스 우클릭 위치를 기준으로 드래그를 초기화하고, 
    드래그 중 및 드래그 종료 시 호출할 이벤트를 바인딩한다
    """
    global offset_x, offset_y, initial_coords
    offset_x, offset_y = event.x, event.y
    initial_coords = [(canvas.coords(obj), obj) for obj in selected_objects] # 선택된 객체들의 초기 좌표를 저장
    canvas.bind("<B3-Motion>", drag_selected) # 우클릭으로 드래그 시 drag_selected 함수 호출
    canvas.bind("<ButtonRelease-3>", release_selected) # 우클릭 버튼 떼면 release_selected 함수 호출

def drag_selected(event):
    """
    선택된 객체들을 드래그하여 이동하는 함수
    마우스 이동 거리를 계산하여 선택된 객체들을 이동시킨다
    """
    global offset_x, offset_y, initial_coords
    dx = event.x - offset_x
    dy = event.y - offset_y

    # 선택된 객체들을 마우스 이동 거리만큼 이동
    for initial, obj in initial_coords:
        new_coords = [coord + dx if i % 2 == 0 else coord + dy for i, coord in enumerate(initial)]
        canvas.coords(obj, *new_coords)

def release_selected(event):
    """
    드래그 종료 시 호출되는 함수
    드래그 관련 이벤트 바인딩을 해제한다
    """
    canvas.unbind("<B3-Motion>")
    canvas.unbind("<ButtonRelease-3>")

def toggle_select_mode():
    """
    선택 모드를 토글하는 함수
    선택 모드를 활성화/비활성화하여 선택 모드와 그리기 모드를 전환한다
    """
    if canvas.cget("cursor") == "cross": # 선택 모드 해제
        canvas.config(cursor="")
        canvas.bind("<Button-1>", paint_start)
        canvas.bind("<B1-Motion>", paint)
        canvas.unbind("<Button-3>")
    else: # 선택 모드 활성화
        canvas.config(cursor="cross")
        canvas.bind("<Button-1>", start_select)
        canvas.bind("<Button-3>", start_drag)

window = Tk()
#Tk 객체를 생성하여 주 윈도우를 만들기
window.title("그림판")

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")
#Canvas 위젯을 생성하여 주 윈도우에 추가
window.geometry("640x400+200+200")
#윈도우이름.geometry("너비x높이+x좌표+y좌표")를 이용하여
#윈도우 창의 너비와 높이, 초기 화면 위치의 x좌표와 y좌표를 설정
window.resizable(True,True)
#윈도우이름.resizeable(상하, 좌우)을 이용하여
#윈도우 창의 창 크기 조절 가능 여부를 설정
canvas.pack(fill="both",expand=True)
#캔버스를 창 너비에 맞춰 동적으로 크기 조절

last_x, last_y = None, None # 마지막 좌표 초기화
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

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode("solid")) # 버튼을 누르면 실선 모드로 바꾼다
button_solid.pack() # 실선 브러쉬 버튼을 윈도우에 배치

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode("dotted")) # 버튼을 누르면 점선 모드로 바꾼다
button_dotted.pack() # 점선 브러쉬 버튼을 윈도우에 배치

button_paint = Button(window, text="normal", command=set_paint_mode_normal) #기본 그리기 모드로 전환하는 기능
button_paint.pack(side=RIGHT)

button_paint = Button(window, text="pressure", command=set_paint_mode_pressure) #감압 브러시 그리기 모드로 전환하는 기능
button_paint.pack(side=RIGHT)

text_box = Entry(window) #텍스트를 입력할 공간을 생성합니다.
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", add_text) #입력한 텍스트를 오른쪽 클릭으로 텍스트를 찍어냅니다.
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window) #"새 창 열기"라는 버튼 생성 command: 버튼 클릭 시 create_new_window: 새로운 창을 만듦 
button_new_window.pack(side=LEFT) # "새 창 열기"버튼을 윈도우에 배치

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", erase)

brush_color = "black"

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_select = Button(window, text="Select", command=toggle_select_mode) # 버튼을 누르면 선택 모드가 활성화되고 한번 더 누르면 선택 모드가 비활성화된다
button_select.pack(side=LEFT) # 선택 버튼을 윈도우에 배치

set_paint_mode_normal() # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
