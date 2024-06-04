
"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from tkinter import ttk
import time #시간 계산을 위한 모듈
import brush_settings  # brush_settings 모듈 임포트
from brush_settings import change_brush_size, change_bg_color, change_brush_color, set_brush_mode, set_paint_mode_normal, set_paint_mode_pressure, paint_start, paint, dotted_paint
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk
import math  # 수학 모듈을 가져옴
import random
from fun_timer import Timer
from picture import ImageEditor #이미지 모듈을 가져옴
from spray import SprayBrush #spray 모듈을 가지고 옴
import os
from tkinter import Scale

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, canvas
brush_size = 1  # 초기 브러시 크기
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
brush_color = "black"  # 기본 색상은 검은색으로 설정
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
brush_modes = ["solid", "dotted", "double_line", "pressure", "marker", "airbrush","spray"]
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
x1, y1 = None, None

#동적 브러시 설정을 위한 변수 초기화
dynamic_brush = False
previous_time = None
previous_x, previous_y = None, None


# 벌집 색상 선택 함수
def choose_hex_color():
    color = askcolor()[1]
    if color:
        draw_honeycomb_pattern(canvas, hex_color=color)

# 벌집 모양 패턴 함수
def draw_honeycomb_pattern(canvas, hex_size=30, hex_color="black"):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    hex_height = math.sqrt(3) * hex_size  # 헥사곤의 높이 계산

    def hex_corner(x, y, size, i):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        return x + size * math.cos(angle_rad), y + size * math.sin(angle_rad)

    for y in range(0, canvas_height, int(hex_height)):
        for x in range(0, canvas_width, int(3 * hex_size // 2)):
            for dx in [0, hex_size * 3 // 2]:
                for dy in [0, hex_height // 2]:
                    hexagon = [hex_corner(x + dx, y + dy, hex_size, i) for i in range(6)]
                    canvas.create_polygon(hexagon, outline=hex_color, fill='')

# 연필 브러시 함수
def pencil_brush(event, canvas):
    global last_x, last_y, brush_size
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = max(abs(dx), abs(dy))
        for i in range(0, distance, 2):  # 이동 거리의 절반마다 포인트 추가
            x = last_x + dx * i / distance
            y = last_y + dy * i / distance
            jitter_x = x + random.randint(-brush_size, brush_size)  # 브러시 크기에 따른 진동 효과
            jitter_y = y + random.randint(-brush_size, brush_size)
            canvas.create_line(jitter_x, jitter_y, jitter_x + 1, jitter_y + 1, fill=brush_color, width=brush_size/2)
    last_x, last_y = event.x, event.y

# 벽돌 색상 선택 함수
def choose_brick_line_color():
    color = askcolor()[1]
    if color:
        draw_brick_pattern(canvas, line_color=color)


# 벽돌 모양 패턴 함수
def draw_brick_pattern(canvas, brick_width=60, brick_height=30, line_color="black"):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    for y in range(0, canvas_height, brick_height):
        for x in range(0, canvas_width, brick_width):
            if (y // brick_height) % 2 == 0:
                canvas.create_rectangle(x, y, x + brick_width, y + brick_height, outline=line_color, fill="")
            else:
                canvas.create_rectangle(x - brick_width // 2, y, x + brick_width // 2, y + brick_height,
                                        outline=line_color, fill="")

def start_pencil(event):
    global last_x, last_y
    last_x, last_y = None, None
    pencil_brush(event, canvas)

def set_brightness(value):
    brightness = int(value) / 100  # 슬라이더 값(0-100)을 0-1 범위로 변환
    rgb = (int(255 * brightness), int(255 * brightness), int(255 * brightness))  # RGB 값 계산
    color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'  # RGB 값을 16진수 색상 코드로 변환
    canvas.configure(bg=color)

def increase_brightness(event=None):
    current_value = brightness_slider.get()
    if current_value < 100:
        brightness_slider.set(current_value + 5)  # 밝기를 5% 올리기
        set_brightness(current_value + 5)

def decrease_brightness(event=None):
    current_value = brightness_slider.get()
    if current_value > 0:
        brightness_slider.set(current_value - 5)  # 밝기를 5% 낮추기
        set_brightness(current_value - 5)




#드래그로 그림 움직이기
#오른쪽 마우스 눌렀을 때 드래그 시작하는 지점 좌표 기록
def start_move(event):
    global last_x, last_y, is_moving
    if event.num == 3:  # 오른쪽 버튼 클릭 여부 확인
        last_x, last_y = event.x, event.y
        is_moving = True
#오른쪽 마우스 누르면 그려진 모든 요소들 이동
def move(event):
    global last_x, last_y, is_moving
    if is_moving:
        x_delta = event.x - last_x
        y_delta = event.y - last_y
        canvas.move("all", x_delta, y_delta)  # 그려진 모든 요소를 이동시킴
        last_x, last_y = event.x, event.y
#오른쪽 마우스 떼면 움직임 종료
def end_move(event):
    global is_moving
    is_moving = False




#+=================================================================================
def close_program(): #프로그램을 종료하는 기능
    if messagebox.askokcancel("Quit", "Do you want to quit?"): #프로그램을 종료할 것인지 확인 매시지를 띄움
        window.destroy() #확인 클릭시 프로그램을 종료

def show_info_window(): #정보를 표시하는 기능
    messagebox.showinfo("Info", "OSS_Paint_2024\n 그림판 v1.0.0")
#+=================================================================================

is_dark_mode = False  # 기본 모드는 라이트 모드

def toggle_dark_mode(): # 다크 모드를 토글하는 함수
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # 토글 동작을 상태 변경 전에 수행
    if is_dark_mode:  # 지금 라이트 모드라면 [수정된 조건 검사]
        apply_dark_mode()  # 다크 모드 적용
    else: # 지금 다크 모드라면
        apply_light_mode()  # 라이트 모드 적용

def apply_light_mode(): # 라이트 모드 적용(기본)
    window.config(bg="sky blue") # 윈도우 배경색
    canvas.config(bg="white") # 캔버스 배경색
    button_frame.config(bg="sky blue") # 버튼 프레임 배경색
    for widget in button_frame.winfo_children(): 
        widget.config(bg="light grey", fg="black") # 버튼 프레임 안의 모든 버튼들 배경색, 글자색
    timer_label.config(bg="white", fg="black") # 타이머 라벨 배경색, 글자색

def apply_dark_mode(): # 다크 모드 적용
    window.config(bg="grey20") # 윈도우 배경색
    canvas.config(bg="grey30") # 캔버스 배경색
    button_frame.config(bg="grey20") # 버튼 프레임 배경색
    for widget in button_frame.winfo_children():
        widget.config(bg="grey40", fg="white") # 버튼 프레임 안의 모든 버튼들 배경색, 글자색
    timer_label.config(bg="grey20", fg="white") # 타이머 라벨 배경색, 글자색

#이미지 파일 불러오기 
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        editor.open_image(file_path)

def on_enter(event):
    event.widget.config(bg="light blue")

def on_leave(event):
    event.widget.config(bg="SystemButtonFace")

def upload_image():
    path = filedialog.askopenfilename()
    if path:
        # 업로드 파일이 PNG파일인지 확인
        if not path.lower().endswith('.png'):
            messagebox.showerror("Invalid File", "PNG 파일만 업로드할 수 있습니다.")
            return

        # 업로드 파일이 PNG일 때 업로드 성공
        image = PhotoImage(file=path)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.image = image

# 문자열 드래그 시작
def start_drag(event):
    drag_data["item"] = canvas.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y
    canvas.unbind("<B1-Motion>")

# 문자열 드래그 중
def drag(event):
    if drag_data["item"]:
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(drag_data["item"], dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# 문자열 드래그 종료
def end_drag(event):
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0
    canvas.bind("<B1-Motion>", paint_stroke)

#텍스트 박스 추가 기능
# 문자열을 드래그하기 위한 변수
drag_data = {"item": None, "x": 0, "y": 0}
drag_data = {"item": None, "x": 0, "y": 0}

def open_text_input_window():
    # 문자열을 입력할 새로운 창 생성
    text_input_window = Toplevel(window)
    text_input_window.title("Text Input")

    # 텍스트 입력 창 생성
    text_input = Text(text_input_window, width=30, height=5)
    text_input.pack()

    # 확인 버튼 생성 및 클릭 이벤트 핸들러 설정
    confirm_button = Button(text_input_window, text="확인", command=lambda: add_text_to_canvas(text_input.get("1.0", "end-1c")))
    confirm_button.pack()

def add_text_to_canvas(text):
    if text.strip():  # 입력된 텍스트가 공백이 아닌 경우에만 캔버스에 추가
        text_item = canvas.create_text(100, 100, text=text, fill="black", font=('Arial', 12))
        canvas.tag_bind(text_item, "<ButtonPress-1>", start_drag)
        canvas.tag_bind(text_item, "<B1-Motion>", drag)
        canvas.tag_bind(text_item, "<ButtonRelease-1>", end_drag)



# 라인 브러쉬 기능 추가 
def set_brush_mode_line(canvas):
    canvas.bind("<Button-1>", lambda event: line_start(event, canvas))

def line_start(event, canvas):
    global x1, y1
    x1, y1 = event.x, event.y
    canvas.bind("<Button-1>", lambda event: draw_line(event, canvas))

def draw_line(event, canvas):
    global x1, y1
    canvas.create_line(x1, y1, x1, y1, event.x, event.y, fill=brush_color, width=2)
    x1, y1 = event.x, event.y

#타이머 기능 추가
timer = Timer()
#타이머의 경과시간 업데이트 
def update_timer():
    elapsed_time = timer.get_elapsed_time()
    timer_label.config(text=f"Time: {int(elapsed_time)} s") #라벨에 표시
    window.after(1000, update_timer)  # 1초마다 updatae_time 함수를 호출
#타이머 STOP
def stop_timer():
    timer.stop()
#타이머 리셋
def reset_timer():
    timer.reset()
    if not timer.running:
        timer.start()

#타이머 재시작
def start_stop():
    if not timer.running:
        timer.start()


def paint_airbrush(event, canvas):
    for _ in range(dot_count.get()):  # 에어브러쉬 효과를 위해 여러 개의 작은 점을 그림
        radius = random.randint(1, brush_size)  # 점의 크기를 무작위로 선택
        angle = random.uniform(0, 2 * math.pi)  # 점의 방향을 무작위로 선택
        distance = random.uniform(0, dot_distance.get())  # 점의 거리를 무작위로 선택
        x = event.x + distance * math.cos(angle)
        y = event.y + distance * math.sin(angle)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=brush_color, outline=brush_color)

# 에어브러쉬 속성을 조정하는 함수
def increase_dot_count():
    dot_count.set(dot_count.get() + 1)

def decrease_dot_count():
    dot_count.set(max(dot_count.get() - 1, 1))  # 최소값 1 설정

def increase_dot_distance():
    dot_distance.set(dot_distance.get() + 1)

def decrease_dot_distance():
    dot_distance.set(max(dot_distance.get() - 1, 0))  # 최소값 0 설정

def set_solid_brush_mode(event):
    set_brush_mode(canvas, "solid")

def set_dotted_brush_mode(event):
    set_brush_mode(canvas, "dotted")

def set_double_line_brush_mode(event):
    set_brush_mode(canvas, "double_line")

    # 맞춤형 단축키 기능 추가
def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(canvas)) #clear 단축키 c
    window.bind("<Control-s>", save_canvas) #save 단축키 crtl+s
    window.bind("<Control-z>", erase_last_stroke) #undo 단축키 crtl+z
    window.bind("d", lambda event: toggle_dark_mode()) #dark 모드 단축키 d
    window.bind("<q>", set_solid_brush_mode)
    window.bind("<w>", set_dotted_brush_mode)
    window.bind("<e>", set_double_line_brush_mode)
    window.bind("<Control-y>", rewrite_last_stroke) # redo 단축키 ctrl+shift+z

# brush_settings.initialize_globals(globals())

def set_paint_mode_airbrush(canvas): #에어브러쉬 그리기 모드로 전환하는 기능
    canvas.bind("<B1-Motion>", lambda event: paint_airbrush(event, canvas))

def set_paint_mode_normal(canvas, set_origin_mode=False):
    canvas.bind("<Button-1>", lambda event: paint_start(event))
    canvas.bind("<B1-Motion>", paint_stroke)
    if set_origin_mode:
        # 추가적인 원점 모드 설정 코드
        pass


def start_paint_pressure(event, canvas):
    global start_time
    start_time = time.time() #마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 20), 1), 8) * brush_size / 4  # 굵가는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)



# 점선 브러쉬 함수
def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = 10 + brush_size  # 점 사이의 간격을 브러시 크기로 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x-brush_size / 2, event.y-brush_size / 2, event.x+brush_size / 2, event.y+brush_size / 2, fill=brush_color, outline=brush_color)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y
        canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

def paint_marker(event, canvas):
    radius = brush_size
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(canvas, mode): # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":  # 브러쉬 모드가 solid면
        canvas.bind("<B1-Motion>", lambda event: set_paint_mode_normal(canvas))  # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted":  # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))  # 점선 브러쉬로 변경
    elif brush_mode == "double_line": #브러쉬 모드가 double_line 면
        canvas.bind("<B1-Motion>", lambda event: double_line_paint(event, canvas))#이중 실선 브러쉬로 변경
        canvas.bind("<Button-1>", start_new_line)
    elif brush_mode == "pressure":
        canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
        canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))
    elif brush_mode == "marker":
        canvas.bind("<B1-Motion>", lambda event: paint_marker(event, canvas))
        canvas.bind("<Button-1>", lambda event: paint_marker(event, canvas))
    elif brush_mode == "airbrush":
        canvas.bind("<B1-Motion>", lambda event: paint_airbrush(event, canvas))
        canvas.bind("<Button-1>", lambda event: paint_airbrush(event, canvas))
    elif brush_mode == "spray":
        canvas.bind("<B1-Motion>",  spray_brush.spray_paint)
        canvas.bind("<Button-1>",  spray_brush.spray_paint)
    elif brush_mode == "pencil":
        canvas.bind("<Button-1>", start_pencil)
        canvas.bind("<B1-Motion>", lambda event: pencil_brush(event, canvas))
        canvas.bind("<ButtonRelease-1>", lambda event: paint_end(event))

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)
    # spray의 크기를 변경하는 기능
    spray_brush.set_brush_size(brush_size)

def zoom_scroll(event):
    # Ctrl 키가 눌려있는지 확인
    if event.state & 0x0004:
        scale = 1.0
        if event.delta > 0:  # 마우스 휠을 위로 스크롤하면 확대
            scale = 1.1
        elif event.delta < 0:  # 마우스 휠을 아래로 스크롤하면 축소
            scale = 0.9
        canvas.scale("all", event.x, event.y, scale, scale)
        canvas.configure(scrollregion=canvas.bbox("all"))
    else:
        # Ctrl 키가 눌려있지 않으면 스크롤
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")  # 위로 스크롤
        elif event.delta < 0:
            canvas.yview_scroll(1, "units")  # 아래로 스크롤

def horizontal_scroll(event):
    if event.delta > 0:
        canvas.xview_scroll(-1, "units")  # 왼쪽으로 스크롤
    elif event.delta < 0:
        canvas.xview_scroll(1, "units")  # 오른쪽으로 스크롤

def on_button_press(event):
    canvas.scan_mark(event.x, event.y)

def on_mouse_drag(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

#all clear 기능 추가
def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None # 마지막 좌표 초기화

def add_text(event, canvas, text_box):# 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.

    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
   
def bind_shortcuts_window(window):
    window.bind("<Alt-Return>", toggle_fullscreen)  # Alt + Enter (Windows/Linux)
    window.bind("<Command-Return>", toggle_fullscreen)  # Command + Enter (Mac)

# 전체화면 토글 함수
def toggle_fullscreen(event=None):
    global window
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))

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

