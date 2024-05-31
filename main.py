from tkinter import *
import time  # 시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴

# 초기 설정 값들
brush_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<Button-1>", paint_start)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭 시작 시
    canvas.bind("<B1-Motion>", paint_pressure)  # 마우스를 클릭 중일 시 -> 그림을 그리고 있을 시

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
    global last_x, last_y
    last_x, last_y = event.x, event.y
    canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

def paint(event):
    global last_x, last_y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, event.x, event.y, fill=brush_color, width=brush_size, capstyle=ROUND, smooth=TRUE)
    last_x, last_y = event.x, event.y

# 점선 브러쉬 함수
def dotted_paint(event):
    global last_x, last_y
    spacing = brush_size  # 점 사이의 간격을 브러시 크기로 설정
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

# 브러쉬 모드를 변경하는 함수
def set_brush_mode(mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        set_paint_mode_normal()
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)
        canvas.bind("<Button-1>", paint_start)

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화

def add_text(event):
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
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
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
    new_canvas.pack(fill="both", expand=True)  # 캔버스가 새로운 창에 배치
    new_window.mainloop()

window = Tk()
window.title("그림판")

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")
window.geometry("640x400+200+200")
window.resizable(True, True)
canvas.pack(fill="both", expand=True)

last_x, last_y = None, None  # 마지막 좌표 초기화
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)

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

button_paint_normal = Button(window, text="Normal", command=set_paint_mode_normal)  # 기본 그리기 모드로 전환하는 기능
button_paint_normal.pack(side=RIGHT)

button_paint_pressure = Button(window, text="Pressure", command=set_paint_mode_pressure)  # 감압 브러시 그리기 모드로 전환하는 기능
button_paint_pressure.pack(side=RIGHT)

text_box = Entry(window)  # 텍스트를 입력할 공간을 생성합니다.
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", add_text)  # 입력한 텍스트를 오른쪽 클릭으로 텍스트를 찍어냅니다.
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window)  # "새 창 열기"라는 버튼 생성
button_new_window.pack(side=LEFT)  # "새 창 열기"버튼을 윈도우에 배치

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", erase)

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

set_paint_mode_normal()  # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
