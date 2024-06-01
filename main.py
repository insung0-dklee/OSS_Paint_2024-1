"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time #시간 계산을 위한 모듈
import brush_settings  # brush_settings 모듈 임포트
from brush_settings import change_brush_size, change_bg_color, change_brush_color, set_brush_mode, set_paint_mode_normal, set_paint_mode_pressure, paint_start, paint, dotted_paint
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
from tkinter import filedialog
from tkinter import PhotoImage
import math  # 수학 모듈을 가져옴
import random
from fun_timer import Timer
from picture import ImageEditor #이미지 모듈을 가져옴


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
        image = PhotoImage(file=path)
        canvas.create_image(0, 0, anchor=NW, image=image)
        canvas.image = image

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

    # 맞춤형 단축키 기능 추가
def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(canvas))
# brush_settings.initialize_globals(globals())

def set_paint_mode_airbrush(canvas): #에어브러쉬 그리기 모드로 전환하는 기능
    canvas.bind("<B1-Motion>", paint_airbrush)

def set_paint_mode_normal(canvas, set_origin_mode=False):
    canvas.bind("<B1-Motion>", paint_stroke)
    if set_origin_mode:
        # 추가적인 원점 모드 설정 코드
        pass
    
def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event, canvas):
    global start_time
    start_time = time.time() #마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵가는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    canvas.create_oval(last_x - 1, last_y - 1, last_x + 1, last_y + 1, fill=brush_color, outline=brush_color)

def paint(event, canvas):
    global last_x, last_y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, event.x, event.y, fill=brush_color, width=brush_size, capstyle=ROUND, smooth=TRUE)
    last_x, last_y = event.x, event.y

# 점선 브러쉬 함수
def dotted_paint(event, canvas):
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

"""
set_brush_mode: 브러쉬 모드를 변경하는 함수
실선 브러쉬와 점선 브러쉬로 전환한다.
매개변수: mode - 브러쉬 모드를 나타내는 문자열 ("solid" 또는 "dotted")
"""
def set_brush_mode(canvas, mode): # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":  # 브러쉬 모드가 solid면
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))  # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted":  # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))  # 점선 브러쉬로 변경

# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# 화면 확대 및 축소 기능 추가
def zoom(event):
    scale = 1.0
    if event.delta > 0:  # 마우스 휠을 위로 스크롤하면 확대
        scale = 1.1
    elif event.delta < 0:  # 마우스 휠을 아래로 스크롤하면 축소
        scale = 0.9
    canvas.scale("all", event.x, event.y, scale, scale)

#all clear 기능 추가
def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None # 마지막 좌표 초기화

def add_text(event, canvas, text_box):# 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.

    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
   

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
            if i % 2 == 0:  # x 좌표를 반전시킵니다.
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

# 캔버스를 파일로 저장하는 함수
def save_canvas(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

def reset_brush(canvas):
    global brush_size, brush_color
    brush_size = 1  # 초기 브러시 크기
    brush_color = "black"  # 초기 브러시 색상
    change_brush_size(brush_size)  # 브러시 크기 조정
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))  # 브러시 모드 초기화


def setup_reset_brush_button(window, canvas):
    button_reset = Button(window, text="Reset Brush", command=lambda: reset_brush(canvas))
    button_reset.pack(side=LEFT)
    button_reset.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_reset.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

