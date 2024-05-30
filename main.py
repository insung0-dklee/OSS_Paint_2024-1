"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

text_mode: text박스를 클릭하면 add_text함수를 실행시킴
add_text: 원하는 곳에 마우스를 클릭하면 텍스트를 입력할 수 있는 entry가 생성되고 원하는 텍스트를 입력하고 enter키를 누르면 submit_text가 실행됨
submit_text: 입력한 텍스트를 Arial글꼴에, 12폰트로 화면에 출력시키고 entry를 파괴시킴. 그 이후 다시 그리기모드로 변경
"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

def text_mode():
    canvas.bind("<Button-1>", add_text)

def add_text(event):
    global text_entry
    text_entry = Entry(window)
    text_entry.place(x=event.x, y=event.y)
    text_entry.bind("<Return>", submit_text)

def submit_text(event):
    text = text_entry.get()
    canvas.create_text(text_entry.winfo_x(), text_entry.winfo_y(), text=text, anchor=NW, font=('Arial', 12))
    text_entry.destroy()
    canvas.bind("<B1-Motion>", paint)

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_text = Button(window, text="text", command=text_mode)
button_delete.pack()
button_text.pack()


window.mainloop()