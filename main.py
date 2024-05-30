from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

# 오른쪽 마우스 클릭으로 별을 그리는 함수
def draw_star(event):
    # 별을 그리기 위한 좌표 계산
    x = event.x
    y = event.y
    points = [x, y-30, x+9, y-9, x+30, y-9, x+15, y+4,
              x+20, y+25, x, y+15, x-20, y+25, x-15, y+4,
              x-30, y-9, x-9, y-9]
    canvas.create_polygon(points)  # 다각형(별) 그리기

window = Tk()
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-3>", draw_star)  # 오른쪽 마우스 버튼 클릭 시 draw_star 함수 호출


window.mainloop()