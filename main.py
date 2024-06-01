from tkinter import *
import time
import math
import random
from tkinter.colorchooser import askcolor
from tkinter import filedialog, PhotoImage
from brush_settings import change_brush_size, change_bg_color, change_brush_color, set_brush_mode, set_paint_mode_normal, set_paint_mode_pressure, paint_start, paint, dotted_paint
from fun_timer import Timer
from picture import ImageEditor

# 초기 설정 값들
global brush_size, brush_color, brush_mode, last_x, last_y, x1, y1, canvas, strokes, current_stroke, redo_strokes, selected_shape
brush_size = 1
brush_color = "black"
brush_mode = "solid"
last_x, last_y = None, None
x1, y1 = None, None
strokes = []
current_stroke = []
redo_strokes = []
selected_shape = None

# 타이머 객체 생성
timer = Timer()

# 타이머의 경과 시간 업데이트
def update_timer():
    elapsed_time = timer.get_elapsed_time()
    timer_label.config(text=f"Time: {int(elapsed_time)} s")
    window.after(1000, update_timer)

# 타이머 멈춤
def stop_timer():
    timer.stop()

# 타이머 리셋
def reset_timer():
    timer.reset()
    if not timer.running:
        timer.start()

# 초기 설정
def setup_paint_app(window):
    global brush_size, brush_color, canvas

    brush_size = 1
    brush_color = "black"
    canvas = Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    button_frame = Frame(window, bg="sky blue")
    button_frame.pack(fill=X)

    # 타이머 멈춤 버튼
    button_stop_timer = Button(button_frame, text="Stop Timer", command=stop_timer)
    button_stop_timer.pack(side=RIGHT)

    # 타이머 리셋 버튼
    button_reset_timer = Button(button_frame, text="Reset Timer", command=reset_timer)
    button_reset_timer.pack(side=RIGHT)

    button_erase_last_stroke = Button(button_frame, text="Erase Last Stroke", command=erase_last_stroke)
    button_erase_last_stroke.pack(side=LEFT)

    button_redo_last_stroke = Button(button_frame, text="Rewrite Last Stroke", command=rewrite_last_stroke)
    button_redo_last_stroke.pack(side=LEFT)

    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.pack(side=LEFT)
    button_clear.bind("<Enter>", on_enter)
    button_clear.bind("<Leave>", on_leave)

    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)

    setup_reset_brush_button(window, canvas)

    button_brush = Button(window, text="Brush", command=choose_brush)
    button_brush.pack(side=RIGHT)
    button_brush.bind("<Enter>", on_enter)
    button_brush.bind("<Leave>", on_leave)

    text_box = Entry(window)
    text_box.pack(side=LEFT)
    canvas.bind("<Button-3>", lambda event: add_text(event, canvas, text_box))
    window.bind("<F11>", toggle_fullscreen)

    button_flip = Button(window, text="Flip Horizontal", command=lambda: flip_horizontal(canvas))
    button_flip.pack(side=LEFT)
    button_flip.bind("<Enter>", on_enter)
    button_flip.bind("<Leave>", on_leave)

    canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

    button_bg_color = Button(window, text="Change Background Color", command=lambda: change_bg_color(canvas))
    button_bg_color.pack(side=LEFT)
    button_bg_color.bind("<Enter>", on_enter)
    button_bg_color.bind("<Leave>", on_leave)

    button_brush_color = Button(window, text="Change Brush Color", command=lambda: change_brush_color(canvas))
    button_brush_color.pack(side=LEFT)
    button_brush_color.bind("<Enter>", on_enter)
    button_brush_color.bind("<Leave>", on_leave)

    button_save = Button(window, text="Save", command=lambda: save_canvas(canvas))
    button_save.pack(side=LEFT)

    button_upload_image = Button(window, text="Upload Image", command=upload_image)
    button_upload_image.pack(side=LEFT)

    button_choose_shape = Button(window, text="Shape", command=choose_shape)
    button_choose_shape.pack(side=LEFT)

    canvas.bind("<Enter>", change_cursor)
    canvas.bind("<Leave>", default_cursor)
    canvas.bind("<Button-3>", show_coordinates)
    canvas.bind("<ButtonRelease-3>", hide_coordinates)
    canvas.bind("<MouseWheel>", zoom)

    bind_shortcuts()

    dot_count = IntVar()
    dot_count.set(10)

    dot_distance = IntVar()
    dot_distance.set(10)

    frame_distance = Frame(window)
    frame_distance.pack(side=RIGHT)

    frame_count = Frame(window)
    frame_count.pack(side=RIGHT)

    Button(frame_distance, text="+", command=increase_dot_distance).pack(side=RIGHT)
    Label(frame_distance, text="Distance").pack(side=RIGHT)
    Label(frame_distance, textvariable=dot_distance).pack(side=RIGHT)
    Button(frame_distance, text="-", command=decrease_dot_distance).pack(side=RIGHT)

    Button(frame_count, text="+", command=increase_dot_count).pack(side=RIGHT)
    Label(frame_count, text="Count").pack(side=RIGHT)
    Label(frame_count, textvariable=dot_count).pack(side=RIGHT)
    Button(frame_count, text="-", command=decrease_dot_count).pack(side=RIGHT)

    button_paint_airbrush = Button(window, text="Airbrush", command=lambda: set_paint_mode_airbrush(canvas))
    button_paint_airbrush.pack(side=RIGHT)

    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint_stroke)
    canvas.bind("<ButtonRelease-1>", paint_end)

    set_paint_mode_normal(canvas)

    button_new_window = Button(window, text="새 창 열기", command=create_new_window)
    button_new_window.pack(side=LEFT)

