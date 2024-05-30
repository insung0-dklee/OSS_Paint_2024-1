from tkinter import *

current_shape = "oval"

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    
    if current_shape == "oval":
        canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
    elif current_shape == "rectangle":
        canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
    elif current_shape == "line":
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

def set_shape(shape):
    global current_shape
    current_shape = shape

def clear_paint():
    canvas.delete("all")

window = Tk()
canvas = Canvas(window)
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<B1-Motion>", paint)

button_oval = Button(window, text="Draw Oval", command=lambda: set_shape("oval"))
button_oval.pack(side=LEFT)

button_rectangle = Button(window, text="Draw Rectangle", command=lambda: set_shape("rectangle"))
button_rectangle.pack(side=LEFT)

button_line = Button(window, text="Draw Line", command=lambda: set_shape("line"))
button_line.pack(side=LEFT)

button_delete = Button(window, text="All Clear", command=clear_paint)
button_delete.pack(side=LEFT)

window.mainloop()
