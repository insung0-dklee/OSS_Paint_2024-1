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

import tkinter as tk

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("텍스트 편집기")

        # 텍스트 상자 생성
        self.text_box = tk.Text(master, width=50, height=10)
        self.text_box.pack()

        # "모두 선택" 버튼 생성
        self.select_all_button = tk.Button(master, text="모두 선택", command=self.select_all)
        self.select_all_button.pack()

    def select_all(self):
        # 텍스트 상자 안의 모든 글자 선택
        self.text_box.tag_add("sel", "1.0", "end")

root = tk.Tk()
app = TextEditor(root)
root.mainloop()
