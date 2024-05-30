from tkinter import *
from tkinter.colorchooser import askcolor

current_color = "black"  # 초기 색상 설정

def paint(event):
    """
        캔버스에 마우스 드래그 이벤트가 발생했을 때 호출되어 점을 그리는 함수.

        Parameters:
        event : Event
            마우스 이벤트 객체로, 마우스 포인터의 위치를 포함.
    """
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)

def choose_color():
    """
        색상 선택 다이얼로그를 열어 사용자가 선택한 색상으로 current_color를 변경하는 함수.
    """
    global current_color
    color = askcolor()[1]
    if color:
        current_color = color

window = Tk()
canvas = Canvas(window)
canvas.pack()

color_button = Button(window, text="Choose Color", command=choose_color)
color_button.pack()

canvas.bind("<B1-Motion>", paint)
window.mainloop()
