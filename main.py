from tkinter import *

def paint(event):
    x1, y1 = (event.x - brush_size.get()), (event.y - brush_size.get())
    x2, y2 = (event.x + brush_size.get()), (event.y + brush_size.get())
    canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color)

def clear_paint():
    canvas.delete("all")

def choose_color():
    color = askcolor()[1]
    if color:
        global current_color
        current_color = color

from tkinter.colorchooser import askcolor

window = Tk()
window.title("그림판")

current_color = "black"

canvas = Canvas(window, bg="white")
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_delete = Button(window, text="all clear", command=clear_paint)
button_delete.pack(side=LEFT)

color_button = Button(window, text="Choose Color", command=choose_color)
color_button.pack(side=LEFT)

brush_size = IntVar(value=1)
size_slider = Scale(window, from_=1, to=10, orient=HORIZONTAL, variable=brush_size, label="Brush Size")
size_slider.pack(side=LEFT)

window.mainloop()
