from tkinter import *

def paint(event):
    x1, y1 = (event.x - brush_size.get() // 2), (event.y - brush_size.get() // 2)
    x2, y2 = (event.x + brush_size.get() // 2), (event.y + brush_size.get() // 2)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

window = Tk()

canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)

brush_size = Scale(window, from_=1, to=20, orient=HORIZONTAL, label="Brush Size") # 1부터 20까지 크기 조정
brush_size.set(5)  # 기본 브러시 크기 설정
brush_size.pack() # 슬라이더 추가

canvas.bind("<B1-Motion>", paint)

window.mainloop()