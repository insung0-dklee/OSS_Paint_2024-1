"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
asksaveasfilename : 이름 입력시 해당이름의 PNG 파일로 그림 저장
button_save : 파일 저장 대화 상자가 열리는 버튼


"""

from tkinter import *
from tkinter import filedialog

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

#그림 저장 기능 추가
def save_image():
    file = filedialog.asksaveasfilename(filetypes=[('PNG Images', '*.png')])
    if file:
        canvas.postscript(file=file + '.eps')
        img = Image.open(file + '.eps')
        img.save(file + '.png', 'png')

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

button_save = Button(window, text="그림 저장", command=save_image)
button_save.pack()


window.mainloop()


