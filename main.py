"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *
import math

def paint(event):
    if current_brush == "circle":
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    elif current_brush == "star":
        # 별 브러쉬: 별 모양을 그림
        draw_star(event.x, event.y)

def clear_paint():
    canvas.delete("all")

# 원형 브러쉬를 선택하는 함수
def use_circle_brush():
    global current_brush
    current_brush = "circle"

# 별 브러쉬를 선택하는 함수
def use_star_brush():
    global current_brush
    current_brush = "star"

# 별 모양을 그리는 함수
def draw_star(x, y):
    points = calculate_star_points(x, y, 10, 5)
    canvas.create_polygon(points, fill="yellow", outline="black")

# 별 모양의 좌표를 계산하는 함수
def calculate_star_points(center_x, center_y, outer_radius, inner_radius):
    points = []
    angle = 0
    for i in range(10):
        if i % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        points.extend([x, y])
        angle += 36
    return points

window = Tk()
window.title("Paint Application with Star Brush")

current_brush = "circle"  # 초기 브러쉬 설정


canvas = Canvas(window, bg="white", width=800, height=600)
canvas.pack()


canvas.bind("<B1-Motion>", paint)

# 원형 브러쉬 선택 버튼 생성 및 설정
button_circle = Button(window, text="Circle Brush", command=use_circle_brush)
button_circle.pack(side=LEFT)

# 별 브러쉬 선택 버튼 생성 및 설정
button_star = Button(window, text="Star Brush", command=use_star_brush)
button_star.pack(side=LEFT)


button_clear = Button(window, text="All Clear", command=clear_paint)
button_clear.pack(side=LEFT)

window.mainloop()
