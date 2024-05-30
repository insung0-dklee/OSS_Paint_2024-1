from tkinter import *

# 현재 선택된 도형 종류를 저장하는 변수 (기본값은 "line")
current_shape = "line"

# 마우스 클릭 시작 위치를 저장할 변수
start_x, start_y = None, None

# 마우스 버튼을 눌렀을 때 호출되는 함수
def start_draw(event):
    global start_x, start_y
    # 현재 마우스 포인터의 위치를 저장
    start_x, start_y = event.x, event.y

# 마우스를 드래그하는 동안 호출되는 함수
def draw_shape(event):
    global current_shape

    # 이전에 그린 임시 도형을 모두 지움
    canvas.delete("preview")

    # 현재 선택된 도형 종류에 따라 임시 도형을 그림
    if current_shape == "line":
        # 임시 직선을 그림
        canvas.create_line(start_x, start_y, event.x, event.y, fill="black", tags="preview")
    elif current_shape == "rectangle":
        # 임시 사각형을 그림
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black", tags="preview")
    elif current_shape == "oval":
        # 임시 원을 그림
        canvas.create_oval(start_x, start_y, event.x, event.y, outline="black", tags="preview")

# 마우스 버튼을 놓았을 때 호출되는 함수
def finalize_shape(event):
    global current_shape

    # 임시 도형을 지우고 최종 도형을 그림
    canvas.delete("preview")
    
    if current_shape == "line":
        # 최종 직선을 그림
        canvas.create_line(start_x, start_y, event.x, event.y, fill="black")
    elif current_shape == "rectangle":
        # 최종 사각형을 그림
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black")
    elif current_shape == "oval":
        # 최종 원을 그림
        canvas.create_oval(start_x, start_y, event.x, event.y, outline="black")

# 도형 선택 버튼이 클릭되었을 때 호출되는 함수
def select_shape(shape):
    global current_shape
    # 현재 선택된 도형 종류를 변경
    current_shape = shape

# 윈도우 생성
window = Tk()

# 그리기 영역인 캔버스 위젯 생성
canvas = Canvas(window, bg="white")
# 캔버스 위젯을 윈도우에 배치
canvas.pack(fill=BOTH, expand=True)

# 직선을 선택하는 버튼 생성 및 배치
line_button = Button(window, text="Line", command=lambda: select_shape("line"))
line_button.pack(side=LEFT)

# 사각형을 선택하는 버튼 생성 및 배치
rectangle_button = Button(window, text="Rectangle", command=lambda: select_shape("rectangle"))
rectangle_button.pack(side=LEFT)

# 원을 선택하는 버튼 생성 및 배치
oval_button = Button(window, text="Oval", command=lambda: select_shape("oval"))
oval_button.pack(side=LEFT)

# 마우스 버튼을 눌렀을 때 start_draw 함수를 호출하도록 설정
canvas.bind("<Button-1>", start_draw)

# 마우스를 드래그하는 동안 draw_shape 함수를 호출하도록 설정
canvas.bind("<B1-Motion>", draw_shape)

# 마우스 버튼을 놓았을 때 finalize_shape 함수를 호출하도록 설정
canvas.bind("<ButtonRelease-1>", finalize_shape)

window.mainloop()
