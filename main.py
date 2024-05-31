"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import time  # 시간 계산을 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
def on_enter(event):
    event.widget.config(bg="light blue")

def on_leave(event):
    event.widget.config(bg="SystemButtonFace")

def set_paint_mode_normal(canvas):
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))

def set_paint_mode_pressure(canvas):
    canvas.bind("<Button-1>", start_paint_pressure)
    canvas.bind("<B1-Motion>", lambda event: paint_pressure(event, canvas))

def start_paint_pressure(event):
    global start_time
    start_time = time.time()  # 마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event, canvas):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵기는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = (event.x - radius), (event.y - radius)
    x2, y2 = (event.x + radius), (event.y + radius)
    canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)

def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)

def paint(event, canvas):
    global x1, y1
    x2, y2 = event.x, event.y
    
    # 선을 그리면서 빈틈을 방지하기 위해 작은 원을 그리는 방식으로 수정
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    steps = int(distance // (brush_size/2)) + 1
    for i in range(steps):
        x = x1 + (x2 - x1) * i / steps
        y = y1 + (y2 - y1) * i / steps
        canvas.create_oval(x - brush_size // 2, y - brush_size // 2, x + brush_size // 2, y + brush_size // 2, fill=brush_color, outline=brush_color)#브러쉬 사이즈 조절 오류 해결 

    x1, y1 = x2, y2
def dotted_paint(event, canvas):
    global last_x, last_y
    spacing = 10  # 점 사이의 간격을 설정
    if last_x is not None and last_y is not None:
        dx = event.x - last_x
        dy = event.y - last_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance >= spacing:
            canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill=brush_color, outline=brush_color)#브러쉬 컬러 변경 에러 수정
            last_x, last_y = event.x, event.y
    else:
        last_x, last_y = event.x, event.y

def set_brush_mode(canvas, mode):  # 브러쉬 모드를 변경하는 함수
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":  # 브러쉬 모드가 solid면
        canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))  # 실선(기본) 브러쉬로 변경
    elif brush_mode == "dotted":  # 브러쉬 모드가 dotted면
        canvas.bind("<B1-Motion>", lambda event: dotted_paint(event, canvas))  # 점선 브러쉬로 변경

def change_brush_size(new_size):
    global brush_size
    brush_size = int(new_size)

def clear_paint(canvas):
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화

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
            if i % 2 == 0:  # x 좌표를 반전시킵니다.
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)

def erase(event, canvas):
    bg_color = canvas.cget("bg")
    x1, y1 = (event.x - 3), (event.y - 3)
    x2, y2 = (event.x + 3), (event.y + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)

def change_bg_color(canvas):
    bg_color = askcolor()
    canvas.config(bg=bg_color[1])

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]

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

    canvas = Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    last_x, last_y = None, None  # 마지막 좌표 초기화
    brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
    canvas.bind("<Button-1>", paint_start)
    canvas.bind("<B1-Motion>", lambda event: paint(event, canvas))
    button_frame = Frame(window,bg="sky blue")#구별하기 위한 버튼 영역 색 변경
    button_frame.pack(fill=X)
    
    
    button_clear = Button(button_frame, text="All Clear", command=lambda: clear_paint(canvas))
    button_clear.pack(side=LEFT)
    button_clear.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_clear.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    
    brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack(side=LEFT)

    
    button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode(canvas, "solid"))
    button_solid.pack()
    button_solid.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_solid.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록
    button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode(canvas, "dotted"))
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

    button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)
    button_brush_color.pack(side=LEFT)
    button_brush_color.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_brush_color.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록

    set_paint_mode_normal(canvas)
    
    button_new_window = Button(window, text="새 창 열기", command=create_new_window)
    button_new_window.pack(side=LEFT)
    button_new_window.bind("<Enter>", on_enter)  # 마우스가 버튼 위에 올라갔을 때의 이벤트 핸들러 등록
    button_new_window.bind("<Leave>", on_leave)  # 마우스가 버튼을 벗어났을 때의 이벤트 핸들러 등록
    

    
def create_new_window():
    new_window = Toplevel(window)  # 새로운 Toplevel 인스턴스 생성
    new_window.title("새 그림판")
    new_window.geometry("800x600+200+200")
    new_window.configure(bg="sky blue")#구별하기 위한 버튼 영역 색 변경
    setup_paint_app(new_window)

window = Tk()
window.title("그림판")
window.geometry("800x600+200+200")
window.resizable(True, True)
window.configure(bg="sky blue") #구별하기 위한 버튼 영역 색 변경

setup_paint_app(window)

window.mainloop()