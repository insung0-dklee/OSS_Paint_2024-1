"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()

from tkinter import *


def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()


def setCanvasOutlineColor(canvas, color, line_width=2):
    """
    캔버스의 윤곽선 색을 설정하는 함수
    
        canvas (tkinter.Canvas): 윤곽선 색을 설정할 캔버스 객체
        color (str): 윤곽선 색상 (예: 'blue')
        line_width (int, optional): 윤곽선 두께, 기본값 2
    """
    canvas.config(highlightthickness=line_width, highlightcolor=color)


def changeFigureOutlineColor(canvas, item_id, new_color):
    """
    캔버스 내부의 도형의 윤곽선 색을 변경하는 함수
    
    canvas (tkinter.Canvas): 도형이 그려진 캔버스 객체
    item_id (int): 변경할 도형의 ID
    new_color (str): 새로운 윤곽선 색상 (예: 'red')
    """
    canvas.itemconfig(item_id, outline=new_color)
    