def flip_vertical(canvas):
    objects = canvas.find_all()
    canvas.update()
    canvas_height = canvas.winfo_height()
    for obj in objects:
        coords = canvas.coords(obj)
        for i in range(len(coords)):
            if i % 2 != 0:  # y 좌표를 반전시킵니다.
                coords[i] = canvas_height - coords[i]
        canvas.coords(obj, *coords)

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color, width=brush_size) # 브러쉬 사이즈 조절

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color(event=None):
    global brush_color
    selected_color = askcolor()[1]
    if selected_color:
        brush_color = selected_color
        set_brush_color(brush_color)
"""
TypeError: change_brush_color() takes 0 positional arguments but 1 was given
함수를 호출 할 때 전달된 인자와 함수의 파라미터 수가 다른 경우 발생
해당 함수는 호출될 때 인자를 받지 않지만 인자를 전달했기 때문에 오류가 발생했다. 
인자를 받지 않기 위해 None로 설정
"""

# 브러시 색상을 설정하는 함수
def set_brush_color(color):
    global brush_color
    brush_color = color
    # spray_brush의 색상 변경을 위한 코드 추가
    spray_brush.set_brush_color(brush_color)

# 사용자 정의 색상을 설정하고 팔레트에 추가하는 함수
def set_custom_color(r_entry, g_entry, b_entry, palette_frame):
    try:
        # R, G, B 값을 입력받아 정수로 변환
        r = int(r_entry.get())
        g = int(g_entry.get())
        b = int(b_entry.get())

        # R, G, B 값이 0에서 255 사이인지 확인
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            # R, G, B 값을 16진수로 변환하여 색상 코드 생성
            color = f'#{r:02x}{g:02x}{b:02x}'
            set_brush_color(color)  # 브러시 색상 설정 함수 호출

            # 사용자 정의 색상을 팔레트에 동적으로 추가
            button = Button(palette_frame, bg=color, width=2, height=1, command=lambda c=color: set_brush_color(c))
            button.pack(side=LEFT, padx=2, pady=2)
        else:
            print("RGB 값은 0에서 255 사이여야 합니다.")
    except ValueError:
        print("유효한 RGB 값을 입력하세요.")

