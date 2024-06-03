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
from tkinter import messagebox
import math  # 수학 모듈을 가져옴
import random
from fun_timer import Timer
from picture import ImageEditor #이미지 모듈을 가져옴
from spray import SprayBrush #spray 모듈을 가지고 옴

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

#동적 브러시 설정을 위한 변수 초기화
dynamic_brush = False
previous_time = None
previous_x, previous_y = None, None

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

    # 맞춤형 단축키 기능 추가
def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(canvas)) #clear 단축키 c
    window.bind("<Control-s>", save_canvas) #save 단축키 crtl+s
    window.bind("<Control-z>", erase_last_stroke) #undo 단축키 crtl+z
# brush_settings.initialize_globals(globals())

def set_paint_mode_airbrush(canvas): #에어브러쉬 그리기 모드로 전환하는 기능
    canvas.bind("<B1-Motion>", lambda event: paint_airbrush(event, canvas))

def set_paint_mode_normal(canvas, set_origin_mode=False):
    canvas.bind("<Button-1>", lambda event: paint_start(event))
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
    elif brush_mode == "double_line": #브러쉬 모드가 double_line 면
        canvas.bind("<B1-Motion>", lambda event: double_line_paint(event, canvas))#이중 실선 브러쉬로 변경
        canvas.bind("<Button-1>", start_new_line)

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

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color(event=None):
    global brush_color
    selected_color = askcolor()[1]
    if selected_color:
        brush_color = selected_color
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

# 색 채우기 기능 추가
def flood_fill(event):
    fill_color = askcolor()[1]  # 색상 선택 대화 상자에서 색상을 선택
    x, y = event.x, event.y
    target = canvas.find_closest(x, y)
    if target:
        canvas.itemconfig(target, fill=fill_color)

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

    # setup_paint_app 함수에 마커 모드 버튼 추가
    button_marker = Button(button_frame, text="Marker Mode", command=lambda: set_paint_mode_marker(canvas))
    button_marker.pack(side=LEFT)
    button_marker.bind("<Enter>", on_enter)
    button_marker.bind("<Leave>", on_leave)

    # 팔레트 설정 버튼 생성 및 버튼 프레임에 추가
    button_palette = Button(button_frame, text="Set Palette", command=lambda: setup_palette(window))
    button_palette.pack(side=LEFT)

    # 타이머 멈춤 버튼
    button_stop_timer = Button(button_frame, text="Stop Timer", command=stop_timer)
    button_stop_timer.pack(side=RIGHT)

    #타이머 리셋 버튼
    button_reset_timer = Button(button_frame, text="Reset Timer", command=reset_timer)
    button_reset_timer.pack(side=RIGHT)

    start_button = Button(button_frame, text="Start", command=start_stop)
    start_button.pack(side = RIGHT)

    # 보조선을 토글하는 버튼
    button_toggle_grid = Button(window, text="Grid on/off", command=lambda: toggle_grid(canvas))
    button_toggle_grid.pack(side=LEFT)

    # 보조선 크기 설정
    button_grid_settings = Button(window, text="Grid setting", command=open_grid_dialog)
    button_grid_settings.pack()

    #spray 인스턴스 생성 
    spray_brush = SprayBrush(canvas, "black")
    # 스프레이 버튼
    button_spray = Button(window, text="spray", command=lambda: canvas.bind("<B1-Motion>", spray_brush.spray_paint))
    button_spray.pack(side=LEFT)

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

    button_double_line = Button(button_frame, text="Double line Brush", command=lambda: set_brush_mode(canvas,"double_line"))
    button_double_line.pack() 
    button_double_line.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_double_line.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

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

    button_brush_color = Button(window, text="Change Brush Color", command=lambda: change_brush_color())
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

#사각형 그리기    
def create_rectangle(event):
    select_shape_color()
    canvas.bind("<Button-1>", start_rectangle)
#삼각형 그리기
def create_triangle(event):
    select_shape_color()
    canvas.bind("<Button-1>", start_triangle)
#원형 그리기
def create_circle(event):
    select_shape_color()
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
    current_shape = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")
    paint_start(event)

#삼각형 그릴 위치 정하고 생성하는 함수 호출
def start_triangle(event):
    global start_x, start_y, current_shape
    start_x, start_y = event.x, event.y
    current_triangle = None
    canvas.bind("<B1-Motion>", draw_triangle)
    canvas.bind("<ButtonRelease-1>", finish_triangle)
#삼각형 생성하기
def draw_triangle(event):
    global start_x, start_y
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

    # 시작점과 세 개의 점으로 정삼각형 그리기
    current_shape = canvas.create_polygon(start_x, start_y, event.x, event.y, (start_x-event.x)+start_x, event.y, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

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
    current_shape = canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline=shape_outline_color, fill=shape_fill_color, tags="temp_shape")

