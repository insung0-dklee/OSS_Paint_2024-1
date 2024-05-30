"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

"""
[기능 추가]
원하는 색상으로 변경하는 기능

color_red : 색상 빨간색으로 변경
color_black : 색상 검정색으로 변경
color_blue : 색상 파란색으로 변경

button_color_red = color_red의 버튼
button_color_black = color_black의 버튼
button_color_blue = color_blue의 버튼

mycolor :색상을 저장하기 위한 변수(default : black)
"""

from tkinter import *
mycolor="black"

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill=mycolor, outline=mycolor)

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

#색상 red으로 바꾸는 기능 추가
def color_red():
     global mycolor
     mycolor="red"
     
#색상 black으로 바꾸는 기능 추가    
def color_black():
     global mycolor
     mycolor="black"

#색상 blue으로 바꾸는 기능 추가
def color_blue():
     global mycolor
     mycolor="blue"


window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_color_red = Button(window, text="red", command=color_red)
button_color_red.place(x=85,y=265)

button_color_black = Button(window, text="black", command=color_black)
button_color_black.place(x=45,y=265)

button_color_blue = Button(window, text="blue", command=color_blue)
button_color_blue.place(x=10,y=265)



window.mainloop()
