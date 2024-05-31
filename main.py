from tkinter import *  # tkinter 모듈 임포트
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자 임포트
from tkinter import filedialog  # 파일 대화 상자 모듈 임포트

# 초기 설정 값
brush_color = "black"  # 초기 브러시 색상을 검은색으로 설정
brush_size = 2  # 초기 브러시 크기를 2로 설정
last_x, last_y = None, None  # 이전 좌표를 저장하기 위한 변수 초기화
shape_start_x, shape_start_y = None, None  # 도형 시작 좌표를 저장하기 위한 변수 초기화
current_shape = None  # 현재 그리고 있는 도형을 저장하기 위한 변수 초기화

# 점선 브러시 함수
def dotted_paint(event):
    """
    점선 모양으로 그림을 그리는 함수
    마우스 움직임 이벤트를 받아서 일정 간격마다 점을 그림
    """
    global last_x, last_y
    spacing = 10  # 점 사이의 간격 설정
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
    """
    브러시 모드를 설정하는 함수
    mode에 따라 실선 브러시 또는 점선 브러시를 설정
    """
    global brush_mode
    brush_mode = mode
    if brush_mode == "solid":
        canvas.bind("<B1-Motion>", paint)
    elif brush_mode == "dotted":
        canvas.bind("<B1-Motion>", dotted_paint)

# 캔버스 초기화 함수
def clear_paint():
    """
    캔버스에 그려진 모든 내용을 지우는 함수
    """
    canvas.delete("all")
    global last_x, last_y
    last_x, last_y = None, None

# 실선 브러시 페인트 함수
def paint(event):
    """
    실선 모양으로 그림을 그리는 함수
    마우스 움직임 이벤트를 받아서 실선으로 그림을 그림 
    """
    global last_x, last_y
    x2, y2 = event.x, event.y
    canvas.create_line(last_x, last_y, x2, y2, fill=brush_color, width=brush_size)
    last_x, last_y = x2, y2

# 페인트 시작 함수
def paint_start(event):
    """
    페인트 시작 지점을 설정하는 함수
    마우스를 눌렀을 때의 좌표를 저장
    """
    global last_x, last_y
    last_x, last_y = event.x, event.y

# 브러시 색상 변경 함수
def change_brush_color():
    """
    색상 선택 대화 상자를 열어 브러시 색상을 변경하는 함수
    """
    global brush_color
    brush_color = askcolor()[1]

# 도형 그리기 시작 함수
def start_shape(event):
    """
    도형 그리기를 시작하는 함수
    마우스를 눌렀을 때의 좌표를 시작 좌표로 저장
    """
    global shape_start_x, shape_start_y
    shape_start_x, shape_start_y = event.x, event.y

# 도형 그리기 함수
def draw_shape(event):
    """
    도형을 그리는 함수
    마우스를 움직일 때의 좌표를 이용하여 현재 도형을 그림
    """
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
    """
    도형 그리기를 완료하는 함수
    마우스를 뗐을 때 현재 도형을 저장하는 변수를 초기화
    """
    global current_shape
    current_shape = None

# 도형 모드 설정 함수
def set_shape_mode(mode):
    """
    도형 그리기 모드를 설정하는 함수
    mode에 따라 직사각형, 타원, 선을 그릴 수 있도록 설정
    """
    global shape_mode
    shape_mode = mode
    canvas.bind("<Button-1>", start_shape)
    canvas.bind("<B1-Motion>", draw_shape)
    canvas.bind("<ButtonRelease-1>", finish_shape)

# 캔버스 저장 함수
def save_canvas():
    """
    현재 캔버스의 내용을 저장하는 함수
    PostScript 형식으로 저장
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path)

# 캔버스 불러오기 함수
def load_canvas():
    """
    저장된 파일에서 캔버스 내용을 불러오는 함수
    PostScript 파일을 불러와서 캔버스에 그림
    """
    file_path = filedialog.askopenfilename(filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as f:
            ps_data = f.read()
            canvas.delete("all")
            canvas.create_text(0, 0, text=ps_data, anchor=NW)

# 메인 윈도우 설정
window = Tk()  # Tkinter 윈도우 생성
window.title("그림판")  # 윈도우 제목 설정
window.geometry("640x400")  # 윈도우 크기 설정
window.resizable(True, True)  # 윈도우 크기 조정 가능하도록 설정

# 캔버스 설정
canvas = Canvas(window, bg="white")  # 흰색 배경의 캔버스 생성
canvas.pack(fill="both", expand=True)  # 캔버스를 윈도우 크기에 맞게 확장
canvas.bind("<Button-1>", paint_start)  # 마우스 왼쪽 버튼 클릭 이벤트와 paint_start 함수 연결

# 버튼 설정
button_frame = Frame(window)  # 버튼들을 담을 프레임 생성
button_frame.pack(fill=X)  # 프레임을 윈도우 너비에 맞게 확장

button_clear = Button(button_frame, text="All Clear", command=clear_paint)  # 캔버스를 초기화하는 버튼 생성
button_clear.pack(side=LEFT)

button_solid = Button(button_frame, text="Solid Brush", command=lambda: set_brush_mode("solid"))  # 실선 브러시 모드를 설정하는 버튼 생성
button_solid.pack(side=LEFT)

button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: set_brush_mode("dotted"))  # 점선 브러시 모드를 설정하는 버튼 생성
button_dotted.pack(side=LEFT)

button_brush_color = Button(button_frame, text="Change Brush Color", command=change_brush_color)  # 브러시 색상을 변경하는 버튼 생성
button_brush_color.pack(side=LEFT)

button_rectangle = Button(button_frame, text="Rectangle", command=lambda: set_shape_mode("rectangle"))  # 직사각형 모드를 설정하는 버튼 생성
button_rectangle.pack(side=LEFT)

button_oval = Button(button_frame, text="Oval", command=lambda: set_shape_mode("oval"))  # 타원 모드를 설정하는 버튼 생성
button_oval.pack(side=LEFT)

button_line = Button(button_frame, text="Line", command=lambda: set_shape_mode("line"))  # 선 모드를 설정하는 버튼 생성
button_line.pack(side=LEFT)

button_save = Button(button_frame, text="Save", command=save_canvas)  # 캔버스를 저장하는 버튼 생성
button_save.pack(side=LEFT)

button_load = Button(button_frame, text="Load", command=load_canvas)  # 저장된 파일을 불러오는 버튼 생성
button_load.pack(side=LEFT)

# 초기 브러시 모드 설정
set_brush_mode("solid")  # 초기 브러시 모드를 실선으로 설정

# 메인 루프 시작
window.mainloop()  # Tkinter 메인 루프 시작
