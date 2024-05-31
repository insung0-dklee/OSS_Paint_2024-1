from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog

# 초기 설정 값
brush_color = "black"
brush_size = 2
last_x, last_y = None, None
shape_start_x, shape_start_y = None, None
current_shape = None

# 점선 브러시 함수
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

# 캔버스 초기화 함수
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

# 실선 브러시 페인트 함수
def paint(event):
    global last_x, last_y
    x2, y2 = event.x, event.y
    canvas.create_line(last_x, last_y, x2, y2, fill=brush_color, width=brush_size)
    last_x, last_y = x2, y2

# 페인트 시작 함수
def paint_start(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

# 브러시 색상 변경 함수
def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

# 도형 그리기 시작 함수
def start_shape(event):
    global shape_start_x, shape_start_y
    shape_start_x, shape_start_y = event.x, event.y

# 도형 그리기 함수
def draw_shape(event):
    global current_shape
    if current_shape:
        canvas.delete(current_shape)
    x1, y1 = shape_start_x, shape_start_y
    x2, y2 = event.x, event.y
    if shape_mode == "rectangle":
        current_shape = canvas.create_rectangle(x1, y1, x2, y2, outline=brush_color)
    elif shape_mode == "oval":
        current_shape = canvas.create_oval(x1, y1, x2, y2, outline=brush_color)
    elif shape_mode == "line":
        current_shape = canvas.create_line(x1, y1, x2, y2, fill=brush_color)

# 도형 그리기 완료 함수
def finish_shape(event):
    global current_shape
    current_shape = None

# 도형 모드 설정 함수
def set_shape_mode(mode):
    global shape_mode
    shape_mode = mode
    canvas.bind("<Button-1>", start_shape)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", finish_shape)

# 캔버스 저장 함수
def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

# 캔버스 불러오기 함수
def load_canvas():
    file_path = filedialog.askopenfilename(filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as f:
            ps_data = f.read()
            canvas.delete("all")
            canvas.create_text(0, 0, text=ps_data, anchor=NW)

# 메인 윈도우 설정
window = Tk()
window.title("그림판")
window.geometry("640x400")
window.resizable(True, True)

# 캔버스 설정
canvas = Canvas(window, bg="white")
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", paint_start)

# 버튼 설정
button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

button_solid = Button(button_frame, text="Solid Brush", command=lambda: set_brush_mode("solid"))
button_solid.pack(side=LEFT)

button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))
button_dotted.pack(side=LEFT)

button_brush_color = Button(button_frame, text="Change Brush Color", command=change_brush_color)
button_brush_color.pack(side=LEFT)

button_rectangle = Button(button_frame, text="Rectangle", command=lambda: set_shape_mode("rectangle"))
button_rectangle.pack(side=LEFT)

button_oval = Button(button_frame, text="Oval", command=lambda: set_shape_mode("oval"))
button_oval.pack(side=LEFT)

button_line = Button(button_frame, text="Line", command=lambda: set_shape_mode("line"))
button_line.pack(side=LEFT)

button_save = Button(button_frame, text="Save", command=save_canvas)
button_save.pack(side=LEFT)

button_load = Button(button_frame, text="Load", command=load_canvas)
button_load.pack(side=LEFT)

# 초기 브러시 모드
set_brush_mode("solid")

# 메인 루프 시작
window.mainloop()
