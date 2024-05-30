"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *  # Tkinter 모듈 임포트

def paint(event):
   
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    #event.x와 event.y는 마우스 커서의 현재 위치를 나타냄 
    #커서 위치에서 -1, -1 좌표를 시작점으로, +1, +1 좌표를 끝점으로 작은 원을 그림
   
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    #canvas.create_oval() 함수는 캔버스에 원을 그리는 함수

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
#Tk 객체를 생성하여 주 윈도우를 만들기
canvas = Canvas(window)
#Canvas 위젯을 생성하여 주 윈도우에 추가
canvas.pack()
#함수로 캔버스를 윈도우에 꽉 차게 설정
canvas.bind("<B1-Motion>", paint)
# 캔버스에 마우스 왼쪽 버튼을 누르고 움직일 때마다 paint 함수를 호출하도록 바인딩

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
