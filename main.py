from tkinter import *

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    dot = canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    # 사용자가 그린 도형의 ID를 actions 리스트에 추가
    actions.append(dot)

def undo(event):
    if actions:
        dot_id = actions.pop()  # 마지막 도형의 ID를 가져옴
        canvas.delete(dot_id)  # 해당 도형 삭제

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

window = Tk()

actions = []  # 사용자의 행동을 저장할 리스트

canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

# Ctrl+Z를 누를 경우 undo 함수 호출
window.bind("<Control-z>", undo)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()