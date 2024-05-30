from tkinter import *

"""
캔버스에 선을 그리는 함수

@Param
    event
@Return    
    None
@exception
    paint_start()          : 왼쪽 마우스가 클릭됐을 때 호출.               클릭 되었을 때의 마우스 위치(x1, y1)를 저장 

    paint()                : 왼쪽 마우스가 클릭된 채로 움질일 때마다 호출.   현재 마우스 위치(x2, y2)를 저장 후 이전의 마우스 위치(x1, y1)와 선을 연결,
                                                                      이전 마우스위치(x1, y1)를 현재 마우스 위치(x2, y2)로 초기화
"""


def paint_start(event):
    global x1, y1
    x1, y1 = event.x, event.y


def paint(event):
    global x1, y1
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    x1, y1 = x2, y2


window = Tk()
canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<Button-1>", paint_start)
canvas.bind("<B1-Motion>", paint)
window.mainloop()
