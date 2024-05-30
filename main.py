"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    global current_color 
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill = current_color, outline = current_color) #color_list에서 설정한 color 사용

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

#set_color 기능 추가
def set_color(choice): # choice : 색깔 선택하는 버튼 클릭 시 버튼이 set_color를 호출하면서 전달하는 자신의 색상을 받는 매개변수
    global color_list
    global current_color
    current_color = color_list[color_list.index(choice)]

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

#[color_list에 있는 모든 색상들의 버튼을 생성하는 코드]-------------------------------------------------------------------

'''
color_list에 색상을 추가하면 해당 색상의 새로운 버튼이 생성됨
'''
color_list = ['black', 'red', 'orange', 'blue', 'green']
current_color = color_list[0]

'''
버튼을 담을 button_frame을 window에 추가 
'''
button_frame = Frame(window)
button_frame.pack()

'''
    i : color_list의 특정 값의 인덱스
    color : color_list의 특정 값
    
    => color_list의 모든 색상의 버튼을 button_frame 0행에 나란히 생성
'''
for i, color in enumerate(color_list):
    button = Button(button_frame, text=color, command=lambda c=color: set_color(c))
    button.grid(row=0, column=i)
#---------------------------------------------------------------------------------------------------------------


button_delete = Button(button_frame, text="all clear", command=clear_paint)
button_delete.grid(row=1, column = 0)

window.mainloop()
