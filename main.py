from tkinter import *  # tkinter 모듈을 임포트

def paint(event):
    # 사용자가 마우스를 드래그할 때 그려지는 점의 좌표 설정
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    # 지정된 좌표에 원을 그려서 점을 생성
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def start_line(event):
    # 직선 그리기를 시작할 때 시작점 좌표 설정
    global x_start, y_start
    x_start, y_start = event.x, event.y

def draw_line(event):
    # 직선을 그리기 위해 마우스를 드래그할 때 끝점 좌표 설정 및 직선 생성
    global x_start, y_start
    canvas.create_line(x_start, y_start, event.x, event.y, fill="black")
    # 새로운 시작점 좌표 업데이트
    x_start, y_start = event.x, event.y

def activate_paint(event):
    # 자유로운 그리기 모드를 활성화
    canvas.bind("<B1-Motion>", paint)

def activate_line(event):
    # 직선 그리기 모드를 활성화
    canvas.bind("<B1-Motion>", draw_line)
    canvas.bind("<Button-1>", start_line)

window = Tk()  # tkinter 윈도우 생성
canvas = Canvas(window)  # 캔버스 위젯 생성
canvas.pack()  # 캔버스를 윈도우에 배치

# 기본적으로 자유로운 그리기 모드 활성화
activate_paint(None)

# 자유로운 그리기 모드로 전환하는 버튼 생성 및 배치
paint_button = Button(window, text="Draw Freehand", command=lambda: activate_paint(None))
paint_button.pack(side=LEFT)

# 직선 그리기 모드로 전환하는 버튼 생성 및 배치
line_button = Button(window, text="Draw Line", command=lambda: activate_line(None))
line_button.pack(side=LEFT)

canvas.bind("<B1-Motion>", paint)  # 기본적으로 자유로운 그리기 모드 바인딩

window.mainloop()  # 윈도우 실행
