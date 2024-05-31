from tkinter import *
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
from tkinter.filedialog import asksaveasfilename  # 파일 저장 대화 상자를 가져옴
from PIL import ImageGrab  # 화면 캡처를 위한 모듈
import os

# 초기 설정 값들
current_color = "black"  # 기본 색상은 검은색으로 설정
brush_size = 1  # 초기 브러시 크기

# 마우스 움직임에 따라 도형을 그리는 함수
def paint(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)

def clear_paint():
    canvas.delete("all")

def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)

def set_brush_mode(mode):
    if mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)
    else:
        canvas.bind("<B1-Motion>", paint)

def dotted_paint(event):
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            paint(event)
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

def change_brush_color():
    global current_color
    color = askcolor()[1]
    if color:
        current_color = color

def change_bg_color():
    bg_color = askcolor()[1]
    if bg_color:
        canvas.config(bg=bg_color)

def save_paint():
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        x = window.winfo_rootx() + canvas.winfo_x()
        y = window.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def create_new_window():
    new_window = Toplevel(window)
    new_canvas = Canvas(new_window, bg="white")
    new_canvas.pack(fill="both", expand=True)

window = Tk()
window.title("그림판")

canvas = Canvas(window, bg="white", width=640, height=400)
canvas.pack(expand=YES, fill=BOTH)
canvas.bind("<B1-Motion>", paint)

frame = Frame(window)
frame.pack()

btn_clear = Button(frame, text="Clear", command=clear_paint)
btn_clear.pack(side=LEFT)

color_button = Button(frame, text="Color", command=change_brush_color)
color_button.pack(side=LEFT)

save_button = Button(frame, text="Save", command=save_paint)
save_button.pack(side=LEFT)

bg_color_button = Button(frame, text="Background Color", command=change_bg_color)
bg_color_button.pack(side=LEFT)

new_window_button = Button(frame, text="New Window", command=create_new_window)
new_window_button.pack(side=LEFT)

solid_button = Button(frame, text="Solid Brush", command=lambda: set_brush_mode("solid"))
solid_button.pack(side=LEFT)

dotted_button = Button(frame, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))
dotted_button.pack(side=LEFT)

normal_button = Button(frame, text="Normal", command=set_paint_mode_normal)
normal_button.pack(side=LEFT)

# 슬라이더 추가: 브러시 크기 조절
brush_size_slider = Scale(frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
brush_size_slider.set(brush_size)
brush_size_slider.pack(side=LEFT)

window.mainloop()
