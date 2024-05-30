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

import pyautogui
from PIL import Image, ImageDraw

pyautogui.press('win')
pyautogui.write('그림판')
pyautogui.press('enter')

pyautogui.sleep(1)

pyautogui.alert("도형을 그린 후 확인 버튼을 눌러주세요.")
screenshot = pyautogui.screenshot()

screenshot.save("screenshot.png")

image = Image.open("screenshot.png")

selected_shape = (100, 100, 200, 200)

draw = ImageDraw.Draw(image)
draw.rectangle(selected_shape, fill="white")  

image.save("filled_screenshot.png")

image.show()

