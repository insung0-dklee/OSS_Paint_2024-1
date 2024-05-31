from tkinter import *
from tkinter.colorchooser import askcolor
import time

# 초기 설정 값들
selected_tool = "brush"  # 현재 선택된 도구
selected_shape = "oval"  # 현재 선택된 도형
brush_mode = "solid"  # 브러시 모드 (solid or dotted)
current_color = "black"
eraser_mode = False
spacing = 10
last_x, last_y = None, None
selected_item = None  # 선택된 도형

def set_paint_mode_normal():
    global selected_tool
    selected_tool = "brush"
    clear_bindings()
    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    global selected_tool
    selected_tool = "pressure_brush"
    clear_bindings()
    canvas.bind("<Button-1>", start_paint_pressure)
    canvas.bind("<B1-Motion>", paint_pressure)

def start_paint_pressure(event):
    global start_time
    start_time = time.time()

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = ( event.x - radius ), ( event.y - radius )
    x2, y2 = ( event.x + radius ), ( event.y + radius )
    action = canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)
    actions.append(action)

def paint_start(event):
    global x1, y1
    x1, y1 = event.x, event.y

def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    action = canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=brush_size)
    actions.append(action)
    x1, y1 = x2, y2

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

def set_brush_mode(mode):
    global brush_mode, selected_tool
    brush_mode = mode
    selected_tool = "brush"
    clear_bindings()
    canvas.bind("<Button-1>", paint_start)
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", paint)
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

def add_text(event):
    text = text_box.get()
    action = canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))
    actions.append(action)

def toggle_fullscreen(event):
    window.state = not window.state
    window.attributes("-fullscreen", window.state)

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

def erase(event):
    bg_color = canvas.cget("bg")
    x1, y1 = ( event.x-3 ), ( event.y-3 )
    x2, y2 = ( event.x+3 ), ( event.y+3 )
    action = canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)
    actions.append(action)

def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

def create_new_window():
    new_window = Tk()
    new_canvas = Canvas(new_window)
    new_canvas.pack()
    new_window.mainloop()

def undo_action():
    if len(actions) > 0:
        action = actions.pop()
        undo_actions.append(action)
        canvas.itemconfigure(action, state='hidden')

def redo_action():
    if len(undo_actions) > 0:
        action = undo_actions.pop()
        actions.append(action)
        canvas.itemconfigure(action, state='normal')

def shape_start(event):
    global start_x, start_y, shape_obj
    start_x, start_y = event.x, event.y
    shape_obj = None

def draw_shape(event):
    global shape_obj
    end_x, end_y = event.x, event.y
    if shape_obj:
        canvas.delete(shape_obj)
    if selected_shape == "rectangle":
        shape_obj = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=brush_color, width=brush_size)
    elif selected_shape == "oval":
        shape_obj = canvas.create_oval(start_x, start_y, end_x, end_y, outline=brush_color, width=brush_size)
    elif selected_shape == "triangle":
        shape_obj = canvas.create_polygon(start_x, start_y, end_x, end_y, (start_x+end_x)/2, start_y - (end_y-start_y), outline=brush_color, fill='', width=brush_size)

def finalize_shape(event):
    global shape_obj
    end_x, end_y = event.x, event.y
    if shape_obj:
        canvas.delete(shape_obj)
    if selected_shape == "rectangle":
        shape_obj = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=brush_color, width=brush_size)
    elif selected_shape == "oval":
        shape_obj = canvas.create_oval(start_x, start_y, end_x, end_y, outline=brush_color, width=brush_size)
    elif selected_shape == "triangle":
        shape_obj = canvas.create_polygon(start_x, start_y, end_x, end_y, (start_x+end_x)/2, start_y - (end_y-start_y), outline=brush_color, fill='', width=brush_size)
    actions.append(shape_obj)
    shape_obj = None

def set_shape_mode(shape):
    global selected_tool, selected_shape
    selected_tool = "shape"
    selected_shape = shape
    clear_bindings()
    canvas.bind("<Button-1>", shape_start)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", finalize_shape)

def clear_bindings():
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def select_item(event):
    global selected_item, start_x, start_y
    clear_bindings()
    canvas.bind("<B1-Motion>", move_item)
    canvas.bind("<ButtonRelease-1>", finalize_move)
    selected_item = canvas.find_closest(event.x, event.y)[0]
    start_x, start_y = event.x, event.y

def move_item(event):
    global start_x, start_y
    if selected_item:
        dx, dy = event.x - start_x, event.y - start_y
        canvas.move(selected_item, dx, dy)
        start_x, start_y = event.x, event.y

def finalize_move(event):
    global selected_item
    selected_item = None

def set_select_mode():
    global selected_tool
    selected_tool = "select"
    clear_bindings()
    canvas.bind("<Button-1>", select_item)

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
shape_obj = None
selected_item = None

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

# 도형 그리기 모드 버튼 설정
button_rectangle = Button(window, text="Rectangle", command=lambda: set_shape_mode("rectangle"))
button_rectangle.pack(side=LEFT)

button_oval = Button(window, text="Oval", command=lambda: set_shape_mode("oval"))
button_oval.pack(side=LEFT)

button_triangle = Button(window, text="Triangle", command=lambda: set_shape_mode("triangle"))
button_triangle.pack(side=LEFT)

# 선택 모드 버튼 설정
button_select = Button(window, text="Select & Move", command=set_select_mode)
button_select.pack(side=LEFT)

# 기본 그리기 모드 설정
set_paint_mode_normal()

# 메인 루프 실행
window.mainloop()