#모양 선택하는 팝업 메뉴
def choose_shape(event):
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Rectangle", command=lambda: create_rectangle(event))
    popup.add_command(label="Triangle", command=lambda: create_triangle(event))
    popup.add_command(label="Circle", command=lambda: create_circle(event))
    popup.post(event.x_root, event.y_root)  # 이벤트가 발생한 위치에 팝업 메뉴 표시

# 마커 모드 추가
def paint_marker(event, canvas):
    radius = brush_size
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def set_paint_mode_marker(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint_marker(event, canvas))
    canvas.bind("<Button-1>", lambda event: paint_marker(event, canvas))

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

def erase_last_stroke(event=None): #마지막으로 그린 획을 지움
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
        canvas.create_line(last_x - dx, last_y - dy, event.x - dx, event.y - dy, width=brush_size, fill=brush_color)
        # 두 번째 선 그리기
        canvas.create_line(last_x + dx, last_y + dy, event.x + dx, event.y + dy, width=brush_size, fill=brush_color)

        last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

def draw_grid(canvas, step):
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
        draw_grid(canvas, grid_spacing)  # 사용자가 선택한 그리드 간격으로 그리드 다시 그리기


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



window = Tk()
#Tk 객체를 생성하여 주 윈도우를 만들기
version = "1.0.0"  # 프로그램 버전
window.title(f"그림판 v{version}")
window.geometry("800x600+200+200")
window.resizable(True, True)
window.configure(bg="sky blue") #구별하기 위한 버튼 영역 색 변경
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

# 눈금자 기본 설정
ruler_on = False
ruler_lines = []
ruler_texts = []

toggle_button = Button(window, text="Ruler", command=toggle_ruler)
toggle_button.pack()

# 눈금자 간격 입력 레이블
interval_label = Label(window, text="Ruler Interval:")
interval_label.pack()

interval_entry = Entry(window)
interval_entry.pack()
interval_entry.insert(0, "10")  # 기본값 설정

canvas.bind("<Configure>", on_resize)

bind_shortcuts_window(window)

#프로그램 시작 시 타이머 시작
timer.start()
update_timer()

window.mainloop()


import tkinter as tk

# 버튼을 눌러 도형을 오른쪽으로 이동시키는 애니메이션 기능
def start_animation(canvas):
    try:
        canvas.move("all", 5, 0)  # 캔버스에 있는 모든 객체를 오른쪽으로 5픽셀 이동시킵니다.
    except tk.TclError as e:
        print(f"Error: {e}")

def create_button(root, text, command):
    button = tk.Button(root, text=text, command=command)
    button.pack()
    return button

def _main():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    # 캔버스에 예제 객체 추가 (예: 직사각형)
    canvas.create_rectangle(50, 50, 150, 150, fill="pink")

    start_button = create_button(root, "Start Animation", lambda: start_animation(canvas))

    root.mainloop()

"""if __name__ == "__main__":
    _main()
"""
"""
이 스크립트가 직접 실행될 경우에만 _main() 함수를 호출합니다.
이 구문은 스크립트가 직접 실행되는 상황과 모듈로 임포트되어 사용되는 상황을 구분하기 위해 사용됩니다.
만약 이 스크립트가 다른 Python 파일에서 import되어 사용된다면, _main() 함수는 실행되지 않습니다.
이 방식을 통해, 스크립트가 모듈로 사용될 때는 필요한 클래스나 함수만을 제공하고,
스크립트가 직접 실행될 때만 특정 로직(여기서는 _main() 함수 내의 로직)을 실행할 수 있습니다.
"""

# 물방울 모양 브러쉬 추가
def draw_droplet(canvas, x, y):
    """
    주어진 위치에 물방울 모양을 그립니다.
    """
    # 물방울 본체 (타원)
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", outline="blue")
    # 물방울 꼬리 (삼각형)
    points = [x, y - 20, x - 10, y - 5, x + 10, y - 5]
    canvas.create_polygon(points, fill="blue", outline="blue")

def on_drag(event):
    """
    마우스 드래그 이벤트를 처리합니다.
    """
    draw_droplet(canvas, event.x, event.y)

# 기능 추가만 해두고 실행하지 않음, 실행 예시
# root = tk.Tk()
# root.title("Water Droplet Brush")
#
# canvas = tk.Canvas(root, width=400, height=400)
# canvas.pack()
#
# # 마우스 드래그 이벤트와 on_drag 함수를 연결
# canvas.bind("<B1-Motion>", on_drag)
#
# root.mainloop()
