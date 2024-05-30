"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
add_text_at_click : 클릭한 위치에 입력된 텍스트를 추가하는 기능
text_entry : 사용자가 텍스트를 입력할 수 있는 입력 상자

"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 클릭한 위치에 텍스트를 추가하는 기능
def add_text_at_click(event):
    text = text_entry.get()  # 입력된 텍스트 가져오기
    if text:  # 텍스트가 비어 있지 않은 경우에만 추가
        x, y = event.x, event.y  # 클릭한 위치 가져오기
        canvas.create_text(x, y, text=text, fill="black", font=("Helvetica", 20))
        text_entry.delete(0, END)  # 입력 상자 비우기

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", add_text_at_click)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack(side=LEFT)

text_entry = Entry(window)
text_entry.pack(side=LEFT)

window.mainloop()