def setup_paint_app(window):
    global brush_size, brush_color

    brush_size = 1  # 초기 브러시 크기
    brush_color = "black"  # 초기 브러시 색상

    global canvas
    canvas = Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    last_x, last_y = None, None  # 마지막 좌표 초기화
    brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정

    button_frame = Frame(window,bg="sky blue")#구별하기 위한 버튼 영역 색 변경
    button_frame.pack(fill=X)

    # 타이머 멈춤 버튼
    button_stop_timer = Button(button_frame, text="Stop Timer", command=stop_timer)
    button_stop_timer.pack(side=RIGHT)

    #타이머 리셋 버튼
    button_reset_timer = Button(button_frame, text="Reset Timer", command=reset_timer)
    button_reset_timer.pack(side=RIGHT)

    
    button_erase_last_stroke = Button(button_frame, text="Erase Last Stroke", command=erase_last_stroke)
    button_erase_last_stroke.pack(side=LEFT)

    button_redo_last_stroke = Button(button_frame, text="Rewrite Last Stroke", command=rewrite_last_stroke)
    button_redo_last_stroke.pack(side=LEFT)

    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.pack(side=LEFT)
    button_clear.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_clear.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록


    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)


    button_solid = Button(button_frame, text="Solid Brush", command=lambda: set_brush_mode(canvas, "solid"))
    button_solid.pack()
    button_solid.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_solid.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: set_brush_mode(canvas, "dotted"))
    button_dotted.pack()
    button_dotted.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_dotted.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    setup_reset_brush_button(window, canvas)  # Reset 버튼 추가



    button_paint = Button(window, text="normal", command=lambda: set_paint_mode_normal(canvas))
    button_paint.pack(side=RIGHT)
    button_paint.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_paint.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    button_paint = Button(window, text="pressure", command=lambda: set_paint_mode_pressure(canvas))
    button_paint.pack(side=RIGHT)
    button_paint.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_paint.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    text_box = Entry(window)
    text_box.pack(side=LEFT)
    canvas.bind("<Button-3>", lambda event: add_text(event, canvas, text_box))
    window.bind("<F11>", toggle_fullscreen)

    button_flip = Button(window, text="Flip Horizontal", command=lambda: flip_horizontal(canvas))
    button_flip.pack(side=LEFT)
    button_flip.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_flip.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

    button_bg_color = Button(window, text="Change Background Color", command=lambda: change_bg_color(canvas))
    button_bg_color.pack(side=LEFT)
    button_bg_color.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_bg_color.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    button_brush_color = Button(window, text="Change Brush Color", command=lambda: change_brush_color(canvas))
    button_brush_color.pack(side=LEFT)
    button_brush_color.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_brush_color.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    # 버튼 프레임에 저장 버튼 추가
    button_save = Button(window, text="Save", command=lambda: save_canvas(canvas))
    button_save.pack(side=LEFT)

    button_upload_image = Button(window, text="Upload Image", command=upload_image)
    button_upload_image.pack(side=LEFT)

    #도형 모양 선택하는 버튼 생성
    button_choose_shape = Button(window, text="shape", command=choose_shape)
    button_choose_shape.bind("<Button-1>", choose_shape)  # 버튼 클릭 시 모양 선택 팝업 메뉴 표시
    button_choose_shape.pack(side=LEFT)

    canvas.bind("<Enter>", change_cursor)
    canvas.bind("<Leave>", default_cursor)

    canvas.bind("<Button-3>", show_coordinates)
    canvas.bind("<ButtonRelease-3>", hide_coordinates)

    canvas.bind("<MouseWheel>", zoom)

    bind_shortcuts()

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
    Button(frame_distance, text="+", command=increase_dot_distance).pack(side=RIGHT)
    Label(frame_distance, text="Distance").pack(side=RIGHT)
    Label(frame_distance, textvariable=dot_distance).pack(side=RIGHT)  # 거리 표시
    Button(frame_distance, text="-", command=decrease_dot_distance).pack(side=RIGHT)

    Button(frame_count, text="+", command=increase_dot_count).pack(side=RIGHT)
    Label(frame_count, text="Count").pack(side=RIGHT)
    Label(frame_count, textvariable=dot_count).pack(side=RIGHT)  # 개수 표시
    Button(frame_count, text="-", command=decrease_dot_count).pack(side=RIGHT)

    button_paint = Button(window, text="airbrush", command=lambda: set_paint_mode_airbrush(canvas)) #에어브러쉬 그리기 모드로 전환하는 기능
    button_paint.pack(side=RIGHT)

    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint_stroke)
    canvas.bind("<ButtonRelease-1>", paint_end)

    set_paint_mode_normal(canvas)

    button_new_window = Button(window, text="새 창 열기", command=create_new_window)
    button_new_window.pack(side=LEFT)

# 새 창 열기 생성
def create_new_window():
    new_window = Toplevel(window)  # 새로운 Toplevel 인스턴스 생성
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")  # 구별하기 위한 버튼 영역 색 변경
    new_window.minsize(1300,400)  # 최소 크기 설정
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