# 새 창 열기 생성
def create_new_window():
    new_window = Toplevel(window)
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")
    setup_paint_app(new_window)

# 마우스 커서를 연필 형태로 변경하기
def change_cursor(event):
    canvas.config(cursor="pencil")

# 연필 형태 커서를 원래대로 변경하기
def default_cursor(event):
    canvas.config(cursor="")

# 우클릭을 누르면 우측 상단에 x, y 좌표값을 백분율로 표시
def show_coordinates(event):
    canvas.delete("coord_text")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_percent = (event.x / width) * 100
    y_percent = (event.y / height) * 100
    coord_text = f"<{x_percent:.1f}% / {100-y_percent:.1f}%>"
    canvas.create_text(10, 10, text=coord_text, anchor="nw", tags="coord_text")

# 우클릭을 떼면 좌표값 삭제
def hide_coordinates(event):
    canvas.delete("coord_text")

# 브러시 선택하는 팝업 메뉴
def choose_brush():
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Solid Brush", command=lambda: set_brush_mode(canvas, "solid"))
    popup.add_command(label="Dotted Brush", command=lambda: set_brush_mode(canvas, "dotted"))
    popup.add_command(label="Pressure Brush", command=lambda: set_paint_mode_pressure(canvas))
    popup.add_command(label="Normal Brush", command=lambda: set_paint_mode_normal(canvas))
    popup.post(window.winfo_pointerx(), window.winfo_pointery())

# 사각형 그리기
def create_rectangle():
    global selected_shape
    selected_shape = "rectangle"
    canvas.bind("<Button-1>", start_shape)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", end_shape)

# 삼각형 그리기
def create_triangle():
    global selected_shape
    selected_shape = "triangle"
    canvas.bind("<Button-1>", start_shape)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", end_shape)

# 원형 그리기
def create_circle():
    global selected_shape
    selected_shape = "circle"
    canvas.bind("<Button-1>", start_shape)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", end_shape)

# 도형 그릴 위치 정하고 생성하는 함수 호출
def start_shape(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

# 도형 그리기
def draw_shape(event):
    global start_x, start_y
    canvas.delete("temp_shape")
    if selected_shape == "rectangle":
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black", fill="white", tags="temp_shape")
    elif selected_shape == "triangle":
        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        x3, y3 = x1 + (x2 - x1) / 2, y1 - (y2 - y1)
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill="white", tags="temp_shape")
    elif selected_shape == "circle":
        r = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
        canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline="black", fill="white", tags="temp_shape")

# 도형 그리기 종료
def end_shape(event):
    global start_x, start_y
    if selected_shape == "rectangle":
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black", fill="white")
    elif selected_shape == "triangle":
        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        x3, y3 = x1 + (x2 - x1) / 2, y1 - (y2 - y1)
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", fill="white")
    elif selected_shape == "circle":
        r = ((start_x - event.x)**2 + (start_y - event.y)**2)**0.5
        canvas.create_oval(start_x - r, start_y - r, start_x + r, start_y + r, outline="black", fill="white")

    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