# 팔레트 설정 함수
def setup_palette(window):
    # 새로운 창 생성
    palette_window = Toplevel(window)
    palette_window.title("팔레트 설정")

    # 팔레트 프레임 생성 및 추가
    palette_frame = Frame(palette_window)
    palette_frame.pack(pady=10)

    # 미리 정의된 색상 목록
    colors = [
        'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'white', 'pink', 'brown', 'grey'
    ]

    # 색상 버튼 생성 및 팔레트 프레임에 추가
    for color in colors:
        button = Button(palette_frame, bg=color, width=2, height=1, command=lambda c=color: set_brush_color(c))
        button.pack(side=LEFT, padx=2, pady=2)

    # 사용자 정의 색상 입력창 생성 및 추가
    custom_color_frame = Frame(palette_window)
    custom_color_frame.pack(pady=10)

    # R 값 입력 라벨과 입력창 생성 및 추가
    Label(custom_color_frame, text="R:").grid(row=0, column=0)
    r_entry = Entry(custom_color_frame, width=3)
    r_entry.grid(row=0, column=1)

    # G 값 입력 라벨과 입력창 생성 및 추가
    Label(custom_color_frame, text="G:").grid(row=0, column=2)
    g_entry = Entry(custom_color_frame, width=3)
    g_entry.grid(row=0, column=3)

    # B 값 입력 라벨과 입력창 생성 및 추가
    Label(custom_color_frame, text="B:").grid(row=0, column=4)
    b_entry = Entry(custom_color_frame, width=3)
    b_entry.grid(row=0, column=5)

    # 색상 설정 버튼 생성 및 사용자 정의 색상 프레임에 추가
    Button(custom_color_frame, text="Set Color", command=lambda: set_custom_color(r_entry, g_entry, b_entry, palette_frame)).grid(row=1, columnspan=6, pady=10)


# 캔버스를 파일로 저장하는 함수
def save_canvas(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PostScript files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

def reset_brush(canvas):
    global brush_size, brush_color
    brush_size = 1  # 초기 브러시 크기
    brush_color = "black"  # 초기 브러시 색상
    change_brush_size(brush_size)  # 브러시 크기 조정
    canvas.bind("<B1-Motion>", lambda event: set_paint_mode_normal(canvas))  # 실선(기본) 브러쉬로 변경


def setup_reset_brush_button(window, canvas):
    global button_reset
    button_reset = Button(labelframe_brush, text="Reset", command=lambda: reset_brush(canvas))
    button_reset.pack(side=BOTTOM)
    button_reset.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_reset.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

# 색 채우기 기능 추가
def flood_fill(event):
    fill_color = askcolor()[1]  # 색상 선택 대화 상자에서 색상을 선택
    x, y = event.x, event.y
    target = canvas.find_closest(x, y)
    if target:
        canvas.itemconfig(target, fill=fill_color)


def draw_actor(event, actor_name):
    """
    draw_actor: 액터를 그리는 함수
    캔버스의 특정 위치에 액터를 그린다.
    """
    x, y = event.x, event.y
    canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white", outline="black") # 머리
    canvas.create_line(x, y + 15, x, y + 40) # 몸통
    canvas.create_line(x, y + 20, x - 10, y + 30) # 왼팔
    canvas.create_line(x, y + 20, x + 10, y + 30) # 오른팔
    canvas.create_line(x, y + 40, x - 10, y + 50) # 왼다리
    canvas.create_line(x, y + 40, x + 10, y + 50) # 오른다리
    canvas.create_text(x, y + 60, text=actor_name, anchor="center") # 액터 이름
    # 바인딩 해제
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def draw_use_case(event, use_case_name):
    """
    draw_use_case: 유스케이스를 그리는 함수
    캔버스의 특정 위치에 유스케이스를 그린다.
    유스케이스는 타원으로 표시되고, 유스케이스의 이름이 타원의 중앙에 표시된다.
    """
    x, y = event.x, event.y
    canvas.create_oval(x - 50, y - 25, x + 50, y + 25, fill="white", outline="black") # 유스케이스 모양
    canvas.create_text(x, y, text=use_case_name, anchor="center") # 유스케이스 이름
    # 바인딩 해제
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def draw_relationship_start(event):
    """
    draw_relationship_start: 관계 그리기를 시작하는 함수
    관계의 시작 지점을 기록하고, 드래그 중에 미리보기 선을 그린다.
    """
    global x1, y1, preview_line
    x1, y1 = event.x, event.y # 시작 지점 기록
    preview_line = None # 미리보기 선 초기화
    canvas.bind("<B1-Motion>", draw_relationship_preview) # 드래그할 때 미리보기 선 그리기

def draw_relationship_preview(event):
    """
    draw_relationship_preview: 관계 그리기 미리보기 함수
    관계를 그리기 위해 드래그할 때 현재 위치까지의 미리보기 선을 그린다.
    """
    global x1, y1, preview_line
    x2, y2 = event.x, event.y # 현재 지점
    if preview_line:
        canvas.delete(preview_line) # 이전 미리보기 선 삭제
    preview_line = canvas.create_line(x1, y1, x2, y2, dash=(4, 2)) # 새로운 미리보기 선 그리기

def draw_relationship_end(event, relationship_type):
    """
    draw_relationship_end: 관계 그리기를 종료하는 함수
    드래그 종료 지점에서 실제 선을 그린다. 
    관계 유형에 따라 화살표와 텍스트를 추가한다.
    """
    global x1, y1, preview_line
    x2, y2 = event.x, event.y # 종료 지점
    if preview_line:
        canvas.delete(preview_line) # 미리보기 선 삭제
    if relationship_type in ["include", "extend"]: # 포함 관계나 확장 관계면
        canvas.create_line(x1, y1, x2, y2, arrow=LAST, dash=(4, 2)) # 화살표가 있는 점선 그리기
    else:
        canvas.create_line(x1, y1, x2, y2) # 일반 선 그리기

    # 관계 유형에 따라 텍스트 추가
    if relationship_type == "include":
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<include>>", anchor="center")
    elif relationship_type == "extend":
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="<<extend>>", anchor="center")

    # 바인딩 해제
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def add_actor():
    """
    add_actor: 액터 추가 함수
    액터의 이름을 입력받고, 캔버스에 액터를 그리는 이벤트를 바인딩한다.
    """
    actor_name = simpledialog.askstring("Input", "액터의 이름을 입력하세요:") # 액터 이름 입력받기
    if actor_name:
        canvas.bind("<Button-1>", lambda event: draw_actor(event, actor_name)) # 클릭 시 액터 그리기

