from tkinter import *
from tkinter.colorchooser import askcolor

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill=current_color.get(), outline=current_color.get())  # 원을 현재 선택된 색상으로 채웁니다. fill과 outline 속성 모두 현재 색상으로 설정됩니다.

def choose_color(): # 사용자가 색상을 선택할 수 있는 대화 상자를 열어주는 함수입니다.
    color = askcolor()[1] # 색상 선택 대화 상자를 열고, 사용자가 선택한 색상 값을 반환받습니다.
    if color:  # 사용자가 색상을 선택한 경우 
        current_color.set(color) # current_color 변수를 선택한 색상으로 업데이트합니다.

window = Tk()
current_color = StringVar() # 현재 선택된 색상을 저장하는 StringVar 객체를 생성합니다.
current_color.set("black") # 초기 색상을 검정색("black")으로 설정합니다.

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True) # 캔버스 위젯을 윈도우 크기에 맞게 확장하고 채웁니다.
canvas.bind("<B1-Motion>", paint)

color_button = Button(window, text="색 선택", command=choose_color) # 색상 선택 버튼을 생성하고, 클릭 시 choose_color 함수를 호출하도록 설정합니다.
color_button.pack(side=BOTTOM) # 색상 선택 버튼을 윈도우의 아래쪽에 배치합니다.

window.mainloop()