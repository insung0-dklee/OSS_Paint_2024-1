from tkinter import *  # tkinter 모듈에서 모든 함수를 불러옴
import time  # 시간을 계산하기 위한 모듈
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
from tkinter import filedialog  # 파일 대화 상자를 가져옴
from PIL import Image, ImageTk  # 이미지 처리 모듈을 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화
undo_stack = []  # undo 기능을 위한 스택
image_id = None  # 이미지를 캔버스에 추가할 때 사용할 ID를 저장할 변수

# 마우스 움직임에 따라 도형을 그리는 함수
def set_paint_mode_normal():
    canvas.bind("<B1-Motion>", paint)  # 마우스를 움직일 때 paint 함수를 호출

def set_paint_mode_pressure():
    canvas.bind("<Button-1>", start_paint_pressure)  # 마우스를 클릭 시작 시
    canvas.bind("<B1-Motion>", paint_pressure)  # 마우스를 클릭 중일 시 -> 그림을 그리고 있을 시

def start_paint_pressure(event):
    global start_time
    start_time = time.time()  # 마우스를 클릭한 시간을 변수에 저장

def paint_pressure(event):
    global start_time
    elapsed_time = time.time() - start_time  # 마우스를 클릭한 시간부터 지금까지의 시간을 계산
    radius = min(max(int(elapsed_time * 5), 1), 5)  # 굵기는 마우스 클릭 시간에 비례하여 최대 5까지 증가
    x1, y1 = ( event.x - radius ), ( event.y - radius )  # 타원의 좌상단 좌표 계산
    x2, y2 = ( event.x + radius ), ( event.y + radius )  # 타원의 우하단 좌표 계산
    oval_id = canvas.create_oval(x1, y1, x2, y2, fill=brush_color, outline=brush_color)  # 타원 그리기
    undo_stack.append(oval_id)  # 그린 도형의 ID를 undo 스택에 추가

def paint_start(event):
    global x1, y1
    x1, y1 = (event.x - brush_size), (event.y - brush_size)  # 마우스를 클릭한 시작 좌표 저장

def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y  # 현재 마우스 위치 저장
    line_id = canvas.create_line(x1, y1, x2, y2, fill=brush_color, width=2)  # 선 그리기
    undo_stack.append(line_id)  # 그린 선의 ID를 undo 스택에 추가
    x1, y1 = x2, y2  # 현재 마우스 위치를 새로운 시작 위치로 설정

def dotted_paint(event):  # 점선 브러쉬 함수
    global last_x, last_y
    if last_x is not None and last_y is not None:
        dx = event.x - last_x  # 이전 마우스 위치와의 x 거리 계산
        dy = event.y - last_y  # 이전 마우스 위치와의 y 거리 계산
        distance = (dx ** 2 + dy ** 2) ** 0.5  # 거리 계산
        if distance >= spacing:
            dot_id = canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black", outline="black")  # 점 그리기
            undo_stack.append(dot_id)  # 그린 점의 ID를 undo 스택에 추가
            last_x, last_y = event.x, event.y  # 현재 마우스 위치를 새로운 마지막 위치로 설정
    else:
        last_x, last_y = event.x, event.y  # 처음 클릭 시 현재 마우스 위치를 저장

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

# 점선 간격을 설정하는 함수
def change_dot_spacing(new_spacing):
    global spacing
    spacing = int(new_spacing)

# all clear 기능 추가
def clear_paint():
    canvas.delete("all")  # 캔버스의 모든 도형 삭제
    global last_x, last_y
    last_x, last_y = None, None  # 마지막 좌표 초기화
    undo_stack.clear()  # undo 스택 초기화

def add_text(event):  # 텍스트 박스의 내용을 가져와서 클릭한 위치에 텍스트를 추가합니다.
    text = text_box.get()  # 텍스트 박스의 내용을 가져옴
    text_id = canvas.create_text(event.x, event.y, text=text, fill="black", font=('Arial', 12))  # 텍스트 추가
    undo_stack.append(text_id)  # 추가한 텍스트의 ID를 undo 스택에 추가

def toggle_fullscreen(event):
    window.state = not window.state  # 현재 창 상태를 반전
    window.attributes("-fullscreen", window.state)  # 창의 전체화면 속성을 설정

