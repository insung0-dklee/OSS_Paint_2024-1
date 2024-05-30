"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

# 그림을 그리는 함수
def paint(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    if eraser_mode:
        # 지우개 모드일 때 하얀색 사각형을 그려서 지움
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")
    else:
        # 브러시 모드일 때 검은색 원을 그림
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# 지우개 모드를 토글하는 함수
def toggle_eraser_mode():
    global eraser_mode
    # 지우개 모드 활성화/비활성화 전환
    eraser_mode = not eraser_mode
    if eraser_mode:
        # 지우개 모드 활성화 시 버튼 텍스트 변경
        button_eraser.config(text="브러시 모드로 전환")
    else:
        # 브러시 모드 활성화 시 버튼 텍스트 변경
        button_eraser.config(text="지우개 모드로 전환")

# 메인 윈도우 설정
window = Tk()
window.title("그림판")

# 초기 브러시 크기와 지우개 모드 설정
brush_size = 5
eraser_mode = False

# 캔버스 설정
canvas = Canvas(window, bg="white")
canvas.pack(expand=True, fill=BOTH)
canvas.bind("<B1-Motion>", paint)

# 지우개/브러시 전환 버튼
button_eraser = Button(window, text="지우개 모드로 전환", command=toggle_eraser_mode)
button_eraser.pack(side=LEFT)

# 메인 루프 시작
window.mainloop()