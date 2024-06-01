"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import webbrowser

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


# 사용자에게 입력을 받아 링크를 여는 함수
def openLink():
    link = link_entry.get()
    webbrowser.open(link)

root = Tk()  # 새로운 Tk 객체 생성
canvas = Canvas(root, width=400, height=400)  # 캔버스 만들기
canvas.pack()

# 사용자에게 링크를 입력하라는 라벨을 캔버스에 만들기
link_label = canvas.create_text(200, 150, text="Enter a link:", fill="hotpink", font=("Arial", 16))
link_entry = Entry(root)
canvas.create_window(200, 200, window=link_entry)

# 클릭 시 openLink() 함수를 호출
open_button = Button(root, text="Open Link", command=openLink)
canvas.create_window(200, 250, window=open_button)

root.mainloop()