# 좌우 반전 기능 추가
def flip_horizontal():
    objects = canvas.find_all()  # 캔버스의 모든 객체를 가져옴
    canvas.update()  # 캔버스를 업데이트
    canvas_width = canvas.winfo_width()  # 캔버스의 너비를 가져옴
    for obj in objects:
        coords = canvas.coords(obj)  # 객체의 좌표를 가져옴
        for i in range(len(coords)):
            if i % 2 == 0:  # x 좌표를 반전시킵니다.
                coords[i] = canvas_width - coords[i]
        canvas.coords(obj, *coords)  # 반전된 좌표로 객체의 위치를 설정

def erase(event):
    bg_color = canvas.cget("bg")  # 배경 색상을 가져옴
    # 그림을 지우기 편하도록 paint의 픽셀보다 더욱 크게 설정
    x1, y1 = ( event.x-3 ), ( event.y-3 )  # 지울 영역의 좌상단 좌표 계산
    x2, y2 = ( event.x+3 ), ( event.y+3 )  # 지울 영역의 우하단 좌표 계산
    erase_id = canvas.create_oval(x1, y1, x2, y2, fill=bg_color, outline=bg_color)  # 타원으로 지우기
    undo_stack.append(erase_id)  # 지운 영역의 ID를 undo 스택에 추가

def change_bg_color():
    bg_color = askcolor()  # 색상 선택 대화 상자 열기
    canvas.config(bg=bg_color[1])  # 선택한 색상으로 배경색 변경

def change_brush_color():
    global brush_color
    brush_color = askcolor()[1]  # 색상 선택 대화 상자 열기 및 색상 변경

# 새 창 열기 생성
def create_new_window():
    new_window = Tk()  # 새로운 Tk 인스턴스 생성
    new_canvas = Canvas(new_window)  # 새로운 창에 캔버스 추가
    new_canvas.pack()  # 캔버스가 새로운 창에 배치
    new_window.mainloop()  # 새로운 창 실행

# 도트 모드로 도형을 그리는 함수
def draw_dotted_shape(event):
    if selected_shape == "heart":
        draw_dotted_heart(event.x, event.y)  # 하트를 그리기
    elif selected_shape == "triangle":
        draw_dotted_triangle(event.x, event.y)  # 삼각형을 그리기
    elif selected_shape == "rectangle":
        draw_dotted_rectangle(event.x, event.y)  # 사각형을 그리기

def draw_dotted_heart(x, y):
    heart_coords = [(x-5, y), (x-10, y-5), (x-15, y-15), (x, y-30), (x+15, y-15), (x+10, y-5), (x+5, y)]  # 하트 모양 좌표
    for coord in heart_coords:
        dot_id = canvas.create_oval(coord[0]-1, coord[1]-1, coord[0]+1, coord[1]+1, fill="black", outline="black")  # 점 그리기
        undo_stack.append(dot_id)  # 그린 점의 ID를 undo 스택에 추가

def draw_dotted_triangle(x, y):
    triangle_coords = [(x, y-15), (x-10, y+5), (x+10, y+5)]  # 삼각형 모양 좌표
    for coord in triangle_coords:
        dot_id = canvas.create_oval(coord[0]-1, coord[1]-1, coord[0]+1, coord[1]+1, fill="black", outline="black")  # 점 그리기
        undo_stack.append(dot_id)  # 그린 점의 ID를 undo 스택에 추가

def draw_dotted_rectangle(x, y):
    rectangle_coords = [(x-10, y-5), (x+10, y-5), (x+10, y+5), (x-10, y+5)]  # 사각형 모양 좌표
    for coord in rectangle_coords:
        dot_id = canvas.create_oval(coord[0]-1, coord[1]-1, coord[0]+1, coord[1]+1, fill="black", outline="black")  # 점 그리기
        undo_stack.append(dot_id)  # 그린 점의 ID를 undo 스택에 추가

def set_shape(shape):
    global selected_shape
    selected_shape = shape  # 선택된 도형 설정
    canvas.bind("<Button-1>", draw_dotted_shape)  # 마우스 클릭 시 도형 그리기

# Undo 기능 추가
def undo():
    if undo_stack:
        last_item = undo_stack.pop()  # 마지막 도형 ID 가져오기
        canvas.delete(last_item)  # 마지막 도형 삭제

# 이미지 로드 기능 추가
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])  # 파일 선택 대화 상자 열기
    if file_path:
        image = Image.open(file_path)  # 이미지 열기
        global photo_image
        photo_image = ImageTk.PhotoImage(image)  # 이미지 객체 생성
        global image_id
        if image_id:
            canvas.delete(image_id)  # 기존 이미지 삭제
        image_id = canvas.create_image(320, 200, image=photo_image, anchor=CENTER)  # 이미지 캔버스에 추가
        undo_stack.append(image_id)  # 추가한 이미지의 ID를 undo 스택에 추가