#사각형 그리기    
def create_rectangle(event):
    canvas.bind("<Button-1>", start_rectangle)
#삼각형 그리기
def create_triangle(event):
    canvas.bind("<Button-1>", start_triangle)
#원형 그리기
def create_circle(event):
    canvas.bind("<Button-1>", start_circle)

#사각형 그릴 위치 정하고 생성하는 함수 호출
def start_rectangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_rectangle(event))
#사각형 생성하기
def draw_rectangle(event):
    global start_x, start_y, current_shape
    canvas.delete(current_shape)
    current_shape = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black", fill="white")

#삼각형 그릴 위치 정하고 생성하는 함수 호출
def start_triangle(event):
    global start_x, start_y, current_triangle
    start_x, start_y = event.x, event.y
    current_triangle = None
    canvas.bind("<B1-Motion>", draw_triangle)
    canvas.bind("<ButtonRelease-1>", finish_triangle)
#삼각형 생성하기
def draw_triangle(event):
    global start_x, start_y, current_triangle
    if current_triangle:
        canvas.delete(current_triangle)
    current_triangle = canvas.create_polygon(start_x, start_y, event.x, start_y, event.x, event.y, outline="black", fill="white")
#삼각형 그리기 종료
def finish_triangle(event):
    global current_triangle
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if current_triangle:
        canvas.delete(current_triangle)
        canvas.create_polygon(start_x, start_y, event.x, start_y, event.x, event.y, outline="black", fill="white")

#원형 그릴 위치 정하고 생성하는 함수 호출
def start_circle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_shape = None
    canvas.bind("<B1-Motion>", lambda event: draw_circle(event))
#원형 생성하기
def draw_circle(event):
    global start_x, start_y, current_shape
    canvas.delete(current_shape)
    r = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
    current_shape = canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline="black", fill="white")

#모양 선택하는 팝업 메뉴
def choose_shape(event):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Rectangle", command=lambda: create_rectangle(event))
    popup.add_command(label="Triangle", command=lambda: create_triangle(event))
    popup.add_command(label="Circle", command=lambda: create_circle(event))
    popup.post(event.x_root, event.y_root)  # 이벤트가 발생한 위치에 팝업 메뉴 표시

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
    x1, y1 = event.x, event.y
    current_stroke = []

def paint_stroke(event): #획 그림
    global x1, y1, current_stroke
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    current_stroke.append((x1, y1, x2, y2))
    x1, y1 = x2, y2

def paint_end(event): #획 끝
    global current_stroke
    strokes.append(list(current_stroke))
    current_stroke.clear()

def erase_last_stroke(): #마지막으로 그린 획을 지움
    if strokes:
        last_stroke = strokes.pop()
        redo_strokes.append(last_stroke)
        for line in last_stroke:
            canvas.create_line(*line, fill="white", width=brush_size)

def rewrite_last_stroke(): #마지막으로 지운 획을 다시 그림
    if redo_strokes:
        last_redo_stroke = redo_strokes.pop()
        strokes.append(last_redo_stroke)
        for line in last_redo_stroke:
            canvas.create_line(*line, fill=brush_color, width=brush_size)


window = Tk()
#Tk 객체를 생성하여 주 윈도우를 만들기
window.title("그림판")
window.geometry("800x600+200+200")
window.minsize(1300, 400)  # 최소 크기 설정
window.resizable(True, True)
window.configure(bg="sky blue") # 구별하기 위한 버튼 영역 색 변경
setup_paint_app(window)
editor = ImageEditor(canvas)

# 타이머 라벨
timer_label = Label(window, text="Time: 0 s")
timer_label.pack(side=RIGHT)


# 에어브러쉬 속성 변수 생성
dot_count = IntVar()
dot_count.set(10)

dot_distance = IntVar()
dot_distance.set(10)

frame_distance = Frame(window)
frame_distance.pack(side=RIGHT)

frame_count = Frame(window)
frame_count.pack(side=RIGHT)


#프로그램 시작 시 타이머 시작
timer.start()
update_timer()

window.mainloop()
