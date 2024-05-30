from tkinter import *
import random

def paint(event):
    x1, y1 = ( event.x-1 ), ( event.y-1 )
    x2, y2 = ( event.x+1 ), ( event.y+1 )
    canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

def change_canvas_color():
    colors = ["red", "green", "blue", "yellow", "pink", "purple", "orange"]
    canvas.configure(bg=random.choice(colors))

window = Tk()
window.title("Paint and Change Canvas Color")

canvas = Canvas(window, width=400, height=400)
canvas.pack()

canvas.bind("<B1-Motion>", paint)

color_button = Button(window, text="Random Canvas Color", command=change_canvas_color)
color_button.pack()

window.mainloop()
