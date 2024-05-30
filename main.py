from tkinter import *  # tkinter 모듈의 모든 클래스를 임포트합니다.
from tkinter.colorchooser import askcolor  # 색상 선택 대화 상자를 사용하기 위해 askcolor 함수를 임포트합니다.

def paint(event):  # 마우스 드래그 시 호출되는 함수입니다.
    x1, y1 = (event.x - 1), (event.y - 1)  # 마우스 포인터의 현재 위치에서 약간 왼쪽 위 좌표를 계산합니다.
    x2, y2 = (event.x + 1), (event.y + 1)  # 마우스 포인터의 현재 위치에서 약간 오른쪽 아래 좌표를 계산합니다.
    # 이 좌표들을 사용하여 작은 타원을 그립니다. 타원은 검정색 또는 사용자가 선택한 색상으로 채워집니다.
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

def choose_color():  # 사용자가 색상을 선택할 수 있게 하는 함수입니다.
    global color  # 색상 변수를 전역 변수로 선언합니다.
    color_code = askcolor(title="Choose color")  # 색상 선택 대화 상자를 열고 사용자가 선택한 색상 값을 반환합니다.
    color = color_code[1]  # 사용자가 선택한 색상의 헥스 코드 값을 저장합니다.

window = Tk()  # 최상위 윈도우를 생성합니다.
color = "black"  # 기본 그림 색상을 검정색으로 설정합니다.

# 색상 선택 버튼을 생성하고 윈도우에 추가합니다.
# 버튼을 클릭하면 choose_color 함수가 호출됩니다.
color_button = Button(window, text="Choose Color", command=choose_color)
color_button.pack()  # 버튼을 윈도우에 배치합니다.

canvas = Canvas(window)  # 그림을 그릴 캔버스를 생성합니다.
canvas.pack(expand=YES, fill=BOTH)  # 캔버스를 윈도우에 배치하고 창 크기에 맞게 확장되도록 설정합니다.
canvas.bind("<B1-Motion>", paint)  # 마우스 왼쪽 버튼을 누른 상태로 움직일 때 paint 함수를 호출합니다.

window.mainloop()  # 이벤트 루프를 시작하여 윈도우가 사용자 이벤트를 처리할 수 있게 합니다.
