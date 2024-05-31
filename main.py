from tkinter import *
import time
from tkinter.colorchooser import askcolor
import math
from tkinter import filedialog  # 파일 다이얼로그를 위한 모듈 가져오기

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형 설정
current_color = "black"  # 기본 색상 설정
eraser_mode = False  # 지우개 모드 비활성화
spacing = 10  # 도형 사이 간격 설정
last_x, last_y = None, None  # 마지막 좌표 초기화

# 일반 페인트 모드 설정 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

# 압력 감지 페인트 모드 설정 함수
def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)
    canvas.bind("<B1-Motion>", paint_pressure)

# 압력 감지 페인트 시작 함수
def start_paint_pressure(event):
    global start_time
    start_time = time.time()

# 압력 감지 페인트 함수
def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

# 페인트 시작 지점 설정 함수
def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

# 페인트 함수
def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=2)
    x1, y1 = x2, y2

# 점선 페인트 함수
def dotted_paint(event):
    global last_x, last_y
    spacing = 10
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

# 브러시 모드 설정 함수
def set_brush_mode(mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", paint)
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)

# 브러시 크기 변경 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# 그림판 초기화 함수
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

# 텍스트 추가 함수
def add_text(event):
    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

# 전체 화면 전환 함수
def toggle_fullscreen(event):
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

# 좌우 반전 함수
def flip_horizontal():
    objects = canvas.find_all()
    canvas.update()
    canvas_width = canvas.winfo_width()
    for obj in objects:
        coords = canvas.coords(obj)
        for i in range(len(coords)):
            if i % 2 == 0:
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)

# 지우개 함수
def erase(event):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

# 배경 색상 변경 함수
def change_bg_color():
    bg_color = askcolor()
    if bg_color[1]:
        canvas.config(bg=bg_color[1])

# 브러시 색상 변경 함수
def change_brush_color():
    global brush_color
    new_color = askcolor()[1]
    if new_color:
        brush_color = new_color
        update_recent_colors(brush_color)

# 최근 색상 업데이트 함수
def update_recent_colors(new_color):
    if new_color in recent_colors:
        recent_colors.remove(new_color)
    recent_colors.append(new_color)
    if len(recent_colors) > 5:
        recent_colors.pop(0)
    update_color_buttons()

# 최근 색상 버튼 업데이트 함수
def update_color_buttons():
    for widget in recent_colors_frame.winfo_children():
        widget.destroy()
    for color in recent_colors:
        btn = Button(recent_colors_frame, bg=color, width=2, height=1, command=lambda col=color: set_brush_color(col))
        btn.pack(side=LEFT)

# 브러시 색상 설정 함수
def set_brush_color(color):
    global brush_color
    brush_color = color

# 캔버스 저장 함수
def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path + '.ps')
        from PIL import Image
        img = Image.open(file_path + '.ps')
        img.save(file_path)
        import os
        os.remove(file_path + '.ps')

# 새 창 열기 함수
def create_new_window():
    new_window = Tk()
    new_canvas = Canvas(new_window)
    new_canvas.pack()
    new_window.mainloop()

# Tk 객체 생성 및 초기 설정
window = Tk()
window.title("그림판")

brush_size = 1
canvas = Canvas(window, bg="white")
window.geometry("640x400+200+200")
window.resizable(True, True)
canvas.pack(fill="both", expand=True)

last_x, last_y = None, None
brush_mode = "solid"
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)

# 버튼 프레임 및 버튼 설정
button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
brush_size_slider.set(brush_size)
brush_size_slider.pack(side=LEFT)

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode("solid"))
button_solid.pack()

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))
button_dotted.pack()

button_paint = Button(window, text="normal", command=set_paint_mode_normal)
button_paint.pack(side=RIGHT)

button_paint = Button(window, text="pressure", command=set_paint_mode_pressure)
button_paint.pack(side=RIGHT)

text_box = Entry(window)
text_box.pack(side=LEFT)
canvas.bind("<Button-3>", add_text)
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window)
button_new_window.pack(side=LEFT)

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", erase)

brush_color = "black"

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_save = Button(button_frame, text="Save", command=save_canvas)
button_save.pack(side=LEFT)

# 최근 사용한 색상 프레임 및 초기 설정
recent_colors_frame = Frame(window)
recent_colors_frame.pack(fill=X)

button_recent_colors = Label(recent_colors_frame, text="Recent Colors:")
button_recent_colors.pack(side=LEFT)

recent_colors = []  # 최근 사용한 색상을 저장할 리스트
update_color_buttons()  # 초기 색상 버튼 업데이트

set_paint_mode_normal()

window.mainloop()
