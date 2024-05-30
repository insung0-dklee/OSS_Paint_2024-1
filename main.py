"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼
start_polygon: 사용자가 다각형을 그리기 시작할 때, 마우스 클릭한 좌표를 다각형의 첫 번째 점으로 기록하는 기능.
draw_polygon: 사용자가 마우스를 드래그하여 다각형을 그릴 때마다 현재 마우스 위치의 좌표를 다각형의 점으로 추가하고, 이전에 그려진 다각형을 지우고, 새로운 다각형을 그리는 기능.

"""

from tkinter import *

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

#all clear 기능 추가
def clear_paint():
    canvas.delete("all")

class PolygonBrush:
    def __init__(self, window):
        self.window = window
        self.window.title("Polygon Brush")

        self.canvas = Canvas(self.window, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.start_polygon)
        self.canvas.bind("<B1-Motion>", self.draw_polygon)

        self.polygon_points = []

    def start_polygon(self, event):
        self.polygon_points = [(event.x, event.y)]

    def draw_polygon(self, event):
        self.polygon_points.append((event.x, event.y))
        self.canvas.delete("polygon")  # Clear previously drawn polygon
        self.canvas.create_polygon(self.polygon_points, outline="black", fill="", width=2, tags="polygon")


window = Tk()
brush = PolygonBrush(window)
canvas = Canvas(window)
canvas.pack()
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack()

window.mainloop()