window = Tk()  # Tk 객체를 생성하여 주 윈도우를 만들기
window.title("그림판")  # 윈도우 제목 설정

brush_size = 1  # 초기 브러시 크기
canvas = Canvas(window, bg="white")  # 캔버스 생성 및 배경색 설정
window.geometry("640x400+200+200")  # 윈도우 창의 너비와 높이, 초기 화면 위치 설정
window.resizable(True, True)  # 윈도우 창 크기 조절 가능 여부 설정
canvas.pack(fill="both", expand=True)  # 캔버스를 창 너비에 맞춰 동적으로 크기 조절

last_x, last_y = None, None  # 마지막 좌표 초기화
brush_mode = "solid"  # 기본 브러쉬 모드를 실선으로 설정
canvas.bind("<Button-1>", paint_start)  # 마우스 클릭 시 paint_start 함수 호출
canvas.bind("<B1-Motion>", paint)  # 마우스를 움직일 때 paint 함수 호출

button_frame = Frame(window)  # 버튼들을 담을 프레임 생성
button_frame.pack(fill=X)  # 프레임을 윈도우에 배치

button_clear = Button(button_frame, text="All Clear", command=clear_paint)  # 모든 그림을 지우는 버튼 생성
button_clear.pack(side=LEFT)  # 버튼을 프레임의 왼쪽에 배치

# 펜 굵기를 조절할 수 있는 슬라이더 추가
brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=change_brush_size)
brush_size_slider.set(brush_size)  # 슬라이더 초기값 설정
brush_size_slider.pack(side=LEFT)  # 슬라이더를 프레임의 왼쪽에 배치

button_solid = Button(window, text="Solid Brush", command=lambda: set_brush_mode("solid"))  # 실선 브러쉬 버튼 생성
button_solid.pack()  # 버튼을 윈도우에 배치

button_dotted = Button(window, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))  # 점선 브러쉬 버튼 생성
button_dotted.pack()  # 버튼을 윈도우에 배치

button_paint = Button(window, text="normal", command=set_paint_mode_normal)  # 기본 그리기 모드 버튼 생성
button_paint.pack(side=RIGHT)  # 버튼을 윈도우의 오른쪽에 배치

button_paint = Button(window, text="pressure", command=set_paint_mode_pressure)  # 감압 브러시 그리기 모드 버튼 생성
button_paint.pack(side=RIGHT)  # 버튼을 윈도우의 오른쪽에 배치

button_undo = Button(window, text="Undo", command=undo)  # undo 버튼 생성
button_undo.pack(side=RIGHT)  # 버튼을 윈도우의 오른쪽에 배치

text_box = Entry(window)  # 텍스트를 입력할 공간을 생성
text_box.pack(side=LEFT)  # 텍스트 박스를 윈도우의 왼쪽에 배치
canvas.bind("<Button-3>", add_text)  # 마우스 오른쪽 클릭 시 add_text 함수 호출
window.bind("<F11>", toggle_fullscreen)  # F11 키를 누를 때 toggle_fullscreen 함수 호출

button_new_window = Button(window, text="새 창 열기", command=create_new_window)  # 새 창 열기 버튼 생성
button_new_window.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

button_flip = Button(window, text="Flip Horizontal", command=flip_horizontal)  # 좌우 반전 버튼 생성
button_flip.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

canvas.bind("<B3-Motion>", erase)  # 마우스 오른쪽 버튼을 누르고 움직일 때 erase 함수 호출

brush_color = "black"  # 초기 브러시 색상 설정

button_bg_color = Button(window, text="Change Background Color", command=change_bg_color)  # 배경색 변경 버튼 생성
button_bg_color.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

button_brush_color = Button(window, text="Change Brush Color", command=change_brush_color)  # 브러시 색상 변경 버튼 생성
button_brush_color.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

# 도형 버튼 추가
button_triangle = Button(window, text="Triangle", command=lambda: set_shape("triangle"))  # 삼각형 도형 버튼 생성
button_triangle.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

button_rectangle = Button(window, text="Rectangle", command=lambda: set_shape("rectangle"))  # 사각형 도형 버튼 생성
button_rectangle.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

# 이미지 로드 버튼 추가
button_load_image = Button(window, text="Load Image", command=load_image)  # 이미지 로드 버튼 생성
button_load_image.pack(side=LEFT)  # 버튼을 윈도우의 왼쪽에 배치

set_paint_mode_normal()  # 프로그램 시작 시 기본 그리기 모드 설정

window.mainloop()  # 윈도우 실행
