from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화


# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)


def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스 클릭시작시
    canvas.bind("<B1-Motion>", paint_pressure)  # 마우스를 클릭중일시 -> 그림을 그리고 있을시


def start_paint_pressure(event):
    global start_time
    start_time = time.time()  # 마우스를 클릭한 시간을 변수에 저장


def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵기는 마우스 클릭 시간에 비례하여 최대 5까지 증가
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


def dotted_paint(event):  # 점선 브러쉬 함수
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y


def set_brush_mode(mode):  # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":  # 브러쉬 모드가 solid면
        canvas.bind("<B1-Motion>", paint)  # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted":  # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", dotted_paint)  # 점선 브러쉬로 변경


# 슬라이더를 통해 펜 굵기를 변경하는 함수
def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)


# all clear 기능 추가
def clear_paint():
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화


def add_text(event):  # 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.
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
            if i % 2 == 0:  # x 좌표를 반전시킵니다.
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)


def erase(event):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)


def change_bg_color():
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])


def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]


# 새 창 열기 생성
def create_new_window():
    new_window = Tk()
    new_canvas = Canvas(new_window)
    new_canvas.pack()
    new_window.mainloop()


def get_color():
    x = canvas.winfo_width() // 2
    y = canvas.winfo_height() // 2
    item = canvas.find_closest(x, y)
    if item:
        color = canvas.itemcget(item, 'fill')
        messagebox.showinfo("중앙 색상", f"중앙 위치의 색상: {color}")
    else:
        messagebox.showinfo("중앙 색상", "해당 위치에 항목이 없습니다.")


window = Tk()
window.title("그림판")

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")
window.geometry("640x400+200+200")
window.resizable(True, True)
canvas.pack(fill="both", expand=True)

last_x, last_y = None, None  # 마지막 좌표 초기화
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)

button_frame = Frame(window)
button_frame.pack(fill=X)

button_clear = Button(button_frame, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size",
                          command=change_brush_size)
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

button_get_color = Button(window, text="Get Center Color", command=get_color)
button_get_color.pack(side=LEFT)

set_paint_mode_normal()

window.mainloop()