def add_use_case():
    """
    add_use_case: 유스케이스 추가 함수
    유스케이스의 이름을 입력받고, 캔버스에 유스케이스를 그리는 이벤트를 바인딩한다.
    """
    use_case_name = simpledialog.askstring("Input", "유스케이스의 이름을 입력하세요:") # 유스케이스 이름 입력받기
    if use_case_name:
        canvas.bind("<Button-1>", lambda event: draw_use_case(event, use_case_name)) # 클릭 시 유스케이스 그리기

def add_relationship():
    """
    add_relationship: 관계 추가 함수
    관계의 유형을 입력받고, 관계를 그리는 이벤트를 바인딩한다.
    """
    relationship_type = simpledialog.askstring("Input", "관계의 유형을 입력하세요 (include/extend/line):") # 관계 유형 입력받기
    if relationship_type in ["include", "extend", "line"]:
        canvas.bind("<Button-1>", draw_relationship_start) # 클릭 시 관계 그리기 시작
        canvas.bind("<ButtonRelease-1>", lambda event: draw_relationship_end(event, relationship_type)) # 마우스 버튼 놓으면 관계 그리기 종료
    else:
        messagebox.showerror("Error", "잘못된 입력입니다. include, extend, line 중에 입력하세요.")  # 잘못된 입력에 대한 오류 메시지

def choose_use_case_element(event=None):
    """
    choose_use_case_element: 유스케이스 다이어그램 요소 선택 함수
    액터, 유스케이스, 관계를 선택할 수 있는 팝업 메뉴를 생성한다.
    """
    popup = Menu(labelframe_additional, tearoff=0)
    popup.add_command(label="Actor", command=add_actor) # 액터 추가
    popup.add_command(label="Use Case", command=add_use_case) # 유스케이스 추가
    popup.add_command(label="Relationship", command=add_relationship) # 관계 추가
    if event:
        popup.post(event.x_root, event.y_root) # 마우스 위치에 팝업 메뉴 표시
    else:
        popup.post(window.winfo_pointerx(), window.winfo_pointery()) # 마우스 포인터 위치에 팝업 메뉴 표시



