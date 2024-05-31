from tkinter import *
from tkinter.colorchooser import askcolor
import time

# 초기 설정 값들
selected_shape = "oval"
current_color = "black"
eraser_mode = False
spacing = 10
last_x, last_y = None, None

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)
    canvas.bind("<B1-Motion>", paint_pressure)

# 감압 브러시 그리기를 시작하는 함수
def start_paint_pressure(event):
    global start_time
    start_time = time.time()

# 감압 브러시로 그림을 그리는 함수
def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    action = canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)
    actions.append(action)

# 그림 그리기를 시작하는 함수
def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

# 그림을 그리는 함수
def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    action = canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    actions.append(action)
    x1, y1 = x2, y2

# 점선 브러시로 그림을 그리는 함수
def dotted_paint(event):
    global last_x, last_y
    spacing = 10
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            action = canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black", outline="black")
            actions.append(action)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

# 브러시 모드를 변경하는 함수
def set_brush_mode(mode):
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", paint)
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)

# 슬라이더를 통해 브러시 크기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

# 캔버스를 지우는 함수
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

# 텍스트를 추가하는 함수
def add_text(event):
    text = text_box.get()
    action = canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
    actions.append(action)

# 전체 화면 모드를 토글하는 함수
def toggle_fullscreen(event):
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

# 좌우 반전 기능을 수행하는 함수
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

# 지우개 기능을 수행하는 함수
def erase(event):
    bg_color = canvas.cget("bg")
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    action = canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    actions.append(action)

# 배경 색상을 변경하는 함수
def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

# 브러시 색상을 변경하는 함수
def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

# 새 창을 여는 함수
def create_new_window():
    new_window = Tk()
    new_canvas = Canvas(new_window)
    new_canvas.pack()
    new_window.mainloop()

# 작업을 되돌리는 함수 (Undo 기능)
def undo_action():
    if len(actions) > 0:
        action = actions.pop()
        undo_actions.append(action)
        canvas.itemconfigure(action, state='hidden')

# 작업을 다시 실행하는 함수 (Redo 기능)
def redo_action():
    if len(undo_actions) > 0:
        action = undo_actions.pop()
        actions.append(action)
        canvas.itemconfigure(action, state='normal')

# 메인 윈도우 설정
window = Tk()
window.title("그림판")

brush_size = 1
brush_color = "black"
canvas = Canvas(window, bg="white")
window.geometry("640x400+200+200")
window.resizable(True, True)
canvas.pack(fill="both", expand=True)

actions = []
undo_actions = []

# 캔버스에 그림 그리기 및 텍스트 추가 기능 바인딩
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-3>", add_text)

# 버튼 및 슬라이더 설정
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
window.bind("<F11>", toggle_fullscreen)

button_new_window = Button(window, text="새 창 열기", command=create_new_window)
button_new_window.pack(side=LEFT)

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)
button_flip.pack(side=LEFT)

canvas.bind("<B3-Motion>", erase)

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)
button_bg_color.pack(side=LEFT)

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_undo = Button(window, text="Undo", command=undo_action)
button_undo.pack(side=LEFT)

button_redo = Button(window, text="Redo", command=redo_action)
button_redo.pack(side=LEFT)

# 기본 그리기 모드 설정
set_paint_mode_normal()

# 메인 루프 실행
window.mainloop()