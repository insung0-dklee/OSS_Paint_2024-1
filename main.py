"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
change_cursor & default_cursor : 그림판 위 커서 형태를 연필로 변경하는 기능
show_coordinates & hide_coordinates : 우클릭을 누르는 동안 좌표값을 좌측 상단에 백분율로 보여주는 기능


"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

# 마우스 커서를 연필 형태로 변경하기
def change_cursor(event):
    canvas.config(cursor="pencil")

# 연필 형태 커서를 원래대로 변경하기
def default_cursor(event):
    canvas.config(cursor="")

# 우클릭을 누르면 우측 상단에 x, y 좌표값을 백분율로 표시
def show_coordinates(event):
    canvas.delete("coord_text")  # 이전 좌표값 삭제
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x_percent = (event.x / width) * 100
    y_percent = (event.y / height) * 100
    coord_text = f"<{x_percent:.1f}% / {100-y_percent:.1f}%>"
    canvas.create_text(10, 10, text=coord_text, anchor="nw", tags="coord_text")

# 우클릭을 떼면 좌표값 삭제
def hide_coordinates(event):
    canvas.delete("coord_text")


window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

canvas.bind("<Enter>", change_cursor)
canvas.bind("<Leave>", default_cursor)


canvas.bind("<Button-3>", show_coordinates)
canvas.bind("<ButtonRelease-3>", hide_coordinates)


button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
