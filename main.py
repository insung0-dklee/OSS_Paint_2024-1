from tkinter import *

# 마우스 드래그로 그림을 그리는 함수
def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )  # 마우스 포인터의 위치에서 -1 좌표
    x2, y2 = ( event.x+1 ), ( event.y+1 )  # 마우스 포인터의 위치에서 +1 좌표
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")  # 작은 원을 그려서 선처럼 보이게 함

# 캔버스를 지우는 함수
def clear_canvas():
    canvas.delete("all")  # 캔버스의 모든 요소를 삭제

# Tk 윈도우 객체 생성
window = Tk()

# 캔버스 위젯 생성
canvas = Canvas(window)
canvas.pack()  # 캔버스를 윈도우에 배치

# 마우스 왼쪽 버튼을 눌러서 드래그할 때 paint 함수 호출
canvas.bind("<B1-Motion>", paint)

# 'Clear Canvas' 버튼 생성 및 clear_canvas 함수와 연결
clear_button = Button(window, text="Clear Canvas", command=clear_canvas)
clear_button.pack()  # 버튼을 윈도우에 배치

# Tk 이벤트 루프 실행
window.mainloop()
