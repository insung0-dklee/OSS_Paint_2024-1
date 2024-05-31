from tkinter import *
import time
from tkinter.colorchooser import askcolor
import math

# 초기 설정 값들
selected_shape = "oval"
current_color = "black"
eraser_mode = False
spacing = 10
last_x, last_y = None, None

def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)
    canvas.bind("<B1-Motion>", paint_pressure)

def start_paint_pressure(event):
    global start_time
    start_time = time.time()

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time
    radius = min(max(int(elapsed_time * 5), 1), 5)
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=2)
    x1, y1 = x2, y2

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

def set_brush_mode(mode):
    global brush_mode
    brush_mode = mode
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
    canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))

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
    x1, y1 = (event.x-3), (event.y-3)
    x2, y2 = (event.x+3), (event.y+3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color():
    bg_color = askcolor()
    if bg_color[1]:
        canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    new_color = askcolor()[1]
    if new_color:
        brush_color = new_color

def create_new_window():
    new_window = Tk()
    new_canvas = Canvas(new_window)
    new_canvas.pack()
    new_window.mainloop()

def start_selection(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    canvas.delete("selection")

def update_selection(event):
    global start_x, start_y
    end_x, end_y = event.x, event.y
    canvas.delete("selection")
    canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="blue", tag="selection")

def end_selection(event):
    global selection
    end_x, end_y = event.x, event.y
    selection = (start_x, start_y, end_x, end_y)
    copy_selection()

def copy_selection():
    global selection_data
    x1, y1, x2, y2 = selection
    selection_data = canvas.create_rectangle(x1, y1, x2, y2, outline="blue", tag="selection")
    selection_data = canvas.find_enclosed(x1, y1, x2, y2)

def paste_selection(event):
    x_offset = event.x - (selection[2] - selection[0]) // 2
    y_offset = event.y - (selection[3] - selection[1]) // 2
    for item in selection_data:
        coords = canvas.coords(item)
        canvas.create_rectangle(coords[0] + x_offset, coords[1] + y_offset, coords[2] + x_offset, coords[3] + y_offset, outline="black")

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

# Selection and copy-paste functionality
canvas.bind("<Button-1>", start_selection)
canvas.bind("<B1-Motion>", update_selection)
canvas.bind("<ButtonRelease-1>", end_selection)
canvas.bind("<Button-2>", paste_selection)

set_paint_mode_normal()

window.mainloop()
