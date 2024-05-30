from tkinter import *
from erase import erase
import thickness_ctrl as tc  # 선 굵기 조절 기능을 담은 파일 import

def paint(event):
    x1, y1 = (event.x - tc.line_thickness), (event.y - tc.line_thickness)
    x2, y2 = (event.x + tc.line_thickness), (event.y + tc.line_thickness)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

window = Tk()
canvas = Canvas(window)
canvas.pack()

canvas.bind("<B1-Motion>", paint)
canvas.bind("<B3-Motion>", lambda event: erase(event, canvas))

# 선 굵기 조절 버튼 추가
increase_button = Button(window, text="+", command=tc.increase_thickness)
decrease_button = Button(window, text="-", command=tc.decrease_thickness)

increase_button.pack(side=LEFT)
decrease_button.pack(side=LEFT)

window.mainloop()