"""
Project : Paint
paint : 내외부 검은색의 2픽셀 크기의 원을 이용해 그림을 그리는 기능
clear_paint : 그림판에 있는 그림을 다 지우는 기능
button_delete : clear_paint의 버튼

"""

from tkinter import *

def paint(event):
    
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    
    # 선택된 도형에 따라 그림 그리기
    if shape.get() == "Circle":
        canvas.create_oval(x1, y1, x2, y2, fill=color.get(), outline=color.get())
    elif shape.get() == "Rectangle":
        canvas.create_rectangle(x1, y1, x2 + 10, y2 + 10, fill=color.get(), outline=color.get())
    elif shape.get() == "Triangle":
        points = [event.x, event.y - 10, event.x - 10, event.y + 10, event.x + 10, event.y + 10]
        canvas.create_polygon(points, fill=color.get(), outline=color.get())

#all clear 기능 추가
def clear_canvas():
    canvas.delete("all")

window = Tk()
window.title("도형 그리기")

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)

canvas.bind("<B1-Motion>", paint)

# 도형과 색상 옵션을 포함할 프레임 생성
frame = Frame(window)
frame.pack(side=TOP, fill=X)

# 선택된 도형을 저장할 변수 생성
shape = StringVar(value="Circle")
# 도형 선택을 위한 버튼 생성
Radiobutton(frame, text="원", variable=shape, value="Circle").pack(side=LEFT)
Radiobutton(frame, text="사각형", variable=shape, value="Rectangle").pack(side=LEFT)
Radiobutton(frame, text="삼각형", variable=shape, value="Triangle").pack(side=LEFT)

# 선택된 색상을 저장할 변수 생성
color = StringVar(value="black")
# 색상 선택을 위한 버튼 생성
Radiobutton(frame, text="검정", variable=color, value="black").pack(side=LEFT)
Radiobutton(frame, text="빨강", variable=color, value="red").pack(side=LEFT)
Radiobutton(frame, text="파랑", variable=color, value="blue").pack(side=LEFT)
Radiobutton(frame, text="초록", variable=color, value="green").pack(side=LEFT)

# 캔버스를 지우기 위한 버튼 생성
Button(frame, text="모두 지우기", command=clear_canvas).pack(side=LEFT)


window.mainloop()