# 모양 선택하는 팝업 메뉴
def choose_shape():
    popup = Menu(window, tearoff=0)
    popup.add_command(label="Rectangle", command=create_rectangle)
    popup.add_command(label="Triangle", command=create_triangle)
    popup.add_command(label="Circle", command=create_circle)
    popup.post(window.winfo_pointerx(), window.winfo_pointery())

def select_shape(shape):
    global selected_shape
    selected_shape = shape

def paint_start(event):
    global x1, y1, current_stroke
    x1, y1 = event.x, event.y
    current_stroke = []

def paint_stroke(event):
    global x1, y1, current_stroke
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    current_stroke.append((x1, y1, x2, y2))
    x1, y1 = x2, y2

def paint_end(event):
    global current_stroke
    strokes.append(list(current_stroke))
    current_stroke.clear()

def erase_last_stroke():
    if strokes:
        last_stroke = strokes.pop()
        redo_strokes.append(last_stroke)
        for line in last_stroke:
            canvas.create_line(*line, fill="white", width=brush_size)

def rewrite_last_stroke():
    if redo_strokes:
        last_redo_stroke = redo_strokes.pop()
        strokes.append(last_redo_stroke)
        for line in last_redo_stroke:
            canvas.create_line(*line, fill=brush_color, width=brush_size)

# 에어브러쉬 기능
def paint_airbrush(event, canvas):
    for _ in range(dot_count.get()):
        radius = random.randint(1, brush_size)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, dot_distance.get())
        x = event.x + distance * math.cos(angle)
        y = event.y + distance * math.sin(angle)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=brush_color, outline=brush_color)

def increase_dot_count():
    dot_count.set(dot_count.get() + 1)

def decrease_dot_count():
    dot_count.set(max(dot_count.get() - 1, 1))

def increase_dot_distance():
    dot_distance.set(dot_distance.get() + 1)

def decrease_dot_distance():
    dot_distance.set(max(dot_distance.get() - 1, 0))

def bind_shortcuts():
    window.bind("<c>", lambda event: clear_paint(canvas))

def set_paint_mode_airbrush(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint_airbrush(event, canvas))

def set_paint_mode_normal(canvas):
    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint_stroke)
    canvas.bind("<ButtonRelease-1>", paint_end)

def set_brush_mode(canvas, mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))

def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", lambda event: start_paint_pressure(event, canvas))
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event, canvas):
    global start_time
    start_time = time.time()

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint(event, canvas):
    global last_x, last_y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, event.x, event.y, fill=brush_color, width=brush_size, capstyle=ROUND, smooth=TRUE)
    last_x, last_y = event.x, event.y

def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = brush_size
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

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def zoom(event):
    scale = 1.0
    if event.delta > 0:
        scale = 1.1
    elif event.delta < 0:
        scale = 0.9
    canvas.scale("all", event.x, event.y, scale, scale)

def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

def add_text(event, canvas, text_box):
    text = text_box.get()
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

def toggle_fullscreen(event):
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

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

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color(canvas):
    bg_color = askcolor()
    if bg_color[1]:
        canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    color = askcolor()
    if color[1]:
        brush_color = color[1]

def save_canvas(canvas):
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

def reset_brush(canvas):
    global brush_size, brush_color
    brush_size = 1
    brush_color = "black"
    change_brush_size(brush_size)
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))

def setup_reset_brush_button(window, canvas):
    button_reset = Button(window, text="Reset Brush", command=lambda: reset_brush(canvas))
    button_reset.pack(side=LEFT)
    button_reset.bind("<Enter>", on_enter)
    button_reset.bind("<Leave>", on_leave)

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

window = Tk()
window.title("그림판")
window.geometry("800x600+200+200")
window.resizable(True, True)
window.configure(bg="sky blue")
setup_paint_app(window)

timer_label = Label(window, text="Time: 0 s")
timer_label.pack(side=RIGHT)

dot_count = IntVar()
dot_count.set(10)

dot_distance = IntVar()
dot_distance.set(10)

frame_distance = Frame(window)
frame_distance.pack(side=RIGHT)

frame_count = Frame(window)
frame_count.pack(side=RIGHT)

timer.start()
update_timer()

window.mainloop()