def setup_paint_app(window):
    global brush_size, brush_color, button_frame, labelframe_additional, labelframe_brush, labelframe_flip, labelframe_timer, labelframe_additional, labelframe_additional2

    brush_size = 1  # 초기 브러시 크기
    brush_color = "black"  # 초기 브러시 색상

    global canvas
    canvas = Canvas(window, bg="white")
    canvas.pack(fill=BOTH, expand=True,side= BOTTOM)

    last_x, last_y = None, None  # 마지막 좌표 초기화
    brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정

    

    button_frame = Frame(window,bg="grey")#구별하기 위한 버튼 영역 색 변경
    button_frame.pack(fill=X)

    labelframe_brush = LabelFrame(button_frame, text="brush mode") #브러시 설정을 정리한 프레임
    labelframe_brush.pack(side = LEFT,fill=Y)

    labelframe_flip = LabelFrame(button_frame, text="flip") #브러시 설정을 정리한 프레임
    labelframe_flip.pack(side = LEFT,fill=Y)

    labelframe_timer = LabelFrame(button_frame, text="timer") #타이머 설정을 정리한 프레임
    labelframe_timer.pack(side = LEFT,fill=Y)

    labelframe_additional = LabelFrame(button_frame,text="additionals") # 추가 기능 설정을 정리한 프레임
    labelframe_additional.pack(side = LEFT,fill=Y)

    labelframe_additional2 = LabelFrame(button_frame) # 추가 기능 설정을 정리한 프레임2
    labelframe_additional2.pack(side = LEFT,fill=Y)

    # 벌집 모양 패턴 버튼
    button_honeycomb = Button(window, text="Honeycomb Pattern", command=lambda: draw_honeycomb_pattern(canvas))
    button_honeycomb.pack(side=LEFT)
    button_honeycomb.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_honeycomb.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 벌집 모양 패턴 색상 선택 버튼
    button_honeycomb_color = Button(window, text="Choose Honeycomb Color", command=choose_hex_color)
    button_honeycomb_color.pack(side=LEFT)
    button_honeycomb_color.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_honeycomb_color.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 연필 브러시 버튼 추가
    button_pencil_brush = Button(window, text="연필브러시", command=lambda: set_brush_mode(canvas, "pencil"))
    button_pencil_brush.pack(side=LEFT)
    button_pencil_brush.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_pencil_brush.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 벽돌 패턴 버튼
    button_brick_pattern = Button(window, text="Brick Pattern", command=lambda: draw_brick_pattern(canvas))
    button_brick_pattern.pack(side=LEFT)
    button_brick_pattern.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_brick_pattern.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 벽돌 패턴 색상 선택 버튼
    button_brick_line_color = Button(window, text="Choose Brick Line Color", command=choose_brick_line_color)
    button_brick_line_color.pack(side=LEFT)
    button_brick_line_color.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_brick_line_color.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 밝기 슬라이더
    brightness_slider = tk.Scale(window, from_=0, to=100, orient='horizontal', command=set_brightness)
    brightness_slider.set(100)  # 초기 밝기를 100%로 설정
    brightness_slider.pack(pady=20)

    #timer 카테고리
    # 타이머 멈춤 버튼
    button_stop_timer = Button(labelframe_timer, text="Stop", command=stop_timer)
    button_stop_timer.pack(side=LEFT)
    button_stop_timer.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_stop_timer.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #타이머 리셋 버튼
    button_reset_timer = Button(labelframe_timer, text="Reset", command=reset_timer)
    button_reset_timer.pack(side=LEFT)
    button_reset_timer.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_reset_timer.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #타이머 시작
    start_button = Button(labelframe_timer, text="Start", command=start_stop)
    start_button.pack(side = LEFT)
    start_button.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    start_button.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    
    #additionals 카테고리
    # "TEXTBOX" 버튼 생성 및 클릭 이벤트 핸들러 설정
    text_box_button = Button(labelframe_additional, text="TEXTBOX", command=open_text_input_window)
    text_box_button.grid(row=1, column=1)
    text_box_button.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    text_box_button.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #다이어그램
    button_use_case = Button(labelframe_additional, text="Case Diagram", command=choose_use_case_element) #추가 기능에 포함됨.
    button_use_case.grid(row=1, column=2) 
    button_use_case.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_use_case.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록
    
    
    #이전 획 설정
    button_erase_last_stroke = Button(labelframe_additional, text="Undo", command=erase_last_stroke)
    button_erase_last_stroke.grid(row=2, column=1)
    button_erase_last_stroke.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_erase_last_stroke.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    button_redo_last_stroke = Button(labelframe_additional, text="Redo", command=rewrite_last_stroke)
    button_redo_last_stroke.grid(row=2, column=2)
    button_redo_last_stroke.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_redo_last_stroke.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #all clear
    button_clear = Button(labelframe_additional, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.grid(row=1, column=3)
    button_clear.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_clear.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #도형 모양 선택하는 버튼 생성
    button_choose_shape = Button(labelframe_additional, text="shape", command=choose_shape)
    button_choose_shape.bind("<Button-1>", choose_shape)  # 버튼 클릭 시 모양 선택 팝업 메뉴 표시
    button_choose_shape.grid(row=2,column=3)
    button_choose_shape.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_choose_shape.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    #filp 카테고리
    button_flip = Button(labelframe_flip, text="Horizontal", command=lambda: flip_horizontal(canvas))
    button_flip.pack(side=TOP)
    button_flip.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_flip.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    button_flip_vertical = Button(labelframe_flip, text="Vertical", command=lambda: flip_vertical(canvas))
    button_flip_vertical.pack(side=TOP)
    button_flip_vertical.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_flip_vertical.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    
    #브러시  모드를 선택하는 콤보박스
    brush_combobox = ttk.Combobox(labelframe_brush, values=brush_modes, state="readonly")
    brush_combobox.current(0)
    brush_combobox.bind("<<ComboboxSelected>>", lambda event: set_brush_mode(canvas, brush_combobox.get()))
    brush_combobox.pack(side=LEFT)
    

    # 에어브러쉬 속성 변수 생성
    dot_count = IntVar()
    dot_count.set(10)

    dot_distance = IntVar()
    dot_distance.set(10)

    frame_distance = Frame(window)
    frame_distance.pack(side=RIGHT)

    frame_count = Frame(window)
    frame_count.pack(side=RIGHT)



    # 에어브러쉬 속성 조절 버튼 추가
    Button(labelframe_additional2, text="+", command=increase_dot_distance).pack(side=RIGHT)
    Label(labelframe_additional2, text="Distance").pack(side=RIGHT)
    Label(labelframe_additional2, textvariable=dot_distance).pack(side=RIGHT)  # 거리 표시
    Button(labelframe_additional2, text="-", command=decrease_dot_distance).pack(side=RIGHT)

    Button(labelframe_additional2, text="+", command=increase_dot_count).pack(side=RIGHT)
    Label(labelframe_additional2, text="Count").pack(side=RIGHT)
    Label(labelframe_additional2, textvariable=dot_count).pack(side=RIGHT)  # 개수 표시
    Button(labelframe_additional2, text="-", command=decrease_dot_count).pack(side=RIGHT)

    # button_paint = Button(window, text="airbrush", command=lambda: set_paint_mode_airbrush(canvas)) #에어브러쉬 그리기 모드로 전환하는 기능
    # button_paint.pack(side=RIGHT)
    # button_paint.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    # button_paint.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint_stroke)
    canvas.bind("<ButtonRelease-1>", paint_end)

    #spray 인스턴스 생성 
    global spray_brush
    spray_brush = SprayBrush(canvas, brush_color)

    #브러시 크기 조정 슬라이더
    brush_size_slider = Scale(labelframe_brush, from_=1, to=20, orient=HORIZONTAL, label="Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)

    #브러시 line 모드(콤보 박스 통합X)
    button_line = Button(labelframe_brush, text="Line", command=lambda: set_brush_mode_line(canvas)) # 해당 기능은 브러시 모드 콤보 박스에 통합 시 기능이 작동안하는 문제가 발생함. 해결 전까지 RESET과 남겨두며, 위치만 이동 시킴.
    button_line.pack(side=RIGHT)
    button_line.bind("<Enter>", on_enter)  
    button_line.bind("<Leave>", on_leave)


    window.bind("<F11>", toggle_fullscreen)

    canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

    set_paint_mode_normal(canvas)
    setup_reset_brush_button(window, canvas)  # Reset 버튼 추가
    canvas.bind("<Enter>", change_cursor)
    canvas.bind("<Leave>", default_cursor)
    canvas.bind("<Button-3>", show_coordinates)
    canvas.bind("<ButtonRelease-3>", hide_coordinates)
    canvas.bind("<MouseWheel>", zoom_scroll)
    bind_shortcuts()

    

#+=================================================================================
    menu_bar = Menu(window) # 메뉴 바 생성
    window.config(menu=menu_bar) # 윈도우에 매뉴바를 menu_bar로 설정

    file_menu = Menu(menu_bar, tearoff=0)  # 메뉴 바에 파일 관련 메뉴를 추가
    color_menu = Menu(menu_bar, tearoff=0) # 메뉴 바에 색 관련 메뉴를 추가
    tool_menu = Menu(menu_bar, tearoff=0) # 메뉴 바에 도구 관련 메뉴를 추가
    help_menu = Menu(menu_bar, tearoff=0) # 메뉴 바에 도움 관련 메뉴를 추가

    menu_bar.add_cascade(label="File", menu=file_menu) # 'File' 메뉴를 매뉴바에 생성
    menu_bar.add_cascade(label="Color", menu=color_menu) # 'Color' 메뉴를 매뉴바에 생성
    menu_bar.add_cascade(label="Tools", menu=tool_menu) # 'Tools' 메뉴를 매뉴바에 생성
    menu_bar.add_cascade(label="Help", menu=help_menu) # 'Help' 메뉴를 매뉴바에 생성

    file_menu.add_command(label="Open New Window", command=create_new_window) # File 메뉴에 Open New Window 기능 버튼 추가
    file_menu.add_command(label="Add Image", command=upload_image) # File 메뉴에 Add Image 기능 버튼 추가
    file_menu.add_command(label="Save", command=lambda: save_canvas(canvas)) # File 메뉴에 Save 기능 버튼 추가
    file_menu.add_command(label="Exit", command=close_program) # File 메뉴에 Exit 기능 버튼 추가

    color_menu.add_command(label="Set Palette", command=lambda: setup_palette(window)) # Color 메뉴에 Set Palette 기능 버튼 추가
    color_menu.add_command(label="Change Background Color", command=lambda: change_bg_color(canvas)) # Color 메뉴에 Change Background Color 기능 버튼 추가
    color_menu.add_command(label="Change Brush Color", command=lambda: change_brush_color()) # Color 메뉴에 Change Brush Color 기능 버튼 추가

    tool_menu.add_command(label="Toggle FullScreen", command=toggle_fullscreen) # Tools 메뉴에 Toggle FullScreen 기능 버튼 추가
    tool_menu.add_command(label="Toggle Ruler", command=toggle_ruler) # Tools 메뉴에 Toggle Ruler 기능 버튼 추가
    tool_menu.add_command(label="Toggle Grid", command=lambda: toggle_grid(canvas)) # Tools 메뉴에 Toggle Grid 기능 버튼 추가
    tool_menu.add_command(label="Grid Setting", command=open_grid_dialog) # Tools 메뉴에 Grid Setting 기능 버튼 추가
    tool_menu.add_command(label="dark mode", command=toggle_dark_mode) # 다크 모드를 Tools 메뉴로 이동

    help_menu.add_command(label="Info", command=show_info_window) # Help 메뉴에 Info를 표시하는 기능 버튼 추가
#+=================================================================================
    
    
# 새 창 열기 생성
def create_new_window():
    new_window = Toplevel(window)  # 새로운 Toplevel 인스턴스 생성
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")#구별하기 위한 버튼 영역 색 변경
    setup_paint_app(new_window)

# 마우스 커서를 연필 형태로 변경하기
def change_cursor(event):
    canvas.config(cursor="pencil")

# 연필 형태 커서를 원래대로 변경하기
def default_cursor(event):
    canvas.config(cursor="")

# 우클릭을 누르면 우측 상단에 x, y 좌표값을 백분율로 표시
def show_coordinates(event):
    canvas.delete("coord_text")  # 이전 좌표값 삭제
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_percent = (event.x / width) * 100
    y_percent = (event.y / height) * 100
    coord_text = f"<{x_percent:.1f}% / {100-y_percent:.1f}%>"
    canvas.create_text(10, 10, text=coord_text, anchor="nw", tags="coord_text")

# 우클릭을 떼면 좌표값 삭제
def hide_coordinates(event):
    canvas.delete("coord_text")

"""
shape로 그릴 도형을 선택할 시 호출되어 윤곽선, 내부 색 선택이 가능하게 해주는 함수
shape_outline_color : 도형의 윤곽선 색
shape_fill_color : 도형의 내부 색
"""

def select_shape_color():
    global shape_outline_color, shape_fill_color
    shape_outline_color = askcolor()[1]  # 윤곽선 색상 선택
    shape_fill_color = askcolor()[1]  # 내부 색상 선택

# 사각형 그리기
def create_rectangle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_rectangle)

# 삼각형 그리기
def create_triangle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_triangle)

# 원형 그리기
def create_circle(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_circle)

