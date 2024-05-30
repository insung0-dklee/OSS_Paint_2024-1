from tkinter import *  # tkinter 모듈의 모든 클래스를 가져옵니다.

# 'paint' 함수 정의: 마우스가 이동하는 경로를 따라 검은색으로 그립니다.
def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )  # 마우스 좌표의 왼쪽 위 모서리 좌표를 계산합니다.
    x2, y2 = ( event.x+1 ), ( event.y+1 )  # 마우스 좌표의 오른쪽 아래 모서리 좌표를 계산합니다.
    # 작은 타원(점)을 그려서 마우스가 움직이는 경로를 따라 선을 만듭니다.
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# 'erase' 함수 정의: 마우스가 이동하는 경로를 따라 흰색으로 그려 지웁니다.
def erase(event):
    x1, y1 = ( event.x-5 ), ( event.y-5 )  # 마우스 좌표의 왼쪽 위 모서리 좌표를 계산합니다.
    x2, y2 = ( event.x+5 ), ( event.y+5 )  # 마우스 좌표의 오른쪽 아래 모서리 좌표를 계산합니다.
    # 큰 타원(지우개 효과)을 그려서 마우스가 움직이는 경로를 따라 지웁니다.
    canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")

# 주 윈도우 창을 생성합니다.
window = Tk()

# 흰색 배경의 캔버스를 생성합니다.
canvas = Canvas(window, bg="white")
# 캔버스를 윈도우에 꽉 차게 배치합니다.
canvas.pack(fill=BOTH, expand=True)

# 마우스 왼쪽 버튼을 눌러 드래그할 때 'paint' 함수를 호출합니다.
canvas.bind("<B1-Motion>", paint)
# 마우스 오른쪽 버튼을 눌러 드래그할 때 'erase' 함수를 호출합니다.
canvas.bind("<B3-Motion>", erase)

# Tkinter 이벤트 루프를 시작합니다.
window.mainloop()
