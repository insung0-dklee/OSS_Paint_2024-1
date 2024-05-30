from tkinter import *  # tkinter 라이브러리의 모든 모듈을 가져옴
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 가져옴
import math  # 수학 모듈을 가져옴

# 초기 설정 값들
selected_shape = "oval"  # 기본 도형은 타원형으로 설정
current_color = "black"  # 기본 색상은 검은색으로 설정
eraser_mode = False  # 기본적으로 지우개 모드는 비활성화
spacing = 10  # 도형 사이의 최소 간격을 10으로 설정
last_x, last_y = None, None  # 마지막 마우스 위치를 저장할 변수 초기화

# 마우스 움직임에 따라 도형을 그리는 함수
def paint(event):
    global last_x, last_y  # 전역 변수를 사용
    if last_x is not None and last_y is not None:
        distance = math.sqrt((event.x - last_x) ** 2 + (event.y - last_y) ** 2)  # 이전 위치와 현재 위치 사이의 거리 계산
        if distance < spacing:  # 거리가 설정된 간격보다 작으면 도형을 그리지 않음
            return

    x1, y1 = (event.x - 1), (event.y - 1)  # 현재 마우스 위치의 왼쪽 위 좌표
    x2, y2 = (event.x + 1), (event.y + 1)  # 현재 마우스 위치의 오른쪽 아래 좌표
    
    color = "white" if eraser_mode else current_color  # 지우개 모드일 경우 흰색, 아니면 현재 색상 사용
    
    # 선택된 도형에 따라 도형을 그림
    if selected_shape == "oval":
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)  # 타원 그리기
    elif selected_shape == "rectangle":
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)  # 사각형 그리기
    elif selected_shape == "triangle":
        points = [event.x, event.y - 5, event.x - 5, event.y + 5, event.x + 5, event.y + 5]  # 삼각형의 꼭짓점 좌표 계산
        canvas.create_polygon(points, fill=color, outline=color)  # 삼각형 그리기
    elif selected_shape == "heart":
        points = [
            event.x, event.y,
            event.x - 5, event.y - 5,
            event.x - 10, event.y,
            event.x - 5, event.y + 10,
            event.x + 5, event.y + 10,
            event.x + 10, event.y,
            event.x + 5, event.y - 5
        ]  # 하트 모양의 꼭짓점 좌표 계산
        canvas.create_polygon(points, fill=color, outline=color)  # 하트 그리기
    
    last_x, last_y = event.x, event.y  # 마지막 마우스 위치 갱신

# 도형을 설정하는 함수
def set_shape(shape):
    global selected_shape, eraser_mode  # 전역 변수를 사용
    selected_shape = shape  # 선택된 도형을 갱신
    eraser_mode = False  # 지우개 모드를 비활성화

# 색상을 선택하는 함수
def choose_color():
    global current_color, eraser_mode  # 전역 변수를 사용
    color = askcolor()[1]  # 색상 선택 대화 상자 열기
    if color:
        current_color = color  # 선택한 색상으로 갱신
        eraser_mode = False  # 지우개 모드를 비활성화

# 지우개 모드를 활성화하는 함수
def activate_eraser():
    global eraser_mode  # 전역 변수를 사용
    eraser_mode = True  # 지우개 모드를 활성화

# 캔버스를 초기화하는 함수
def clear_canvas():
    global last_x, last_y  # 전역 변수를 사용
    canvas.delete("all")  # 캔버스의 모든 내용을 지움
    last_x, last_y = None, None  # 마지막 마우스 위치 초기화

# 도형 간격을 설정하는 함수
def set_spacing(new_spacing):
    global spacing  # 전역 변수를 사용
    spacing = new_spacing  # 새로운 간격 값으로 갱신

# 윈도우 창 설정
window = Tk()
canvas = Canvas(window, bg="white")  # 흰색 배경의 캔버스 생성
canvas.pack(fill=BOTH, expand=True)  # 캔버스를 창 크기에 맞게 조절
canvas.bind("<B1-Motion>", paint)  # 마우스 왼쪽 버튼을 누른 채 움직일 때 paint 함수 호출

# 버튼 프레임 설정
button_frame = Frame(window)
button_frame.pack(side=BOTTOM)

# 각 도형을 선택할 수 있는 버튼 생성
oval_button = Button(button_frame, text="Oval", command=lambda: set_shape("oval"))
oval_button.pack(side=LEFT)

rectangle_button = Button(button_frame, text="Rectangle", command=lambda: set_shape("rectangle"))
rectangle_button.pack(side=LEFT)

triangle_button = Button(button_frame, text="Triangle", command=lambda: set_shape("triangle"))
triangle_button.pack(side=LEFT)

heart_button = Button(button_frame, text="Heart", command=lambda: set_shape("heart"))
heart_button.pack(side=LEFT)

# 색상을 선택할 수 있는 버튼 생성
color_button = Button(button_frame, text="Choose Color", command=choose_color)
color_button.pack(side=LEFT)

# 지우개 모드를 활성화할 수 있는 버튼 생성
eraser_button = Button(button_frame, text="Eraser", command=activate_eraser)
eraser_button.pack(side=LEFT)

# 캔버스를 초기화할 수 있는 버튼 생성
clear_button = Button(button_frame, text="Clear", command=clear_canvas)
clear_button.pack(side=LEFT)

# 도형 간격을 조절할 수 있는 슬라이더 생성
spacing_scale = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Spacing", command=lambda v: set_spacing(int(v)))
spacing_scale.set(spacing)  # 슬라이더의 초기값 설정
spacing_scale.pack(side=LEFT)

# 윈도우 창 루프 시작
window.mainloop()