# 사각형 그릴 위치 정하고 생성하는 함수 호출
def start_rectangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_rectangle(event))
    canvas.bind("<ButtonRelease-1>", finish_rectangle) # 마우스 버튼을 떼면 사각형 그리기 종료

# 사각형 생성하기
def draw_rectangle(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    current_shape = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")
    paint_start(event)

# 사각형 그리기 종료
def finish_rectangle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 삼각형 그릴 위치 정하고 생성하는 함수 호출
def start_triangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", draw_triangle)
    canvas.bind("<ButtonRelease-1>", finish_triangle)

# 삼각형 생성하기
def draw_triangle(event):
    global start_x, start_y, current_shape 
    canvas.delete("temp_shape")
    x2, y2 = event.x, event.y

    # 시작점과 마우스 이벤트가 발생한 점 사이의 거리 계산
    side_length = math.sqrt((x2 - start_x) ** 2 + (y2 - start_y) ** 2)

    # 정삼각형의 꼭짓점을 계산
    angle = math.radians(60)  # 120도를 라디안으로 변환
    x3 = start_x + side_length * math.cos(angle)
    y3 = start_y + side_length * math.sin(angle)

    angle += math.radians(60)  # 240도를 라디안으로 변환
    x4 = start_x + side_length * math.cos(angle)
    y4 = start_y + side_length * math.sin(angle)

    current_shape = canvas.create_polygon(start_x, start_y, x2, y2, x3, y3, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 삼각형 그리기 종료
def finish_triangle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 원형 그릴 위치 정하고 생성하는 함수 호출
def start_circle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_circle(event))
    canvas.bind("<ButtonRelease-1>", finish_circle)

# 원형 생성하기
def draw_circle(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    r = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    current_shape = canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 원형 그리기 종료
def finish_circle(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 별 모양 그리기
def create_star(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_star)

# 별 모양 그릴 위치 정하고 생성하는 함수 호출
def start_star(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_star(event))
    canvas.bind("<ButtonRelease-1>", finish_star)

# 별 모양 생성하기
def draw_star(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    outer_radius = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    inner_radius = outer_radius / 2.5  # 내각 반지름은 외각 반지름의 2.5분의 1
    points = []
    
    for i in range(5):
        angle_outer = math.radians(i * 72 - 90)
        angle_inner = math.radians(i * 72 + 36 - 90)
        
        x_outer = start_x + outer_radius * math.cos(angle_outer)
        y_outer = start_y + outer_radius * math.sin(angle_outer)
        x_inner = start_x + inner_radius * math.cos(angle_inner)
        y_inner = start_y + inner_radius * math.sin(angle_inner)
        
        points.append(x_outer)
        points.append(y_outer)
        points.append(x_inner)
        points.append(y_inner)
    
    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 별 모양 그리기 종료
def finish_star(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 육각별 모양 그리기
def create_six_pointed_star(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_six_pointed_star)

# 육각별 모양 그릴 위치 정하고 생성하는 함수 호출
def start_six_pointed_star(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_six_pointed_star(event))
    canvas.bind("<ButtonRelease-1>", finish_six_pointed_star)

# 육각별 모양 생성하기
def draw_six_pointed_star(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    outer_radius = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    inner_radius = outer_radius / 2.0  # 내각 반지름은 외각 반지름의 2분의 1
    points = []

    for i in range(6):
        angle_outer = math.radians(i * 60 - 90)
        angle_inner = math.radians(i * 60 + 30 - 90)

        x_outer = start_x + outer_radius * math.cos(angle_outer)
        y_outer = start_y + outer_radius * math.sin(angle_outer)
        x_inner = start_x + inner_radius * math.cos(angle_inner)
        y_inner = start_y + inner_radius * math.sin(angle_inner)

        points.append(x_outer)
        points.append(y_outer)
        points.append(x_inner)
        points.append(y_inner)

    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 육각별 모양 그리기 종료
def finish_six_pointed_star(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 하트 모양 그리기
def create_heart(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_heart)

# 하트 모양 그릴 위치 정하고 생성하는 함수 호출
def start_heart(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_heart(event))
    canvas.bind("<ButtonRelease-1>", finish_heart)

# 하트 모양 생성하기
def draw_heart(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    size = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5 / 10
    points = []

    for t in range(0, 361, 1):
        t_rad = math.radians(t)
        x = 16 * math.sin(t_rad)**3
        y = -(13 * math.cos(t_rad) - 5 * math.cos(2*t_rad) - 2 * math.cos(3*t_rad) - math.cos(4*t_rad))

        x_scaled = start_x + x * size  
        y_scaled = start_y + y * size  

        points.append(x_scaled)
        points.append(y_scaled)

    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")
# 하트 모양 그리기 종료
def finish_heart(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 십자형 도형 그리기 
def create_cross(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_cross)

# 십자형 도형 그릴 위치 정하고 생성하는 함수 호출
def start_cross(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_cross(event))
    canvas.bind("<ButtonRelease-1>", finish_cross)

# 십자형 도형 생성하기
def draw_cross(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    width = abs(start_x - event.x)  # 가로 길이
    height = abs(start_y - event.y)  # 세로 길이
    cross_width = min(width, height) / 3  # 십자형의 arm 너비

    # 중심점을 기준으로 십자형의 4개 arm 그리기
    points = [
        start_x - cross_width, start_y - height,  
        start_x + cross_width, start_y - height, 
        start_x + cross_width, start_y - cross_width, 
        start_x + width, start_y - cross_width,  
        start_x + width, start_y + cross_width,  
        start_x + cross_width, start_y + cross_width,
        start_x + cross_width, start_y + height,  
        start_x - cross_width, start_y + height, 
        start_x - cross_width, start_y + cross_width,
        start_x - width, start_y + cross_width, 
        start_x - width, start_y - cross_width,  
        start_x - cross_width, start_y - cross_width
    ]

    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 십자형 도형 그리기 종료
def finish_cross(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def create_diamond(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_diamond)

def start_diamond(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_diamond(event))
    canvas.bind("<ButtonRelease-1>", finish_diamond)

def draw_diamond(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    x2, y2 = event.x, event.y

    # 중심에서 각 꼭짓점까지의 거리 계산
    width = abs(x2 - start_x)
    height = abs(y2 - start_y)

    # 마름모의 네 꼭짓점 좌표 계산
    points = [
        start_x, start_y - height,  # 위쪽 꼭짓점
        start_x + width, start_y,  # 오른쪽 꼭짓점
        start_x, start_y + height,  # 아래쪽 꼭짓점
        start_x - width, start_y  # 왼쪽 꼭짓점
    ]

    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

def finish_diamond(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 화살표 그리기
def create_arrow(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_arrow)
# 화살표 그릴 위치 정하고 생성하는 함수 호출
def start_arrow(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", draw_arrow)
    canvas.bind("<ButtonRelease-1>", finish_arrow)
#화살표 생성하기
def draw_arrow(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    end_x, end_y = event.x, event.y
    # 화살표의 선 부분
    current_shape = canvas.create_line(start_x, start_y, end_x, end_y, fill=shape_outline_color, tags="temp_shape")
    # 화살표 머리 부분 계산
    arrow_size = 10
    angle = math.atan2(end_y - start_y, end_x - start_x)
    left_x = end_x - arrow_size * math.cos(angle - math.pi / 6)
    left_y = end_y - arrow_size * math.sin(angle - math.pi / 6)
    right_x = end_x - arrow_size * math.cos(angle + math.pi / 6)
    right_y = end_y - arrow_size * math.sin(angle + math.pi / 6)
    canvas.create_polygon(end_x, end_y, left_x, left_y, right_x, right_y, fill=shape_outline_color, outline=shape_outline_color, tags="temp_shape")
#화살표 그리기 종료
def finish_arrow(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

# 정오각형 그리기
def create_pentagon(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_pentagon)

# 정오각형 시작 지점 설정 및 함수 호출
def start_pentagon(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_pentagon(event))
    canvas.bind("<ButtonRelease-1>", finish_pentagon)

"""
radius : 오각형의 중심으로 부터 꼭짓점까지의 거리
angle : 오각형의 각 꼭짓점을 찾기 위해 사용하는 각도의 값
"""
# 정오각형 그리기 함수
def draw_pentagon(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    radius = math.sqrt((event.x - start_x)**2 + (event.y - start_y)**2)
    points = []
    for i in range(5):
        angle = 2 * math.pi / 5 * i + 60
        x = start_x + radius * math.cos(angle)
        y = start_y + radius * math.sin(angle)
        points.extend([x, y])
    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 정오각형 그리기 종료
def finish_pentagon(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

def create_V(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_V)

# 체크 도형 그릴 위치 정하고 생성하는 함수 호출
def start_V(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_V(event))
    canvas.bind("<ButtonRelease-1>", finish_cross)

# 체크 도형 생성하기
def draw_V(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    width = abs(start_x - event.x)  # 가로 길이
    height = abs(start_y - event.y)  # 세로 길이
    cross_width = min(width, height) / 3


    points = [
        start_x,start_y,
        start_x + width/3, start_y,  
        start_x + width/2, start_y + height-width/3, 
        start_x + width*2/3, start_y, 
        event.x, start_y,  
        start_x + width/2, event.y,  
        ]

    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

    # 육각형 도형 그리기
def create_hexagon(event=None):
    select_shape_color()
    canvas.bind("<Button-1>", start_hexagon)

# 육각형 도형 시작점 지정 및 그리기 함수 호출
def start_hexagon(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_hexagon(event))
    canvas.bind("<ButtonRelease-1>", finish_hexagon)

"""
육각형 그리기 함수
mid_x : 각 변의 중점의 x 좌표
mid_y : 각 변의 중점의 y 좌표
x : 각 꼭짓점의 x 좌표
y : 각 꼭짓점의 y 좌표
"""
def draw_hexagon(event):
    global start_x, start_y, current_shape
    canvas.delete("temp_shape")
    mid_x = (start_x + event.x) / 2
    mid_y = (start_y + event.y) / 2

    # 육각형 꼭짓점 계산
    points = []
    for i in range(6):
        angle = (2 * math.pi / 6) * i
        x = mid_x + math.cos(angle) * (event.x - start_x) / 2
        y = mid_y + math.sin(angle) * (event.y - start_y) / 2
        points.extend([x, y])
    current_shape = canvas.create_polygon(points, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

# 육각형 그리기 종료
def finish_hexagon(event):
    global current_shape
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_shape:
        canvas.itemconfig(current_shape, tags="")

#모양 선택하는 팝업 메뉴
def choose_shape(event):
    popup = Menu(labelframe_additional, tearoff=0)
    popup.add_command(label="Rectangle", command=lambda: create_rectangle(event))
    popup.add_command(label="Triangle", command=lambda: create_triangle(event))
    popup.add_command(label="Circle", command=lambda: create_circle(event))
    popup.add_command(label="Star", command=lambda: create_star(event))
    popup.add_command(label="Six Pointed Star", command=lambda: create_six_pointed_star(event))
    popup.add_command(label="Heart", command=lambda: create_heart(event))
    popup.add_command(label="Cross", command=lambda: create_cross(event))
    popup.add_command(label="Diamond", command=lambda: create_diamond(event))
    popup.add_command(label="Arrow", command=lambda: create_arrow(event))
    popup.add_command(label="V", command=lambda: create_V(event))
    popup.add_command(label="Hexagon", command=lambda: create_hexagon(event))
    popup.add_command(label="Pentagon", command=lambda: create_pentagon(event))
    popup.post(event.x_root, event.y_root)  # 이벤트가 발생한 위치에 팝업 메뉴 표시


def get_canvas_resolution(canvas):
    # 캔버스의 해상도(너비와 높이)를 반환하는 함수
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    return width, height

def print_canvas_resolution(canvas):
    # 캔버스의 해상도(너비와 높이)를 출력하는 함수
    width, height = get_canvas_resolution(canvas)
    print("Canvas resolution:", width, "x", height)

"""
그림그리는 것을 획 단위로 그리도록 개선, 획 단위로 지우는 지우개 기능 추가, 지웠던 획을 다시 되돌리는 기능 추가
그림그리는 것을 획 단위로 그리도록 개선하였으며, 마우스 클릭 후 놓을 때 까지를 한 획으로 보았다.
이를 최근에 그린 획을 지우는 기능을 추가하였으며, 지웠던 획을 다시 되돌리도록 하는 기능을 구현하였다.
지웠던 획들 다시 되돌리는 것은 획 지우기 기능을 이용해 지웠던 경우에만 한함
"""
strokes = [] #획을 담아 둠
current_stroke = []
redo_strokes = []

def paint_start(event): #획 시작
    global x1, y1, current_stroke
    x1, y1 = canvas.canvasx(event.x), canvas.canvasy(event.y)
    current_stroke = []

def paint_stroke(event): #획 그림
    global x1, y1, current_stroke
    x2, y2 = canvas.canvasx(event.x), canvas.canvasy(event.y)
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size, capstyle=ROUND)
    current_stroke.append((x1, y1, x2, y2))
    x1, y1 = x2, y2
    # 작업 내역 추적
    set_modified()

def paint_end(event): #획 끝
    global current_stroke
    strokes.append(list(current_stroke))
    current_stroke.clear()

def erase_last_stroke(event=None): #마지막으로 그린 획을 지움
    if strokes:
        last_stroke = strokes.pop()
        redo_strokes.append(last_stroke)
        for line in last_stroke:
            canvas.create_line(*line, fill="white", width=brush_size)

def rewrite_last_stroke(event=None): #마지막으로 지운 획을 다시 그림
    if redo_strokes:
        last_redo_stroke = redo_strokes.pop()
        strokes.append(last_redo_stroke)
        for line in last_redo_stroke:
            canvas.create_line(*line, fill=brush_color, width=brush_size)

def start_new_line(event):
    global last_x, last_y
    last_x, last_y = None, None

# 이중실선 브러쉬 함수
def double_line_paint(event, canvas):
    global last_x, last_y
    spacing = brush_size  # 두 선 사이의 간격 설정
    if last_x is not None and last_y is not None:
        # 마지막 위치와 현재 위치 사이의 각도 계산
        angle = math.atan2(event.y - last_y, event.x - last_x)
        # 각도에 따라 선 사이의 수직 거리를 계산하여 두 선의 시작점과 끝점을 결정
        dx = math.cos(angle + math.pi / 2) * spacing
        dy = math.sin(angle + math.pi / 2) * spacing

        # 첫 번째 선 그리기
        canvas.create_line(last_x - dx, last_y - dy, event.x - dx, event.y - dy, width=brush_size, fill=brush_color, capstyle=ROUND)
        # 두 번째 선 그리기
        canvas.create_line(last_x + dx, last_y + dy, event.x + dx, event.y + dy, width=brush_size, fill=brush_color, capstyle=ROUND)

        last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

# 패턴을 그리는 함수들 추가
def draw_tile_pattern(canvas, tile_size=50):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for x in range(0, canvas_width, tile_size):
        for y in range(0, canvas_height, tile_size):
            canvas.create_rectangle(x, y, x + tile_size, y + tile_size, outline="black")

def draw_wave_pattern(canvas, wave_length=50, amplitude=20):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for y in range(0, canvas_height, wave_length):
        for x in range(0, canvas_width, wave_length):
            canvas.create_arc(x, y, x + wave_length, y + wave_length, start=0, extent=180, style=ARC)
            canvas.create_arc(x, y + amplitude, x + wave_length, y + wave_length + amplitude, start=180, extent=180, style=ARC)

def draw_diagonal_pattern(canvas, line_spacing=50):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    for x in range(0, canvas_width, line_spacing):
        canvas.create_line(x, 0, 0, x, fill="black")
        canvas.create_line(canvas_width - x, canvas_height, canvas_width, canvas_height - x, fill="black")
    for y in range(0, canvas_height, line_spacing):
        canvas.create_line(0, y, y, 0, fill="black")
        canvas.create_line(canvas_width, canvas_height - y, canvas_width - y, canvas_height, fill="black")

def draw_grid(canvas, step):
    canvas.delete("grid_line") #새로 grid를 그리기 위해 기존 grid를 삭제
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for x in range(0, width, step):
        canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid_line")
    for y in range(0, height, step):
        canvas.create_line(0, y, width, y, fill="lightgray", tags="grid_line")

def toggle_grid(canvas):
    if canvas.find_withtag("grid_line"):
        canvas.delete("grid_line")
    else:
        draw_grid(canvas, 50)

def change_grid_spacing(value):
    draw_grid(canvas, value)

def change_grid_spacing(value):
    draw_grid(canvas, value)

class GridDialog:
    def __init__(self, window):
        self.top = Toplevel(window)
        self.top.title("Grid scale")

        Label(self.top, text="그리드 간격:").pack()
        self.gridscale_slider = Scale(self.top, from_=50, to=100, resolution=5, orient=HORIZONTAL)
        self.gridscale_slider.set(50)
        self.gridscale_slider.pack()

        self.ok_button = Button(self.top, text="OK", command=self.ok)
        self.ok_button.pack()

        self.cancel_button = Button(self.top, text="Cancel", command=self.cancel)
        self.cancel_button.pack()

        self.result = None

    def ok(self):
        self.result = self.gridscale_slider.get()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

def open_grid_dialog():
    dialog = GridDialog(window)  # GridDialog 인스턴스 생성
    window.wait_window(dialog.top)  # 다이얼로그 창이 닫힐 때까지 대기
    grid_spacing = dialog.result  # 사용자가 선택한 그리드 간격 가져오기
    if grid_spacing is not None:
        global grid_spacing_global # 전역 변수로 그리드 간격 설정 (수정)
        grid_spacing_global = grid_spacing
        window.bind("<Configure>", on_window_grid) # 윈도우 크기 변경 이벤트 핸들러 등록
"""
on_window_grid : 윈도우 크기가 변경될 때마다 호출되는 이벤트 핸들러

@Param
    event : 이벤트 객체 (윈도우 크기 변경 이벤트에 반응)
@Return
    None
"""
def on_window_grid(event):
    global grid_spacing_global  # 전역 변수로부터 그리드 간격 가져오기
    draw_grid(canvas, grid_spacing_global)  # 윈도우 크기가 변경될 때마다 그리드 다시 그리기

"""
눈금자를 그리는 기능
ruler_lines : 눈금자의 선을 저장하는 리스트
ruler_text : 눈금자의 텍스트(숫자)를 저장하는 리스트
try문을 통해 int형 데이터가 아닌 다른 데이터가 들어올 경우(ValueError) 간격을 10(기본값)으로 조정
interval : 격자의 간격 변수
5번째로 생성된 눈금에 숫자 표기 및 크기 증가
눈금자을 생성할 시 각 리스트에 눈금 선과 숫자값을 저장
"""


def draw_ruler():
    global ruler_lines, ruler_texts
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    try:
        interval = int(interval_entry.get())
    except ValueError:
        interval = 10

    # 상단 눈금자 그리기
    for x in range(0, canvas_width, interval):
        if x % (interval * 5) == 0:
            line = canvas.create_line(x, 0, x, 15, fill="black")
            text = canvas.create_text(x, 25, text=str(x), anchor=N)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = canvas.create_line(x, 0, x, 10, fill="black")
            ruler_lines.append(line)

    # 좌측 눈금자 그리기
    for y in range(0, canvas_height, interval):
        if y % (interval * 5) == 0:
            line = canvas.create_line(0, y, 15, y, fill="black")
            text = canvas.create_text(25, y, text=str(y), anchor=W)
            ruler_lines.append(line)
            ruler_texts.append(text)
        else:
            line = canvas.create_line(0, y, 10, y, fill="black")
            ruler_lines.append(line)

"""
clear_ruler : 눈금자를 지우는 함수
리스트 내의 요소를 전부 제거한 후 리스트 초기화
toggle_ruler
ruler_on : 눈금자가 활성화되어 있는 지 확인하는 변수
눈금자가 켜져 있을 경우 clear_ruler() 함수를 호출
아닐 경우 draw_ruler() 함수를 호출
on_resize : 위젯의 크기가 변경될 경우 눈금자 재생성
<Configure> : 크기가 변경될 경우
"""
def clear_ruler():
    global ruler_lines, ruler_texts
    for item in ruler_lines + ruler_texts:
        canvas.delete(item)
    ruler_lines.clear()
    ruler_texts.clear()

def toggle_ruler():
    global ruler_on
    if ruler_on:
        clear_ruler()
    else:
        draw_ruler()
    ruler_on = not ruler_on

def on_resize(event):
    if ruler_on:
        clear_ruler()
        draw_ruler()

def on_closing():
    # 프로그램 종료 시 호출되는 함수
    global is_modified
    if is_modified:
        if messagebox.askokcancel("Quit", "그림을 저장하시겠습니까?"):
            save_canvas(canvas)  # 저장 함수 호출
    window.destroy()

def get_image_size(file_path):
    # 파일 경로가 주어졌을 때 해당 파일의 용량을 반환합니다.
    # 파일이 존재하지 않을 경우 0을 반환합니다.
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return size
    else:
        print("File not found.")
        return 0

def get_canvas_size(canvas):
    # 캔버스를 PostScript 파일로 저장하여 용량을 측정합니다.
    temp_file = "temp_canvas.ps"
    canvas.postscript(file=temp_file)
    size = get_image_size(temp_file)
    os.remove(temp_file)  # 임시 파일 삭제
    return size

def print_image_size(file_path):
    # 이미지 파일의 경로가 주어졌을 때 해당 이미지 파일의 용량을 출력합니다.
    size = get_image_size(file_path)
    print("Image size:", size, "bytes")

def print_canvas_size(canvas):
    # 캔버스의 용량을 출력하는 함수입니다.
    size = get_canvas_size(canvas)
    print("Canvas size:", size, "bytes")

is_modified = False

def set_modified():
    # 사용자의 작업 내역이 발생할 때마다 호출되어 is_modified 변수를 True로 설정한다
    global is_modified
    is_modified = True



window = Tk()
#Tk 객체를 생성하여 주 윈도우를 만들기
version = "1.0.0"  # 프로그램 버전
window.title(f"그림판 v{version}")
window.geometry("1280x960+200+200")
window.resizable(True, True)
window.configure(bg="sky blue") #구별하기 위한 버튼 영역 색 변경
setup_paint_app(window)
editor = ImageEditor(canvas)

# 타이머 라벨
timer_label = Label(labelframe_timer, text="Time: 0 s")
timer_label.pack(side=RIGHT)


#작업 시작 시간 기능
def format_time(hours, minutes): #시간과 분을 매개변수로 받아 시간: 분 형태로 보여줌
    return f"{hours:02}:{minutes:02}"


current_time = time.localtime() 
initial_hours = current_time.tm_hour
initial_minutes = current_time.tm_min 

time_label = Label(labelframe_timer, text=f"작업시작 시간: {format_time(initial_hours, initial_minutes)}")
time_label.pack()

# 에어브러쉬 속성 변수 생성
dot_count = IntVar()
dot_count.set(10)

dot_distance = IntVar()
dot_distance.set(10)

frame_distance = Frame(window)
frame_distance.pack(side=RIGHT)

frame_count = Frame(window)
frame_count.pack(side=RIGHT)

# 눈금자 기본 설정
ruler_on = False
ruler_lines = []
ruler_texts = []

# 오른쪽 버튼 드래그 이벤트 바인딩
canvas.bind("<ButtonPress-3>", start_move)
canvas.bind("<B3-Motion>", move)
canvas.bind("<ButtonRelease-3>", end_move)

# 눈금자 간격 입력 레이블
interval_label = Label(labelframe_additional2, text="Ruler Interval:")
interval_label.pack()

interval_entry = Entry(labelframe_additional2)
interval_entry.pack()
interval_entry.insert(0, "10")  # 기본값 설정

canvas.bind("<Configure>", on_resize)

bind_shortcuts_window(window)

window.protocol("WM_DELETE_WINDOW", on_closing)

#프로그램 시작 시 타이머 시작
timer.start()
update_timer()

window.mainloop()
