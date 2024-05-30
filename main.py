"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
from PIL import ImageGrab, Image # pip install pillow 필요


def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

def get_color(event): # 색상을 클릭하면 해당 색상의 rgb값을 출력
    # 캔버스의 스크린 좌표를 가져옴
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    print(f"Canvas coordinates: ({x}, {y}), ({x1}, {y1})")


    # 캔버스 영역을 스크린샷으로 저장
    image = ImageGrab.grab((x, y, x1, y1))

    # 클릭한 좌표의 색상 추출
    try:
        color = image.getpixel((event.x, event.y))
        color_label.config(text=f"Color: {color}")
    except Exception as e:
        print(f"Error getting color: {e}")
        color_label.config(text="Error getting color")

def test_colors():
    # 테스트용으로 다양한 색상의 사각형을 그림
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    for i, color in enumerate(colors):
        canvas.create_rectangle(10, 10 + i*50, 110, 60 + i*50, fill=color, outline=color)


window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", get_color)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

color_label = Label(window, text="Color: ")
color_label.pack()

# 테스트 색상 버튼 추가
test_button = Button(window, text="Test Colors", command=test_colors)
test_button.pack()

window.mainloop()
