from tkinter import *

current_tool = "brush"  # 초기 도구를 붓으로 설정

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def clear_paint():
    canvas.delete("all")

def select_tool(tool):
    global current_tool
    current_tool = tool

def on_canvas_click(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    if current_tool == "brush":
        canvas.bind("<B1-Motion>", paint)
    else:
        canvas.bind("<B1-Motion>", draw_shape)

def draw_shape(event):
    global start_x, start_y
    canvas.delete("preview")  # 기존 프리뷰 도형 삭제
    if current_tool == "rectangle":
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black", tags="preview")
    elif current_tool == "line":
        canvas.create_line(start_x, start_y, event.x, event.y, fill="black", tags="preview")
    elif current_tool == "oval":
        canvas.create_oval(start_x, start_y, event.x, event.y, outline="black", tags="preview")

def on_canvas_release(event):
    if current_tool != "brush":
        canvas.delete("preview")
        if current_tool == "rectangle":
            canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="black")
        elif current_tool == "line":
            canvas.create_line(start_x, start_y, event.x, event.y, fill="black")
        elif current_tool == "oval":
            canvas.create_oval(start_x, start_y, event.x, event.y, outline="black")

window = Tk()
window.title("Paint Program")

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<ButtonRelease-1>", on_canvas_release)

button_frame = Frame(window)
button_frame.pack(fill=X)

clear_button = Button(button_frame, text="Clear", command=clear_paint)
clear_button.pack(side=LEFT)

brush_button = Button(button_frame, text="Brush", command=lambda: select_tool("brush"))
brush_button.pack(side=LEFT)

line_button = Button(button_frame, text="Line", command=lambda: select_tool("line"))
line_button.pack(side=LEFT)

rectangle_button = Button(button_frame, text="Rectangle", command=lambda: select_tool("rectangle"))
rectangle_button.pack(side=LEFT)

oval_button = Button(button_frame, text="Oval", command=lambda: select_tool("oval"))
oval_button.pack(side=LEFT)

window.mainloop()
