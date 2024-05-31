"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
undo_stack = []  

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal(canvas):
    reset_last_coordinates()
    canvas.bind("<Button-1>", lambda event: paint_start(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event, canvas))

def set_paint_mode_pressure(canvas):
    reset_last_coordinates()
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))
    canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event, canvas))

def reset_last_coordinates():
    global last_x, last_y
    last_x, last_y = None, None

def start_paint_pressure(event, canvas):
    global start_time, current_segment
    start_time = time.time()
    current_segment = []  

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    shape_id = canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)
    current_segment.append(shape_id)  

def paint_start(event, canvas):
    global x1, y1, current_segment
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    current_segment = []  

def paint(event, canvas):
    global x1, y1
    x2, y2 = event.x, event.y
    shape_id = canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    current_segment.append(shape_id)  
    x1, y1 = x2, y2

def paint_end(event, canvas):
    if current_segment:
        undo_stack.append(current_segment)  

"""
dotted_paint: 점선 브러쉬 함수
이벤트가 발생한 위치에 검은색 원을 일정한 간격으로 그린다.
매개변수: event - 마우스 이벤트 객체로, 마우스의 현재 좌표를 포함
"""
def dotted_paint(event, canvas):
    global last_x, last_y, current_segment
    spacing = 10
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            shape_id = canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black", outline="black")
            current_segment.append(shape_id)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(mode, canvas):
    global brush_mode
    brush_mode = mode
    reset_last_coordinates()
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

#all clear 기능 추가
def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y, undo_stack
    last_x, last_y = None, None
    undo_stack = []  

def add_text(event, text_box, canvas): 
    text = text_box.get()
    shape_id = canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
    undo_stack.append([shape_id])  

def toggle_fullscreen(event):
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
            if i % 2 == 0:
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)

# 상하 반전 기능 추가
def flip_vertical(canvas):
    objects = canvas.find_all()
    canvas.update()
    canvas_height = canvas.winfo_height()
    for obj in objects:
        coords = canvas.coords(obj)
        for i in range(len(coords)):
            if i % 2 == 1:
                coords[i] = canvas_height - coords[i]
        canvas.coords(obj, *coords)

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    shape_id = canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    current_segment.append(shape_id)

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

def create_new_window():
    new_window = Toplevel(window)
    new_window.title("새로운 그림판 창")
    new_window.geometry("1024x768+100+100")

    new_canvas = Canvas(new_window, bg="white")
    new_canvas.pack(fill="both", expand=True)

    new_button_frame = Frame(new_window)
    new_button_frame.pack(fill=X)

    new_button_clear = Button(new_button_frame, text="All Clear", command=lambda: clear_paint(new_canvas))
    new_button_clear.pack(side=LEFT)

    new_brush_size_slider = Scale(new_button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    new_brush_size_slider.set(brush_size)
    new_brush_size_slider.pack(side=LEFT)

    new_button_solid = Button(new_window, text="Solid Brush", command=lambda: set_brush_mode("solid", new_canvas))
    new_button_solid.pack(side=LEFT)

    new_button_dotted = Button(new_window, text="Dotted Brush", command=lambda: set_brush_mode("dotted", new_canvas))
    new_button_dotted.pack(side=LEFT)

    new_button_paint_normal = Button(new_window, text="normal", command=lambda: set_paint_mode_normal(new_canvas))
    new_button_paint_normal.pack(side=RIGHT)

    new_button_paint_pressure = Button(new_window, text="pressure", command=lambda: set_paint_mode_pressure(new_canvas))
    new_button_paint_pressure.pack(side=RIGHT)

    new_text_box = Entry(new_window)
    new_text_box.pack(side=LEFT)
    new_canvas.bind("<Button-3>", lambda event: add_text(event, new_text_box, new_canvas))

    new_button_flip = Button(new_window, text="Flip Horizontal", command=lambda: flip_horizontal(new_canvas))
    new_button_flip.pack(side=LEFT)

    new_button_flip_vertical = Button(new_window, text="Flip Vertical", command=lambda: flip_vertical(new_canvas))
    new_button_flip_vertical.pack(side=LEFT)

    new_canvas.bind("<B3-Motion>", lambda event: erase(event, new_canvas))

    new_button_bg_color = Button(new_window, text="Change Background Color", command=lambda: change_bg_color(new_canvas))
    new_button_bg_color.pack(side=LEFT)

    new_button_brush_color = Button(new_window, text="Change Brush Color", command=change_brush_color)
    new_button_brush_color.pack(side=LEFT)

    new_button_undo = Button(new_window, text="Undo", command=lambda: undo_last_action(new_canvas))
    new_button_undo.pack(side=LEFT)

    new_canvas.bind("<Button-1>", lambda event: paint_start(event, new_canvas))
    new_canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event, new_canvas))
    new_canvas.bind("<B1-Motion>", lambda event: paint(event, new_canvas))

    set_paint_mode_normal(new_canvas)

