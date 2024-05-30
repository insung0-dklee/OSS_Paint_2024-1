from tkinter import *

# 초기 펜 색상을 검정색으로 설정한다
pen_color = "black"

# 마우스 드래그 이벤트가 발생할 때 호출되는 함수
def paint(event):
    # 마우스 포인터의 현재 위치를 기준으로 작은 원의 좌표를 계산한다
    x1, y1 = ( event.x - 1 ), ( event.y - 1 )
    x2, y2 = ( event.x + 1 ), ( event.y + 1 )
    # 현재 펜 색상으로 채워진 원을 캔버스에 그린다
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline=pen_color)

# "Red" 버튼이 클릭되었을 때 호출되는 함수
def change_color_to_red():
    global pen_color
    # 펜 색상을 빨간색으로 변경한다
    pen_color = "red"

# 윈도우를 생성한다
window = Tk()

# 그리기 영역인 캔버스 위젯을 생성한다
canvas = Canvas(window)
# 캔버스 위젯을 윈도우에 배치한다
canvas.pack()

# 펜 색상을 빨간색으로 변경하는 "Red" 버튼 생성한다
red_button = Button(window, text="Red", command=change_color_to_red)
# "Red" 버튼을 윈도우에 배치한다
red_button.pack()

# 마우스 왼쪽 버튼을 누른 상태에서 움직일 때 paint 함수를 호출하도록 설정한다
canvas.bind("<B1-Motion>", paint)

window.mainloop()
