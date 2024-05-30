from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    # 현재 배경이 흰색이기 때문에 흰색선을 그림으로써 지우개의 역할을 함
    if draw_mode.get() == "paint":
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    elif draw_mode.get() == "erase":
        canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")

def set_paint_mode():
    draw_mode.set("paint")

def set_erase_mode():
    draw_mode.set("erase")
window = Tk()
canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

draw_mode = StringVar()
draw_mode.set("paint")

button_frame = Frame(window)
button_frame.pack()

# 그리기 또는지우개 버튼을 왼쪽 마우스로 클릭시 선 그리기 모드로 변경되고 선을 그릴 수 있음
paint_button = Button(button_frame, text="선 그리기", command=set_paint_mode)
paint_button.pack(side=LEFT)

erase_button = Button(button_frame, text="지우개", command=set_erase_mode)
erase_button.pack(side=LEFT)

window.mainloop()