def undo_last_action(canvas):
    if undo_stack:
        last_segment = undo_stack.pop()
        for shape_id in last_segment:
            canvas.delete(shape_id)

window = Tk()
# Tk 객체를 생성하여 주 윈도우를 만들기
window.title("그림판")

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")
# Canvas 위젯을 생성하여 주 윈도우에 추가
window.geometry("1024x768+100+100")
# 윈도우이름.geometry("너비x높이+x좌표+y좌표")를 이용하여
# 윈도우 창의 너비와 높이, 초기 화면 위치의 x좌표와 y좌표를 설정
window.resizable(True,True)
# 윈도우이름.resizeable(상하, 좌우)을 이용하여
# 윈도우 창의 창 크기 조절 가능 여부를 설정
canvas.pack(fill="both",expand=True)
# 캔버스를 창 너비에 맞춰 동적으로 크기 조절

last_x, last_y = None, None # 마지막 좌표 초기화
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
canvas.bind("<Button-1>", lambda event: paint_start(event, canvas))
canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event, canvas))
# 캔버스에 마우스 왼쪽 버튼을 누르고 움직일 때마다 paint 함수를 호출하도록 바인딩

button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
button_clear.pack(side=LEFT)

# 펜 굵기를 조절할 수 있는 슬라이더 추가
brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
brush_size_slider.set(brush_size)  # 슬라이더 초기값 설정
brush_size_slider.pack(side=LEFT)

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode("solid", canvas)) # 버튼을 누르면 실선 모드로 바꾼다
button_solid.pack() # 실선 브러쉬 버튼을 윈도우에 배치

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode("dotted", canvas)) # 버튼을 누르면 점선 모드로 바꾼다
button_dotted.pack() # 점선 브러쉬 버튼을 윈도우에 배치

button_paint_normal = Button(window, text="normal", command=lambda: set_paint_mode_normal(canvas)) # 기본 그리기 모드로 전환하는 기능
button_paint_normal.pack(side=RIGHT)

button_paint_pressure = Button(window, text="pressure", command=lambda: set_paint_mode_pressure(canvas)) # 감압 브러시 그리기 모드로 전환하는 기능
button_paint_pressure.pack(side=RIGHT)

text_box = Entry(window) # 텍스트를 입력할 공간을 생성합니다.
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", lambda event: add_text(event, text_box, canvas)) # 입력한 텍스트를 오른쪽 클릭으로 텍스트를 찍어냅니다.
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window) # "새 창 열기"라는 버튼 생성 command: 버튼 클릭 시 create_new_window: 새로운 창을 만듦 
button_new_window.pack(side=LEFT) # "새 창 열기"버튼을 윈도우에 배치

button_flip = Button(window, text="Flip Horizontal", command=lambda: flip_horizontal(canvas))
button_flip.pack(side=LEFT)

button_flip_vertical = Button(window, text="Flip Vertical", command=lambda: flip_vertical(canvas))
button_flip_vertical.pack(side=LEFT)

canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

brush_color = "black"

button_bg_color = Button(window, text="Change Background Color", command=lambda: change_bg_color(canvas))
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_undo = Button(window, text="Undo", command=lambda: undo_last_action(canvas))
button_undo.pack(side=LEFT)

set_paint_mode_normal(canvas) # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
