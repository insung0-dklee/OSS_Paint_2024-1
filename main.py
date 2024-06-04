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
from tkinter import font

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Text Editor")

        # 텍스트 입력 영역 생성
        self.text_area = tk.Text(master, font=("Arial", 16))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 실행 취소 기능 구현
        self.undo_stack = []
        self.text_area.bind("<KeyRelease>", self.save_state)
        self.undo_button = tk.Button(master, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.BOTTOM)

    def save_state(self, event):
        self.undo_stack.append(self.text_area.get("1.0", tk.END))

    def undo(self):
        if self.undo_stack:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", self.undo_stack.pop())

root = tk.Tk()
text_editor = TextEditor(root)
root.mainloop()
