"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import brush_settings  # brush_settings 모듈 임포트
from brush_settings import change_brush_size, change_bg_color, change_brush_color, set_brush_mode, set_paint_mode_normal, set_paint_mode_pressure, paint_start, paint, paint_end
import history  # history 모듈 임포트
import time  # 시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, canvas

brush_size = 1  # 초기 브러시 크기
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
brush_color = "black"  # 기본 색상은 검은색으로 설정
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
x1, y1 = None, None

# brush_settings 모듈에 전역 변수 전달
brush_settings.initialize_globals(globals())

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

canvas.bind("<Button-1>", lambda event: paint_start(event, canvas))
canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event, canvas))

# history_manager 인스턴스 생성
history_manager = history.HistoryManager(canvas)
canvas.history_manager = history_manager  # canvas에 history_manager 속성 추가


# all clear 기능 추가
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화
    history_manager.add_state()

def add_text(event):  # 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.
    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
    history_manager.add_state()

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
    history_manager.add_state()

def erase(event):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    history_manager.add_state()

# 새 창 열기 생성
def create_new_window():
    new_window = Tk()  # 새로운 Tk 인스턴스 생성
    new_canvas = Canvas(new_window)  # 새로운 창에 캔버스 추가
    new_canvas.pack()  # 캔버스가 새로운 창에 배치
    new_window.mainloop()



button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

# 펜 굵기를 조절할 수 있는 슬라이더 추가
brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=lambda new_size: change_brush_size(new_size))
brush_size_slider.set(brush_size)  # 슬라이더 초기값 설정
brush_size_slider.pack(side=LEFT)

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode(canvas, "solid"))  # 버튼을 누르면 실선 모드로 바꾼다
button_solid.pack()  # 실선 브러쉬 버튼을 윈도우에 배치

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode(canvas, "dotted"))  # 버튼을 누르면 점선 모드로 바꾼다
button_dotted.pack()  # 점선 브러쉬 버튼을 윈도우에 배치

button_paint_normal = Button(window, text="normal", command=lambda: set_paint_mode_normal(canvas))  # 기본 그리기 모드로 전환하는 기능
button_paint_normal.pack(side=RIGHT)

button_paint_pressure = Button(window, text="pressure", command=lambda: set_paint_mode_pressure(canvas))  # 감압 브러시 그리기 모드로 전환하는 기능
button_paint_pressure.pack(side=RIGHT)

text_box = Entry(window)  # 텍스트를 입력할 공간을 생성합니다.
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", lambda event: add_text(event))  # 입력한 텍스트를 오른쪽 클릭으로 텍스트를 찍어냅니다.
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window)  # "새 창 열기"라는 버튼 생성 command: 버튼 클릭 시 create_new_window: 새로운 창을 만듦
button_new_window.pack(side=LEFT)  # "새 창 열기"버튼을 윈도우에 배치

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", lambda event: erase(event))

button_bg_color = Button(window, text="Change Background Color", command=lambda: change_bg_color(canvas))
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_undo = Button(window, text="Undo", command=history_manager.undo)
button_undo.place(x=10, y=10)

button_redo = Button(window, text="Redo", command=history_manager.redo)
button_redo.place(x=70, y=10)


set_paint_mode_normal(canvas)  # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()
